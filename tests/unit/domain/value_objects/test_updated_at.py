import pytest
from datetime import datetime, timezone

from domain.value_objects.updated_at import UpdatedAt

### Happy path test ###

def test_updated_at_accepts_timezone_aware_datetime():
    dt = datetime.now(timezone.utc)
    updated_at = UpdatedAt(dt)
    assert updated_at.value == dt

def test_updated_at_now_returns_utc_datetime():
    updated_at = UpdatedAt.now()
    assert updated_at.value.tzinfo is not None
    assert updated_at.value.tzinfo == timezone.utc

### failures test ###

def test_updated_at_rejects_naive_datetime():
    naive_datetime = datetime.now()
    with pytest.raises(ValueError, match="timezone-aware"):
        UpdatedAt(naive_datetime)