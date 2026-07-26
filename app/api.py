import uvicorn
from fastapi import FastAPI, Request
from sqlmodel import Session

from adapter.controllers.dashboard_controller import router as dashboard_router
from adapter.controllers.leitura_controller import router as leitura_router
from adapter.controllers.pirometro_controller import router as pirometro_router
from infra.config.container import Container
from infra.config.context import db_session_context
from infra.config.database import run_migrations
from infra.config.settings import settings


def create_app() -> FastAPI:
    if settings.RUN_MIGRATIONS:
        run_migrations()
        from infra.config.database import engine
        from infra.config.seed import seed_data

        with Session(engine) as session:
            seed_data(session)

    container = Container()
    container.wire(
        modules=[
            "adapter.controllers.pirometro_controller",
            "adapter.controllers.leitura_controller",
            "adapter.controllers.dashboard_controller",
        ]
    )

    app = FastAPI(
        title="Forno Fundicao API",
        description="API para o registro de medicoes dos pirometros da Rei Auto Parts",
        version="0.1.0",
    )

    app.container = container  # type: ignore[attr-defined]

    app.include_router(pirometro_router)
    app.include_router(leitura_router)
    app.include_router(dashboard_router)

    @app.on_event("startup")
    async def startup_event():
        import asyncio

        from infra.tools.db_monitor import monitor_database

        asyncio.create_task(monitor_database(get_engine=container.engine))

    @app.middleware("http")
    async def db_session_middleware(request: Request, call_next):
        engine = container.engine()
        with Session(engine) as session:
            token = db_session_context.set(session)
            try:
                response = await call_next(request)
                return response
            finally:
                db_session_context.reset(token)

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "UP"}

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
