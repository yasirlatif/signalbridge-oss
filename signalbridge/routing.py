from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable

from signalbridge.normalization.timestamps import normalize_timestamp
from signalbridge.validation.rules import validate_value


@dataclass
class RoutedRecords:
    """Container for records split by routing outcome."""

    raw_records: list[dict[str, Any]] = field(default_factory=list)
    validated_records: list[dict[str, Any]] = field(default_factory=list)
    flagged_records: list[dict[str, Any]] = field(default_factory=list)


def _flag_record(
    record: dict[str, Any],
    routing_reason: str,
    issues: list[str],
) -> dict[str, Any]:
    """Return a flagged record with routing metadata attached."""
    return {
        **record,
        "routing_reason": routing_reason,
        "issues": issues,
    }


def route_records(
    records: Iterable[dict[str, Any]],
    *,
    min_value: float | None = None,
    max_value: float | None = None,
    allow_negative: bool = True,
) -> RoutedRecords:
    """Route records into raw, validated, and flagged collections."""
    routed = RoutedRecords()
    seen_keys: set[tuple[str, str]] = set()
    last_timestamp_by_tag: dict[str, datetime] = {}

    for record in records:
        raw_record = dict(record)
        routed.raw_records.append(raw_record)

        missing_fields = [
            field_name for field_name in ("tag", "timestamp", "value") if field_name not in raw_record
        ]
        if missing_fields:
            routed.flagged_records.append(
                _flag_record(
                    raw_record,
                    "missing_required_field",
                    [f"missing required field: {field_name}" for field_name in missing_fields],
                )
            )
            continue

        try:
            normalized_timestamp = normalize_timestamp(str(raw_record["timestamp"]))
        except (TypeError, ValueError) as exc:
            routed.flagged_records.append(
                _flag_record(
                    raw_record,
                    "normalization_failed",
                    [f"timestamp normalization failed: {exc}"],
                )
            )
            continue

        tag = str(raw_record["tag"])
        record_key = (tag, normalized_timestamp)
        normalized_datetime = datetime.fromisoformat(normalized_timestamp.replace("Z", "+00:00"))
        routing_issues: list[str] = []

        if record_key in seen_keys:
            routing_issues.append(
                f"duplicate record for tag '{tag}' at timestamp '{normalized_timestamp}'"
            )

        previous_timestamp = last_timestamp_by_tag.get(tag)
        if previous_timestamp is not None and normalized_datetime < previous_timestamp:
            routing_issues.append(
                f"out-of-order timestamp for tag '{tag}': '{normalized_timestamp}' arrived after '{previous_timestamp.isoformat().replace('+00:00', 'Z')}'"
            )

        validation_result = validate_value(
            raw_record["value"],
            min_value=min_value,
            max_value=max_value,
            allow_negative=allow_negative,
        )

        issues = routing_issues + validation_result.issues
        if issues:
            if routing_issues and validation_result.issues:
                routing_reason = "routing_and_validation_failed"
            elif routing_issues:
                routing_reason = "routing_failed"
            else:
                routing_reason = "validation_failed"

            routed.flagged_records.append(
                _flag_record(raw_record, routing_reason, issues)
            )
            continue

        seen_keys.add(record_key)
        last_timestamp_by_tag[tag] = normalized_datetime
        routed.validated_records.append(
            {
                "tag": tag,
                "timestamp": normalized_timestamp,
                "value": raw_record["value"],
            }
        )

    return routed
