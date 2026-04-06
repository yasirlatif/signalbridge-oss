def validate_value(value: float, min_value=None, max_value=None, allow_negative=True):
    issues = []

    if not allow_negative and value < 0:
        issues.append("negative values are not allowed")
    if min_value is not None and value < min_value:
        issues.append(f"value below minimum threshold: {min_value}")
    if max_value is not None and value > max_value:
        issues.append(f"value above maximum threshold: {max_value}")

    return (len(issues) == 0, issues)
