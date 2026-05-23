import logging


class AuditLogger:
    def __init__(self, logger_name: str = "cryptora.audit") -> None:
        self._logger = logging.getLogger(logger_name)

    def record(self, event: str, **fields: object) -> None:
        if not isinstance(event, str):
            raise TypeError("event must be str")
        if not event.strip():
            raise ValueError("event cannot be empty")

        if fields:
            self._logger.info("%s | %s", event.strip(), fields)
            return
        self._logger.info("%s", event.strip())
