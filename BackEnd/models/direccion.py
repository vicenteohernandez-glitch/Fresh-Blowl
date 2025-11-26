from pydantic import BaseModel, Field
from typing import Optional
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

class DireccionBase(BaseModel):
    usuario_id: str
    calle: str
    numero: str
    comuna: str
    ciudad: str
    lat: Optional[float] = None
    lng: Optional[float] = None
    favorita: bool = False

class DireccionCreate(DireccionBase):
    pass

class DireccionUpdate(BaseModel):
    calle: Optional[str] = None
    numero: Optional[str] = None
    comuna: Optional[str] = None
    ciudad: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    favorita: Optional[bool] = None

class Direccion(DireccionBase):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class DireccionResponse(DireccionBase):
    id: str = Field(alias="_id")
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
