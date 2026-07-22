from typing import Any, Dict

from core.domain.models import Leitura
from core.interfaces.adapters.repositories.i_leitura_repository import (
    ILeituraRepository,
)


class VincularContextoLeituraUseCase:

    def __init__(self, leitura_repo: ILeituraRepository):
        self.leitura_repo = leitura_repo

    def execute(self, leitura_id: int, contexto_data: Dict[str, Any]) -> Leitura:
        leitura = self.leitura_repo.get_by_id(leitura_id)
        if not leitura:
            raise ValueError("Leitura não encontrada.")

        # Atualiza os campos permitidos
        if "corrida_id" in contexto_data:
            leitura.corrida_id = contexto_data["corrida_id"]
        if "lote_id" in contexto_data:
            leitura.lote_id = contexto_data["lote_id"]
        if "panela_id" in contexto_data:
            leitura.panela_id = contexto_data["panela_id"]
        if "observacao" in contexto_data:
            leitura.observacao = contexto_data["observacao"]
        if "operador_id" in contexto_data:
            leitura.operador_id = contexto_data["operador_id"]

        return self.leitura_repo.update(leitura)
