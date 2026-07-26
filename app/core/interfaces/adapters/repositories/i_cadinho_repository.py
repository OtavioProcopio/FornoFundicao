from abc import ABC, abstractmethod
from typing import List, Optional

from core.domain.models import Cadinho, RegistroDesgasteCadinho


class ICadinhoRepository(ABC):

    @abstractmethod
    def save(self, cadinho: Cadinho) -> Cadinho:
        pass

    @abstractmethod
    def get_by_id(self, cadinho_id: int) -> Optional[Cadinho]:
        pass

    @abstractmethod
    def list_all(
        self,
        pirometro_id: Optional[str] = None,
        forno_id: Optional[int] = None,
    ) -> List[Cadinho]:
        pass

    @abstractmethod
    def list_active_by_forno(self, forno_id: int) -> List[Cadinho]:
        pass

    @abstractmethod
    def get_ativo_by_pirometro(self, pirometro_id: str) -> Optional[Cadinho]:
        pass

    @abstractmethod
    def update(self, cadinho: Cadinho) -> Cadinho:
        pass

    @abstractmethod
    def save_registro_desgaste(
        self, registro: RegistroDesgasteCadinho
    ) -> RegistroDesgasteCadinho:
        pass

    @abstractmethod
    def list_registros_desgaste(self, cadinho_id: int) -> List[RegistroDesgasteCadinho]:
        pass
