from enum import StrEnum


class SyncStatus(StrEnum):
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
