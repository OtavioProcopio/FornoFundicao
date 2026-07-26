from datetime import datetime
from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
    status,
)
from pydantic import BaseModel

from core.application.use_cases.obter_leituras_processadas import (
    ObterLeiturasProcessadasUseCase,
)
from core.application.use_cases.vincular_contexto_leitura import (
    VincularContextoLeituraUseCase,
)
from infra.config.container import Container
from infra.tools.websocket_manager import websocket_manager

router = APIRouter(prefix="/api/v1/leituras", tags=["Leituras"])


class ContextoLeituraUpdate(BaseModel):
    corrida_id: Optional[str] = None
    lote_id: Optional[str] = None
    panela_id: Optional[str] = None
    observacao: Optional[str] = None
    operador_id: Optional[str] = None


@router.get("")
@inject
def list_leituras(
    pirometro_id: Optional[str] = None,
    corrida_id: Optional[str] = None,
    panela_id: Optional[str] = None,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
    use_case: ObterLeiturasProcessadasUseCase = Depends(
        Provide[Container.obter_leituras_processadas_use_case]
    ),
):
    filters = {
        "pirometro_id": pirometro_id,
        "corrida_id": corrida_id,
        "panela_id": panela_id,
        "start_date": start_date,
        "end_date": end_date,
    }
    return use_case.execute(filters)


@router.patch("/{id}")
@inject
def update_contexto(
    id: int,
    payload: ContextoLeituraUpdate,
    use_case: VincularContextoLeituraUseCase = Depends(
        Provide[Container.vincular_contexto_leitura_use_case]
    ),
):
    try:
        # Remover chaves não passadas no request
        contexto_data = payload.model_dump(exclude_unset=True)
        return use_case.execute(id, contexto_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            # Manter a conexão ativa
            await websocket.receive_text()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
