import httpx

from app.core.settings import settings


async def solicitar_autorizacion_bancaria(
    franquicia: str, datos_tarjeta: dict, monto: float
) -> dict:
    franquicia_normalizada = franquicia.strip().lower()
    if franquicia_normalizada == "visa":
        url = settings.visa_service_url
    elif franquicia_normalizada == "mastercard":
        url = settings.mastercard_service_url
    else:
        return {"status": "Error", "mensaje": "Franquicia no soportada"}

    payload = {"datos_tarjeta": datos_tarjeta, "monto": monto}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError:
        return {"status": "Error", "mensaje": "Error de conexion con el banco"}
