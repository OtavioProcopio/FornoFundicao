from typing import List

from core.domain.models import Pirometro
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


class ListarPirometrosUseCase:

    def __init__(self, pirometro_repo: IPirometroRepository):
        self.pirometro_repo = pirometro_repo

    def execute(self) -> List[Pirometro]:
        return self.pirometro_repo.list_all()
