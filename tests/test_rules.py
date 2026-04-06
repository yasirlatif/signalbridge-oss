from signalbridge.validation.rules import validate_value

def test_validate_value() -> None:
    ok, issues = validate_value(10.0, min_value=0.0, max_value=100.0, allow_negative=True)
    assert ok is True
    assert issues == []


def test_validate_value_collects_rule_issues() -> None:
    ok, issues = validate_value(-5.0, min_value=0.0, max_value=4.0, allow_negative=False)

    assert ok is False
    assert issues == [
        "negative values are not allowed",
        "value below minimum threshold: 0.0",
    ]
