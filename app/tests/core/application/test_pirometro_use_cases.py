from unittest.mock import MagicMock

import pytest

from core.application.use_cases.cadastrar_pirometro import (
    CadastrarPirometroUseCase,
)
from core.application.use_cases.configurar_codigo_pirometro import (
    ConfigurarCodigoPirometroUseCase,
)
from core.application.use_cases.listar_pirometros import ListarPirometrosUseCase
from core.domain.models import Pirometro
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


def test_listar_pirometros():
    # Arrange
    mock_repo = MagicMock(spec=IPirometroRepository)
    p1 = Pirometro(
        id="PIR-01", nome="P1", setor="A", material_alvo="M", processo="P", molde="M"
    )
    mock_repo.list_all.return_value = [p1]

    use_case = ListarPirometrosUseCase(pirometro_repo=mock_repo)

    # Act
    result = use_case.execute()

    # Assert
    assert len(result) == 1
    assert result[0].id == "PIR-01"
    mock_repo.list_all.assert_called_once()


def test_cadastrar_pirometro():
    # Arrange
    mock_repo = MagicMock(spec=IPirometroRepository)
    mock_repo.save.side_effect = lambda x: x
    use_case = CadastrarPirometroUseCase(pirometro_repo=mock_repo)
    data = {
        "id": "PIR-01",
        "nome": "P1",
        "setor": "A",
        "material_alvo": "M",
        "processo": "P",
        "molde": "M",
    }

    # Act
    result = use_case.execute(data)

    # Assert
    assert result.id == "PIR-01"
    assert result.nome == "P1"
    mock_repo.save.assert_called_once()


def test_configurar_codigo_pirometro_sucesso_novo():
    # Arrange
    mock_repo = MagicMock(spec=IPirometroRepository)
    pirometro = Pirometro(
        id="PIR-01", nome="P1", setor="A", material_alvo="M", processo="P", molde="M"
    )
    mock_repo.get_by_id.return_value = pirometro
    mock_repo.get_codigo.return_value = None
    mock_repo.save_codigo.side_effect = lambda x: x

    use_case = ConfigurarCodigoPirometroUseCase(pirometro_repo=mock_repo)
    codigo_data = {
        "codigo": 5,
        "etapa_nome": "Vazamento",
        "temp_min_esperada": 1500.0,
        "temp_max_esperada": 1600.0,
    }

    # Act
    result = use_case.execute(pirometro_id="PIR-01", codigo_data=codigo_data)

    # Assert
    assert result.pirometro_id == "PIR-01"
    assert result.codigo == 5
    assert result.etapa_nome == "Vazamento"
    mock_repo.get_by_id.assert_called_once_with("PIR-01")
    mock_repo.get_codigo.assert_called_once_with("PIR-01", 5)
    mock_repo.save_codigo.assert_called_once()


def test_configurar_codigo_pirometro_inexistente():
    # Arrange
    mock_repo = MagicMock(spec=IPirometroRepository)
    mock_repo.get_by_id.return_value = None

    use_case = ConfigurarCodigoPirometroUseCase(pirometro_repo=mock_repo)

    # Act & Assert
    with pytest.raises(ValueError, match="Pirômetro não encontrado"):
        use_case.execute(
            pirometro_id="PIR-99", codigo_data={"codigo": 1, "etapa_nome": "X"}
        )

    mock_repo.get_by_id.assert_called_once_with("PIR-99")
    mock_repo.save_codigo.assert_not_called()
