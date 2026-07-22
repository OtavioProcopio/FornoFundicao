from abc import ABC, abstractmethod
from typing import List, Optional

from core.domain.models import CodigoPirometro, Pirometro


class IPirometroRepository(ABC):

    @abstractmethod
    def save(self, pirometro: Pirometro) -> Pirometro:
        pass

    @abstractmethod
    def get_by_id(self, pirometro_id: str) -> Optional[Pirometro]:
        pass

    @abstractmethod
    def list_all(self) -> List[Pirometro]:
        pass

    @abstractmethod
    def save_codigo(self, codigo: CodigoPirometro) -> CodigoPirometro:
        pass

    @abstractmethod
    def get_codigo(self, pirometro_id: str, codigo: int) -> Optional[CodigoPirometro]:
        pass

    @abstractmethod
    def get_codigo_by_id(self, codigo_id: int) -> Optional[CodigoPirometro]:
        pass
