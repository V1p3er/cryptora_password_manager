from datetime import datetime, timezone
from domain.value_objects.created_at import CreatedAt

def test_created_at_now():
    ca = CreatedAt.now()
    assert isinstance(ca.value, datetime)
    assert ca.value.tzinfo is timezone.utc
