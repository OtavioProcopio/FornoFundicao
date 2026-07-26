import pytest
from sqlmodel import Session, SQLModel, create_engine

from adapter.repositories.cadinho_repository import CadinhoRepository
from adapter.repositories.pirometro_repository import PirometroRepository
from core.application.use_cases.cadastrar_cadinho import CadastrarCadinhoUseCase
from core.application.use_cases.obter_status_campanha import (
    ObterStatusCampanhaUseCase,
)
from core.application.use_cases.registrar_desgaste_cadinho import (
    RegistrarDesgasteCadinhoUseCase,
)
from core.domain.models import Pirometro


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_cadastrar_cadinho_use_case_success(session):
    pir_repo = PirometroRepository(session=session)
    cad_repo = CadinhoRepository(session=session)
    pir_repo.save(
        Pirometro(
            id="PIR-01",
            nome="Forno 1",
            setor="Aço",
            material_alvo="M1",
            processo="P",
            molde="M",
        )
    )

    use_case = CadastrarCadinhoUseCase(cadinho_repo=cad_repo, pirometro_repo=pir_repo)
    cadinho = use_case.execute(
        {
            "pirometro_id": "PIR-01",
            "codigo_identificador": "CAD-100",
            "espessura_inicial_mm": 180.0,
            "espessura_minima_seguranca_mm": 60.0,
        }
    )

    assert cadinho.id is not None
    assert cadinho.espessura_atual_mm == 180.0
    assert cadinho.status == "ATIVO"


def test_cadastrar_cadinho_use_case_invalid_pirometro(session):
    pir_repo = PirometroRepository(session=session)
    cad_repo = CadinhoRepository(session=session)
    use_case = CadastrarCadinhoUseCase(cadinho_repo=cad_repo, pirometro_repo=pir_repo)

    with pytest.raises(ValueError, match="não encontrado"):
        use_case.execute(
            {
                "pirometro_id": "PIR-999",
                "codigo_identificador": "CAD-100",
                "espessura_inicial_mm": 180.0,
            }
        )


def test_registrar_desgaste_cadinho_use_case_and_alert(session):
    pir_repo = PirometroRepository(session=session)
    cad_repo = CadinhoRepository(session=session)
    pir_repo.save(
        Pirometro(
            id="PIR-01",
            nome="Forno 1",
            setor="Aço",
            material_alvo="M1",
            processo="P",
            molde="M",
        )
    )

    cad_uc = CadastrarCadinhoUseCase(cadinho_repo=cad_repo, pirometro_repo=pir_repo)
    cadinho = cad_uc.execute(
        {
            "pirometro_id": "PIR-01",
            "codigo_identificador": "CAD-101",
            "espessura_inicial_mm": 150.0,
            "espessura_minima_seguranca_mm": 50.0,
        }
    )
    assert cadinho.id is not None

    desgaste_uc = RegistrarDesgasteCadinhoUseCase(cadinho_repo=cad_repo)

    # 1. Medição normal
    res1 = desgaste_uc.execute(
        cadinho.id,
        {
            "espessura_medida_mm": 100.0,
            "corridas_no_momento": 30,
            "operador_id": "OP-01",
        },
    )
    assert res1["cadinho"].espessura_atual_mm == 100.0
    assert res1["cadinho"].status == "ATIVO"
    assert not res1["alerta_troca"]

    # 2. Medição em nível crítico (dispara alerta)
    res2 = desgaste_uc.execute(
        cadinho.id,
        {
            "espessura_medida_mm": 45.0,
            "corridas_no_momento": 80,
            "operador_id": "OP-01",
        },
    )
    assert res2["cadinho"].espessura_atual_mm == 45.0
    assert res2["cadinho"].status == "ALERTA"
    assert res2["alerta_troca"]


def test_obter_status_campanha_use_case(session):
    pir_repo = PirometroRepository(session=session)
    cad_repo = CadinhoRepository(session=session)
    pir_repo.save(
        Pirometro(
            id="PIR-01",
            nome="Forno 1",
            setor="Aço",
            material_alvo="M1",
            processo="P",
            molde="M",
        )
    )

    cad_uc = CadastrarCadinhoUseCase(cadinho_repo=cad_repo, pirometro_repo=pir_repo)
    cadinho = cad_uc.execute(
        {
            "pirometro_id": "PIR-01",
            "codigo_identificador": "CAD-102",
            "espessura_inicial_mm": 150.0,
            "espessura_minima_seguranca_mm": 50.0,
        }
    )
    assert cadinho.id is not None

    desgaste_uc = RegistrarDesgasteCadinhoUseCase(cadinho_repo=cad_repo)
    desgaste_uc.execute(cadinho.id, {"espessura_medida_mm": 100.0})

    status_uc = ObterStatusCampanhaUseCase(cadinho_repo=cad_repo)
    campanha = status_uc.execute(pirometro_id="PIR-01")

    assert len(campanha) == 1
    assert campanha[0]["codigo_identificador"] == "CAD-102"
    # Espessura atual: 100, inicial: 150, min: 50 -> (100-50)/(150-50) = 50%
    assert campanha[0]["percentual_vida_util_refratario"] == 50.0
    assert campanha[0]["total_registros_desgaste"] == 1
