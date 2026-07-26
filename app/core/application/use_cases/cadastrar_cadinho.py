from core.domain.models import Cadinho
from core.interfaces.adapters.repositories.i_cadinho_repository import (
    ICadinhoRepository,
)
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


class CadastrarCadinhoUseCase:

    def __init__(
        self,
        cadinho_repo: ICadinhoRepository,
        pirometro_repo: IPirometroRepository,
    ):
        self.cadinho_repo = cadinho_repo
        self.pirometro_repo = pirometro_repo

    def execute(self, data: dict) -> Cadinho:
        pirometro_id = data["pirometro_id"]
        pirometro = self.pirometro_repo.get_by_id(pirometro_id)
        if not pirometro:
            raise ValueError(f"Pirômetro {pirometro_id} não encontrado.")

        espessura_inicial = float(data["espessura_inicial_mm"])
        espessura_minima = float(data.get("espessura_minima_seguranca_mm", 50.0))

        if espessura_inicial <= 0:
            raise ValueError("Espessura inicial deve ser maior que zero.")
        if espessura_minima >= espessura_inicial:
            raise ValueError(
                "Espessura mínima de segurança deve ser menor que a espessura inicial."
            )

        cadinho = Cadinho(
            pirometro_id=pirometro_id,
            codigo_identificador=data["codigo_identificador"],
            espessura_inicial_mm=espessura_inicial,
            espessura_atual_mm=espessura_inicial,
            espessura_minima_seguranca_mm=espessura_minima,
            max_corridas_esperadas=data.get("max_corridas_esperadas", 200),
            observacao=data.get("observacao"),
            status="ATIVO",
        )
        return self.cadinho_repo.save(cadinho)
