from domain.value_objects.master_password import MasterPassword
from infrastructure.security.password_hasher import Argon2PasswordHasher, Argon2PasswordVerifier


def test_hash_and_verify():
    password = MasterPassword("ValidPassw0rd!")
    hashed = Argon2PasswordHasher.hash(password)
    verifier = Argon2PasswordVerifier()
    assert verifier.verify(password, hashed) is True


def test_verify_wrong_password_returns_false():
    hashed = Argon2PasswordHasher.hash(MasterPassword("ValidPassw0rd!"))
    verifier = Argon2PasswordVerifier()
    assert verifier.verify(MasterPassword("WrongPassw0rd!"), hashed) is False
