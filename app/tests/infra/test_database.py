from unittest.mock import MagicMock, patch

from infra.config.database import get_session, run_migrations


def test_get_session():
    mock_session = MagicMock()
    with patch("infra.config.database.Session") as mock_session_cls:
        mock_session_cls.return_value.__enter__.return_value = mock_session
        generator = get_session()
        session = next(generator)
        assert session == mock_session
        try:
            next(generator)
        except StopIteration:
            pass


def test_run_migrations():
    with patch("infra.config.database.command.upgrade") as mock_upgrade, patch(
        "infra.config.database.Config"
    ) as mock_config_cls:
        run_migrations()
        mock_config_cls.assert_called_once()
        mock_upgrade.assert_called_once()
