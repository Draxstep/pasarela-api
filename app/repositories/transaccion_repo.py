from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx
import structlog

from app.core.settings import settings

logger = structlog.get_logger(__name__)


async def buscar_por_idempotencia(id_idem: str) -> Optional[Dict[str, Any]]:
    url = f"{settings.pocketbase_url}/api/collections/transacciones/records"
    params = {"filter": f'id_idempotencia="{id_idem}"', "perPage": 1}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            logger.info(
                "busqueda_idempotencia_error",
                id_idempotencia=id_idem,
                status_code=response.status_code,
            )
            return None
        data = response.json()
        items = data.get("items") or []
        logger.info("busqueda_idempotencia", id_idempotencia=id_idem, encontrado=bool(items))
        return items[0] if items else None


async def crear_transaccion(datos: Dict[str, Any]) -> str:
    url = f"{settings.pocketbase_url}/api/collections/transacciones/records"
    payload = {
        **datos,
        "estado": "Procesando",
        "fecha": datetime.now(timezone.utc).isoformat(),
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        logger.info(
            "transaccion_creada",
            transaccion_id=data.get("id"),
            empresa_id=payload.get("empresa_id"),
            monto=payload.get("monto"),
        )
        return data["id"]


async def actualizar_estado(transaccion_id: str, nuevo_estado: str) -> None:
    url = (
        f"{settings.pocketbase_url}/api/collections/transacciones/records/{transaccion_id}"
    )
    payload = {"estado": nuevo_estado}
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=payload)
        response.raise_for_status()
        logger.info(
            "transaccion_actualizada",
            transaccion_id=transaccion_id,
            nuevo_estado=nuevo_estado,
        )


async def obtener_pendientes_por_empresa(empresa_id: str) -> List[Dict[str, Any]]:
    url = f"{settings.pocketbase_url}/api/collections/transacciones/records"
    filtro = f'empresa_id="{empresa_id}" && estado="No Liquidado"'
    params = {"filter": filtro}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info(
            "pendientes_por_empresa",
            empresa_id=empresa_id,
            cantidad=len(data.get("items") or []),
        )
        return data.get("items") or []


async def obtener_pendientes_todas() -> List[Dict[str, Any]]:
    url = f"{settings.pocketbase_url}/api/collections/transacciones/records"
    params = {"filter": 'estado="No Liquidado"'}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        logger.info("pendientes_todas", cantidad=len(data.get("items") or []))
        return data.get("items") or []


async def liquidar_batch(transaccion_ids: List[str]) -> None:
    async with httpx.AsyncClient() as client:
        for transaccion_id in transaccion_ids:
            url = (
                f"{settings.pocketbase_url}/api/collections/transacciones/records/{transaccion_id}"
            )
            payload = {"estado": "Liquidado"}
            response = await client.patch(url, json=payload)
            response.raise_for_status()
        logger.info("liquidacion_batch", cantidad=len(transaccion_ids))
