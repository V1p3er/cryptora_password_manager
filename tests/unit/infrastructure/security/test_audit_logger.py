import logging

from infrastructure.security.audit_logger import AuditLogger


def test_record_emits_log(caplog):
    caplog.set_level(logging.INFO)
    logger = AuditLogger("test.audit")
    logger.record("vault_unlocked", user_id="abc")
    assert "vault_unlocked" in caplog.text
