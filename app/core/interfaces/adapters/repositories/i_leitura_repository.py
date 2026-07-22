from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from core.domain.models import Leitura


class ILeituraRepository(ABC):

    @abstractmethod
    def save(self, leitura: Leitura) -> Leitura:
        pass

    @abstractmethod
    def get_by_id(self, leitura_id: int) -> Optional[Leitura]:
        pass

    @abstractmethod
    def update(self, leitura: Leitura) -> Leitura:
        pass

    @abstractmethod
    def list_by_filters(
        self,
        pirometro_id: Optional[str] = None,
        corrida_id: Optional[str] = None,
        panela_id: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> List[Leitura]:
        pass
