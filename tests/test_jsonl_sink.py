import json
from io import StringIO
from unittest.mock import patch

from signalbridge.sinks.jsonl_sink import write_rows


class NonClosingStringIO(StringIO):
    def close(self) -> None:
        pass


def test_write_rows_writes_jsonl_file() -> None:
    file_buffer = NonClosingStringIO()

    with patch("pathlib.Path.mkdir") as mock_mkdir:
        with patch("pathlib.Path.open", return_value=file_buffer):
            result = write_rows(
                "output/validated.jsonl",
                [
                    {"tag": "temperature", "timestamp": "2026-04-06T10:30:00Z", "value": 42.0},
                    {"tag": "pressure", "timestamp": "2026-04-06T10:31:00Z", "value": 101.3},
                ],
            )

    file_buffer.seek(0)
    lines = [json.loads(line) for line in file_buffer.read().splitlines()]

    mock_mkdir.assert_called_once()
    assert str(result).endswith("output\\validated.jsonl") or str(result).endswith("output/validated.jsonl")
    assert lines == [
        {"tag": "temperature", "timestamp": "2026-04-06T10:30:00Z", "value": 42.0},
        {"tag": "pressure", "timestamp": "2026-04-06T10:31:00Z", "value": 101.3},
    ]


def test_write_rows_creates_empty_jsonl_file_when_rows_are_empty() -> None:
    with patch("pathlib.Path.mkdir") as mock_mkdir:
        with patch("pathlib.Path.write_text") as mock_write_text:
            result = write_rows("output/flagged.jsonl", [])

    mock_mkdir.assert_called_once()
    mock_write_text.assert_called_once_with("", encoding="utf-8")
    assert str(result).endswith("output\\flagged.jsonl") or str(result).endswith("output/flagged.jsonl")
