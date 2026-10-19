from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.leads.service import to_lead_responses_bulk
from app.leads.models import Lead, LeadStatus
from app.models import MatchedPost


@pytest.mark.anyio
async def test_to_lead_responses_bulk_empty():
    """Ensure bulk mapping gracefully handles an empty lead list without DB calls."""
    mock_db = MagicMock()
    mock_db.execute = AsyncMock()

    results = await to_lead_responses_bulk(mock_db, [])
    assert results == []
    mock_db.execute.assert_not_awaited()


@pytest.mark.anyio
async def test_to_lead_responses_bulk_hydration():
    """Ensure bulk mapping successfully enriches leads with post snapshots."""
    lead_id = uuid4()
    post_id = uuid4()
    project_id = uuid4()

    mock_lead = Lead(
        id=lead_id,
        project_id=project_id,
        matched_post_id=post_id,
        status=LeadStatus.NEW.value,
        intent_score=0.9,
        url="https://reddit.com/r/saas/test",
        matched_keyword="saas",
    )

    mock_post = MatchedPost(
        id=post_id,
        project_id=project_id,
        title="Looking for a tool",
        author="testuser",
        subreddit="saas",
    )

    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_post]

    mock_db = MagicMock()
    mock_db.execute = AsyncMock(return_value=mock_result)

    responses = await to_lead_responses_bulk(mock_db, [mock_lead])

    assert len(responses) == 1
    assert responses[0].post_title == "Looking for a tool"
    assert responses[0].post_author == "testuser"
    assert responses[0].post_subreddit == "saas"
    mock_db.execute.assert_awaited_once()