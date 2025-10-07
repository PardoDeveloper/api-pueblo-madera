from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List

from session import get_session
from repositories.cliente_repository import ClienteRepository
from schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["Clientes"])

# Crear cliente
@router.post("/", response_model=ClienteRead, status_code=201)
def create_cliente(data: ClienteCreate, session: Session = Depends(get_session)):
    return ClienteRepository.create(session, data)

# Listar clientes
@router.get("/", response_model=List[ClienteRead])
def list_clientes(session: Session = Depends(get_session)):
    return ClienteRepository.get_all(session)

# Obtener cliente por ID
@router.get("/{cliente_id}", response_model=ClienteRead)
def get_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = ClienteRepository.get_by_id(session, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

# Actualizar cliente
@router.put("/{cliente_id}", response_model=ClienteRead)
def update_cliente(cliente_id: int, data: ClienteUpdate, session: Session = Depends(get_session)):
    cliente = ClienteRepository.get_by_id(session, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return ClienteRepository.update(session, cliente, data)

# Eliminar cliente
@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, session: Session = Depends(get_session)):
    cliente = ClienteRepository.get_by_id(session, cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    ClienteRepository.delete(session, cliente)
    return {"ok": True, "message": "Cliente eliminado correctamente"}