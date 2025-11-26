from pydantic import BaseModel, EmailStr, Field
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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    hash_password: str
    creado_en: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UsuarioResponse(UsuarioBase):
    id: str = Field(alias="_id")
    creado_en: datetime
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class UsuarioLogin(BaseModel):
    email: EmailStr
    password: str
