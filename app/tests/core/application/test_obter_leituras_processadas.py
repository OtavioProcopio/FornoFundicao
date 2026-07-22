from unittest.mock import MagicMock

from core.application.use_cases.obter_leituras_processadas import (
    ObterLeiturasProcessadasUseCase,
)
from core.domain.models import CodigoPirometro, Leitura
from core.interfaces.adapters.repositories.i_leitura_repository import (
    ILeituraRepository,
)
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


def test_obter_leituras_processadas_dentro_dos_limites():
    # 1. Arrange
    mock_leitura_repo = MagicMock(spec=ILeituraRepository)
    mock_pirometro_repo = MagicMock(spec=IPirometroRepository)

    leitura = Leitura(
        id=1,
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1550.0,
        corrida_id="CR-01",
    )
    mock_leitura_repo.list_by_filters.return_value = [leitura]

    codigo_meta = CodigoPirometro(
        id=101,
        pirometro_id="PIR-01",
        codigo=5,
        etapa_nome="Vazamento",
        temp_min_esperada=1500.0,
        temp_max_esperada=1600.0,
    )
    mock_pirometro_repo.get_codigo_by_id.return_value = codigo_meta

    use_case = ObterLeiturasProcessadasUseCase(
        leitura_repo=mock_leitura_repo, pirometro_repo=mock_pirometro_repo
    )

    # 2. Act
    result = use_case.execute(filters={"pirometro_id": "PIR-01"})

    # 3. Assert
    assert len(result) == 1
    assert result[0]["id"] == 1
    assert result[0]["etapa_nome"] == "Vazamento"
    assert result[0]["codigo_num"] == 5
    assert result[0]["alerta_temperatura"] is False


def test_obter_leituras_processadas_abaixo_do_limite_minimo():
    # 1. Arrange
    mock_leitura_repo = MagicMock(spec=ILeituraRepository)
    mock_pirometro_repo = MagicMock(spec=IPirometroRepository)

    leitura = Leitura(
        id=1,
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1490.0,  # Abaixo de 1500
    )
    mock_leitura_repo.list_by_filters.return_value = [leitura]

    codigo_meta = CodigoPirometro(
        id=101,
        pirometro_id="PIR-01",
        codigo=5,
        etapa_nome="Vazamento",
        temp_min_esperada=1500.0,
        temp_max_esperada=1600.0,
    )
    mock_pirometro_repo.get_codigo_by_id.return_value = codigo_meta

    use_case = ObterLeiturasProcessadasUseCase(
        leitura_repo=mock_leitura_repo, pirometro_repo=mock_pirometro_repo
    )

    # 2. Act
    result = use_case.execute(filters={})

    # 3. Assert
    assert len(result) == 1
    assert result[0]["alerta_temperatura"] is True


def test_obter_leituras_processadas_acima_do_limite_maximo():
    # 1. Arrange
    mock_leitura_repo = MagicMock(spec=ILeituraRepository)
    mock_pirometro_repo = MagicMock(spec=IPirometroRepository)

    leitura = Leitura(
        id=1,
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1610.0,  # Acima de 1600
    )
    mock_leitura_repo.list_by_filters.return_value = [leitura]

    codigo_meta = CodigoPirometro(
        id=101,
        pirometro_id="PIR-01",
        codigo=5,
        etapa_nome="Vazamento",
        temp_min_esperada=1500.0,
        temp_max_esperada=1600.0,
    )
    mock_pirometro_repo.get_codigo_by_id.return_value = codigo_meta

    use_case = ObterLeiturasProcessadasUseCase(
        leitura_repo=mock_leitura_repo, pirometro_repo=mock_pirometro_repo
    )

    # 2. Act
    result = use_case.execute(filters={})

    # 3. Assert
    assert len(result) == 1
    assert result[0]["alerta_temperatura"] is True


def test_obter_leituras_processadas_etapa_desconhecida():
    # 1. Arrange
    mock_leitura_repo = MagicMock(spec=ILeituraRepository)
    mock_pirometro_repo = MagicMock(spec=IPirometroRepository)

    leitura = Leitura(
        id=1,
        pirometro_id="PIR-01",
        codigo_pirometro_id=999,  # Inexistente
        temperatura_lida=1500.0,
    )
    mock_leitura_repo.list_by_filters.return_value = [leitura]
    mock_pirometro_repo.get_codigo_by_id.return_value = None

    use_case = ObterLeiturasProcessadasUseCase(
        leitura_repo=mock_leitura_repo, pirometro_repo=mock_pirometro_repo
    )

    # 2. Act
    result = use_case.execute(filters={})

    # 3. Assert
    assert len(result) == 1
    assert result[0]["etapa_nome"] == "Etapa Desconhecida"
    assert result[0]["codigo_num"] is None
    assert result[0]["alerta_temperatura"] is False
