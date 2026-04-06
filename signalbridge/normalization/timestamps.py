from datetime import datetime, timezone

def normalize_timestamp(value: str) -> str:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).isoformat()
