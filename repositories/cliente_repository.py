# repositories/cliente_repository.py
from sqlmodel import Session, select
from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteUpdate
from typing import List, Optional

class ClienteRepository:

    @staticmethod
    def create(session: Session, data: ClienteCreate) -> Cliente:
        cliente = Cliente.from_orm(data)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente

    @staticmethod
    def get_all(session: Session) -> List[Cliente]:
        return session.exec(select(Cliente)).all()

    @staticmethod
    def get_by_id(session: Session, cliente_id: int) -> Optional[Cliente]:
        return session.get(Cliente, cliente_id)

    @staticmethod
    def update(session: Session, cliente: Cliente, data: ClienteUpdate) -> Cliente:
        for key, value in data.dict(exclude_unset=True).items():
            setattr(cliente, key, value)
        session.add(cliente)
        session.commit()
        session.refresh(cliente)
        return cliente

    @staticmethod
    def delete(session: Session, cliente: Cliente) -> None:
        session.delete(cliente)
        session.commit()
