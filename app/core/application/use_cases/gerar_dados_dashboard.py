from datetime import datetime, timedelta
from typing import Any, Dict, List

from core.interfaces.adapters.repositories.i_leitura_repository import (
    ILeituraRepository,
)
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


class GerarDadosDashboardUseCase:

    def __init__(
        self,
        leitura_repo: ILeituraRepository,
        pirometro_repo: IPirometroRepository,
    ):
        self.leitura_repo = leitura_repo
        self.pirometro_repo = pirometro_repo

    def execute(self) -> Dict[str, Any]:
        # 1. Obter todos os pirômetros
        pirometros = self.pirometro_repo.list_all()

        # 2. Definir janela do turno (últimas 8 horas de forma dinâmica)
        start_date = datetime.utcnow() - timedelta(hours=8)
        leituras_turno_raw = self.leitura_repo.list_by_filters(start_date=start_date)

        # 3. Cache dos metadados de código para evitar múltiplas queries
        codigo_meta_cache: Dict[int, Any] = {}
        leituras_processadas = []

        total_nc = 0
        total_falhas = 0
        nc_baixa = 0
        nc_alta = 0

        # Mapeamento de leituras por forno
        leituras_por_forno: Dict[str, List[Dict[str, Any]]] = {
            p.id: [] for p in pirometros
        }

        for leitura in leituras_turno_raw:
            # Buscar ou cachear metadados do código
            cid = leitura.codigo_pirometro_id
            if cid not in codigo_meta_cache:
                codigo_meta_cache[cid] = self.pirometro_repo.get_codigo_by_id(cid)

            codigo_meta = codigo_meta_cache[cid]

            # Processar status da temperatura
            status_qualidade = "OK"
            temp = leitura.temperatura_lida

            if temp <= 0 or temp > 2000:
                status_qualidade = "FALHA_SENSOR"
                total_falhas += 1
            elif codigo_meta:
                if (
                    codigo_meta.temp_min_esperada is not None
                    and temp < codigo_meta.temp_min_esperada
                ):
                    status_qualidade = "NC_BAIXA"
                    total_nc += 1
                    nc_baixa += 1
                elif (
                    codigo_meta.temp_max_esperada is not None
                    and temp > codigo_meta.temp_max_esperada
                ):
                    status_qualidade = "NC_ALTA"
                    total_nc += 1
                    nc_alta += 1

            leitura_item = {
                "id": leitura.id,
                "pirometro_id": leitura.pirometro_id,
                "temperatura": temp,
                "timestamp": leitura.timestamp,
                "status_qualidade": status_qualidade,
                "etapa_nome": (
                    codigo_meta.etapa_nome if codigo_meta else "Etapa Desconhecida"
                ),
                "codigo_num": (codigo_meta.codigo if codigo_meta else None),
                "temp_min": (codigo_meta.temp_min_esperada if codigo_meta else None),
                "temp_max": (codigo_meta.temp_max_esperada if codigo_meta else None),
                "corrida_id": leitura.corrida_id,
                "lote_id": leitura.lote_id,
                "panela_id": leitura.panela_id,
                "observacao": leitura.observacao,
                "operador_id": leitura.operador_id,
            }

            leituras_processadas.append(leitura_item)
            if leitura.pirometro_id in leituras_por_forno:
                leituras_por_forno[leitura.pirometro_id].append(leitura_item)

        # 4. Calcular KPIs de Qualidade
        total_leituras = len(leituras_processadas)
        denominador = total_leituras - total_falhas
        taxa_conformidade = 100.0
        if denominador > 0:
            conformes = denominador - total_nc
            taxa_conformidade = (conformes / denominador) * 100.0

        # 5. Montar Nível Operacional (Tempo Real)
        status_fornos = {}
        for p in pirometros:
            forno_leituras = leituras_por_forno[p.id]
            # Primeiro item é o mais recente (list_by_filters ordenado desc)
            ultima = forno_leituras[0] if forno_leituras else None

            status_fornos[p.id] = {
                "equipamento_nome": p.nome,
                "setor": p.setor,
                "ativo": p.ativo,
                "contexto_producao": {
                    "corrida_ativa": (ultima["corrida_id"] if ultima else None),
                    "lote_ativo": (ultima["lote_id"] if ultima else None),
                    "panela_ativa": (ultima["panela_id"] if ultima else None),
                },
                "ultima_leitura": (
                    {
                        "id": ultima["id"],
                        "temperatura": ultima["temperatura"],
                        "timestamp": ultima["timestamp"],
                        "codigo_num": ultima["codigo_num"],
                        "etapa_nome": ultima["etapa_nome"],
                        "temp_min": ultima["temp_min"],
                        "temp_max": ultima["temp_max"],
                        "status_qualidade": ultima["status_qualidade"],
                    }
                    if ultima
                    else None
                ),
                "tendencia_recente": [
                    {
                        "timestamp": item["timestamp"],
                        "temperatura": item["temperatura"],
                        "status": item["status_qualidade"],
                    }
                    for item in reversed(forno_leituras[:10])
                ],
            }

        # 6. Montar Nível Gerencial (Estabilidade)
        estabilidade_fornos = {}
        for p in pirometros:
            forno_leituras = leituras_por_forno[p.id]
            temps = [
                item["temperatura"]
                for item in forno_leituras
                if item["status_qualidade"] != "FALHA_SENSOR"
            ]

            std_dev = 0.0
            avg_temp = 0.0
            n = len(temps)

            if n > 0:
                avg_temp = sum(temps) / n
                if n >= 2:
                    variance = sum((t - avg_temp) ** 2 for t in temps) / n
                    std_dev = variance**0.5

            estabilidade_fornos[p.id] = {
                "leituras_turno": n,
                "temperatura_media": round(avg_temp, 1),
                "desvio_padrao": round(std_dev, 2),
            }

        fornos_ativos = sum(1 for p in pirometros if p.ativo)
        fornos_inativos = sum(1 for p in pirometros if not p.ativo)

        return {
            "operacional": {"status_fornos": status_fornos},
            "qualidade": {
                "kpis": {
                    "total_leituras": total_leituras,
                    "total_nc": total_nc,
                    "taxa_conformidade": round(taxa_conformidade, 2),
                    "falhas_sensor": total_falhas,
                },
                "distribuicao_nc": {
                    "NC_BAIXA": nc_baixa,
                    "NC_ALTA": nc_alta,
                },
            },
            "gerencial": {
                "produtividade": {
                    "fornos_ativos": fornos_ativos,
                    "fornos_inativos": fornos_inativos,
                    "total_equipamentos": len(pirometros),
                },
                "estabilidade_fornos": estabilidade_fornos,
            },
        }
