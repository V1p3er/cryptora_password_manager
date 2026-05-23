from domain.services.master_password_hasher import MasterPasswordHasher
from domain.services.master_password_verifier import MasterPasswordVerifier
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash


class Argon2PasswordHasher:
    @staticmethod
    def hash(password: MasterPassword) -> PasswordHash:
        return MasterPasswordHasher.hash(password)


class Argon2PasswordVerifier(MasterPasswordVerifier):
    def verify(self, raw_password: MasterPassword, stored_hash: PasswordHash) -> bool:
        if not isinstance(raw_password, MasterPassword):
            raise TypeError("raw_password must be MasterPassword")
        if not isinstance(stored_hash, PasswordHash):
            raise TypeError("stored_hash must be PasswordHash")
        return MasterPasswordHasher.verify(raw_password, stored_hash)
