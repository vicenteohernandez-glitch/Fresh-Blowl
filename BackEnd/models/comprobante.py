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

class ComprobanteBase(BaseModel):
    pedido_id: str
    tipo: str  # boleta, factura
    numero: str
    pdf_url: Optional[str] = None

class ComprobanteCreate(ComprobanteBase):
    pass

class ComprobanteUpdate(BaseModel):
    pdf_url: Optional[str] = None

class Comprobante(ComprobanteBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    emitido_en: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class ComprobanteResponse(ComprobanteBase):
    id: str = Field(alias="_id")
    emitido_en: datetime
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
