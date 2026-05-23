from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CredentialDTO:
    item_id: int
    title: str | None
    username: str | None
    password: str
    domain: str
