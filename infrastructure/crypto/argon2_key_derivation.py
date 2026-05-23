from argon2.low_level import Type, hash_secret_raw

from domain.services.data_encryption_key_deriver import DataEncryptionKeyDeriver
from domain.value_objects.master_password import MasterPassword


class Argon2KeyDerivation(DataEncryptionKeyDeriver):
    def __init__(
        self,
        *,
        time_cost: int = 3,
        memory_cost: int = 65536,
        parallelism: int = 4,
        hash_len: int = 32,
    ) -> None:
        self._time_cost = time_cost
        self._memory_cost = memory_cost
        self._parallelism = parallelism
        self._hash_len = hash_len

    def derive_key(self, master_password: MasterPassword, salt: bytes) -> bytes:
        if not isinstance(master_password, MasterPassword):
            raise TypeError("master_password must be MasterPassword")
        self._validate_salt(salt)

        return hash_secret_raw(
            secret=master_password.value.encode("utf-8"),
            salt=salt,
            time_cost=self._time_cost,
            memory_cost=self._memory_cost,
            parallelism=self._parallelism,
            hash_len=self._hash_len,
            type=Type.ID,
        )
