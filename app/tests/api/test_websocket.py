import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

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


def test_websocket_realtime_broadcast(client_context):
    client, engine = client_context

    # 1. Configurar metadados do pirômetro
    with Session(engine) as session:
        p = Pirometro(
            id="PIR-01",
            nome="Forno 1",
            setor="Aço",
            material_alvo="SAE 1045",
            processo="C",
            molde="M",
        )
        session.add(p)
        c = CodigoPirometro(
            pirometro_id="PIR-01",
            codigo=5,
            etapa_nome="Vazamento",
            temp_min_esperada=1500.0,
            temp_max_esperada=1600.0,
        )
        session.add(c)
        session.commit()
        session.refresh(c)
        codigo_meta_id = c.id

    # 2. Conectar ao WebSocket
    with client.websocket_connect("/api/v1/leituras/ws") as websocket:
        # Inserir uma leitura no banco
        with Session(engine) as session:
            leitura = Leitura(
                pirometro_id="PIR-01",
                codigo_pirometro_id=codigo_meta_id,
                temperatura_lida=1550.0,
            )
            session.add(leitura)
            session.commit()

        # O monitor de banco rodando em background deve capturar e propagar a leitura
        data = websocket.receive_json()
        assert data["event"] == "new_reading"
        assert data["data"]["temperatura"] == 1550.0
        assert data["data"]["status_qualidade"] == "OK"
