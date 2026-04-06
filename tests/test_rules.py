from signalbridge.validation.rules import validate_value


def test_validate_value() -> None:
    result = validate_value(10.0, min_value=0.0, max_value=100.0, allow_negative=True)

    assert result.is_valid is True
    assert result.issues == []
    assert result.severity == "none"


def test_validate_value_collects_rule_issues() -> None:
    result = validate_value(-5.0, min_value=0.0, max_value=4.0, allow_negative=False)

    assert result.is_valid is False
    assert result.issues == [
        "negative values are not allowed",
        "value below minimum threshold: 0.0",
    ]
    assert result.severity == "error"


def test_validate_value_still_supports_tuple_unpacking() -> None:
    is_valid, issues = validate_value(1.0, min_value=0.0, max_value=10.0, allow_negative=True)

    assert is_valid is True
    assert issues == []
