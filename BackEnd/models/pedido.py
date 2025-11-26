from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class PedidoBase(BaseModel):
    usuario_id: str
    direccion_id: str
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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    creado_en: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PedidoResponse(PedidoBase):
    id: str = Field(alias="_id")
    creado_en: datetime
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class PedidoItemResponse(PedidoItemBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
