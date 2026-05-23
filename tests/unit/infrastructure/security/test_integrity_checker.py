from infrastructure.security.integrity_checker import IntegrityChecker


def test_sign_and_verify():
    data = b"vault-bytes"
    key = b"k" * 32
    signature = IntegrityChecker.sign(data, key)
    assert IntegrityChecker.verify(data, key, signature) is True


def test_verify_fails_for_tampered_data():
    key = b"k" * 32
    signature = IntegrityChecker.sign(b"data-a", key)
    assert IntegrityChecker.verify(b"data-b", key, signature) is False
