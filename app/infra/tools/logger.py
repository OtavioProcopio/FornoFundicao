import logging

from core.interfaces.infra.tools.i_logger import ILogger
from infra.config.settings import settings


class Logger(ILogger):
    def __init__(self) -> None:
        logging.basicConfig(level=settings.LOG_LEVEL)
        self._logger = logging.getLogger("forno-fundicao")

    def info(self, message: str) -> None:
        self._logger.info(message)

    def error(self, message: str) -> None:
        self._logger.error(message)

    def warning(self, message: str) -> None:
        self._logger.warning(message)
