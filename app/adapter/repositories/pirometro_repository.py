from typing import List, Optional

from sqlmodel import Session, select

from core.domain.models import CodigoPirometro, Pirometro
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


class PirometroRepository(IPirometroRepository):

    def __init__(self, session: Session):
        self.session = session

    def save(self, pirometro: Pirometro) -> Pirometro:
        self.session.add(pirometro)
        self.session.commit()
        self.session.refresh(pirometro)
        return pirometro

    def get_by_id(self, pirometro_id: str) -> Optional[Pirometro]:
        return self.session.get(Pirometro, pirometro_id)

    def list_all(self) -> List[Pirometro]:
        return list(self.session.exec(select(Pirometro)).all())

    def save_codigo(self, codigo: CodigoPirometro) -> CodigoPirometro:
        self.session.add(codigo)
        self.session.commit()
        self.session.refresh(codigo)
        return codigo

    def get_codigo(self, pirometro_id: str, codigo: int) -> Optional[CodigoPirometro]:
        statement = select(CodigoPirometro).where(
            CodigoPirometro.pirometro_id == pirometro_id,
            CodigoPirometro.codigo == codigo,
        )
        return self.session.exec(statement).first()

    def get_codigo_by_id(self, codigo_id: int) -> Optional[CodigoPirometro]:
        return self.session.get(CodigoPirometro, codigo_id)
