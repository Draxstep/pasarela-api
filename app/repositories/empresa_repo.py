import httpx
import structlog

from app.core.settings import settings

logger = structlog.get_logger(__name__)


async def verificar_empresa(empresa_id: str) -> bool:
    url = f"{settings.pocketbase_url}/api/collections/empresas/records/{empresa_id}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            logger.info(
                "empresa_no_encontrada",
                empresa_id=empresa_id,
                status_code=response.status_code,
            )
            return False
        data = response.json()
        activa = bool(data.get("activa"))
        logger.info("empresa_verificada", empresa_id=empresa_id, activa=activa)
        return activa
