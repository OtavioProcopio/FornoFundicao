from typing import Any, Dict, List, Optional

from core.interfaces.adapters.repositories.i_cadinho_repository import (
    ICadinhoRepository,
)


class ObterStatusCampanhaUseCase:

    def __init__(self, cadinho_repo: ICadinhoRepository):
        self.cadinho_repo = cadinho_repo

    def execute(self, pirometro_id: Optional[str] = None) -> List[Dict[str, Any]]:
        cadinhos = self.cadinho_repo.list_all(pirometro_id=pirometro_id)
        resultado = []

        for cadinho in cadinhos:
            registros = (
                self.cadinho_repo.list_registros_desgaste(cadinho.id)
                if cadinho.id is not None
                else []
            )

            # Cálculo da porcentagem de vida útil restante da espessura refratária
            den = cadinho.espessura_inicial_mm - cadinho.espessura_minima_seguranca_mm
            if den > 0:
                num = cadinho.espessura_atual_mm - cadinho.espessura_minima_seguranca_mm
                pct_refratario = round(max(0.0, min(100.0, (num / den) * 100)), 2)
            else:
                pct_refratario = 0.0

            resultado.append(
                {
                    "id": cadinho.id,
                    "pirometro_id": cadinho.pirometro_id,
                    "codigo_identificador": cadinho.codigo_identificador,
                    "espessura_inicial_mm": cadinho.espessura_inicial_mm,
                    "espessura_atual_mm": cadinho.espessura_atual_mm,
                    "espessura_minima_seguranca_mm": (
                        cadinho.espessura_minima_seguranca_mm
                    ),
                    "percentual_vida_util_refratario": pct_refratario,
                    "corridas_acumuladas": cadinho.corridas_acumuladas,
                    "max_corridas_esperadas": cadinho.max_corridas_esperadas,
                    "data_instalacao": cadinho.data_instalacao.isoformat(),
                    "data_substituicao": (
                        cadinho.data_substituicao.isoformat()
                        if cadinho.data_substituicao
                        else None
                    ),
                    "status": cadinho.status,
                    "observacao": cadinho.observacao,
                    "total_registros_desgaste": len(registros),
                    "registros_desgaste": [
                        {
                            "id": r.id,
                            "espessura_medida_mm": r.espessura_medida_mm,
                            "corridas_no_momento": r.corridas_no_momento,
                            "operador_id": r.operador_id,
                            "timestamp": r.timestamp.isoformat(),
                            "observacao": r.observacao,
                        }
                        for r in registros
                    ],
                }
            )

        return resultado
