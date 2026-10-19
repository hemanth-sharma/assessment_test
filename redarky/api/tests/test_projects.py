from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4
import pytest

from app.projects.schemas import ProjectCreate
from app.projects.service import create_project, activate_pipeline, deactivate_pipeline


@pytest.fixture
def mock_db():
    """Provide a mocked async database session for projects."""
    session = MagicMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest.mark.anyio
async def test_create_project_default_platforms(mock_db):
    """Ensure projects default to ['reddit'] if the platforms list is empty."""
    project_in = ProjectCreate(
        name="SaaS Lead Finder",
        goal="Find high-intent leads on social platforms",
        goal_description="Looking for startup discussions",
        goal_type="lead_gen",
        platforms=[]
    )
    owner_id = uuid4()

    project = await create_project(mock_db, project_in, owner_id)

    assert project.platforms == ["reddit"]
    assert project.owner_id == owner_id
    mock_db.add.assert_called_once()
    mock_db.commit.assert_awaited_once()
    mock_db.refresh.assert_awaited_once()


@pytest.mark.anyio
async def test_pipeline_activation(mock_db):
    """Test activating and deactivating a project pipeline."""
    from types import SimpleNamespace
    project = SimpleNamespace(
        is_pipeline_active=False,
        pipeline_activated_at=None
    )

    activated = await activate_pipeline(mock_db, project)
    assert activated.is_pipeline_active is True
    assert activated.pipeline_activated_at is not None

    deactivated = await deactivate_pipeline(mock_db, project)
    assert deactivated.is_pipeline_active is False