from typing import List, Optional

from sqlmodel import Session, col, select

from core.domain.models import Cadinho, RegistroDesgasteCadinho
from core.interfaces.adapters.repositories.i_cadinho_repository import (
    ICadinhoRepository,
)


class CadinhoRepository(ICadinhoRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, cadinho: Cadinho) -> Cadinho:
        self.session.add(cadinho)
        self.session.commit()
        self.session.refresh(cadinho)
        return cadinho

    def get_by_id(self, cadinho_id: int) -> Optional[Cadinho]:
        return self.session.get(Cadinho, cadinho_id)

    def list_all(self, pirometro_id: Optional[str] = None) -> List[Cadinho]:
        statement = select(Cadinho)
        if pirometro_id:
            statement = statement.where(Cadinho.pirometro_id == pirometro_id)
        statement = statement.order_by(col(Cadinho.id).desc())
        return list(self.session.exec(statement).all())

    def get_ativo_by_pirometro(self, pirometro_id: str) -> Optional[Cadinho]:
        statement = select(Cadinho).where(
            Cadinho.pirometro_id == pirometro_id,
            Cadinho.status.in_(["ATIVO", "ALERTA"]),  # type: ignore[attr-defined]
        )
        return self.session.exec(statement).first()

    def update(self, cadinho: Cadinho) -> Cadinho:
        self.session.add(cadinho)
        self.session.commit()
        self.session.refresh(cadinho)
        return cadinho

    def save_registro_desgaste(
        self, registro: RegistroDesgasteCadinho
    ) -> RegistroDesgasteCadinho:
        self.session.add(registro)
        self.session.commit()
        self.session.refresh(registro)
        return registro

    def list_registros_desgaste(
        self, cadinho_id: int
    ) -> List[RegistroDesgasteCadinho]:
        statement = (
            select(RegistroDesgasteCadinho)
            .where(RegistroDesgasteCadinho.cadinho_id == cadinho_id)
            .order_by(col(RegistroDesgasteCadinho.timestamp).desc())
        )
        return list(self.session.exec(statement).all())
