import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

from api import app
from core.domain.models import Cadinho, Pirometro, RegistroDesgasteCadinho  # noqa: F401


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


def test_cadinho_endpoints_workflow(client):
    # 1. Cadastrar pirômetro
    client.post(
        "/api/v1/pirometros",
        json={
            "id": "PIR-01",
            "nome": "Forno 1",
            "setor": "Fundição",
            "material_alvo": "Ferro",
            "processo": "Fusão",
            "molde": "Sand",
        },
    )

    # 2. Cadastrar novo cadinho
    res_create = client.post(
        "/api/v1/cadinhos",
        json={
            "pirometro_id": "PIR-01",
            "codigo_identificador": "CAD-FORNO-1",
            "espessura_inicial_mm": 160.0,
            "espessura_minima_seguranca_mm": 50.0,
        },
    )
    assert res_create.status_code == 201
    cadinho = res_create.json()
    cadinho_id = cadinho["id"]
    assert cadinho["codigo_identificador"] == "CAD-FORNO-1"

    # 3. Listar campanha dos cadinhos
    res_list = client.get("/api/v1/cadinhos?pirometro_id=PIR-01")
    assert res_list.status_code == 200
    lista = res_list.json()
    assert len(lista) == 1
    assert lista[0]["percentual_vida_util_refratario"] == 100.0

    # 4. Registrar medição de desgaste
    res_desgaste = client.post(
        f"/api/v1/cadinhos/{cadinho_id}/desgaste",
        json={
            "espessura_medida_mm": 105.0,
            "corridas_no_momento": 25,
            "operador_id": "OP-42",
        },
    )
    assert res_desgaste.status_code == 200
    desgaste_res = res_desgaste.json()
    assert desgaste_res["cadinho"]["espessura_atual_mm"] == 105.0
    assert not desgaste_res["alerta_troca"]

    # 5. Listar novamente e conferir atualização do percentual
    res_list2 = client.get("/api/v1/cadinhos")
    assert res_list2.status_code == 200
    lista2 = res_list2.json()
    assert lista2[0]["percentual_vida_util_refratario"] == 50.0
    assert lista2[0]["total_registros_desgaste"] == 1


def test_cadinho_desgaste_invalid_id(client):
    res = client.post(
        "/api/v1/cadinhos/9999/desgaste",
        json={"espessura_medida_mm": 100.0},
    )
    assert res.status_code == 404
