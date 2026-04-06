from signalbridge.routing import route_records


def test_route_records_splits_records_by_outcome() -> None:
    records = [
        {"tag": "pump_vibration_x", "timestamp": "2026-04-06T15:30:00+05:00", "value": 2.15},
        {"tag": "pump_vibration_y", "timestamp": "2026-04-06T15:31:00+05:00", "value": -2.0},
        {"tag": "pump_vibration_z", "timestamp": "not-a-timestamp", "value": 4.1},
        {"tag": "pump_vibration_q", "value": 4.1},
    ]

    routed = route_records(
        records,
        min_value=0.0,
        max_value=1000.0,
        allow_negative=False,
    )

    assert len(routed.raw_records) == 4
    assert routed.validated_records == [
        {
            "tag": "pump_vibration_x",
            "timestamp": "2026-04-06T10:30:00Z",
            "value": 2.15,
        }
    ]
    assert routed.flagged_records == [
        {
            "tag": "pump_vibration_y",
            "timestamp": "2026-04-06T15:31:00+05:00",
            "value": -2.0,
            "routing_reason": "validation_failed",
            "issues": [
                "negative values are not allowed",
                "value below minimum threshold: 0.0",
            ],
        },
        {
            "tag": "pump_vibration_z",
            "timestamp": "not-a-timestamp",
            "value": 4.1,
            "routing_reason": "normalization_failed",
            "issues": ["timestamp normalization failed: Invalid isoformat string: 'not-a-timestamp'"],
        },
        {
            "tag": "pump_vibration_q",
            "value": 4.1,
            "routing_reason": "missing_required_field",
            "issues": ["missing required field: timestamp"],
        },
    ]
