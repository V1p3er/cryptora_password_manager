from domain.value_objects.userid import UserId
from application.services.unlock_vault import VaultSessionStore


class LockVaultService:
    def __init__(self, session_store: VaultSessionStore) -> None:
        self._session_store = session_store

    def execute(self, user_id: UserId) -> None:
        self._session_store.lock(user_id)
