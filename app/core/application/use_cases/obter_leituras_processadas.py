from typing import Any, Dict, List

from core.interfaces.adapters.repositories.i_leitura_repository import (
    ILeituraRepository,
)
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


class ObterLeiturasProcessadasUseCase:

    def __init__(
        self,
        leitura_repo: ILeituraRepository,
        pirometro_repo: IPirometroRepository,
    ):
        self.leitura_repo = leitura_repo
        self.pirometro_repo = pirometro_repo

    def execute(self, filters: Dict[str, Any]) -> List[Dict[str, Any]]:
        raw_leituras = self.leitura_repo.list_by_filters(**filters)
        processadas = []

        for leitura in raw_leituras:
            # Buscar a tradução do código e limites térmicos
            codigo_meta = self.pirometro_repo.get_codigo_by_id(
                leitura.codigo_pirometro_id
            )

            # Validar se a temperatura lida está fora dos limites
            is_outside_bounds = False
            if codigo_meta:
                temp = leitura.temperatura_lida
                if (
                    codigo_meta.temp_min_esperada is not None
                    and temp < codigo_meta.temp_min_esperada
                ):
                    is_outside_bounds = True
                if (
                    codigo_meta.temp_max_esperada is not None
                    and temp > codigo_meta.temp_max_esperada
                ):
                    is_outside_bounds = True

            processadas.append(
                {
                    "id": leitura.id,
                    "pirometro_id": leitura.pirometro_id,
                    "temperatura_lida": leitura.temperatura_lida,
                    "timestamp": leitura.timestamp,
                    "corrida_id": leitura.corrida_id,
                    "lote_id": leitura.lote_id,
                    "panela_id": leitura.panela_id,
                    "observacao": leitura.observacao,
                    "operador_id": leitura.operador_id,
                    "etapa_nome": (
                        codigo_meta.etapa_nome if codigo_meta else "Etapa Desconhecida"
                    ),
                    "codigo_num": (codigo_meta.codigo if codigo_meta else None),
                    "temp_min_esperada": (
                        codigo_meta.temp_min_esperada if codigo_meta else None
                    ),
                    "temp_max_esperada": (
                        codigo_meta.temp_max_esperada if codigo_meta else None
                    ),
                    "alerta_temperatura": is_outside_bounds,
                }
            )

        return processadas
