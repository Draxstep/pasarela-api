from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import httpx

from app.core.settings import settings


async def buscar_por_idempotencia(id_idem: str) -> Optional[Dict[str, Any]]:
    url = f"{settings.pocketbase_url}/api/collections/transacciones/records"
    params = {"filter": f'id_idempotencia="{id_idem}"', "perPage": 1}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        if response.status_code != 200:
            return None
        data = response.json()
        items = data.get("items") or []
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
        return data["id"]


async def actualizar_estado(transaccion_id: str, nuevo_estado: str) -> None:
    url = (
        f"{settings.pocketbase_url}/api/collections/transacciones/records/{transaccion_id}"
    )
    payload = {"estado": nuevo_estado}
    async with httpx.AsyncClient() as client:
        response = await client.patch(url, json=payload)
        response.raise_for_status()


async def obtener_pendientes_por_empresa(empresa_id: str) -> List[Dict[str, Any]]:
    url = f"{settings.pocketbase_url}/api/collections/transacciones/records"
    filtro = f'empresa_id="{empresa_id}" && estado="No Liquidado"'
    params = {"filter": filtro}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("items") or []


async def obtener_pendientes_todas() -> List[Dict[str, Any]]:
    url = f"{settings.pocketbase_url}/api/collections/transacciones/records"
    params = {"filter": 'estado="No Liquidado"'}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        data = response.json()
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
