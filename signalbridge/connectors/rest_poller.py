from typing import Any

import requests


def fetch_json(
    url: str,
    headers: dict[str, str] | None = None,
    timeout_seconds: int = 30,
) -> Any:
    response = requests.get(url, headers=headers or {}, timeout=timeout_seconds)
    response.raise_for_status()
    return response.json()
