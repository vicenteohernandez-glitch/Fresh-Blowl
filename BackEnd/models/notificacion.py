from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

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
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")
    enviado_en: Optional[datetime] = None

class NotificacionResponse(NotificacionBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    enviado_en: Optional[datetime] = None
