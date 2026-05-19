from app.models.pasarela_schemas import LiquidacionBatchRequest, ReporteResponse
from app.repositories import transaccion_repo


async def generar_reporte_deuda(empresa_id: str) -> ReporteResponse:
    pendientes = await transaccion_repo.obtener_pendientes_por_empresa(empresa_id)
    total_deuda = sum(item.get("monto", 0) for item in pendientes)
    cantidad_transacciones = len(pendientes)
    return ReporteResponse(
        empresa_id=empresa_id,
        total_deuda=total_deuda,
        cantidad_transacciones=cantidad_transacciones,
    )


async def procesar_liquidacion_masiva(request: LiquidacionBatchRequest) -> None:
    await transaccion_repo.liquidar_batch(request.transaccion_id)
