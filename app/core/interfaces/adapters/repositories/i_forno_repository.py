from abc import ABC, abstractmethod
from typing import List, Optional

from core.domain.models import Forno


class IFornoRepository(ABC):

    @abstractmethod
    def save(self, forno: Forno) -> Forno:
        pass

    @abstractmethod
    def get_by_id(self, forno_id: int) -> Optional[Forno]:
        pass

    @abstractmethod
    def get_by_codigo(self, codigo_identificador: str) -> Optional[Forno]:
        pass

    @abstractmethod
    def list_all(self, setor: Optional[str] = None) -> List[Forno]:
        pass

    @abstractmethod
    def update(self, forno: Forno) -> Forno:
        pass
