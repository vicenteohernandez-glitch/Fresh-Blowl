from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models.utils import PyObjectId

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
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class IngredienteResponse(IngredienteBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")

# Relación Producto-Ingrediente
class ProductoIngredienteBase(BaseModel):
    producto_id: str
    ingrediente_id: str
    tipo: str  # "base", "adicional", "extra"
    opcional: bool = False

class ProductoIngredienteCreate(ProductoIngredienteBase):
    pass

class ProductoIngrediente(ProductoIngredienteBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class ProductoIngredienteResponse(ProductoIngredienteBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
