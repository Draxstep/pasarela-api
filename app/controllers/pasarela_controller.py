from fastapi import HTTPException, status

from app.models.pasarela_schemas import PagoRequest, PagoResponse
from app.services.orchestration_service import procesar_pago


async def procesar_pago_controller(request: PagoRequest) -> PagoResponse:
    try:
        return await procesar_pago(request)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno en el procesamiento del pago",
        ) from exc
