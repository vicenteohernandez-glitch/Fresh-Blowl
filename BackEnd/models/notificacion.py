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

class NotificacionBase(BaseModel):
    usuario_id: str
    canal: str  # email, sms, push
    asunto: str
    estado: str = "pendiente"  # pendiente, enviado, fallido

class NotificacionCreate(NotificacionBase):
    pass

class NotificacionUpdate(BaseModel):
    estado: Optional[str] = None

class Notificacion(NotificacionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    enviado_en: Optional[datetime] = None
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class NotificacionResponse(NotificacionBase):
    id: str = Field(alias="_id")
    enviado_en: Optional[datetime] = None
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
