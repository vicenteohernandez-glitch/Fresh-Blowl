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
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class CuponResponse(CuponBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
