import pytest
from dataclasses import FrozenInstanceError

from domain.value_objects.service_name import ServiceName

### Happy path test ###

def test_valid_service_name():
    sv_name = ServiceName("Spotify")
    assert sv_name.value == "spotify"

def test_service_name_is_immutable():
    sv_name = ServiceName("Spotify")
    with pytest.raises(FrozenInstanceError):
        sv_name.value = "Google"

def test_service_name_equality():
    sv_name = ServiceName("  Spotify  ")
    sv_name1 = ServiceName("spotify")
    assert sv_name == sv_name1

### failures test ###

@pytest.mark.parametrize(
    "invalid_input, error_type",
    [
        (1421412, TypeError),
        (None, TypeError),
        ("sh", ValueError),
        ("toooolonggggggggggggggggggggggggggggggggggggggggggggggggggg", ValueError),
        (" s", ValueError),
        (" ", ValueError),
        ("", ValueError),
    ]
)
def test_invalid_service_names(invalid_input, error_type):
    with pytest.raises(error_type):
        ServiceName(invalid_input)