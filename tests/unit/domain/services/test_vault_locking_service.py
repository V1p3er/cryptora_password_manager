import pytest
import uuid
from domain.services.vault_locking_service import VaultLockingService
from domain.value_objects.userid import UserId
from domain.value_objects.master_password import MasterPassword
from domain.value_objects.password_hash import PasswordHash


class FakeVaultItem:
    def __init__(self, name="item"):
        self.name = name
        self.decrypted = False

    def unlock(self, plaintext):
        self.decrypted = True


class FakeLocking(VaultLockingService):
    def __init__(self):
        self.unlocked_vaults = []
        self.locked_vaults = []

    def unlock_vault(self, user_id, raw_master_password, stored_password_hash, vault_items):
        self._validate_vault_items(vault_items)
        self.unlocked_vaults.append(user_id)
        for item in vault_items:
            item.unlock("fake_plaintext")
        return vault_items

    def lock_vault(self, user_id):
        self.locked_vaults.append(user_id)


def test_unlock_vault_returns_items():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())
    mp = MasterPassword(value="StrongP@ssword1")
    ph = PasswordHash(value="s" * 48)
    items = [FakeVaultItem("spotify"), FakeVaultItem("github")]

    result = svc.unlock_vault(uid, mp, ph, items)

    assert result == items
    assert len(result) == 2


def test_unlock_vault_single_item():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())
    mp = MasterPassword(value="SingleItem12!@")
    ph = PasswordHash(value="x" * 48)
    items = [FakeVaultItem("only_item")]

    result = svc.unlock_vault(uid, mp, ph, items)

    assert len(result) == 1
    assert result[0].name == "only_item"


def test_unlock_vault_empty_list_raises_error():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())
    mp = MasterPassword(value="EmptyListErr1!")
    ph = PasswordHash(value="e" * 48)

    with pytest.raises(ValueError, match="cannot be empty"):
        svc.unlock_vault(uid, mp, ph, [])


def test_unlock_vault_not_list_raises_error():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())
    mp = MasterPassword(value="NotListErr12!@")
    ph = PasswordHash(value="n" * 48)

    with pytest.raises(TypeError, match="must be list"):
        svc.unlock_vault(uid, mp, ph, "not_list")


def test_unlock_vault_records_user_id():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())
    mp = MasterPassword(value="RecordUID12!@")
    ph = PasswordHash(value="r" * 48)
    items = [FakeVaultItem()]

    svc.unlock_vault(uid, mp, ph, items)

    assert len(svc.unlocked_vaults) == 1
    assert svc.unlocked_vaults[0] == uid


def test_unlock_vault_two_users():
    svc = FakeLocking()
    mp = MasterPassword(value="TwoUsers123!@")
    ph = PasswordHash(value="t" * 48)
    items = [FakeVaultItem()]

    uid1 = UserId(value=uuid.uuid4())
    uid2 = UserId(value=uuid.uuid4())

    svc.unlock_vault(uid1, mp, ph, items)
    svc.unlock_vault(uid2, mp, ph, items)

    assert len(svc.unlocked_vaults) == 2
    assert svc.unlocked_vaults[0] == uid1
    assert svc.unlocked_vaults[1] == uid2
    assert uid1 != uid2


def test_lock_vault_records_user_id():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())

    svc.lock_vault(uid)

    assert len(svc.locked_vaults) == 1
    assert svc.locked_vaults[0] == uid


def test_lock_vault_multiple_calls():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())

    svc.lock_vault(uid)
    svc.lock_vault(uid)

    assert len(svc.locked_vaults) == 2


def test_unlock_then_lock():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())
    mp = MasterPassword(value="LockUnlock12!@")
    ph = PasswordHash(value="l" * 48)
    items = [FakeVaultItem()]

    svc.unlock_vault(uid, mp, ph, items)
    svc.lock_vault(uid)

    assert len(svc.unlocked_vaults) == 1
    assert len(svc.locked_vaults) == 1


def test_unlock_vault_items_become_decrypted():
    svc = FakeLocking()
    uid = UserId(value=uuid.uuid4())
    mp = MasterPassword(value="DecryptMe123!@")
    ph = PasswordHash(value="d" * 48)
    item = FakeVaultItem("spotify")

    svc.unlock_vault(uid, mp, ph, [item])

    assert item.decrypted is True