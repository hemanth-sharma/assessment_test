from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.keywords.schemas import KeywordCreate, KeywordType, KeywordUpdate
from app.keywords.service import create_keyword, update_keyword


@pytest.fixture
def mock_db():
    """Provide a mocked async database session for keywords."""
    session = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.mark.anyio
async def test_create_keyword_normalization(mock_db):
    """Ensure that create_keyword lowercases, strips text, and commits asynchronously."""
    project_id = uuid4()
    keyword_in = KeywordCreate(
        project_id=project_id,
        keyword="   REdArKy AlTeRnaTiVe   ",
        keyword_type=KeywordType.INCLUDE,
    )

    result = await create_keyword(mock_db, keyword_in)

    assert result.keyword == "redarky alternative"
    assert result.project_id == project_id
    assert result.keyword_type == KeywordType.INCLUDE.value
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.anyio
async def test_update_keyword_normalization(mock_db):
    """Ensure that update_keyword normalizes updated text fields."""
    from types import SimpleNamespace
    keyword = SimpleNamespace(
        keyword="old keyword",
        keyword_type=KeywordType.INCLUDE.value,
    )
    keyword_in = KeywordUpdate(keyword="   New Updated Keyword   ")

    result = await update_keyword(mock_db, keyword, keyword_in)

    assert result.keyword == "new updated keyword"
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()