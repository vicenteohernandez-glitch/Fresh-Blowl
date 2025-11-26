from pydantic import BaseModel, Field
from typing import Optional, List
from decimal import Decimal
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

class ProductoBase(BaseModel):
    categoria_id: str
    nombre: str
    descripcion: Optional[str] = None
    precio_base: float
    activo: bool = True
    agotado: bool = False

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    categoria_id: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    activo: Optional[bool] = None
    agotado: Optional[bool] = None

class Producto(ProductoBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProductoResponse(ProductoBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

# Variante de producto
class VarianteBase(BaseModel):
    producto_id: str
    nombre: str
    precio: float
    activo: bool = True

class VarianteCreate(VarianteBase):
    pass

class VarianteUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    activo: Optional[bool] = None

class Variante(VarianteBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class VarianteResponse(VarianteBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
