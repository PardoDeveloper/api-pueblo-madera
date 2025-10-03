from sqlmodel import Session, select
from models.material import Material
from schemas.material import MaterialCreate, MaterialUpdate
from typing import List, Optional


class MaterialRepository:
    @staticmethod
    def create(session: Session, data: MaterialCreate) -> Material:
        m = Material.from_orm(data)
        session.add(m)
        session.commit()
        session.refresh(m)
        return m

    @staticmethod
    def get_all(session: Session) -> List[Material]:
        return session.exec(select(Material)).all()

    @staticmethod
    def get_by_id(session: Session, material_id: int) -> Optional[Material]:
        return session.get(Material, material_id)

    @staticmethod
    def update(session: Session, material: Material, data: MaterialUpdate) -> Material:
        for k, v in data.dict(exclude_unset=True).items():
            setattr(material, k, v)
        session.add(material)
        session.commit()
        session.refresh(material)
        return material

    @staticmethod
    def delete(session: Session, material: Material) -> None:
        session.delete(material)
        session.commit()
