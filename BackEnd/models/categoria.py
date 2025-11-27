from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models.utils import PyObjectId

class CategoriaBase(BaseModel):
    nombre: str
    slug: Optional[str] = None
    descripcion: Optional[str] = None
    visible: bool = True
    activa: bool = True

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    slug: Optional[str] = None
    descripcion: Optional[str] = None
    visible: Optional[bool] = None
    activa: Optional[bool] = None

class Categoria(CategoriaBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class CategoriaResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')
    id: str = Field(alias="_id")
    nombre: str
    slug: Optional[str] = None
    descripcion: Optional[str] = None
    visible: Optional[bool] = True
    activa: Optional[bool] = True
