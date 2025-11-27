from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

class RolBase(BaseModel):
    nombre: str
    descripcion: Optional[str] = None

class RolCreate(RolBase):
    pass

class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None

class Rol(RolBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class RolResponse(RolBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    creado_en: Optional[datetime] = None

class UsuarioRol(BaseModel):
    usuario_id: str
    rol_id: str
