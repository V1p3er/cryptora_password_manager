import pytest

from datetime import datetime, timezone
from domain.value_objects.created_at import CreatedAt

### Happy path test ###

def test_created_at_accepts_timezone_aware_datetime():
    dt = datetime.now(timezone.utc)
    created_at = CreatedAt(dt)
    assert created_at.value == dt

def test_created_at_now_returns_utc_datetime():
    created_at = CreatedAt.now()
    assert created_at.value.tzinfo is not None
    assert created_at.value.tzinfo == timezone.utc

### failures test ###

def test_created_at_rejects_naive_datetime():
    naive_datetime = datetime.now()
    with pytest.raises(ValueError, match="timezone-aware"):
        CreatedAt(naive_datetime)