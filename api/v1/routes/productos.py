from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel import Session
from session import get_session
from repositories.producto_repository import ProductoRepository
from schemas.producto import ProductoCreate, ProductoRead

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoRead, status_code=status.HTTP_201_CREATED)
def create_producto(data: ProductoCreate, session: Session = Depends(get_session)):
    return ProductoRepository.create(session, data)


@router.get("/", response_model=List[ProductoRead])
def list_productos(session: Session = Depends(get_session)):
    return ProductoRepository.get_all(session)


@router.get("/{producto_id}", response_model=ProductoRead)
def get_producto(producto_id: int, session: Session = Depends(get_session)):
    p = ProductoRepository.get_by_id(session, producto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p
