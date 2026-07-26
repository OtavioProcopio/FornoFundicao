from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from core.application.use_cases.gerar_dados_dashboard import (
    GerarDadosDashboardUseCase,
)
from infra.config.container import Container

router = APIRouter(prefix="/api/v1/dashboard", tags=["Dashboard"])


@router.get("")
@inject
def get_dashboard(
    use_case: GerarDadosDashboardUseCase = Depends(
        Provide[Container.gerar_dados_dashboard_use_case]
    ),
):
    return use_case.execute()
