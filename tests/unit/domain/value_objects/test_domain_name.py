import pytest
from dataclasses import FrozenInstanceError

from domain.value_objects.domain_name import DomainName


def test_valid_domain_name():
    domain = DomainName("google.com")
    assert domain.value == "google.com"


def test_domain_name_is_immutable():
    domain = DomainName("google.com")

    with pytest.raises(FrozenInstanceError):
        domain.value = "newvalue.com"


def test_domain_name_equality():
    domain = DomainName("Google.com")
    domain1 = DomainName("google.com")

    assert domain == domain1


def test_domain_name_is_normalized():
    domain = DomainName("  Google.COM  ")
    assert domain.value == "google.com"


@pytest.mark.parametrize(
    "invalid_input, error",
    [
        (123413, TypeError),
        (None, TypeError),
        ("", ValueError),
        (" ", ValueError),
        ("testsdfds", ValueError),
        ("google^$.com", ValueError),
        ("google..com", ValueError),
        ("-google.com", ValueError),
        (".com", ValueError),
    ],
)
def test_invalid_domain_name(invalid_input, error):
    with pytest.raises(error):
        DomainName(invalid_input)