from datetime import datetime, timedelta
from unittest.mock import MagicMock

import pytest

from core.application.use_cases.gerar_dados_dashboard import (
    GerarDadosDashboardUseCase,
)
from core.domain.models import CodigoPirometro, Leitura, Pirometro
from core.interfaces.adapters.repositories.i_leitura_repository import (
    ILeituraRepository,
)
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


def test_gerar_dados_dashboard_workflow():
    # 1. Arrange
    mock_leitura_repo = MagicMock(spec=ILeituraRepository)
    mock_pirometro_repo = MagicMock(spec=IPirometroRepository)

    now = datetime.utcnow()

    # Setup Pirômetro
    p1 = Pirometro(
        id="PIR-01",
        nome="Forno 1",
        setor="Aço",
        material_alvo="SAE 1045",
        processo="C",
        molde="M",
        ativo=True,
    )
    mock_pirometro_repo.list_all.return_value = [p1]

    # Setup Códigos de Limites
    codigo_meta = CodigoPirometro(
        id=101,
        pirometro_id="PIR-01",
        codigo=5,
        etapa_nome="Vazamento",
        temp_min_esperada=1500.0,
        temp_max_esperada=1600.0,
    )
    mock_pirometro_repo.get_codigo_by_id.return_value = codigo_meta

    # Setup Leituras do Turno (3 leituras: 2 OK, 1 NC_BAIXA)
    l1 = Leitura(
        id=1,
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1550.0,  # OK
        corrida_id="CR-01",
        panela_id="P-01",
        timestamp=now - timedelta(minutes=30),
    )
    l2 = Leitura(
        id=2,
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1480.0,  # NC_BAIXA
        corrida_id="CR-01",
        panela_id="P-01",
        timestamp=now - timedelta(minutes=15),
    )
    l3 = Leitura(
        id=3,
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1560.0,  # OK
        corrida_id="CR-01",
        panela_id="P-02",
        timestamp=now,
    )

    # O repositório retorna as leituras do turno para estatísticas
    mock_leitura_repo.list_by_filters.return_value = [l3, l2, l1]

    use_case = GerarDadosDashboardUseCase(
        leitura_repo=mock_leitura_repo, pirometro_repo=mock_pirometro_repo
    )

    # 2. Act
    dashboard_data = use_case.execute()

    # 3. Assert - Nível Operacional (Tempo Real)
    fornos = dashboard_data["operacional"]["status_fornos"]
    assert "PIR-01" in fornos
    assert fornos["PIR-01"]["equipamento_nome"] == "Forno 1"
    assert fornos["PIR-01"]["ultima_leitura"]["temperatura"] == 1560.0
    assert fornos["PIR-01"]["contexto_producao"]["corrida_ativa"] == "CR-01"
    assert len(fornos["PIR-01"]["tendencia_recente"]) == 3

    # Assert - Nível de Qualidade
    qualidade = dashboard_data["qualidade"]
    assert qualidade["kpis"]["total_leituras"] == 3
    assert qualidade["kpis"]["total_nc"] == 1
    assert qualidade["kpis"]["taxa_conformidade"] == pytest.approx(66.67, 0.01)
    assert qualidade["distribuicao_nc"]["NC_BAIXA"] == 1
    assert qualidade["distribuicao_nc"]["NC_ALTA"] == 0

    # Assert - Nível Gerencial (Fornos Ativos & Estabilidade)
    gerencial = dashboard_data["gerencial"]
    assert gerencial["produtividade"]["fornos_ativos"] == 1
    assert gerencial["produtividade"]["fornos_inativos"] == 0
    assert "PIR-01" in gerencial["estabilidade_fornos"]
    # Desvio padrão térmico calculado para PIR-01
    assert gerencial["estabilidade_fornos"]["PIR-01"]["desvio_padrao"] > 0
