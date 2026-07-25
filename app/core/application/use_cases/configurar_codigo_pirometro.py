from typing import Any, Dict

from core.domain.models import CodigoPirometro
from core.interfaces.adapters.repositories.i_pirometro_repository import (
    IPirometroRepository,
)


class ConfigurarCodigoPirometroUseCase:

    def __init__(self, pirometro_repo: IPirometroRepository):
        self.pirometro_repo = pirometro_repo

    def execute(
        self, pirometro_id: str, codigo_data: Dict[str, Any]
    ) -> CodigoPirometro:
        pirometro = self.pirometro_repo.get_by_id(pirometro_id)
        if not pirometro:
            raise ValueError("Pirômetro não encontrado.")

        # Verificar se o código já existe para este pirômetro
        existing = self.pirometro_repo.get_codigo(pirometro_id, codigo_data["codigo"])

        if existing:
            # Atualiza dados existentes
            existing.etapa_nome = codigo_data["etapa_nome"]
            existing.descricao = codigo_data.get("descricao", existing.descricao)
            existing.temp_min_esperada = codigo_data.get(
                "temp_min_esperada", existing.temp_min_esperada
            )
            existing.temp_max_esperada = codigo_data.get(
                "temp_max_esperada", existing.temp_max_esperada
            )
            existing.ordem_no_processo = codigo_data.get(
                "ordem_no_processo", existing.ordem_no_processo
            )
            existing.ativo = codigo_data.get("ativo", existing.ativo)
            return self.pirometro_repo.save_codigo(existing)

        # Cria um novo código
        codigo = CodigoPirometro(
            pirometro_id=pirometro_id,
            codigo=codigo_data["codigo"],
            etapa_nome=codigo_data["etapa_nome"],
            descricao=codigo_data.get("descricao"),
            temp_min_esperada=codigo_data.get("temp_min_esperada"),
            temp_max_esperada=codigo_data.get("temp_max_esperada"),
            ordem_no_processo=codigo_data.get("ordem_no_processo"),
            ativo=codigo_data.get("ativo", True),
        )
        return self.pirometro_repo.save_codigo(codigo)
