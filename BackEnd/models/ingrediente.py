from pydantic import BaseModel, Field
from typing import Optional
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

class IngredienteBase(BaseModel):
    nombre: str
    adicional: bool = False
    precio_adicional: float = 0.0

class IngredienteCreate(IngredienteBase):
    pass

class IngredienteUpdate(BaseModel):
    nombre: Optional[str] = None
    adicional: Optional[bool] = None
    precio_adicional: Optional[float] = None

class Ingrediente(IngredienteBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class IngredienteResponse(IngredienteBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

# Relación Producto-Ingrediente
class ProductoIngredienteBase(BaseModel):
    producto_id: str
    ingrediente_id: str
    tipo: str  # "base", "adicional", "extra"
    opcional: bool = False

class ProductoIngredienteCreate(ProductoIngredienteBase):
    pass

class ProductoIngrediente(ProductoIngredienteBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ProductoIngredienteResponse(ProductoIngredienteBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
