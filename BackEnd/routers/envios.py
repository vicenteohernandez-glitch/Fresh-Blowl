from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from api.models.envio import EnvioCreate, EnvioUpdate, EnvioResponse
from api.database import get_collection

router = APIRouter()

@router.post("/", response_model=EnvioResponse, status_code=status.HTTP_201_CREATED)
async def create_envio(envio: EnvioCreate):
    """Crear un nuevo envío"""
    collection = get_collection("envios")
    
    envio_dict = envio.dict()
    result = await collection.insert_one(envio_dict)
    created_envio = await collection.find_one({"_id": result.inserted_id})
    
    return created_envio

@router.get("/", response_model=List[EnvioResponse])
async def get_envios(skip: int = 0, limit: int = 100, estado: str = None):
    """Obtener lista de envíos"""
    collection = get_collection("envios")
    
    query = {}
    if estado:
        query["estado"] = estado
    
    envios = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return envios

@router.get("/{envio_id}", response_model=EnvioResponse)
async def get_envio(envio_id: str):
    """Obtener un envío por ID"""
    collection = get_collection("envios")
    
    if not ObjectId.is_valid(envio_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    envio = await collection.find_one({"_id": ObjectId(envio_id)})
    if not envio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
    
    return envio

@router.get("/tracking/{tracking}", response_model=EnvioResponse)
async def get_envio_by_tracking(tracking: str):
    """Obtener un envío por código de tracking"""
    collection = get_collection("envios")
    
    envio = await collection.find_one({"tracking": tracking})
    if not envio:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
    
    return envio

@router.put("/{envio_id}", response_model=EnvioResponse)
async def update_envio(envio_id: str, envio: EnvioUpdate):
    """Actualizar un envío"""
    collection = get_collection("envios")
    
    if not ObjectId.is_valid(envio_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in envio.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(envio_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
    
    updated_envio = await collection.find_one({"_id": ObjectId(envio_id)})
    return updated_envio

@router.post("/{envio_id}/actualizar-estado")
async def actualizar_estado_envio(envio_id: str, estado: str):
    """Actualizar el estado de un envío"""
    collection = get_collection("envios")
    
    if not ObjectId.is_valid(envio_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    estados_validos = ["pendiente", "en_camino", "entregado"]
    if estado not in estados_validos:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}"
        )
    
    result = await collection.update_one(
        {"_id": ObjectId(envio_id)},
        {"$set": {"estado": estado}}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
    
    return {"message": f"Estado actualizado a: {estado}"}

@router.delete("/{envio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_envio(envio_id: str):
    """Eliminar un envío"""
    collection = get_collection("envios")
    
    if not ObjectId.is_valid(envio_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(envio_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Envío no encontrado")
    
    return None
