from fastapi import APIRouter, HTTPException, status
from typing import List
from bson import ObjectId
from api.models.categoria import CategoriaCreate, CategoriaUpdate, CategoriaResponse
from api.database import get_collection

router = APIRouter()

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
async def create_categoria(categoria: CategoriaCreate):
    """Crear una nueva categoría"""
    collection = get_collection("categorias")
    
    categoria_dict = categoria.dict()
    result = await collection.insert_one(categoria_dict)
    created_categoria = await collection.find_one({"_id": result.inserted_id})
    
    return created_categoria

@router.get("/", response_model=List[CategoriaResponse])
async def get_categorias(skip: int = 0, limit: int = 100, visible: bool = None):
    """Obtener lista de categorías"""
    collection = get_collection("categorias")
    
    query = {}
    if visible is not None:
        query["visible"] = visible
    
    categorias = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)
    return categorias

@router.get("/{categoria_id}", response_model=CategoriaResponse)
async def get_categoria(categoria_id: str):
    """Obtener una categoría por ID"""
    collection = get_collection("categorias")
    
    if not ObjectId.is_valid(categoria_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    categoria = await collection.find_one({"_id": ObjectId(categoria_id)})
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    return categoria

@router.get("/slug/{slug}", response_model=CategoriaResponse)
async def get_categoria_by_slug(slug: str):
    """Obtener una categoría por slug"""
    collection = get_collection("categorias")
    
    categoria = await collection.find_one({"slug": slug})
    if not categoria:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    return categoria

@router.put("/{categoria_id}", response_model=CategoriaResponse)
async def update_categoria(categoria_id: str, categoria: CategoriaUpdate):
    """Actualizar una categoría"""
    collection = get_collection("categorias")
    
    if not ObjectId.is_valid(categoria_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    update_data = {k: v for k, v in categoria.dict(exclude_unset=True).items() if v is not None}
    
    if not update_data:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No hay datos para actualizar")
    
    result = await collection.update_one(
        {"_id": ObjectId(categoria_id)},
        {"$set": update_data}
    )
    
    if result.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    updated_categoria = await collection.find_one({"_id": ObjectId(categoria_id)})
    return updated_categoria

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_categoria(categoria_id: str):
    """Eliminar una categoría"""
    collection = get_collection("categorias")
    
    if not ObjectId.is_valid(categoria_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="ID inválido")
    
    result = await collection.delete_one({"_id": ObjectId(categoria_id)})
    
    if result.deleted_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Categoría no encontrada")
    
    return None
