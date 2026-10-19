"""
tests/test_exceptions.py

Unit and integration tests verifying exception handling and standardized error JSON responses.
"""
import pytest
from uuid import uuid4
from fastapi.testclient import TestClient
from app.main import app
from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.utils.exceptions import NotFoundException, DomainException, ConflictException

client = TestClient(app)

@pytest.fixture(autouse=True)
def override_auth():
    """Temporarily override authentication for testing exception responses without leaking state."""
    mock_user = User(id=uuid4(), email="test@example.com")
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    app.dependency_overrides.pop(get_current_user, None)


def test_domain_exception_structure():
    """Verify base domain exception correctly sets message and attributes."""
    exc = DomainException("Custom domain error occurred")
    assert exc.message == "Custom domain error occurred"
    assert str(exc) == "Custom domain error occurred"


def test_not_found_exception_message():
    """Verify not found exception defaults and messaging."""
    exc = NotFoundException("Project not found")
    assert exc.message == "Project not found"
    assert isinstance(exc, DomainException)


def test_conflict_exception_message():
    """Verify conflict exception structure."""
    exc = ConflictException("Resource already exists")
    assert exc.message == "Resource already exists"
    assert isinstance(exc, DomainException)


def test_standardized_not_found_error_response():
    """Ensure accessing a non-existent project endpoint returns the standardized JSON error shape."""
    fake_id = uuid4()
    response = client.get(f"/projects/{fake_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "success" in data
    assert data["success"] is False
    assert "error" in data
    assert data["error"]["type"] == "RESOURCE_NOT_FOUND"
    assert str(fake_id) in data["error"]["message"]