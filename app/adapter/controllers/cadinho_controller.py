from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from core.application.use_cases.cadastrar_cadinho import CadastrarCadinhoUseCase
from core.application.use_cases.obter_status_campanha import (
    ObterStatusCampanhaUseCase,
)
from core.application.use_cases.registrar_desgaste_cadinho import (
    RegistrarDesgasteCadinhoUseCase,
)
from infra.config.container import Container

router = APIRouter(prefix="/api/v1/cadinhos", tags=["Cadinhos & Campanha do Forno"])


class CadinhoCreateRequest(BaseModel):
    pirometro_id: str
    codigo_identificador: str
    espessura_inicial_mm: float
    espessura_minima_seguranca_mm: Optional[float] = 50.0
    max_corridas_esperadas: Optional[int] = 200
    observacao: Optional[str] = None


class DesgasteCadinhoRequest(BaseModel):
    espessura_medida_mm: float
    corridas_no_momento: Optional[int] = None
    operador_id: Optional[str] = None
    observacao: Optional[str] = None


@router.post("", status_code=status.HTTP_201_CREATED)
@inject
def create_cadinho(
    payload: CadinhoCreateRequest,
    use_case: CadastrarCadinhoUseCase = Depends(
        Provide[Container.cadastrar_cadinho_use_case]
    ),
):
    try:
        return use_case.execute(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("")
@inject
def list_campanha_cadinhos(
    pirometro_id: Optional[str] = None,
    use_case: ObterStatusCampanhaUseCase = Depends(
        Provide[Container.obter_status_campanha_use_case]
    ),
):
    return use_case.execute(pirometro_id=pirometro_id)


@router.post("/{id}/desgaste", status_code=status.HTTP_200_OK)
@inject
def register_desgaste(
    id: int,
    payload: DesgasteCadinhoRequest,
    use_case: RegistrarDesgasteCadinhoUseCase = Depends(
        Provide[Container.registrar_desgaste_cadinho_use_case]
    ),
):
    try:
        return use_case.execute(id, payload.model_dump())
    except ValueError as e:
        detail = str(e)
        if "não encontrado" in detail.lower():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
