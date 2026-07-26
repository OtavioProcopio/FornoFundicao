from typing import Any, Dict, List, Optional

from core.interfaces.adapters.repositories.i_cadinho_repository import (
    ICadinhoRepository,
)
from core.interfaces.adapters.repositories.i_forno_repository import (
    IFornoRepository,
)


class ListarFornosECadinhosUseCase:

    def __init__(
        self,
        forno_repo: IFornoRepository,
        cadinho_repo: ICadinhoRepository,
    ):
        self.forno_repo = forno_repo
        self.cadinho_repo = cadinho_repo

    def execute(self, setor: Optional[str] = None) -> List[Dict[str, Any]]:
        fornos = self.forno_repo.list_all(setor=setor)
        resultado = []

        for forno in fornos:
            if forno.id is None:
                continue

            active_cadinhos = self.cadinho_repo.list_active_by_forno(forno.id)
            cadinhos_info = []

            for cadinho in active_cadinhos:
                den = (
                    cadinho.espessura_inicial_mm
                    - cadinho.espessura_minima_seguranca_mm
                )
                if den > 0:
                    num = (
                        cadinho.espessura_atual_mm
                        - cadinho.espessura_minima_seguranca_mm
                    )
                    pct_refratario = round(
                        max(0.0, min(100.0, (num / den) * 100)), 2
                    )
                else:
                    pct_refratario = 0.0

                cadinhos_info.append(
                    {
                        "id": cadinho.id,
                        "posicao_no_forno": cadinho.posicao_no_forno,
                        "codigo_identificador": cadinho.codigo_identificador,
                        "espessura_inicial_mm": cadinho.espessura_inicial_mm,
                        "espessura_atual_mm": cadinho.espessura_atual_mm,
                        "espessura_minima_seguranca_mm": (
                            cadinho.espessura_minima_seguranca_mm
                        ),
                        "percentual_vida_util_refratario": pct_refratario,
                        "corridas_acumuladas": cadinho.corridas_acumuladas,
                        "max_corridas_esperadas": cadinho.max_corridas_esperadas,
                        "status": cadinho.status,
                        "pirometro_id": cadinho.pirometro_id,
                        "data_instalacao": cadinho.data_instalacao.isoformat(),
                        "observacao": cadinho.observacao,
                    }
                )

            resultado.append(
                {
                    "id": forno.id,
                    "nome": forno.nome,
                    "codigo_identificador": forno.codigo_identificador,
                    "setor": forno.setor,
                    "capacidade_kg": forno.capacidade_kg,
                    "tipo_liga": forno.tipo_liga,
                    "max_cadinhos": forno.max_cadinhos,
                    "total_cadinhos_ativos": len(active_cadinhos),
                    "ativo": forno.ativo,
                    "observacao": forno.observacao,
                    "cadinhos": cadinhos_info,
                }
            )

        return resultado
