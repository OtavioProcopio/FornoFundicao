from core.domain.models import Pirometro
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


class CadastrarPirometroUseCase:

    def __init__(self, pirometro_repo: IPirometroRepository):
        self.pirometro_repo = pirometro_repo

    def execute(self, pirometro_data: dict) -> Pirometro:
        pirometro = Pirometro(
            id=pirometro_data["id"],
            nome=pirometro_data["nome"],
            setor=pirometro_data["setor"],
            material_alvo=pirometro_data["material_alvo"],
            processo=pirometro_data["processo"],
            molde=pirometro_data["molde"],
            ativo=pirometro_data.get("ativo", True),
        )
        return self.pirometro_repo.save(pirometro)


class_name = "CadastrarPirometroUseCase"
