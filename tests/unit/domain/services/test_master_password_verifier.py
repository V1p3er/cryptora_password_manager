import pytest
from domain.services.master_password_verifier import MasterPasswordVerifier
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash


class FakeVerifier(MasterPasswordVerifier):
    def __init__(self, should_match=True):
        self.should_match = should_match
        self.last_raw = None
        self.last_hash = None

    def verify(self, raw_password, stored_hash):
        self.last_raw = raw_password
        self.last_hash = stored_hash
        return self.should_match


def test_verify_returns_true_when_password_matches():
    verifier = FakeVerifier(should_match=True)
    mp = MasterPassword(value="StrongP@ssword1")
    ph = PasswordHash(value="a" * 48)

    result = verifier.verify(mp, ph)

    assert result is True


def test_verify_returns_false_when_password_does_not_match():
    verifier = FakeVerifier(should_match=False)
    mp = MasterPassword(value="WrongP@ssword2")
    ph = PasswordHash(value="b" * 48)

    result = verifier.verify(mp, ph)

    assert result is False


def test_verify_receives_master_password_unchanged():
    verifier = FakeVerifier()
    mp = MasterPassword(value="MyP@ssword123")
    ph = PasswordHash(value="c" * 48)

    verifier.verify(mp, ph)

    assert verifier.last_raw == mp
    assert verifier.last_raw.value == "MyP@ssword123"


def test_verify_receives_password_hash_unchanged():
    verifier = FakeVerifier()
    mp = MasterPassword(value="MyP@ssword456")
    ph = PasswordHash(value="d" * 48)

    verifier.verify(mp, ph)

    assert verifier.last_hash == ph
    assert verifier.last_hash.value == "d" * 48


def test_verify_accepts_different_password_hashes():
    verifier = FakeVerifier()
    mp = MasterPassword(value="TestP@ssword1")
    ph1 = PasswordHash(value="1" * 48)
    ph2 = PasswordHash(value="2" * 48)

    verifier.verify(mp, ph1)
    assert verifier.last_hash == ph1

    verifier.verify(mp, ph2)
    assert verifier.last_hash == ph2


def test_verify_multiple_calls_independent():
    verifier = FakeVerifier(should_match=True)
    mp1 = MasterPassword(value="FirstP@ssword1")
    mp2 = MasterPassword(value="SecndP@ssword2")
    ph = PasswordHash(value="z" * 48)

    result1 = verifier.verify(mp1, ph)
    result2 = verifier.verify(mp2, ph)

    assert result1 is True
    assert result2 is True
    assert verifier.last_raw == mp2