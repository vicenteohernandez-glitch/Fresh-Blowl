"""
Utilidades comunes para los modelos Pydantic v2
"""
from typing import Annotated, Any
from bson import ObjectId
from pydantic import BeforeValidator, ConfigDict

# Validador para convertir ObjectId a string
def validate_object_id(v: Any) -> str:
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str) and ObjectId.is_valid(v):
        return v
    raise ValueError("Invalid ObjectId")

# Tipo anotado para ObjectId
PyObjectId = Annotated[str, BeforeValidator(validate_object_id)]

# Configuración común para modelos que usan MongoDB
mongo_config = ConfigDict(
    populate_by_name=True,
    arbitrary_types_allowed=True,
    json_encoders={ObjectId: str}
)
