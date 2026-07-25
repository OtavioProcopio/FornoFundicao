import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, create_engine

from api import app
from core.domain.models import CodigoPirometro, Leitura, Pirometro  # noqa: F401


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


def test_pirometro_endpoints_workflow(client):
    # 1. Listar inicialmente (deve estar vazio ou retornar lista)
    response = client.get("/api/v1/pirometros")
    assert response.status_code == 200
    initial_list = response.json()

    # 2. Criar novo pirômetro
    payload = {
        "id": "PIR-01",
        "nome": "Centrífuga 1",
        "setor": "Aço",
        "material_alvo": "SAE 1045",
        "processo": "Centrifugação",
        "molde": "Coquilha",
        "ativo": True,
    }
    response = client.post("/api/v1/pirometros", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["id"] == "PIR-01"

    # 3. Listar novamente (deve conter o criado)
    response = client.get("/api/v1/pirometros")
    assert response.status_code == 200
    current_list = response.json()
    assert len(current_list) == len(initial_list) + 1
    assert any(p["id"] == "PIR-01" for p in current_list)

    # 4. Configurar código/etapa para o pirômetro
    codigo_payload = {
        "codigo": 5,
        "etapa_nome": "Vazamento",
        "temp_min_esperada": 1500.0,
        "temp_max_esperada": 1600.0,
    }
    response = client.post("/api/v1/pirometros/PIR-01/codigos", json=codigo_payload)
    assert response.status_code == 200
    codigo_meta = response.json()
    assert codigo_meta["codigo"] == 5
    assert codigo_meta["etapa_nome"] == "Vazamento"
    assert codigo_meta["pirometro_id"] == "PIR-01"


def test_configure_codigo_pirometro_inexistente(client):
    codigo_payload = {
        "codigo": 1,
        "etapa_nome": "X",
    }
    response = client.post(
        "/api/v1/pirometros/PIR-INVALID/codigos", json=codigo_payload
    )
    assert response.status_code == 404
    assert "Pirômetro não encontrado" in response.json()["detail"]
