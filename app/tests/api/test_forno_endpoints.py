import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

from api import app
from core.domain.models import Cadinho, Forno  # noqa: F401


@pytest.fixture(name="client")
def client_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    app.container.engine.override(engine)  # type: ignore

    with TestClient(app) as test_client:
        yield test_client

    app.container.engine.reset_override()  # type: ignore


def test_forno_endpoints_workflow(client):
    # 1. Cadastrar Forno
    res = client.post(
        "/api/v1/fornos",
        json={
            "nome": "Forno Indução #1",
            "codigo_identificador": "FORNO-IND-01",
            "setor": "Fundição Principal",
            "capacidade_kg": 2500.0,
            "tipo_liga": "SAE 1045",
        },
    )
    assert res.status_code == 201
    forno = res.json()
    forno_id = forno["id"]
    assert forno["codigo_identificador"] == "FORNO-IND-01"

    # 2. Adicionar 2 cadinhos ao forno
    res_cad1 = client.post(
        f"/api/v1/fornos/{forno_id}/cadinhos",
        json={
            "codigo_identificador": "CAD-P1",
            "espessura_inicial_mm": 170.0,
            "posicao_no_forno": 1,
        },
    )
    assert res_cad1.status_code == 201
    c1 = res_cad1.json()
    assert c1["posicao_no_forno"] == 1

    res_cad2 = client.post(
        f"/api/v1/fornos/{forno_id}/cadinhos",
        json={
            "codigo_identificador": "CAD-P2",
            "espessura_inicial_mm": 170.0,
            "posicao_no_forno": 2,
        },
    )
    assert res_cad2.status_code == 201

    # 3. Listar fornos com cadinhos ativos
    res_list = client.get("/api/v1/fornos")
    assert res_list.status_code == 200
    fornos_lista = res_list.json()
    assert len(fornos_lista) == 1
    assert fornos_lista[0]["total_cadinhos_ativos"] == 2
    assert len(fornos_lista[0]["cadinhos"]) == 2

    # 4. Remover um cadinho do forno
    res_del = client.delete(f"/api/v1/fornos/{forno_id}/cadinhos/{c1['id']}")
    assert res_del.status_code == 200
    assert res_del.json()["status"] == "SUBSTITUIDO"

    # 5. Listar novamente (agora apenas 1 ativo)
    res_list2 = client.get("/api/v1/fornos")
    assert res_list2.status_code == 200
    assert res_list2.json()[0]["total_cadinhos_ativos"] == 1
