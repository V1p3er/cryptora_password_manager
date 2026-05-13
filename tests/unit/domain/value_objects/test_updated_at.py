from datetime import datetime, timezone
from domain.value_objects.updated_at import UpdatedAt


def test_updated_at_now():
    ua = UpdatedAt.now()

    assert isinstance(ua.value, datetime)
    assert ua.value.tzinfo == timezone.utc