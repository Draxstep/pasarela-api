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
    elif franquicia_normalizada == "nu":
        url = settings.nu_service_url
    else:
        return {"status": "Error", "mensaje": "Franquicia no soportada"}

    try:
        async with httpx.AsyncClient() as client:
            if franquicia_normalizada == "nu":
                payload = {
                    "number": datos_tarjeta.get("numero_tarjeta"),
                    "csv": datos_tarjeta.get("cvc"),
                    "token": settings.nu_service_token,
                }
                response = await client.post(
                    url, json=payload, headers={"Accept": "text/plain"}
                )
                if response.status_code == 200:
                    if response.text.strip().upper() == "VALID":
                        return {
                            "status": "aprobado",
                            "mensaje": "Autorizacion aprobada",
                        }
                    return {
                        "status": "rechazado",
                        "mensaje": "Validacion rechazada",
                    }
                if response.status_code == 400:
                    return {"status": "error", "mensaje": response.text.strip()}
                response.raise_for_status()
            payload = {**datos_tarjeta, "monto": monto}
            response = await client.post(url, json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.RequestError:
        return {"status": "Error", "mensaje": "Error de conexion con el banco"}
