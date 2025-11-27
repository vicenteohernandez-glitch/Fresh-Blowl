from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

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
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class EnvioResponse(EnvioBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
