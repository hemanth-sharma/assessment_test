"""
tests/test_exceptions.py

Unit tests verifying domain exception structure and custom handlers.
"""
import pytest
from app.utils.exceptions import NotFoundException, DomainException, ConflictException

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