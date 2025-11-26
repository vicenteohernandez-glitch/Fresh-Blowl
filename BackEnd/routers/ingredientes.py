from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from api.models.ingrediente import (
    IngredienteCreate, IngredienteUpdate, IngredienteResponse,
    ProductoIngredienteCreate, ProductoIngredienteResponse
)
from api.database import get_collection

router = APIRouter()

# ============= INGREDIENTES =============

@router.post("/", response_model=IngredienteResponse, status_code=status.HTTP_201_CREATED)
async def create_ingrediente(ingrediente: IngredienteCreate):
    """Crear un nuevo ingrediente"""
    collection = get_collection("ingredientes")
    
    ingrediente_dict = ingrediente.dict()
    result = await collection.insert_one(ingrediente_dict)
    created_ingrediente = await collection.find_one({"_id": result.inserted_id})
    
    return created_ingrediente

@router.get("/", response_model=List[IngredienteResponse])
async def get_ingredientes(skip: int = 0, limit: int = 100, adicional: bool = None):
    """Obtener lista de ingredientes"""
    collection = get_collection("ingredientes")
    
    query = {}
    if adicional is not None:
        query["adicional"] = adicional
    
    ingredientes = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return ingredientes

@router.get("/{ingrediente_id}", response_model=IngredienteResponse)
async def get_ingrediente(ingrediente_id: str):
    """Obtener un ingrediente por ID"""
    collection = get_collection("ingredientes")
    
    if not ObjectId.is_valid(ingrediente_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    ingrediente = await collection.find_one({"_id": ObjectId(ingrediente_id)})
    if not ingrediente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    
    return ingrediente

@router.put("/{ingrediente_id}", response_model=IngredienteResponse)
async def update_ingrediente(ingrediente_id: str, ingrediente: IngredienteUpdate):
    """Actualizar un ingrediente"""
    collection = get_collection("ingredientes")
    
    if not ObjectId.is_valid(ingrediente_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in ingrediente.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(ingrediente_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    
    updated_ingrediente = await collection.find_one({"_id": ObjectId(ingrediente_id)})
    return updated_ingrediente

@router.delete("/{ingrediente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ingrediente(ingrediente_id: str):
    """Eliminar un ingrediente"""
    collection = get_collection("ingredientes")
    
    if not ObjectId.is_valid(ingrediente_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(ingrediente_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    
    return None

# ============= PRODUCTO-INGREDIENTE =============

@router.post("/producto-ingrediente", response_model=ProductoIngredienteResponse, status_code=status.HTTP_201_CREATED)
async def create_producto_ingrediente(relacion: ProductoIngredienteCreate):
    """Asociar un ingrediente a un producto"""
    collection = get_collection("producto_ingredientes")
    
    # Verificar que producto e ingrediente existen
    productos_collection = get_collection("productos")
    ingredientes_collection = get_collection("ingredientes")
    
    if ObjectId.is_valid(relacion.producto_id):
        producto = await productos_collection.find_one({"_id": ObjectId(relacion.producto_id)})
    else:
        producto = None
    
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    
    if ObjectId.is_valid(relacion.ingrediente_id):
        ingrediente = await ingredientes_collection.find_one({"_id": ObjectId(relacion.ingrediente_id)})
    else:
        ingrediente = None
    
    if not ingrediente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ingrediente no encontrado")
    
    relacion_dict = relacion.dict()
    result = await collection.insert_one(relacion_dict)
    created_relacion = await collection.find_one({"_id": result.inserted_id})
    
    return created_relacion

@router.get("/producto/{producto_id}/ingredientes", response_model=List[ProductoIngredienteResponse])
async def get_ingredientes_producto(producto_id: str):
    """Obtener todos los ingredientes de un producto"""
    collection = get_collection("producto_ingredientes")
    
    relaciones = await collection.find({"producto_id": producto_id}).to_list(length=100)
    return relaciones

@router.delete("/producto-ingrediente/{relacion_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_producto_ingrediente(relacion_id: str):
    """Eliminar la asociación de un ingrediente con un producto"""
    collection = get_collection("producto_ingredientes")
    
    if not ObjectId.is_valid(relacion_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(relacion_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Relación no encontrada")
    
    return None
