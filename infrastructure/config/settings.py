import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Settings:
    storage_file_path: str
    postgresql_dsn: str

    @classmethod
    def from_env(cls) -> "Settings":
        storage_file_path = os.getenv("CRYPTORA_STORAGE_FILE_PATH", ".cryptora_vault.json")
        postgresql_dsn = os.getenv("CRYPTORA_POSTGRESQL_DSN", "")
        return cls(
            storage_file_path=storage_file_path,
            postgresql_dsn=postgresql_dsn,
        )
