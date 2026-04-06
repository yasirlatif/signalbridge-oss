from datetime import datetime, timezone


def normalize_timestamp(value: str) -> str:
    """Normalize an ISO-like timestamp string to UTC with a trailing Z suffix."""
    timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return timestamp.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
