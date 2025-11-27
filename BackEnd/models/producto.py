from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any
from models.utils import PyObjectId

class ProductoBase(BaseModel):
    categoria_id: Optional[str] = None
    nombre: str
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    precio: Optional[float] = None  # Alternativa
    imagen: Optional[str] = None
    imagen_url: Optional[str] = None  # Alternativa
    activo: bool = True
    agotado: bool = False
    disponible: bool = True
    stock: Optional[int] = None
    ingredientes: Optional[List[str]] = None

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(BaseModel):
    categoria_id: Optional[str] = None
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    precio: Optional[float] = None
    imagen: Optional[str] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None
    agotado: Optional[bool] = None
    disponible: Optional[bool] = None
    stock: Optional[int] = None
    ingredientes: Optional[List[str]] = None

class Producto(ProductoBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class ProductoResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    id: str = Field(alias="_id")
    nombre: str
    categoria_id: Optional[str] = None
    descripcion: Optional[str] = None
    precio_base: Optional[float] = None
    precio: Optional[float] = None
    imagen: Optional[str] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = True
    agotado: Optional[bool] = False
    disponible: Optional[bool] = True
    stock: Optional[int] = None
    ingredientes: Optional[List[str]] = None

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
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class VarianteResponse(VarianteBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
