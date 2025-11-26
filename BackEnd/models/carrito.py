from pydantic import BaseModel, Field
from typing import Optional, List
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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    actualizado_en: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CarritoResponse(CarritoBase):
    id: str = Field(alias="_id")
    actualizado_en: datetime
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CarritoItemResponse(CarritoItemBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
