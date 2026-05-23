import hashlib
import hmac


class IntegrityChecker:
    @staticmethod
    def sign(data: bytes, key: bytes) -> str:
        if not isinstance(data, bytes):
            raise TypeError("data must be bytes")
        if not isinstance(key, bytes):
            raise TypeError("key must be bytes")
        return hmac.new(key, data, hashlib.sha256).hexdigest()

    @staticmethod
    def verify(data: bytes, key: bytes, signature: str) -> bool:
        if not isinstance(signature, str):
            raise TypeError("signature must be str")
        expected = IntegrityChecker.sign(data, key)
        return hmac.compare_digest(expected, signature)
