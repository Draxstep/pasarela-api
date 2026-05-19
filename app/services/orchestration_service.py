import structlog

from app.models.pasarela_schemas import PagoRequest, PagoResponse
from app.repositories import empresa_repo, transaccion_repo
from app.services import bank_clients

logger = structlog.get_logger(__name__)


async def procesar_pago(request: PagoRequest) -> PagoResponse:
    logger.info(
        "pago_iniciado",
        empresa_id=request.empresa_id,
        id_idempotencia=request.id_idempotencia,
        franquicia=request.franquicia,
        monto=request.monto,
    )

    empresa_valida = await empresa_repo.verificar_empresa(request.empresa_id)
    if not empresa_valida:
        logger.info("empresa_invalida", empresa_id=request.empresa_id)
        raise ValueError("Empresa no existe o esta inactiva")

    existente = await transaccion_repo.buscar_por_idempotencia(request.id_idempotencia)
    if existente:
        logger.info(
            "pago_duplicado",
            empresa_id=request.empresa_id,
            id_idempotencia=request.id_idempotencia,
            transaccion_id=existente.get("id"),
            estado=existente.get("estado"),
        )
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
    logger.info(
        "transaccion_registrada",
        transaccion_id=transaccion_id,
        empresa_id=request.empresa_id,
        id_idempotencia=request.id_idempotencia,
    )

    franquicia = request.franquicia.strip()
    if franquicia.lower() not in {"visa", "mastercard", "nu"}:
        logger.info("franquicia_no_soportada", franquicia=franquicia)
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

    logger.info(
        "respuesta_banco",
        franquicia=franquicia,
        transaccion_id=transaccion_id,
        status=resultado.get("status"),
    )

    estado_banco = (resultado.get("status") or "").strip().lower()
    if estado_banco == "aprobado":
        await transaccion_repo.actualizar_estado(transaccion_id, "No Liquidado")
        logger.info(
            "pago_aprobado",
            transaccion_id=transaccion_id,
            empresa_id=request.empresa_id,
        )
        return PagoResponse(
            status="Aprobado",
            transaccion_id=transaccion_id,
            mensaje=resultado.get("mensaje", "Pago aprobado"),
        )

    await transaccion_repo.actualizar_estado(transaccion_id, "Rechazado")
    logger.info(
        "pago_rechazado",
        transaccion_id=transaccion_id,
        empresa_id=request.empresa_id,
        motivo=resultado.get("mensaje"),
    )
    return PagoResponse(
        status="Rechazado",
        transaccion_id=transaccion_id,
        mensaje=resultado.get("mensaje", "Pago rechazado"),
    )
