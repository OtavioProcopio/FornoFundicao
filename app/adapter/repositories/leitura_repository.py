from datetime import datetime
from typing import List, Optional

from sqlmodel import Session, col, select

from core.domain.models import Leitura
from core.interfaces.adapters.repositories.i_leitura_repository import (
    ILeituraRepository,
)


class LeituraRepository(ILeituraRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, leitura: Leitura) -> Leitura:
        self.session.add(leitura)
        self.session.commit()
        self.session.refresh(leitura)
        return leitura

    def get_by_id(self, leitura_id: int) -> Optional[Leitura]:
        return self.session.get(Leitura, leitura_id)

    def update(self, leitura: Leitura) -> Leitura:
        self.session.add(leitura)
        self.session.commit()
        self.session.refresh(leitura)
        return leitura

    def list_by_filters(
        self,
        pirometro_id: Optional[str] = None,
        corrida_id: Optional[str] = None,
        panela_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Leitura]:
        statement = select(Leitura)
        if pirometro_id is not None:
            statement = statement.where(Leitura.pirometro_id == pirometro_id)
        if corrida_id is not None:
            statement = statement.where(Leitura.corrida_id == corrida_id)
        if panela_id is not None:
            statement = statement.where(Leitura.panela_id == panela_id)
        if start_date is not None:
            statement = statement.where(Leitura.timestamp >= start_date)
        if end_date is not None:
            statement = statement.where(Leitura.timestamp <= end_date)

        statement = statement.order_by(col(Leitura.timestamp).desc())
        return list(self.session.exec(statement).all())
