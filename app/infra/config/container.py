from dependency_injector import containers, providers
from sqlmodel import Session, create_engine

from adapter.repositories.leitura_repository import LeituraRepository
from adapter.repositories.pirometro_repository import PirometroRepository
from core.application.use_cases.cadastrar_pirometro import (
    CadastrarPirometroUseCase,
)
from core.application.use_cases.configurar_codigo_pirometro import (
    ConfigurarCodigoPirometroUseCase,
)
from core.application.use_cases.listar_pirometros import ListarPirometrosUseCase
from core.application.use_cases.obter_leituras_processadas import (
    ObterLeiturasProcessadasUseCase,
)
from core.application.use_cases.vincular_contexto_leitura import (
    VincularContextoLeituraUseCase,
)
from infra.config.context import db_session_context
from infra.config.settings import settings
from infra.tools.logger import Logger


def get_db_session(engine):
    session = db_session_context.get()
    if session is None:
        return Session(bind=engine)
    return session


class Container(containers.DeclarativeContainer):
    settings = providers.Object(settings)

    engine = providers.Singleton(create_engine, url=settings.provided.database_url)
    db_session = providers.Callable(get_db_session, engine=engine)

    logger = providers.Singleton(Logger)

    pirometro_repo = providers.Factory(PirometroRepository, session=db_session)
    leitura_repo = providers.Factory(LeituraRepository, session=db_session)

    listar_pirometros_use_case = providers.Factory(
        ListarPirometrosUseCase, pirometro_repo=pirometro_repo
    )
    cadastrar_pirometro_use_case = providers.Factory(
        CadastrarPirometroUseCase, pirometro_repo=pirometro_repo
    )
    configurar_codigo_pirometro_use_case = providers.Factory(
        ConfigurarCodigoPirometroUseCase, pirometro_repo=pirometro_repo
    )
    vincular_contexto_leitura_use_case = providers.Factory(
        VincularContextoLeituraUseCase, leitura_repo=leitura_repo
    )
    obter_leituras_processadas_use_case = providers.Factory(
        ObterLeiturasProcessadasUseCase,
        leitura_repo=leitura_repo,
        pirometro_repo=pirometro_repo,
    )
