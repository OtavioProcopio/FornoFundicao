import pytest
from sqlmodel import Session, SQLModel, create_engine

from adapter.repositories.cadinho_repository import CadinhoRepository
from adapter.repositories.pirometro_repository import PirometroRepository
from core.domain.models import Cadinho, Pirometro, RegistroDesgasteCadinho


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_cadinho_repository_save_get_and_list(session):
    pir_repo = PirometroRepository(session=session)
    pir = Pirometro(
        id="PIR-01",
        nome="P1",
        setor="Aço",
        material_alvo="M1",
        processo="P",
        molde="M",
    )
    pir_repo.save(pir)

    repo = CadinhoRepository(session=session)
    cadinho = Cadinho(
        pirometro_id="PIR-01",
        codigo_identificador="CAD-001",
        espessura_inicial_mm=150.0,
        espessura_atual_mm=150.0,
        espessura_minima_seguranca_mm=50.0,
        status="ATIVO",
    )

    saved = repo.save(cadinho)
    assert saved.id is not None

    retrieved = repo.get_by_id(saved.id)
    assert retrieved is not None
    assert retrieved.codigo_identificador == "CAD-001"

    ativo = repo.get_ativo_by_pirometro("PIR-01")
    assert ativo is not None
    assert ativo.id == saved.id

    all_cadinhos = repo.list_all("PIR-01")
    assert len(all_cadinhos) == 1


def test_cadinho_repository_registro_desgaste(session):
    pir_repo = PirometroRepository(session=session)
    pir = Pirometro(
        id="PIR-01",
        nome="P1",
        setor="Aço",
        material_alvo="M1",
        processo="P",
        molde="M",
    )
    pir_repo.save(pir)

    repo = CadinhoRepository(session=session)
    cadinho = repo.save(
        Cadinho(
            pirometro_id="PIR-01",
            codigo_identificador="CAD-002",
            espessura_inicial_mm=150.0,
            espessura_atual_mm=150.0,
        )
    )
    assert cadinho.id is not None

    reg = RegistroDesgasteCadinho(
        cadinho_id=cadinho.id,
        espessura_medida_mm=120.0,
        corridas_no_momento=15,
        operador_id="OP-123",
        observacao="Medição periódica",
    )

    saved_reg = repo.save_registro_desgaste(reg)
    assert saved_reg.id is not None

    registros = repo.list_registros_desgaste(cadinho.id)
    assert len(registros) == 1
    assert registros[0].espessura_medida_mm == 120.0
