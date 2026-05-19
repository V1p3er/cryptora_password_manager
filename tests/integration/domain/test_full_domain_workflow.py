import time
import uuid
import pytest

from domain.value_objects.userid import UserId
from domain.value_objects.username import Username
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash
from domain.value_objects.created_at import CreatedAt
from domain.value_objects.domain_name import DomainName
from domain.value_objects.service_name import ServiceName
from domain.value_objects.vault_item_username import VaultItemUsername
from domain.value_objects.encrypted_value import EncryptedValue
from domain.value_objects.password_strength import PasswordStrength

from domain.entities.user import User
from domain.entities.vault import Vault

from domain.services.master_password_verifier import MasterPasswordVerifier
from domain.services.data_encryption_key_deriver import DataEncryptionKeyDeriver
from domain.services.vault_item_encryption_service import VaultItemEncryptionService
from domain.services.password_strength_calculator import PasswordStrengthCalculator
from domain.services.vault_locking_service import VaultLockingService

from domain.repositories.user_repository import UserRepository
from domain.repositories.vault_repository import VaultRepository


# ============================================================
# FAKE INFRASTRUCTURE
# ============================================================

class FakeMasterPasswordVerifier(MasterPasswordVerifier):
    def verify(self, raw_password: MasterPassword, stored_hash: PasswordHash) -> bool:
        # Simple check: hash contains the password value
        return raw_password.value in stored_hash.value


class FakeKeyDeriver(DataEncryptionKeyDeriver):
    def derive_key(self, master_password: MasterPassword, salt: bytes) -> bytes:
        self._validate_salt(salt)
        import hashlib
        return hashlib.sha256(master_password.value.encode() + salt).digest()


class FakeEncryptionService(VaultItemEncryptionService):
    """XOR encryption producing hex strings for EncryptedValue."""
    
    def encrypt(self, plaintext: str, key: bytes) -> EncryptedValue:
        self._validate_plaintext(plaintext)
        self._validate_key(key)
        encrypted_bytes = bytes(
            ord(c) ^ key[i % len(key)] for i, c in enumerate(plaintext)
        )
        return EncryptedValue(value=encrypted_bytes.hex())
    
    def decrypt(self, encrypted: EncryptedValue, key: bytes) -> str:
        self._validate_key(key)
        encrypted_bytes = bytes.fromhex(encrypted.value)
        return "".join(
            chr(b ^ key[i % len(key)]) for i, b in enumerate(encrypted_bytes)
        )


class FakeVaultLockingService(VaultLockingService):
    """
    Locking service that tracks decrypted passwords externally.
    VaultItem has slots - cannot attach _decrypted_password to it.
    We store decrypted data in a dict keyed by item_id.
    """
    
    def __init__(self, verifier, key_deriver, encryption):
        self._verifier = verifier
        self._key_deriver = key_deriver
        self._encryption = encryption
        self._decrypted_passwords: dict[int, str] = {}
        self._unlocked_vaults: set = set()
    
    def unlock_vault(self, user_id, raw_master_password, stored_password_hash, vault_items):
        self._validate_vault_items(vault_items)
        
        if not self._verifier.verify(raw_master_password, stored_password_hash):
            raise ValueError("Invalid master password")
        
        salt = stored_password_hash.value[:16].encode()
        key = self._key_deriver.derive_key(raw_master_password, salt)
        
        for item in vault_items:
            decrypted = self._encryption.decrypt(item.password, key)
            self._decrypted_passwords[item.item_id] = decrypted
        
        self._unlocked_vaults.add(user_id)
        return vault_items
    
    def lock_vault(self, user_id):
        if user_id in self._unlocked_vaults:
            self._decrypted_passwords.clear()
            self._unlocked_vaults.discard(user_id)
    
    def get_decrypted_password(self, item_id: int) -> str | None:
        return self._decrypted_passwords.get(item_id)


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self._users = {}
    def save(self, user): self._users[user.user_id] = user
    def get(self, user_id): return self._users.get(user_id)
    def get_by_username(self, username):
        for u in self._users.values():
            if u.username == username:
                return u
        return None
    def exists(self, user_id): return user_id in self._users
    def exists_by_username(self, username):
        return any(u.username == username for u in self._users.values())
    def delete(self, user_id): self._users.pop(user_id, None)


class InMemoryVaultRepository(VaultRepository):
    def __init__(self):
        self._vaults = {}
    def save(self, vault): self._vaults[vault._user_id] = vault
    def get_for_user(self, user_id): return self._vaults.get(user_id)
    def exists(self, user_id): return user_id in self._vaults
    def delete(self, user_id): self._vaults.pop(user_id, None)


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def services():
    verifier = FakeMasterPasswordVerifier()
    key_deriver = FakeKeyDeriver()
    encryption = FakeEncryptionService()
    locking = FakeVaultLockingService(verifier, key_deriver, encryption)
    return {
        "verifier": verifier,
        "key_deriver": key_deriver,
        "encryption": encryption,
        "locking": locking,
    }


@pytest.fixture
def repositories():
    return {
        "users": InMemoryUserRepository(),
        "vaults": InMemoryVaultRepository(),
    }


def make_user_id():
    return UserId(value=uuid.uuid4())


# Valid master password: 12+ chars, uppercase, lowercase, digit, special
VALID_PASSWORD = "ValidP@ssword1"


# ============================================================
# TESTS
# ============================================================

class TestFullUserWorkflow:
    
    def test_register_and_authenticate_user(self, services, repositories):
        user_repo = repositories["users"]
        verifier = services["verifier"]
        
        user_id = make_user_id()
        username = Username(value="testuser1234")
        master_pw = MasterPassword(value=VALID_PASSWORD)
        password_hash = PasswordHash(value=f"hashed_{VALID_PASSWORD}_salt16bytes!")
        
        user = User.create(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            created_at=CreatedAt.now(),
        )
        user_repo.save(user)
        
        retrieved = user_repo.get(user_id)
        assert retrieved is not None
        assert verifier.verify(master_pw, retrieved.password_hash) is True
    
    def test_change_password_and_verify(self, services, repositories):
        user_repo = repositories["users"]
        verifier = services["verifier"]
        
        old_pw = MasterPassword(value="OldP@ssword12")
        new_pw = MasterPassword(value="NewP@ssword34")
        
        user = User.create(
            user_id=make_user_id(),
            username=Username(value="changepw_user"),
            password_hash=PasswordHash(value="hashed_OldP@ssword12_salt16b"),
            created_at=CreatedAt.now(),
        )
        user_repo.save(user)
        
        assert verifier.verify(old_pw, user.password_hash) is True
        
        new_hash = PasswordHash(value="hashed_NewP@ssword34_salt16b")
        user.change_password(new_hash)
        user_repo.save(user)
        
        retrieved = user_repo.get(user.user_id)
        assert verifier.verify(old_pw, retrieved.password_hash) is False
        assert verifier.verify(new_pw, retrieved.password_hash) is True


class TestVaultWorkflow:
    
    def test_create_vault_and_add_items(self, services, repositories):
        vault_repo = repositories["vaults"]
        user_id = make_user_id()
        vault = Vault.create_for_user(user_id)
        
        vault.add_item(
            title=ServiceName(value="Spotify"),
            username=VaultItemUsername(value="spotify_user"),
            password=EncryptedValue(value="enc_spotify_pass"),
            domain_name=DomainName(value="spotify.com"),
        )
        vault.add_item(
            title=ServiceName(value="GitHub"),
            username=VaultItemUsername(value="github_user"),
            password=EncryptedValue(value="enc_github_pass"),
            domain_name=DomainName(value="github.com"),
        )
        vault_repo.save(vault)
        
        retrieved = vault_repo.get_for_user(user_id)
        assert retrieved is not None
        assert len(retrieved.items) == 2
    
    def test_update_vault_item(self, services, repositories):
        vault_repo = repositories["vaults"]
        user_id = make_user_id()
        vault = Vault.create_for_user(user_id)
        vault.add_item(
            title=ServiceName(value="OldTitle"),
            username=VaultItemUsername(value="old_user"),
            password=EncryptedValue(value="old_pass_val"),
            domain_name=DomainName(value="old.com"),
        )
        vault_repo.save(vault)
        
        retrieved = vault_repo.get_for_user(user_id)
        retrieved.update_item_title(0, ServiceName(value="NewTitle"))
        vault_repo.save(retrieved)
        
        final = vault_repo.get_for_user(user_id)
        assert final.items[0].title == ServiceName(value="NewTitle")
    
    def test_remove_item_reindexes(self, services, repositories):
        vault_repo = repositories["vaults"]
        user_id = make_user_id()
        vault = Vault.create_for_user(user_id)
        vault.add_item(None, None, EncryptedValue(value="item0_val"), DomainName(value="0.com"))
        vault.add_item(None, None, EncryptedValue(value="item1_val"), DomainName(value="1.com"))
        vault.add_item(None, None, EncryptedValue(value="item2_val"), DomainName(value="2.com"))
        vault_repo.save(vault)
        
        retrieved = vault_repo.get_for_user(user_id)
        retrieved.remove_item(1)
        vault_repo.save(retrieved)
        
        final = vault_repo.get_for_user(user_id)
        assert len(final.items) == 2
        assert final.items[0].item_id == 0
        assert final.items[1].item_id == 1


class TestEncryptionWorkflow:
    
    def test_encrypt_decrypt_roundtrip(self, services):
        encryption = services["encryption"]
        key = b"a" * 32
        
        plaintext = "MySuperSecret123!"
        encrypted = encryption.encrypt(plaintext, key)
        decrypted = encryption.decrypt(encrypted, key)
        
        assert decrypted == plaintext
    
    def test_wrong_key_cannot_decrypt(self, services):
        encryption = services["encryption"]
        key1 = b"a" * 32
        key2 = b"b" * 32
        
        encrypted = encryption.encrypt("SecretPassword1", key1)
        decrypted = encryption.decrypt(encrypted, key2)
        
        assert decrypted != "SecretPassword1"


class TestLockingWorkflow:
    
    def test_unlock_vault_with_correct_password(self, services):
        locking = services["locking"]
        encryption = services["encryption"]
        
        user_id = make_user_id()
        master_pw = MasterPassword(value=VALID_PASSWORD)
        stored_hash = PasswordHash(value=f"hashed_{VALID_PASSWORD}_salt16bytes!")
        
        salt = stored_hash.value[:16].encode()
        key = services["key_deriver"].derive_key(master_pw, salt)
        encrypted = encryption.encrypt("my_secret_password", key)
        
        vault = Vault.create_for_user(user_id)
        vault.add_item(None, None, encrypted, DomainName(value="test.com"))
        
        unlocked = locking.unlock_vault(user_id, master_pw, stored_hash, vault.items)
        
        assert len(unlocked) == 1
        decrypted = locking.get_decrypted_password(unlocked[0].item_id)
        assert decrypted == "my_secret_password"
    
    def test_unlock_vault_with_wrong_password_fails(self, services):
        locking = services["locking"]
        
        user_id = make_user_id()
        wrong_pw = MasterPassword(value="WrongP@ssword12")
        stored_hash = PasswordHash(value=f"hashed_{VALID_PASSWORD}_salt16bytes!")
        
        vault = Vault.create_for_user(user_id)
        vault.add_item(
            None, None,
            EncryptedValue(value="deadbeef" * 8),
            DomainName(value="test.com"),
        )
        
        with pytest.raises(ValueError, match="Invalid master password"):
            locking.unlock_vault(user_id, wrong_pw, stored_hash, vault.items)
    
    def test_lock_vault_clears_decrypted_data(self, services):
        locking = services["locking"]
        encryption = services["encryption"]
        
        user_id = make_user_id()
        master_pw = MasterPassword(value=VALID_PASSWORD)
        stored_hash = PasswordHash(value=f"hashed_{VALID_PASSWORD}_salt16bytes!")
        
        salt = stored_hash.value[:16].encode()
        key = services["key_deriver"].derive_key(master_pw, salt)
        encrypted = encryption.encrypt("secret_data", key)
        
        vault = Vault.create_for_user(user_id)
        vault.add_item(None, None, encrypted, DomainName(value="test.com"))
        
        unlocked = locking.unlock_vault(user_id, master_pw, stored_hash, vault.items)
        assert locking.get_decrypted_password(unlocked[0].item_id) == "secret_data"
        
        locking.lock_vault(user_id)
        assert locking.get_decrypted_password(unlocked[0].item_id) is None


class TestPasswordStrengthWorkflow:
    
    def test_strong_password(self):
        result = PasswordStrengthCalculator.calculate("Str0ng!P@ssword")
        assert result.score == 4
    
    def test_medium_password(self):
        result = PasswordStrengthCalculator.calculate("StrongPass1")
        assert result.score >= 2
    
    def test_weak_password(self):
        result = PasswordStrengthCalculator.calculate("short")
        assert result.score <= 1
    
    def test_is_weak(self):
        result = PasswordStrengthCalculator.calculate("abc")
        assert result.is_weak() is True
    
    def test_is_strong(self):
        result = PasswordStrengthCalculator.calculate("Str0ng!P@ssword")
        assert result.is_strong() is True


class TestCrossCuttingSecurity:
    
    def test_user_data_isolation(self, services, repositories):
        user_repo = repositories["users"]
        vault_repo = repositories["vaults"]
        locking = services["locking"]
        
        # User A
        user_a_id = make_user_id()
        user_a_pw = MasterPassword(value="UserA_P@ssword1")
        user_a_hash = PasswordHash(value="hashed_UserA_P@ssword1_salt16!")
        
        user_a = User.create(
            user_id=user_a_id,
            username=Username(value="useraaaaaa"),
            password_hash=user_a_hash,
            created_at=CreatedAt.now(),
        )
        user_repo.save(user_a)
        
        vault_a = Vault.create_for_user(user_a_id)
        vault_a.add_item(
            ServiceName(value="A_Service"), None,
            EncryptedValue(value="a" * 32),
            DomainName(value="a.com"),
        )
        vault_repo.save(vault_a)
        
        # User B
        user_b_id = make_user_id()
        user_b_pw = MasterPassword(value="UserB_P@ssword2")
        user_b_hash = PasswordHash(value="hashed_UserB_P@ssword2_salt16!")
        
        user_b = User.create(
            user_id=user_b_id,
            username=Username(value="userbbbbbb"),
            password_hash=user_b_hash,
            created_at=CreatedAt.now(),
        )
        user_repo.save(user_b)
        
        vault_b = Vault.create_for_user(user_b_id)
        vault_b.add_item(
            ServiceName(value="B_Service"), None,
            EncryptedValue(value="b" * 32),
            DomainName(value="b.com"),
        )
        vault_repo.save(vault_b)
        
        # User A tries User B's vault with A's password -> fails
        with pytest.raises(ValueError, match="Invalid master password"):
            locking.unlock_vault(user_b_id, user_a_pw, user_b_hash, vault_b.items)
        
        # User A accesses own vault -> succeeds
        unlocked = locking.unlock_vault(user_a_id, user_a_pw, user_a_hash, vault_a.items)
        assert len(unlocked) == 1
    
    def test_password_hash_does_not_contain_raw_password(self, services, repositories):
        user_repo = repositories["users"]
        
        user = User.create(
            user_id=make_user_id(),
            username=Username(value="secureuser1"),
            password_hash=PasswordHash(value="completely_different_hash_value_here!"),
            created_at=CreatedAt.now(),
        )
        user_repo.save(user)
        
        retrieved = user_repo.get(user.user_id)
        # The hash is a separate value, not containing the real password
        assert VALID_PASSWORD not in retrieved.password_hash.value


class TestPerformance:
    
    def test_bulk_item_addition(self, services, repositories):
        vault_repo = repositories["vaults"]
        user_id = make_user_id()
        vault = Vault.create_for_user(user_id)
        
        start = time.perf_counter()
        for i in range(1000):
            vault.add_item(
                title=ServiceName(value=f"Svc{i}"),
                username=VaultItemUsername(value=f"u_{i:04d}"),
                password=EncryptedValue(value=f"p_{i:04d}_" + "x" * 20),
                domain_name=DomainName(value=f"s{i}.com"),
            )
        elapsed = time.perf_counter() - start
        
        vault_repo.save(vault)
        retrieved = vault_repo.get_for_user(user_id)
        
        assert len(retrieved.items) == 1000
        assert elapsed < 1.0, f"Adding 1000 items took {elapsed:.3f}s"
    
    def test_bulk_user_creation(self, services, repositories):
        user_repo = repositories["users"]
        
        start = time.perf_counter()
        for i in range(100):
            user = User.create(
                user_id=UserId(value=uuid.uuid4()),
                username=Username(value=f"bulk_{i:03d}"),
                password_hash=PasswordHash(value=f"h_{i:03d}_" + "x" * 30),
                created_at=CreatedAt.now(),
            )
            user_repo.save(user)
        elapsed = time.perf_counter() - start
        
        assert elapsed < 0.5, f"Creating 100 users took {elapsed:.3f}s"


class TestFullEndToEndScenario:
    
    def test_complete_user_journey(self, services, repositories):
        user_repo = repositories["users"]
        vault_repo = repositories["vaults"]
        encryption = services["encryption"]
        locking = services["locking"]
        
        # 1. Register
        user_id = make_user_id()
        username = Username(value="realuser1234")
        master_pw = MasterPassword(value=VALID_PASSWORD)
        password_hash = PasswordHash(value=f"hashed_{VALID_PASSWORD}_salt16b!")
        
        user = User.create(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            created_at=CreatedAt.now(),
        )
        user_repo.save(user)
        
        # 2. Create vault
        vault = Vault.create_for_user(user_id)
        vault_repo.save(vault)
        
        # 3. Add items with properly encrypted passwords
        salt = password_hash.value[:16].encode()
        key = services["key_deriver"].derive_key(master_pw, salt)
        enc_email = encryption.encrypt("email_password_123", key)
        enc_bank = encryption.encrypt("bank_password_456", key)
        
        vault.add_item(
            title=ServiceName(value="Email"),
            username=VaultItemUsername(value="me@email.com"),
            password=enc_email,
            domain_name=DomainName(value="gmail.com"),
        )
        vault.add_item(
            title=ServiceName(value="Bank"),
            username=VaultItemUsername(value="bank_user1"),
            password=enc_bank,
            domain_name=DomainName(value="bank.com"),
        )
        vault_repo.save(vault)
        
        # 4. Authenticate and unlock
        retrieved_vault = vault_repo.get_for_user(user_id)
        unlocked = locking.unlock_vault(
            user_id, master_pw, user.password_hash, retrieved_vault.items
        )
        assert len(unlocked) == 2
        assert locking.get_decrypted_password(0) == "email_password_123"
        assert locking.get_decrypted_password(1) == "bank_password_456"
        
        # 5. Check password strength
        strength = PasswordStrengthCalculator.calculate("MyNewBankP@ss1")
        assert strength.score >= 3
        
        # 6. Update a password
        new_enc = encryption.encrypt("new_email_password", key)
        retrieved_vault.update_item_password(0, new_enc)
        vault_repo.save(retrieved_vault)
        
        # 7. Lock vault
        locking.lock_vault(user_id)
        assert locking.get_decrypted_password(0) is None
        
        # 8. Unlock again later
        final_vault = vault_repo.get_for_user(user_id)
        relocked = locking.unlock_vault(
            user_id, master_pw, user.password_hash, final_vault.items
        )
        assert len(relocked) == 2
        
        # 9. Verify updated password
        assert locking.get_decrypted_password(0) == "new_email_password"