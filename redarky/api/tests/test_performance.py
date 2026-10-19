from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.leads.service import to_lead_responses_bulk
from app.leads.models import Lead


@pytest.mark.anyio
async def test_to_lead_responses_bulk_empty():
    """Ensure bulk mapping handles an empty lead list without DB calls."""
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    results = await to_lead_responses_bulk(mock_db, [])
    assert results == []
    mock_db.execute.assert_not_awaited()