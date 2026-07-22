from datetime import datetime, timedelta

import pytest
from sqlmodel import Session, SQLModel, create_engine

from adapter.repositories.leitura_repository import LeituraRepository
from core.domain.models import CodigoPirometro, Leitura, Pirometro


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_leitura_repository_save_get_and_update(session):
    # 1. Arrange
    pirometro = Pirometro(
        id="PIR-01",
        nome="P1",
        setor="A",
        material_alvo="M1",
        processo="P",
        molde="M",
    )
    codigo = CodigoPirometro(
        id=101,
        pirometro_id="PIR-01",
        codigo=5,
        etapa_nome="V",
        ativo=True,
    )
    session.add(pirometro)
    session.add(codigo)
    session.commit()

    repo = LeituraRepository(session=session)
    leitura = Leitura(
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1550.0,
    )

    # 2. Act
    saved = repo.save(leitura)
    retrieved = repo.get_by_id(saved.id)

    # Update context fields
    retrieved.corrida_id = "CR-999"
    retrieved.lote_id = "LT-888"
    retrieved.panela_id = "PN-07"
    retrieved.observacao = "Leitura atualizada"
    retrieved.operador_id = "OP-123"
    updated = repo.update(retrieved)

    # 3. Assert
    assert saved.id is not None
    assert retrieved is not None
    assert updated.corrida_id == "CR-999"
    assert updated.lote_id == "LT-888"
    assert updated.panela_id == "PN-07"
    assert updated.observacao == "Leitura atualizada"
    assert updated.operador_id == "OP-123"


def test_leitura_repository_list_by_filters(session):
    # 1. Arrange
    pirometro = Pirometro(
        id="PIR-01",
        nome="P1",
        setor="A",
        material_alvo="M1",
        processo="P",
        molde="M",
    )
    codigo = CodigoPirometro(
        id=101,
        pirometro_id="PIR-01",
        codigo=5,
        etapa_nome="V",
        ativo=True,
    )
    session.add(pirometro)
    session.add(codigo)
    session.commit()

    repo = LeituraRepository(session=session)
    now = datetime.utcnow()

    l1 = Leitura(
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1500.0,
        corrida_id="CR-01",
        panela_id="P-01",
        timestamp=now - timedelta(hours=2),
    )
    l2 = Leitura(
        pirometro_id="PIR-01",
        codigo_pirometro_id=101,
        temperatura_lida=1550.0,
        corrida_id="CR-02",
        panela_id="P-02",
        timestamp=now,
    )

    repo.save(l1)
    repo.save(l2)

    # 2. Act & Assert
    # Filter by pirometro_id
    r1 = repo.list_by_filters(pirometro_id="PIR-01")
    assert len(r1) == 2

    # Filter by corrida_id
    r2 = repo.list_by_filters(corrida_id="CR-01")
    assert len(r2) == 1
    assert r2[0].temperatura_lida == 1500.0

    # Filter by panela_id
    r3 = repo.list_by_filters(panela_id="P-02")
    assert len(r3) == 1
    assert r3[0].temperatura_lida == 1550.0

    # Filter by date range
    r4 = repo.list_by_filters(
        start_date=now - timedelta(hours=1), end_date=now + timedelta(hours=1)
    )
    assert len(r4) == 1
    assert r4[0].corrida_id == "CR-02"
