from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

class PagoBase(BaseModel):
    pedido_id: str
    pasarela: str  # webpay, mercadopago, etc
    estado: str = "pendiente"  # pendiente, aprobado, rechazado, reembolsado
    monto: float
    medio: str  # tarjeta_credito, tarjeta_debito, transferencia
    token: Optional[str] = None

class PagoCreate(PagoBase):
    pass

class PagoUpdate(BaseModel):
    estado: Optional[str] = None
    token: Optional[str] = None

class Pago(PagoBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class PagoResponse(PagoBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    creado_en: Optional[datetime] = None
