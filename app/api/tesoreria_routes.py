from fastapi import APIRouter

from app.controllers.tesoreria_controller import (
    generar_reporte_deuda_controller,
    procesar_liquidacion_masiva_controller,
)
from app.models.pasarela_schemas import LiquidacionBatchRequest, ReporteResponse

router = APIRouter(prefix="", tags=["tesoreria"])


@router.get("/reportes/{empresa_id}", response_model=ReporteResponse)
async def generar_reporte_deuda_endpoint(empresa_id: str) -> ReporteResponse:
    return await generar_reporte_deuda_controller(empresa_id)


@router.post("/liquidar/batch")
async def procesar_liquidacion_masiva_endpoint(
    request: LiquidacionBatchRequest,
) -> dict:
    return await procesar_liquidacion_masiva_controller(request)
