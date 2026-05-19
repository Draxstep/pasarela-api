from fastapi import APIRouter

from app.controllers.pasarela_controller import procesar_pago_controller
from app.models.pasarela_schemas import PagoRequest, PagoResponse

router = APIRouter(prefix="", tags=["gateway"])


@router.post(
    "/procesar-pago",
    response_model=PagoResponse,
    summary="Procesar pago",
    description="Recibe un cobro y lo enruta al banco correspondiente.",
    responses={
        400: {"description": "Error de validacion o negocio"},
        500: {"description": "Error interno"},
    },
)
async def procesar_pago_endpoint(request: PagoRequest) -> PagoResponse:
    return await procesar_pago_controller(request)
