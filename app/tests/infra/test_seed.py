from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine, select

from core.domain.models import Pirometro
from infra.config.seed import seed_data


def test_seed_data_workflow():
    # 1. Setup in-memory database
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    # 2. Run seed on empty database
    with Session(engine) as session:
        seed_data(session)

    # 3. Assert data was created
    with Session(engine) as session:
        pirometros = session.exec(select(Pirometro)).all()
        assert len(pirometros) == 4
        ids = {p.id for p in pirometros}
        assert "PIR-01" in ids
        assert "PIR-02" in ids
        assert "PIR-03" in ids
        assert "PIR-04" in ids

    # 4. Run seed again to verify idempotency (should not duplicate)
    with Session(engine) as session:
        seed_data(session)

    with Session(engine) as session:
        pirometros_after = session.exec(select(Pirometro)).all()
        assert len(pirometros_after) == 4
