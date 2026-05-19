import structlog

from app.models.pasarela_schemas import ReporteResponse
from app.repositories import transaccion_repo

logger = structlog.get_logger(__name__)


async def generar_reporte_deuda(empresa_id: str) -> ReporteResponse:
    pendientes = await transaccion_repo.obtener_pendientes_por_empresa(empresa_id)
    total_deuda = sum(item.get("monto", 0) for item in pendientes)
    cantidad_transacciones = len(pendientes)
    logger.info(
        "reporte_generado",
        empresa_id=empresa_id,
        total_deuda=total_deuda,
        cantidad_transacciones=cantidad_transacciones,
    )
    return ReporteResponse(
        empresa_id=empresa_id,
        total_deuda=total_deuda,
        cantidad_transacciones=cantidad_transacciones,
        transacciones=pendientes,
    )


async def procesar_liquidacion_masiva() -> int:
    pendientes = await transaccion_repo.obtener_pendientes_todas()
    transaccion_ids = [item.get("id") for item in pendientes if item.get("id")]
    if transaccion_ids:
        await transaccion_repo.liquidar_batch(transaccion_ids)
    logger.info("liquidacion_masiva", cantidad_liquidadas=len(transaccion_ids))
    return len(transaccion_ids)
