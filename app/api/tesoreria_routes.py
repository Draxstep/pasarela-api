from fastapi import APIRouter

from app.controllers.tesoreria_controller import (
    generar_reporte_deuda_controller,
    procesar_liquidacion_masiva_controller,
)
from app.models.pasarela_schemas import LiquidacionResponse, ReporteResponse

router = APIRouter(prefix="", tags=["tesoreria"])


@router.get(
    "/reportes/{empresa_id}",
    response_model=ReporteResponse,
    summary="Reporte de deuda",
    description="Devuelve el total pendiente y el detalle de transacciones no liquidadas.",
)
async def generar_reporte_deuda_endpoint(empresa_id: str) -> ReporteResponse:
    return await generar_reporte_deuda_controller(empresa_id)


@router.post(
    "/liquidar/batch",
    response_model=LiquidacionResponse,
    summary="Liquidacion masiva",
    description="Liquida todas las transacciones con estado No Liquidado.",
)
async def procesar_liquidacion_masiva_endpoint() -> LiquidacionResponse:
    return await procesar_liquidacion_masiva_controller()
