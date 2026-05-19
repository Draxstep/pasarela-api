from fastapi import HTTPException, status

from app.models.pasarela_schemas import LiquidacionBatchRequest, ReporteResponse
from app.services.tesoreria_service import (
    generar_reporte_deuda,
    procesar_liquidacion_masiva,
)


async def generar_reporte_deuda_controller(empresa_id: str) -> ReporteResponse:
    try:
        return await generar_reporte_deuda(empresa_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al generar el reporte",
        ) from exc


async def procesar_liquidacion_masiva_controller(
    request: LiquidacionBatchRequest,
) -> dict:
    try:
        await procesar_liquidacion_masiva(request)
        return {"status": "ok", "mensaje": "Liquidacion procesada"}
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar la liquidacion",
        ) from exc
