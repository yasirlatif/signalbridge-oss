from signalbridge.normalization.timestamps import normalize_timestamp

def test_normalize_timestamp():
    result = normalize_timestamp("2026-04-06T10:30:00Z")
    assert result.startswith("2026-04-06T10:30:00")
