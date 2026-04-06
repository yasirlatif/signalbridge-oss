import requests

def fetch_json(url: str, headers: dict | None = None, timeout_seconds: int = 30):
    response = requests.get(url, headers=headers or {}, timeout=timeout_seconds)
    response.raise_for_status()
    return response.json()
