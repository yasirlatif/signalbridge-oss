from typing import Any

import requests


def fetch_json(
    url: str,
    headers: dict[str, str] | None = None,
    timeout_seconds: int = 30,
) -> Any:
    """Fetch JSON from a REST endpoint and raise on HTTP errors."""
    response = requests.get(url, headers=headers or {}, timeout=timeout_seconds)
    response.raise_for_status()
    return response.json()
