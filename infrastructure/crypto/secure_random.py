import secrets


class SecureRandom:
    """Cryptographically secure random byte provider."""

    @staticmethod
    def bytes(length: int) -> bytes:
        if not isinstance(length, int):
            raise TypeError("length must be int")
        if length <= 0:
            raise ValueError("length must be greater than zero")
        return secrets.token_bytes(length)

    @staticmethod
    def salt(length: int = 16) -> bytes:
        return SecureRandom.bytes(length)
