from fastapi import HTTPException, status

from app.models.pasarela_schemas import (
    LiquidacionResponse,
    LiquidacionSeleccionRequest,
    ReporteResponse,
)
from app.services.tesoreria_service import (
    generar_reporte_deuda,
    procesar_liquidacion_masiva,
    procesar_liquidacion_seleccionada,
)


async def generar_reporte_deuda_controller(empresa_id: str) -> ReporteResponse:
    try:
        return await generar_reporte_deuda(empresa_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al generar el reporte",
        ) from exc


async def procesar_liquidacion_masiva_controller() -> dict:
    try:
        total = await procesar_liquidacion_masiva()
        return LiquidacionResponse(
            status="ok",
            mensaje="Liquidacion procesada",
            cantidad_liquidadas=total,
        ).model_dump()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar la liquidacion",
        ) from exc


async def procesar_liquidacion_seleccionada_controller(
    request: LiquidacionSeleccionRequest,
) -> dict:
    try:
        total = await procesar_liquidacion_seleccionada(request.transaccion_ids)
        return LiquidacionResponse(
            status="ok",
            mensaje="Liquidacion procesada",
            cantidad_liquidadas=total,
        ).model_dump()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al procesar la liquidacion",
        ) from exc
