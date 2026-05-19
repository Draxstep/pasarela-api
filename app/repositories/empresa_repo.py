import httpx

from app.core.settings import settings


async def verificar_empresa(empresa_id: str) -> bool:
    url = f"{settings.pocketbase_url}/api/collections/empresas/records/{empresa_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            return False
        data = response.json()
        return bool(data.get("activa"))
