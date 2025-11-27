from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

class CuponBase(BaseModel):
    codigo: str
    descuento_porcentaje: Optional[float] = 0.0
    descuento_fijo: Optional[float] = 0.0
    valido_desde: datetime
    valido_hasta: datetime
    uso_maximo: int = 0
    uso_actual: int = 0
    activo: bool = True

class CuponCreate(CuponBase):
    pass

class CuponUpdate(BaseModel):
    descuento_porcentaje: Optional[float] = None
    descuento_fijo: Optional[float] = None
    valido_desde: Optional[datetime] = None
    valido_hasta: Optional[datetime] = None
    uso_maximo: Optional[int] = None
    uso_actual: Optional[int] = None
    activo: Optional[bool] = None

class Cupon(CuponBase):
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class CuponResponse(CuponBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
