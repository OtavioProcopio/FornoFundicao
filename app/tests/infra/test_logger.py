from unittest.mock import MagicMock, patch

from infra.tools.logger import Logger


def test_logger_methods():
    with patch("logging.getLogger") as mock_get_logger:
        mock_logger_instance = MagicMock()
        mock_get_logger.return_value = mock_logger_instance

        logger = Logger()

        logger.info("info msg")
        mock_logger_instance.info.assert_called_once_with("info msg")

        logger.error("error msg")
        mock_logger_instance.error.assert_called_once_with("error msg")

        logger.warning("warning msg")
        mock_logger_instance.warning.assert_called_once_with("warning msg")
