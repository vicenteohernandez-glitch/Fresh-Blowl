from pydantic import BaseModel, Field
from typing import Optional
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

class EnvioBase(BaseModel):
    tipo: str  # retiro, delivery
    proveedor: Optional[str] = None
    tracking: Optional[str] = None
    estimado: Optional[datetime] = None
    estado: str = "pendiente"  # pendiente, en_camino, entregado

class EnvioCreate(EnvioBase):
    pass

class EnvioUpdate(BaseModel):
    proveedor: Optional[str] = None
    tracking: Optional[str] = None
    estimado: Optional[datetime] = None
    estado: Optional[str] = None

class Envio(EnvioBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class EnvioResponse(EnvioBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
