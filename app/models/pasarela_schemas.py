from typing import List

from pydantic import BaseModel, ConfigDict, Field


class PagoRequest(BaseModel):
    id_idempotencia: str = Field(
        ..., description="Identificador idempotente del pago", examples=["idem-001"]
    )
    empresa_id: str = Field(
        ..., description="ID de la empresa en PocketBase", examples=["empresa_123"]
    )
    franquicia: str = Field(
        ...,
        description="Franquicia de la tarjeta: Visa, Mastercard o Nu",
        examples=["Visa"],
    )
    numero_tarjeta: str = Field(
        ..., description="Numero de la tarjeta", examples=["4111111111111111"]
    )
    cvc: str = Field(..., description="Codigo de seguridad", examples=["123"])
    fecha_expiracion: str = Field(
        ..., description="Fecha de expiracion", examples=["12/28"]
    )
    monto: float = Field(..., description="Monto a cobrar", examples=[120.5])


class PagoResponse(BaseModel):
    status: str = Field(..., description="Estado del pago", examples=["Aprobado"])
    transaccion_id: str = Field(
        ..., description="ID de la transaccion en PocketBase", examples=["pb_id"]
    )
    mensaje: str = Field(..., description="Mensaje de negocio", examples=["Pago aprobado"])


class TransaccionDetalle(BaseModel):
    id: str = Field(..., description="ID de la transaccion", examples=["pb_id"])
    id_idempotencia: str | None = None
    empresa_id: str | None = None
    monto: float | None = None
    estado: str | None = None
    fecha: str | None = None

    model_config = ConfigDict(extra="allow")


class ReporteResponse(BaseModel):
    empresa_id: str = Field(..., description="ID de la empresa")
    total_deuda: float = Field(..., description="Suma de montos pendientes")
    cantidad_transacciones: int = Field(..., description="Numero de transacciones")
    transacciones: List[TransaccionDetalle]


class LiquidacionResponse(BaseModel):
    status: str = Field(..., description="Estado de la operacion", examples=["ok"])
    mensaje: str = Field(..., description="Mensaje de negocio")
    cantidad_liquidadas: int = Field(
        ..., description="Cantidad de transacciones liquidadas", examples=[2]
    )
