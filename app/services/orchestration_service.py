from app.models.pasarela_schemas import PagoRequest, PagoResponse
from app.repositories import empresa_repo, transaccion_repo
from app.services import bank_clients


async def procesar_pago(request: PagoRequest) -> PagoResponse:
    empresa_valida = await empresa_repo.verificar_empresa(request.empresa_id)
    if not empresa_valida:
        raise ValueError("Empresa no existe o esta inactiva")

    existente = await transaccion_repo.buscar_por_idempotencia(request.id_idempotencia)
    if existente:
        return PagoResponse(
            status=existente.get("estado", "Desconocido"),
            transaccion_id=existente.get("id", ""),
            mensaje="Transaccion duplicada",
        )

    transaccion_id = await transaccion_repo.crear_transaccion(
        {
            "id_idempotencia": request.id_idempotencia,
            "empresa_id": request.empresa_id,
            "monto": request.monto,
        }
    )

    if request.numero_tarjeta.startswith("4"):
        franquicia = "Visa"
    elif request.numero_tarjeta.startswith("5"):
        franquicia = "Mastercard"
    else:
        await transaccion_repo.actualizar_estado(transaccion_id, "Rechazado")
        return PagoResponse(
            status="Rechazado",
            transaccion_id=transaccion_id,
            mensaje="Franquicia no soportada",
        )

    datos_tarjeta = {
        "numero_tarjeta": request.numero_tarjeta,
        "cvc": request.cvc,
        "fecha_expiracion": request.fecha_expiracion,
    }

    resultado = await bank_clients.solicitar_autorizacion_bancaria(
        franquicia, datos_tarjeta, request.monto
    )

    estado_banco = (resultado.get("status") or "").strip().lower()
    if estado_banco == "aprobado":
        await transaccion_repo.actualizar_estado(transaccion_id, "No Liquidado")
        return PagoResponse(
            status="Aprobado",
            transaccion_id=transaccion_id,
            mensaje=resultado.get("mensaje", "Pago aprobado"),
        )

    await transaccion_repo.actualizar_estado(transaccion_id, "Rechazado")
    return PagoResponse(
        status="Rechazado",
        transaccion_id=transaccion_id,
        mensaje=resultado.get("mensaje", "Pago rechazado"),
    )
