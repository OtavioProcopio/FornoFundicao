import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from api import app
from core.domain.models import CodigoPirometro, Leitura, Pirometro  # noqa: F401


@pytest.fixture(name="client_context")
def client_context_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    app.container.engine.override(engine)  # type: ignore

    with TestClient(app) as test_client:
        yield test_client, engine

    app.container.engine.reset_override()  # type: ignore


def test_dashboard_endpoint_workflow(client_context):
    client, engine = client_context

    # 1. Configurar Pirômetro e Código via API
    client.post(
        "/api/v1/pirometros",
        json={
            "id": "PIR-01",
            "nome": "Forno 1",
            "setor": "Aço",
            "material_alvo": "SAE 1045",
            "processo": "C",
            "molde": "M",
        },
    )
    client.post(
        "/api/v1/pirometros/PIR-01/codigos",
        json={
            "codigo": 5,
            "etapa_nome": "Vazamento",
            "temp_min_esperada": 1500.0,
            "temp_max_esperada": 1600.0,
        },
    )

    # Buscar o ID do código criado e inserir uma leitura direta
    with Session(engine) as session:
        codigo_meta = session.exec(select(CodigoPirometro)).first()
        assert codigo_meta is not None
        codigo_meta_id = codigo_meta.id

        leitura = Leitura(
            pirometro_id="PIR-01",
            codigo_pirometro_id=codigo_meta_id,
            temperatura_lida=1550.0,  # Dentro dos limites (OK)
            corrida_id="CR-100",
            lote_id="LT-200",
            panela_id="PN-03",
        )
        session.add(leitura)
        session.commit()

    # 2. Chamar o endpoint do Dashboard
    response = client.get("/api/v1/dashboard")
    assert response.status_code == 200
    data = response.json()

    # 3. Assert - Nível Operacional
    assert "PIR-01" in data["operacional"]["status_fornos"]
    forno_data = data["operacional"]["status_fornos"]["PIR-01"]
    assert forno_data["equipamento_nome"] == "Forno 1"
    assert forno_data["ultima_leitura"]["temperatura"] == 1550.0
    assert forno_data["ultima_leitura"]["status_qualidade"] == "OK"
    assert forno_data["contexto_producao"]["corrida_ativa"] == "CR-100"

    # Assert - Nível de Qualidade
    assert data["qualidade"]["kpis"]["total_leituras"] == 1
    assert data["qualidade"]["kpis"]["total_nc"] == 0
    assert data["qualidade"]["kpis"]["taxa_conformidade"] == 100.0

    # Assert - Nível Gerencial
    assert data["gerencial"]["produtividade"]["fornos_ativos"] == 1
    assert data["gerencial"]["estabilidade_fornos"]["PIR-01"]["leituras_turno"] == 1
