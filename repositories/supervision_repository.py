from sqlmodel import Session
from models.supervision import Supervision


class SupervisionRepository:
    @staticmethod
    def create(session: Session, data) -> Supervision:
        sup = Supervision.from_orm(data)
        session.add(sup)
        session.commit()
        session.refresh(sup)
        return sup
