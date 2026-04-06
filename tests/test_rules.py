from signalbridge.validation.rules import validate_value

def test_validate_value():
    ok, issues = validate_value(10.0, min_value=0.0, max_value=100.0, allow_negative=True)
    assert ok is True
    assert issues == []
