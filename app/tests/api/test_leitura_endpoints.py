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


def test_leitura_endpoints_workflow(client_context):
    client, engine = client_context

    # 1. Configurar Pirômetro e Etapas via API
    client.post(
        "/api/v1/pirometros",
        json={
            "id": "PIR-01",
            "nome": "P1",
            "setor": "Aço",
            "material_alvo": "M",
            "processo": "P",
            "molde": "M",
        },
    )
    client.post(
        "/api/v1/pirometros/PIR-01/codigos",
        json={
            "codigo": 3,
            "etapa_nome": "Vazamento",
            "temp_min_esperada": 1500.0,
            "temp_max_esperada": 1600.0,
        },
    )

    # Buscar o ID do CodigoPirometro no banco
    with Session(engine) as session:
        codigo_meta = session.exec(select(CodigoPirometro)).first()
        assert codigo_meta is not None
        codigo_meta_id = codigo_meta.id

        # Simular a inserção direta do receptor USB
        leitura_raw = Leitura(
            pirometro_id="PIR-01",
            codigo_pirometro_id=codigo_meta_id,
            temperatura_lida=1550.0,
            corrida_id=None,
            lote_id=None,
            panela_id=None,
        )
        session.add(leitura_raw)
        session.commit()
        session.refresh(leitura_raw)
        leitura_id = leitura_raw.id

    # 2. Obter leituras via GET API (verificar tradução e validação térmica)
    response = client.get("/api/v1/leituras")
    assert response.status_code == 200
    leituras = response.json()
    assert len(leituras) >= 1
    target = next(item for item in leituras if item["id"] == leitura_id)
    assert target["temperatura_lida"] == 1550.0
    assert target["etapa_nome"] == "Vazamento"
    assert target["alerta_temperatura"] is False
    assert target["corrida_id"] is None

    # 3. Vincular contexto via PATCH API
    update_payload = {
        "corrida_id": "CR-0123",
        "lote_id": "LT-0987",
        "panela_id": "PN-05",
        "observacao": "Corrida quente",
        "operador_id": "OP-456",
    }
    response = client.patch(f"/api/v1/leituras/{leitura_id}", json=update_payload)
    assert response.status_code == 200
    updated = response.json()
    assert updated["corrida_id"] == "CR-0123"
    assert updated["lote_id"] == "LT-0987"
    assert updated["panela_id"] == "PN-05"

    # 4. Obter com filtro de Corrida
    response = client.get("/api/v1/leituras", params={"corrida_id": "CR-0123"})
    assert response.status_code == 200
    filtered = response.json()
    assert len(filtered) == 1
    assert filtered[0]["id"] == leitura_id
    assert filtered[0]["corrida_id"] == "CR-0123"


def test_update_contexto_leitura_inexistente(client_context):
    client, _ = client_context
    response = client.patch("/api/v1/leituras/9999", json={"corrida_id": "CR-00"})
    assert response.status_code == 404
    assert "Leitura não encontrada" in response.json()["detail"]
