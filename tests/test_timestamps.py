from signalbridge.normalization.timestamps import normalize_timestamp

def test_normalize_timestamp() -> None:
    result = normalize_timestamp("2026-04-06T10:30:00Z")
    assert result == "2026-04-06T10:30:00Z"


def test_normalize_timestamp_converts_offset_to_utc() -> None:
    result = normalize_timestamp("2026-04-06T15:30:00+05:00")

    assert result == "2026-04-06T10:30:00Z"
