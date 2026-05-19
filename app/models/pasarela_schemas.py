from typing import List

from pydantic import BaseModel


class PagoRequest(BaseModel):
    id_idempotencia: str
    empresa_id: str
    numero_tarjeta: str
    cvc: str
    fecha_expiracion: str
    monto: float


class PagoResponse(BaseModel):
    status: str
    transaccion_id: str
    mensaje: str


class LiquidacionBatchRequest(BaseModel):
    transaccion_id: List[str]


class ReporteResponse(BaseModel):
    empresa_id: str
    total_deuda: float
    cantidad_transacciones: int
