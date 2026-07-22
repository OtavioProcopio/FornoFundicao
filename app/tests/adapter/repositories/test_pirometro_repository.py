import pytest
from sqlmodel import Session, SQLModel, create_engine

from adapter.repositories.pirometro_repository import PirometroRepository
from core.domain.models import CodigoPirometro, Pirometro


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_pirometro_repository_save_and_get(session):
    # 1. Arrange
    repo = PirometroRepository(session=session)
    pirometro = Pirometro(
        id="PIR-01",
        nome="Centrífuga 1",
        setor="Aço",
        material_alvo="SAE 1045",
        processo="Centrifugação",
        molde="Coquilha",
        ativo=True,
    )

    # 2. Act
    saved = repo.save(pirometro)
    retrieved = repo.get_by_id("PIR-01")

    # 3. Assert
    assert saved.id == "PIR-01"
    assert retrieved is not None
    assert retrieved.nome == "Centrífuga 1"


def test_pirometro_repository_list_all(session):
    # 1. Arrange
    repo = PirometroRepository(session=session)
    p1 = Pirometro(
        id="PIR-01",
        nome="P1",
        setor="A",
        material_alvo="M1",
        processo="P",
        molde="M",
    )
    p2 = Pirometro(
        id="PIR-02",
        nome="P2",
        setor="B",
        material_alvo="M2",
        processo="P",
        molde="M",
    )
    repo.save(p1)
    repo.save(p2)

    # 2. Act
    pirometros = repo.list_all()

    # 3. Assert
    assert len(pirometros) == 2
    assert {p.id for p in pirometros} == {"PIR-01", "PIR-02"}


def test_pirometro_repository_save_and_get_codigo(session):
    # 1. Arrange
    repo = PirometroRepository(session=session)
    pirometro = Pirometro(
        id="PIR-01",
        nome="P1",
        setor="A",
        material_alvo="M1",
        processo="P",
        molde="M",
    )
    repo.save(pirometro)

    codigo = CodigoPirometro(
        pirometro_id="PIR-01",
        codigo=5,
        etapa_nome="Vazamento",
        temp_min_esperada=1500.0,
        temp_max_esperada=1600.0,
        ativo=True,
    )

    # 2. Act
    saved_codigo = repo.save_codigo(codigo)
    retrieved_codigo = repo.get_codigo("PIR-01", 5)
    retrieved_by_id = repo.get_codigo_by_id(saved_codigo.id)

    # 3. Assert
    assert saved_codigo.id is not None
    assert retrieved_codigo is not None
    assert retrieved_codigo.etapa_nome == "Vazamento"
    assert retrieved_by_id is not None
    assert retrieved_by_id.codigo == 5
