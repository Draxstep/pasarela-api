from typing import List

from pydantic import BaseModel, ConfigDict


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


class TransaccionDetalle(BaseModel):
    id: str
    id_idempotencia: str | None = None
    empresa_id: str | None = None
    monto: float | None = None
    estado: str | None = None
    fecha: str | None = None

    model_config = ConfigDict(extra="allow")


class ReporteResponse(BaseModel):
    empresa_id: str
    total_deuda: float
    cantidad_transacciones: int
    transacciones: List[TransaccionDetalle]
