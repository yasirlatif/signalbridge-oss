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
    assert "Total records: 1" in result.stdout
    assert "Valid records: 1" in result.stdout
    assert "Flagged records: 0" in result.stdout


def test_run_demo_filters_flagged_records_and_writes_csv() -> None:
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
    written_rows: list[dict] = []

    def capture_rows(path: str | Path, rows: list[dict]) -> Path:
        written_rows.extend(rows)
        return Path(path)

    with patch("signalbridge.cli.load_config", return_value=config):
        with patch("pathlib.Path.open", return_value=StringIO(json.dumps(payload))):
            with patch("signalbridge.cli.write_rows", side_effect=capture_rows):
                summary = run_demo("payload.json", "config.yaml")

    assert summary["total_records"] == 2
    assert summary["valid_records"] == 1
    assert summary["flagged_records"] == 1
    assert written_rows == [
        {
            "tag": "pump_vibration_x",
            "timestamp": "2026-04-06T10:30:00Z",
            "value": 2.15,
        }
    ]
