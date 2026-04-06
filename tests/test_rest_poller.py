from unittest.mock import Mock, patch

from signalbridge.connectors.rest_poller import fetch_json


def test_fetch_json_returns_response_payload() -> None:
    response = Mock()
    response.json.return_value = {"items": [1, 2, 3]}

    with patch("signalbridge.connectors.rest_poller.requests.get", return_value=response) as mock_get:
        payload = fetch_json(
            "https://example.com/api/tags",
            headers={"Authorization": "Bearer token"},
            timeout_seconds=15,
        )

    mock_get.assert_called_once_with(
        "https://example.com/api/tags",
        headers={"Authorization": "Bearer token"},
        timeout=15,
    )
    response.raise_for_status.assert_called_once_with()
    assert payload == {"items": [1, 2, 3]}
