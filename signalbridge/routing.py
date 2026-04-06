from dataclasses import dataclass, field
from typing import Any, Iterable

from signalbridge.normalization.timestamps import normalize_timestamp
from signalbridge.validation.rules import validate_value


@dataclass
class RoutedRecords:
    """Container for records split by routing outcome."""

    raw_records: list[dict[str, Any]] = field(default_factory=list)
    validated_records: list[dict[str, Any]] = field(default_factory=list)
    flagged_records: list[dict[str, Any]] = field(default_factory=list)


def route_records(
    records: Iterable[dict[str, Any]],
    *,
    min_value: float | None = None,
    max_value: float | None = None,
    allow_negative: bool = True,
) -> RoutedRecords:
    """Route records into raw, validated, and flagged collections."""
    routed = RoutedRecords()

    for record in records:
        raw_record = dict(record)
        routed.raw_records.append(raw_record)

        missing_fields = [
            field_name for field_name in ("tag", "timestamp", "value") if field_name not in raw_record
        ]
        if missing_fields:
            routed.flagged_records.append(
                {
                    **raw_record,
                    "routing_reason": "missing_required_field",
                    "issues": [f"missing required field: {field_name}" for field_name in missing_fields],
                }
            )
            continue

        try:
            normalized_timestamp = normalize_timestamp(str(raw_record["timestamp"]))
        except (TypeError, ValueError) as exc:
            routed.flagged_records.append(
                {
                    **raw_record,
                    "routing_reason": "normalization_failed",
                    "issues": [f"timestamp normalization failed: {exc}"],
                }
            )
            continue

        is_valid, issues = validate_value(
            raw_record["value"],
            min_value=min_value,
            max_value=max_value,
            allow_negative=allow_negative,
        )
        if not is_valid:
            routed.flagged_records.append(
                {
                    **raw_record,
                    "routing_reason": "validation_failed",
                    "issues": issues,
                }
            )
            continue

        routed.validated_records.append(
            {
                "tag": raw_record["tag"],
                "timestamp": normalized_timestamp,
                "value": raw_record["value"],
            }
        )

    return routed
