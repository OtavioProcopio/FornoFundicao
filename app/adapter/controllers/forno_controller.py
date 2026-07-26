from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from core.application.use_cases.cadastrar_forno import CadastrarFornoUseCase
from core.application.use_cases.gerenciar_cadinhos_forno import (
    GerenciarCadinhosFornoUseCase,
)
from core.application.use_cases.listar_fornos import (
    ListarFornosECadinhosUseCase,
)
from infra.config.container import Container

router = APIRouter(prefix="/api/v1/fornos", tags=["Fornos & Multi-Cadinhos"])


class FornoCreateRequest(BaseModel):
    nome: str
    codigo_identificador: str
    setor: str
    capacidade_kg: Optional[float] = None
    tipo_liga: Optional[str] = None
    max_cadinhos: Optional[int] = 4
    ativo: Optional[bool] = True
    observacao: Optional[str] = None


class AdicionarCadinhoFornoRequest(BaseModel):
    codigo_identificador: str
    espessura_inicial_mm: float
    espessura_minima_seguranca_mm: Optional[float] = 50.0
    posicao_no_forno: Optional[int] = None
    pirometro_id: Optional[str] = None
    max_corridas_esperadas: Optional[int] = 200
    observacao: Optional[str] = None


class EditarCadinhoRequest(BaseModel):
    codigo_identificador: Optional[str] = None
    espessura_minima_seguranca_mm: Optional[float] = None
    max_corridas_esperadas: Optional[int] = None
    pirometro_id: Optional[str] = None
    observacao: Optional[str] = None


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_forno(
    payload: FornoCreateRequest,
    use_case: CadastrarFornoUseCase = Depends(
        Provide[Container.cadastrar_forno_use_case]
    ),
):
    try:
        return use_case.execute(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("")
@inject
def list_fornos(
    setor: Optional[str] = None,
    use_case: ListarFornosECadinhosUseCase = Depends(
        Provide[Container.listar_fornos_use_case]
    ),
):
    return use_case.execute(setor=setor)


@router.post("/{id}/cadinhos", status_code=status.HTTP_201_CREATED)
@inject
def add_cadinho_to_forno(
    id: int,
    payload: AdicionarCadinhoFornoRequest,
    use_case: GerenciarCadinhosFornoUseCase = Depends(
        Provide[Container.gerenciar_cadinhos_forno_use_case]
    ),
):
    try:
        return use_case.adicionar_cadinho(id, payload.model_dump())
    except ValueError as e:
        detail = str(e)
        if "não encontrado" in detail.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


@router.put("/{id}/cadinhos/{cadinho_id}", status_code=status.HTTP_200_OK)
@inject
def edit_cadinho(
    id: int,
    cadinho_id: int,
    payload: EditarCadinhoRequest,
    use_case: GerenciarCadinhosFornoUseCase = Depends(
        Provide[Container.gerenciar_cadinhos_forno_use_case]
    ),
):
    try:
        return use_case.editar_cadinho(cadinho_id, payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{id}/cadinhos/{cadinho_id}", status_code=status.HTTP_200_OK)
@inject
def remove_cadinho(
    id: int,
    cadinho_id: int,
    observacao: Optional[str] = None,
    use_case: GerenciarCadinhosFornoUseCase = Depends(
        Provide[Container.gerenciar_cadinhos_forno_use_case]
    ),
):
    try:
        return use_case.remover_cadinho(cadinho_id, observacao=observacao)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
