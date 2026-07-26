import asyncio
import logging
from typing import Callable, Optional

from sqlmodel import Session, col, select

from core.domain.models import CodigoPirometro, Leitura
from infra.tools.websocket_manager import websocket_manager

logger = logging.getLogger("db_monitor")


def _default_get_engine():
    from infra.config.database import engine

    return engine


async def monitor_database(get_engine: Optional[Callable] = None):
    """Monitora o banco de dados por novas leituras e faz broadcast em real-time."""
    engine_getter = get_engine or _default_get_engine

    last_id: int = 0

    # Obter o último ID cadastrado na inicialização
    # para começar a monitorar a partir de agora
    try:
        current_engine = engine_getter()
        with Session(current_engine) as session:
            statement = select(Leitura).order_by(col(Leitura.id).desc())
            latest = session.exec(statement).first()
            if latest and latest.id is not None:
                last_id = latest.id
    except Exception as e:
        logger.error(f"Erro ao obter último ID na inicialização: {e}")

    while True:
        try:
            await asyncio.sleep(0.2)
            current_engine = engine_getter()
            with Session(current_engine) as session:
                statement = (
                    select(Leitura)
                    .where(col(Leitura.id) > last_id)
                    .order_by(col(Leitura.id).asc())
                )
                new_readings = session.exec(statement).all()

                for leitura in new_readings:
                    if leitura.id is not None:
                        last_id = leitura.id

                    # Buscar metadados do código
                    cid = leitura.codigo_pirometro_id
                    codigo_meta = session.get(CodigoPirometro, cid) if cid else None

                    # Processar status da temperatura
                    status_qualidade = "OK"
                    temp = leitura.temperatura_lida

                    if temp <= 0 or temp > 2000:
                        status_qualidade = "FALHA_SENSOR"
                    elif codigo_meta:
                        if (
                            codigo_meta.temp_min_esperada is not None
                            and temp < codigo_meta.temp_min_esperada
                        ):
                            status_qualidade = "NC_BAIXA"
                        elif (
                            codigo_meta.temp_max_esperada is not None
                            and temp > codigo_meta.temp_max_esperada
                        ):
                            status_qualidade = "NC_ALTA"

                    msg = {
                        "event": "new_reading",
                        "data": {
                            "id": leitura.id,
                            "pirometro_id": leitura.pirometro_id,
                            "temperatura": temp,
                            "timestamp": leitura.timestamp.isoformat(),
                            "status_qualidade": status_qualidade,
                            "etapa_nome": (
                                codigo_meta.etapa_nome
                                if codigo_meta
                                else "Etapa Desconhecida"
                            ),
                            "codigo_num": (codigo_meta.codigo if codigo_meta else None),
                            "corrida_id": leitura.corrida_id,
                            "lote_id": leitura.lote_id,
                            "panela_id": leitura.panela_id,
                            "observacao": leitura.observacao,
                        },
                    }
                    await websocket_manager.broadcast(msg)
        except Exception as e:
            logger.error(f"Erro no monitor de banco de dados: {e}")
