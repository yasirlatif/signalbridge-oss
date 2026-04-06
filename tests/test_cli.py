import csv
import json
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from typer.testing import CliRunner

from signalbridge.cli import app, run_demo
from signalbridge.config import AppConfig, ApiConfig, OutputConfig, PollingConfig, ValidationConfig


runner = CliRunner()


def test_validate_command_loads_sample_config() -> None:
    result = runner.invoke(app, ["validate"])

    assert result.exit_code == 0
    assert "Configuration is valid" in result.stdout
    assert "examples/config.sample.yaml" in result.stdout


def test_demo_run_command_processes_sample_files() -> None:
    result = runner.invoke(app, ["demo-run"])

    assert result.exit_code == 0
    assert "Execution summary" in result.stdout
    assert "Total records: 1" in result.stdout
    assert "Valid records: 1" in result.stdout
    assert "Flagged records: 0" in result.stdout
    assert "Duplicate records: 0" in result.stdout
    assert "Out-of-order records: 0" in result.stdout
    assert "Validated output: output\\validated.csv" in result.stdout or "Validated output: output/validated.csv" in result.stdout
    assert "Flagged output: output\\flagged.csv" in result.stdout or "Flagged output: output/flagged.csv" in result.stdout


def test_run_demo_filters_flagged_records_and_writes_separate_csv_outputs() -> None:
    config = AppConfig(
        api=ApiConfig(base_url="https://example.com/api/tags"),
        polling=PollingConfig(interval_seconds=60),
        validation=ValidationConfig(min_value=0.0, max_value=1000.0, allow_negative=False),
        output=OutputConfig(csv_path=Path("output/validated.csv")),
    )
    payload = [
        {
            "tag": "pump_vibration_x",
            "timestamp": "2026-04-06T15:30:00+05:00",
            "value": 2.15,
        },
        {
            "tag": "pump_vibration_y",
            "timestamp": "2026-04-06T15:31:00+05:00",
            "value": -2.0,
        },
    ]
    written_payloads: dict[str, list[dict]] = {}

    def capture_rows(path: str | Path, rows: list[dict]) -> Path:
        written_payloads[str(Path(path))] = list(rows)
        return Path(path)

    with patch("signalbridge.cli.load_config", return_value=config):
        with patch("pathlib.Path.open", return_value=StringIO(json.dumps(payload))):
            with patch("signalbridge.cli.write_rows", side_effect=capture_rows):
                summary = run_demo("payload.json", "config.yaml")

    assert summary["total_records"] == 2
    assert summary["valid_records"] == 1
    assert summary["flagged_records"] == 1
    assert summary["duplicate_records"] == 0
    assert summary["out_of_order_records"] == 0
    assert str(summary["validated_output_path"]).endswith("output\\validated.csv") or str(summary["validated_output_path"]).endswith("output/validated.csv")
    assert str(summary["flagged_output_path"]).endswith("output\\flagged.csv") or str(summary["flagged_output_path"]).endswith("output/flagged.csv")
    assert written_payloads[str(summary["validated_output_path"])] == [
        {
            "tag": "pump_vibration_x",
            "timestamp": "2026-04-06T10:30:00Z",
            "value": 2.15,
        }
    ]
    assert written_payloads[str(summary["flagged_output_path"])] == [
        {
            "tag": "pump_vibration_y",
            "timestamp": "2026-04-06T15:31:00+05:00",
            "value": -2.0,
            "routing_reason": "validation_failed",
            "issues": [
                "negative values are not allowed",
                "value below minimum threshold: 0.0",
            ],
        }
    ]


def test_run_demo_reports_duplicate_and_out_of_order_counts() -> None:
    config = AppConfig(
        api=ApiConfig(base_url="https://example.com/api/tags"),
        polling=PollingConfig(interval_seconds=60),
        validation=ValidationConfig(min_value=0.0, max_value=1000.0, allow_negative=True),
        output=OutputConfig(csv_path=Path("output/validated.csv")),
    )
    payload = [
        {"tag": "pump_vibration_x", "timestamp": "2026-04-06T10:30:00Z", "value": 2.15},
        {"tag": "pump_vibration_x", "timestamp": "2026-04-06T10:30:00Z", "value": 2.20},
        {"tag": "pump_vibration_x", "timestamp": "2026-04-06T10:29:00Z", "value": 2.10},
    ]

    with patch("signalbridge.cli.load_config", return_value=config):
        with patch("pathlib.Path.open", return_value=StringIO(json.dumps(payload))):
            with patch("signalbridge.cli.write_rows"):
                summary = run_demo("payload.json", "config.yaml")

    assert summary["total_records"] == 3
    assert summary["valid_records"] == 1
    assert summary["flagged_records"] == 2
    assert summary["duplicate_records"] == 1
    assert summary["out_of_order_records"] == 1
