from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from models.utils import PyObjectId

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
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")

class DireccionResponse(DireccionBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
