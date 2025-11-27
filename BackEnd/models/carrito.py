from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

class CarritoBase(BaseModel):
    usuario_id: str
    estado: str = "activo"  # activo, abandonado, convertido
    cupon_codigo: Optional[str] = None

class CarritoCreate(CarritoBase):
    pass

class CarritoUpdate(BaseModel):
    estado: Optional[str] = None
    cupon_codigo: Optional[str] = None

class Carrito(CarritoBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)

class CarritoResponse(CarritoBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    actualizado_en: Optional[datetime] = None

# Item del carrito
class CarritoItemBase(BaseModel):
    carrito_id: str
    producto_id: str
    variante_id: Optional[str] = None
    cantidad: int = 1
    precio_unitario: float

class CarritoItemCreate(CarritoItemBase):
    pass

class CarritoItemUpdate(BaseModel):
    cantidad: Optional[int] = None
    precio_unitario: Optional[float] = None

class CarritoItem(CarritoItemBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class CarritoItemResponse(CarritoItemBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
