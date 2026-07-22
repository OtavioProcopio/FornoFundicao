from unittest.mock import MagicMock

import pytest

from core.application.use_cases.vincular_contexto_leitura import (
    VincularContextoLeituraUseCase,
)
from core.domain.models import Leitura
from core.interfaces.adapters.repositories.i_leitura_repository import (
    ILeituraRepository,
)


def test_vincular_contexto_sucesso():
    # 1. Arrange
    mock_repo = MagicMock(spec=ILeituraRepository)
    existing_leitura = Leitura(
        id=10,
        pirometro_id="PIR-01",
        codigo_pirometro_id=1,
        temperatura_lida=1550.0,
    )
    mock_repo.get_by_id.return_value = existing_leitura
    mock_repo.update.side_effect = lambda x: x

    use_case = VincularContextoLeituraUseCase(leitura_repo=mock_repo)
    contexto = {
        "corrida_id": "CR-100",
        "lote_id": "LT-200",
        "panela_id": "PN-03",
        "observacao": "Medição normal",
        "operador_id": "OP-99",
    }

    # 2. Act
    updated_leitura = use_case.execute(leitura_id=10, contexto_data=contexto)

    # 3. Assert
    assert updated_leitura.id == 10
    assert updated_leitura.corrida_id == "CR-100"
    assert updated_leitura.lote_id == "LT-200"
    assert updated_leitura.panela_id == "PN-03"
    assert updated_leitura.observacao == "Medição normal"
    assert updated_leitura.operador_id == "OP-99"

    mock_repo.get_by_id.assert_called_once_with(10)
    mock_repo.update.assert_called_once_with(existing_leitura)


def test_vincular_contexto_leitura_nao_encontrada():
    # 1. Arrange
    mock_repo = MagicMock(spec=ILeituraRepository)
    mock_repo.get_by_id.return_value = None

    use_case = VincularContextoLeituraUseCase(leitura_repo=mock_repo)

    # 2. Act & Assert
    with pytest.raises(ValueError, match="Leitura não encontrada"):
        use_case.execute(leitura_id=999, contexto_data={"corrida_id": "CR-100"})

    mock_repo.get_by_id.assert_called_once_with(999)
    mock_repo.update.assert_not_called()
