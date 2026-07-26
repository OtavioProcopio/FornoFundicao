import pytest
from sqlmodel import Session, SQLModel, create_engine

from adapter.repositories.forno_repository import FornoRepository
from core.domain.models import Forno


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_forno_repository_save_get_and_list(session):
    repo = FornoRepository(session=session)
    forno = Forno(
        nome="Forno Indução A",
        codigo_identificador="FORNO-01",
        setor="Fundição Aço",
        capacidade_kg=2000.0,
        tipo_liga="SAE 1045",
        max_cadinhos=4,
    )

    saved = repo.save(forno)
    assert saved.id is not None

    by_id = repo.get_by_id(saved.id)
    assert by_id is not None
    assert by_id.nome == "Forno Indução A"

    by_codigo = repo.get_by_codigo("FORNO-01")
    assert by_codigo is not None
    assert by_codigo.id == saved.id

    fornos = repo.list_all("Fundição Aço")
    assert len(fornos) == 1
