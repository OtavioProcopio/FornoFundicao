from typing import Any, Dict

from core.domain.models import RegistroDesgasteCadinho
from core.interfaces.adapters.repositories.i_cadinho_repository import (
    ICadinhoRepository,
)


class RegistrarDesgasteCadinhoUseCase:

    def __init__(self, cadinho_repo: ICadinhoRepository):
        self.cadinho_repo = cadinho_repo

    def execute(self, cadinho_id: int, data: dict) -> Dict[str, Any]:
        cadinho = self.cadinho_repo.get_by_id(cadinho_id)
        if not cadinho:
            raise ValueError(f"Cadinho com ID {cadinho_id} não encontrado.")

        espessura_medida = float(data["espessura_medida_mm"])
        if espessura_medida <= 0:
            raise ValueError("Espessura medida deve ser maior que zero.")

        if espessura_medida > cadinho.espessura_inicial_mm:
            raise ValueError(
                "Espessura medida não pode ser maior que a "
                "espessura inicial do cadinho."
            )

        corridas = data.get("corridas_no_momento")
        if corridas is not None:
            if corridas < 0:
                raise ValueError("Contador de corridas não pode ser negativo.")
            cadinho.corridas_acumuladas = corridas

        cadinho.espessura_atual_mm = espessura_medida

        if espessura_medida <= cadinho.espessura_minima_seguranca_mm:
            cadinho.status = "ALERTA"

        registro = RegistroDesgasteCadinho(
            cadinho_id=cadinho_id,
            espessura_medida_mm=espessura_medida,
            corridas_no_momento=cadinho.corridas_acumuladas,
            operador_id=data.get("operador_id"),
            observacao=data.get("observacao"),
        )

        registro_salvo = self.cadinho_repo.save_registro_desgaste(registro)
        cadinho_atualizado = self.cadinho_repo.update(cadinho)

        return {
            "cadinho": cadinho_atualizado,
            "registro": registro_salvo,
            "alerta_troca": cadinho_atualizado.status == "ALERTA",
        }
