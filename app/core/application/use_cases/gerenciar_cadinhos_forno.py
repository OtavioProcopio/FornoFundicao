from datetime import datetime
from typing import Optional

from core.domain.models import Cadinho
from core.interfaces.adapters.repositories.i_cadinho_repository import (
    ICadinhoRepository,
)
from core.interfaces.adapters.repositories.i_forno_repository import (
    IFornoRepository,
)


class GerenciarCadinhosFornoUseCase:

    def __init__(
        self,
        cadinho_repo: ICadinhoRepository,
        forno_repo: IFornoRepository,
    ):
        self.cadinho_repo = cadinho_repo
        self.forno_repo = forno_repo

    def adicionar_cadinho(self, forno_id: int, data: dict) -> Cadinho:
        forno = self.forno_repo.get_by_id(forno_id)
        if not forno:
            raise ValueError(f"Forno com ID {forno_id} não encontrado.")

        active_cadinhos = self.cadinho_repo.list_active_by_forno(forno_id)
        if len(active_cadinhos) >= forno.max_cadinhos:
            raise ValueError(
                f"Limite máximo de {forno.max_cadinhos} cadinhos por forno atingido."
            )

        posicao = data.get("posicao_no_forno")
        if posicao is not None:
            if posicao < 1 or posicao > 4:
                raise ValueError("A posição do cadinho no forno deve ser entre 1 e 4.")
            posicoes_ocupadas = [c.posicao_no_forno for c in active_cadinhos]
            if posicao in posicoes_ocupadas:
                raise ValueError(
                    f"A posição {posicao} no forno já está ocupada "
                    "por um cadinho ativo."
                )
        else:
            posicoes_ocupadas_set = {c.posicao_no_forno for c in active_cadinhos}
            posicao = next(i for i in range(1, 5) if i not in posicoes_ocupadas_set)

        espessura_inicial = float(data["espessura_inicial_mm"])
        espessura_minima = float(data.get("espessura_minima_seguranca_mm", 50.0))

        if espessura_inicial <= 0:
            raise ValueError("Espessura inicial deve ser maior que zero.")
        if espessura_minima >= espessura_inicial:
            raise ValueError(
                "Espessura mínima de segurança deve ser menor que a espessura inicial."
            )

        cadinho = Cadinho(
            forno_id=forno_id,
            posicao_no_forno=posicao,
            pirometro_id=data.get("pirometro_id"),
            codigo_identificador=data["codigo_identificador"],
            espessura_inicial_mm=espessura_inicial,
            espessura_atual_mm=espessura_inicial,
            espessura_minima_seguranca_mm=espessura_minima,
            max_corridas_esperadas=data.get("max_corridas_esperadas", 200),
            observacao=data.get("observacao"),
            status="ATIVO",
        )
        return self.cadinho_repo.save(cadinho)

    def editar_cadinho(self, cadinho_id: int, data: dict) -> Cadinho:
        cadinho = self.cadinho_repo.get_by_id(cadinho_id)
        if not cadinho:
            raise ValueError(f"Cadinho com ID {cadinho_id} não encontrado.")

        if "codigo_identificador" in data and data["codigo_identificador"]:
            cadinho.codigo_identificador = data["codigo_identificador"]
        if "espessura_minima_seguranca_mm" in data:
            cadinho.espessura_minima_seguranca_mm = float(
                data["espessura_minima_seguranca_mm"]
            )
        if "max_corridas_esperadas" in data:
            cadinho.max_corridas_esperadas = data["max_corridas_esperadas"]
        if "observacao" in data:
            cadinho.observacao = data["observacao"]
        if "pirometro_id" in data:
            cadinho.pirometro_id = data["pirometro_id"]

        return self.cadinho_repo.update(cadinho)

    def remover_cadinho(
        self, cadinho_id: int, observacao: Optional[str] = None
    ) -> Cadinho:
        cadinho = self.cadinho_repo.get_by_id(cadinho_id)
        if not cadinho:
            raise ValueError(f"Cadinho com ID {cadinho_id} não encontrado.")

        cadinho.status = "SUBSTITUIDO"
        cadinho.data_substituicao = datetime.utcnow()
        if observacao:
            cadinho.observacao = (
                f"{cadinho.observacao} | Removido: {observacao}"
                if cadinho.observacao
                else f"Removido: {observacao}"
            )
        return self.cadinho_repo.update(cadinho)
