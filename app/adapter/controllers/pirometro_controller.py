from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from core.application.use_cases.cadastrar_pirometro import (
    CadastrarPirometroUseCase,
)
from core.application.use_cases.configurar_codigo_pirometro import (
    ConfigurarCodigoPirometroUseCase,
)
from core.application.use_cases.listar_pirometros import ListarPirometrosUseCase
from infra.config.container import Container

router = APIRouter(prefix="/api/v1/pirometros", tags=["Pirometros"])


class PirometroCreate(BaseModel):
    id: str
    nome: str
    setor: str
    material_alvo: str
    processo: str
    molde: str
    ativo: Optional[bool] = True


class CodigoPirometroCreate(BaseModel):
    codigo: int
    etapa_nome: str
    descricao: Optional[str] = None
    temp_min_esperada: Optional[float] = None
    temp_max_esperada: Optional[float] = None
    ordem_no_processo: Optional[int] = None
    ativo: Optional[bool] = True


@router.get("")
@inject
def list_pirometros(
    use_case: ListarPirometrosUseCase = Depends(
        Provide[Container.listar_pirometros_use_case]
    ),
):
    return use_case.execute()


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_pirometro(
    payload: PirometroCreate,
    use_case: CadastrarPirometroUseCase = Depends(
        Provide[Container.cadastrar_pirometro_use_case]
    ),
):
    return use_case.execute(payload.model_dump())


@router.post("/{id}/codigos", status_code=status.HTTP_200_OK)
@inject
def configure_codigo(
    id: str,
    payload: CodigoPirometroCreate,
    use_case: ConfigurarCodigoPirometroUseCase = Depends(
        Provide[Container.configurar_codigo_pirometro_use_case]
    ),
):
    try:
        return use_case.execute(id, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
