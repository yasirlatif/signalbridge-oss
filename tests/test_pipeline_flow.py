import csv
from io import StringIO
from unittest.mock import patch

from signalbridge.normalization.timestamps import normalize_timestamp
from signalbridge.sinks.csv_sink import write_rows
from signalbridge.validation.rules import validate_value


class NonClosingStringIO(StringIO):
    def close(self) -> None:
        pass


def test_end_to_end_flow_normalizes_validates_and_writes_rows() -> None:
    source_rows = [
        {"tag": "temperature", "timestamp": "2026-04-06T15:30:00+05:00", "value": 42.0},
        {"tag": "pressure", "timestamp": "2026-04-06T15:31:00+05:00", "value": -3.0},
    ]

    validated_rows = []
    for row in source_rows:
        is_valid, issues = validate_value(
            row["value"],
            min_value=0.0,
            max_value=100.0,
            allow_negative=False,
        )
        if is_valid:
            validated_rows.append(
                {
                    "tag": row["tag"],
                    "timestamp": normalize_timestamp(row["timestamp"]),
                    "value": row["value"],
                }
            )
        else:
            assert issues

    file_buffer = NonClosingStringIO()
    with patch("pathlib.Path.mkdir"):
        with patch("pathlib.Path.open", return_value=file_buffer):
            write_rows("output/validated.csv", validated_rows)

    file_buffer.seek(0)
    rows = list(csv.DictReader(file_buffer))

    assert rows == [
        {"tag": "temperature", "timestamp": "2026-04-06T10:30:00Z", "value": "42.0"}
    ]
