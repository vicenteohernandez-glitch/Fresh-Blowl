from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    telefono: Optional[str] = None
    email_verificado: bool = False
    activo: bool = True

class UsuarioCreate(UsuarioBase):
    password: str

class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    email_verificado: Optional[bool] = None
    activo: Optional[bool] = None

class Usuario(UsuarioBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    
    id: PyObjectId = Field(alias="_id")
    hash_password: str
    creado_en: datetime = Field(default_factory=datetime.utcnow)

class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(populate_by_name=True)
    
    id: str = Field(alias="_id")
    creado_en: Optional[datetime] = None

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
