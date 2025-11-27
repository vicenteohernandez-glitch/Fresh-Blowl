from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from models.utils import PyObjectId

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
    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)
    id: PyObjectId = Field(alias="_id")
    emitido_en: datetime = Field(default_factory=datetime.utcnow)

class ComprobanteResponse(ComprobanteBase):
    model_config = ConfigDict(populate_by_name=True)
    id: str = Field(alias="_id")
    emitido_en: Optional[datetime] = None
