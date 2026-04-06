from dataclasses import dataclass, field


@dataclass
class ValidationResult:
    """Structured result for a validation check."""

    is_valid: bool
    issues: list[str] = field(default_factory=list)
    severity: str = "none"

    def __iter__(self):
        """Allow tuple-style unpacking for existing callers."""
        yield self.is_valid
        yield self.issues


def validate_value(
    value: float,
    min_value: float | None = None,
    max_value: float | None = None,
    allow_negative: bool = True,
) -> ValidationResult:
    """Validate a numeric value against simple threshold rules."""
    issues = []

    if not allow_negative and value < 0:
        issues.append("negative values are not allowed")
    if min_value is not None and value < min_value:
        issues.append(f"value below minimum threshold: {min_value}")
    if max_value is not None and value > max_value:
        issues.append(f"value above maximum threshold: {max_value}")

    return ValidationResult(
        is_valid=len(issues) == 0,
        issues=issues,
        severity="error" if issues else "none",
    )
