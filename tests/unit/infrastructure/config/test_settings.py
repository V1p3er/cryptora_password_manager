from infrastructure.config.settings import Settings


def test_from_env_uses_defaults(monkeypatch):
    monkeypatch.delenv("CRYPTORA_STORAGE_FILE_PATH", raising=False)
    monkeypatch.delenv("CRYPTORA_POSTGRESQL_DSN", raising=False)
    settings = Settings.from_env()
    assert settings.storage_file_path == ".cryptora_vault.json"
    assert settings.postgresql_dsn == ""
