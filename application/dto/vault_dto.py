from dataclasses import dataclass

from application.dto.credential_dto import CredentialDTO


@dataclass(frozen=True, slots=True)
class VaultDTO:
    vault_id: str
    user_id: str
    items: list[CredentialDTO]
