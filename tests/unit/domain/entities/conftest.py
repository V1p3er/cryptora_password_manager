import pytest
from argon2 import PasswordHasher

@pytest.fixture(scope="session")
def argon2_hasher() -> PasswordHasher:
    return PasswordHasher()
