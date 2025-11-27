from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

class PedidoBase(BaseModel):
    usuario_id: str
    direccion_id: Optional[str] = None
    estado: str = "pendiente"  # pendiente, confirmado, preparando, enviado, entregado, cancelado
    subtotal: float
    descuento: float = 0.0
    envio: float = 0.0
    total: float

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(BaseModel):
    estado: Optional[str] = None
    subtotal: Optional[float] = None
    descuento: Optional[float] = None
    envio: Optional[float] = None
    total: Optional[float] = None

class Pedido(PedidoBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class PedidoResponse(PedidoBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    creado_en: Optional[datetime] = None

# Item del pedido
class PedidoItemBase(BaseModel):
    pedido_id: str
    producto_id: str
    variante_id: Optional[str] = None
    cantidad: int
    precio_unitario: float

class PedidoItemCreate(PedidoItemBase):
    pass

class PedidoItem(PedidoItemBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class PedidoItemResponse(PedidoItemBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
