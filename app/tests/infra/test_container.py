from unittest.mock import MagicMock, patch

from infra.config.container import get_db_session
from infra.config.context import db_session_context


def test_get_db_session_returns_existing_session():
    mock_session = MagicMock()
    token = db_session_context.set(mock_session)
    try:
        session = get_db_session(MagicMock())
        assert session == mock_session
    finally:
        db_session_context.reset(token)


def test_get_db_session_creates_new_session_if_none():
    token = db_session_context.set(None)
    try:
        mock_engine = MagicMock()
        with patch("infra.config.container.Session") as mock_session_cls:
            get_db_session(mock_engine)
            mock_session_cls.assert_called_once_with(bind=mock_engine)
    finally:
        db_session_context.reset(token)
