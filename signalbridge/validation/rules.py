def validate_value(
    value: float,
    min_value: float | None = None,
    max_value: float | None = None,
    allow_negative: bool = True,
) -> tuple[bool, list[str]]:
    """Validate a numeric value against simple threshold rules."""
    issues = []

    if not allow_negative and value < 0:
        issues.append("negative values are not allowed")
    if min_value is not None and value < min_value:
        issues.append(f"value below minimum threshold: {min_value}")
    if max_value is not None and value > max_value:
        issues.append(f"value above maximum threshold: {max_value}")

    return (len(issues) == 0, issues)
