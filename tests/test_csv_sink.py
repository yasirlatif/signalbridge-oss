import csv
from io import StringIO
from unittest.mock import patch

from signalbridge.sinks.csv_sink import write_rows


class NonClosingStringIO(StringIO):
    def close(self) -> None:
        pass


def test_write_rows_writes_csv_file() -> None:
    file_buffer = NonClosingStringIO()

    with patch("pathlib.Path.mkdir") as mock_mkdir:
        with patch("pathlib.Path.open", return_value=file_buffer):
            result = write_rows(
                "output/validated.csv",
                [
                    {"tag": "temperature", "timestamp": "2026-04-06T10:30:00Z", "value": 42.0},
                    {"tag": "pressure", "timestamp": "2026-04-06T10:31:00Z", "value": 101.3},
                ],
            )

    file_buffer.seek(0)
    rows = list(csv.DictReader(file_buffer))

    mock_mkdir.assert_called_once()
    assert str(result).endswith("output\\validated.csv") or str(result).endswith("output/validated.csv")
    assert rows == [
        {"tag": "temperature", "timestamp": "2026-04-06T10:30:00Z", "value": "42.0"},
        {"tag": "pressure", "timestamp": "2026-04-06T10:31:00Z", "value": "101.3"},
    ]
