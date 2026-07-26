from typing import List, Optional

from sqlmodel import Session, col, select

from core.domain.models import Forno
from core.interfaces.adapters.repositories.i_forno_repository import (
    IFornoRepository,
)


class FornoRepository(IFornoRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, forno: Forno) -> Forno:
        self.session.add(forno)
        self.session.commit()
        self.session.refresh(forno)
        return forno

    def get_by_id(self, forno_id: int) -> Optional[Forno]:
        return self.session.get(Forno, forno_id)

    def get_by_codigo(self, codigo_identificador: str) -> Optional[Forno]:
        statement = select(Forno).where(
            Forno.codigo_identificador == codigo_identificador
        )
        return self.session.exec(statement).first()

    def list_all(self, setor: Optional[str] = None) -> List[Forno]:
        statement = select(Forno)
        if setor:
            statement = statement.where(Forno.setor == setor)
        statement = statement.order_by(col(Forno.id).asc())
        return list(self.session.exec(statement).all())

    def update(self, forno: Forno) -> Forno:
        self.session.add(forno)
        self.session.commit()
        self.session.refresh(forno)
        return forno
