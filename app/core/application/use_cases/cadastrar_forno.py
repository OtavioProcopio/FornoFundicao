from core.domain.models import Forno
from core.interfaces.adapters.repositories.i_forno_repository import (
    IFornoRepository,
)


class CadastrarFornoUseCase:

    def __init__(self, forno_repo: IFornoRepository):
        self.forno_repo = forno_repo

    def execute(self, data: dict) -> Forno:
        codigo = data["codigo_identificador"]
        existente = self.forno_repo.get_by_codigo(codigo)
        if existente:
            raise ValueError(f"Já existe um forno cadastrado com o código {codigo}.")

        max_cad = int(data.get("max_cadinhos", 4))
        if max_cad < 1 or max_cad > 4:
            raise ValueError(
                "O limite máximo de cadinhos por forno deve ser entre 1 e 4."
            )

        forno = Forno(
            nome=data["nome"],
            codigo_identificador=codigo,
            setor=data["setor"],
            capacidade_kg=data.get("capacidade_kg"),
            tipo_liga=data.get("tipo_liga"),
            max_cadinhos=max_cad,
            ativo=data.get("ativo", True),
            observacao=data.get("observacao"),
        )
        return self.forno_repo.save(forno)
