import pytest
from sqlmodel import Session, SQLModel, create_engine

from adapter.repositories.cadinho_repository import CadinhoRepository
from adapter.repositories.forno_repository import FornoRepository
from core.application.use_cases.cadastrar_forno import CadastrarFornoUseCase
from core.application.use_cases.gerenciar_cadinhos_forno import (
    GerenciarCadinhosFornoUseCase,
)
from core.application.use_cases.listar_fornos import (
    ListarFornosECadinhosUseCase,
)


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def test_cadastrar_forno_use_case_success_and_duplicate(session):
    forno_repo = FornoRepository(session=session)
    uc = CadastrarFornoUseCase(forno_repo=forno_repo)

    forno = uc.execute(
        {
            "nome": "Forno 01",
            "codigo_identificador": "FORNO-01",
            "setor": "Aço",
            "capacidade_kg": 1500.0,
        }
    )
    assert forno.id is not None
    assert forno.max_cadinhos == 4

    with pytest.raises(ValueError, match="Já existe um forno"):
        uc.execute(
            {
                "nome": "Forno Duplicado",
                "codigo_identificador": "FORNO-01",
                "setor": "Aço",
            }
        )


def test_gerenciar_cadinhos_forno_max_4_limit_and_positions(session):
    forno_repo = FornoRepository(session=session)
    cadinho_repo = CadinhoRepository(session=session)

    f_uc = CadastrarFornoUseCase(forno_repo=forno_repo)
    forno = f_uc.execute(
        {
            "nome": "Forno 02",
            "codigo_identificador": "FORNO-02",
            "setor": "Fundição",
        }
    )
    assert forno.id is not None

    g_uc = GerenciarCadinhosFornoUseCase(
        cadinho_repo=cadinho_repo, forno_repo=forno_repo
    )

    # Adicionar 4 cadinhos (limite máximo)
    c1 = g_uc.adicionar_cadinho(
        forno.id,
        {"codigo_identificador": "CAD-1", "espessura_inicial_mm": 150.0},
    )
    c2 = g_uc.adicionar_cadinho(
        forno.id,
        {"codigo_identificador": "CAD-2", "espessura_inicial_mm": 150.0},
    )
    c3 = g_uc.adicionar_cadinho(
        forno.id,
        {"codigo_identificador": "CAD-3", "espessura_inicial_mm": 150.0},
    )
    c4 = g_uc.adicionar_cadinho(
        forno.id,
        {"codigo_identificador": "CAD-4", "espessura_inicial_mm": 150.0},
    )

    assert c1.posicao_no_forno == 1
    assert c2.posicao_no_forno == 2
    assert c3.posicao_no_forno == 3
    assert c4.posicao_no_forno == 4

    # Tentativa de adicionar o 5º cadinho no forno deve falhar
    with pytest.raises(ValueError, match="Limite máximo de 4 cadinhos"):
        g_uc.adicionar_cadinho(
            forno.id,
            {"codigo_identificador": "CAD-5", "espessura_inicial_mm": 150.0},
        )

    # Remover/substituir o cadinho 2
    assert c2.id is not None
    g_uc.remover_cadinho(c2.id, observacao="Trinca detectada")

    # Agora deve ser possível adicionar um novo cadinho que ocupará a posição vaga (2)
    c_novo = g_uc.adicionar_cadinho(
        forno.id,
        {"codigo_identificador": "CAD-2-NOVO", "espessura_inicial_mm": 160.0},
    )
    assert c_novo.posicao_no_forno == 2


def test_listar_fornos_e_cadinhos_use_case(session):
    forno_repo = FornoRepository(session=session)
    cadinho_repo = CadinhoRepository(session=session)

    f_uc = CadastrarFornoUseCase(forno_repo=forno_repo)
    forno = f_uc.execute(
        {
            "nome": "Forno 03",
            "codigo_identificador": "FORNO-03",
            "setor": "Centrífugas",
        }
    )
    assert forno.id is not None

    g_uc = GerenciarCadinhosFornoUseCase(
        cadinho_repo=cadinho_repo, forno_repo=forno_repo
    )
    g_uc.adicionar_cadinho(
        forno.id,
        {
            "codigo_identificador": "CAD-CENT-1",
            "espessura_inicial_mm": 200.0,
            "espessura_minima_seguranca_mm": 50.0,
        },
    )

    l_uc = ListarFornosECadinhosUseCase(
        forno_repo=forno_repo, cadinho_repo=cadinho_repo
    )
    lista = l_uc.execute("Centrífugas")

    assert len(lista) == 1
    assert lista[0]["total_cadinhos_ativos"] == 1
    assert lista[0]["cadinhos"][0]["codigo_identificador"] == "CAD-CENT-1"
    assert lista[0]["cadinhos"][0]["percentual_vida_util_refratario"] == 100.0
