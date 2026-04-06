param(
    [string]$ProjectRoot = "."
)

$ErrorActionPreference = "Stop"

function Ensure-Directory {
    param([string]$Path)
    if (-not (Test-Path -Path $Path)) {
        New-Item -ItemType Directory -Path $Path | Out-Null
        Write-Host "Created directory: $Path"
    }
    else {
        Write-Host "Exists: $Path"
    }
}

function Ensure-File {
    param(
        [string]$Path,
        [string]$Content = ""
    )

    $parent = Split-Path -Parent $Path
    if ($parent -and -not (Test-Path $parent)) {
        New-Item -ItemType Directory -Path $parent | Out-Null
    }

    if (-not (Test-Path -Path $Path)) {
        Set-Content -Path $Path -Value $Content -Encoding UTF8
        Write-Host "Created file: $Path"
    }
    else {
        Write-Host "Skipped existing file: $Path"
    }
}

$root = Resolve-Path $ProjectRoot

$dirs = @(
    ".github",
    ".github/workflows",
    "docs",
    "examples",
    "signalbridge",
    "signalbridge/connectors",
    "signalbridge/normalization",
    "signalbridge/validation",
    "signalbridge/sinks",
    "tests"
)

foreach ($dir in $dirs) {
    Ensure-Directory (Join-Path $root $dir)
}

Ensure-File (Join-Path $root "pyproject.toml") @'
[build-system]
requires = ["setuptools>=68", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "signalbridge-oss"
version = "0.1.0"
description = "Resilient time-series API ingestion, validation, anomaly preservation, and analytics-ready storage."
readme = "README.md"
requires-python = ">=3.11"
license = { text = "Apache-2.0" }
authors = [
  { name = "Yasir" }
]
dependencies = [
  "requests>=2.32.0",
  "pydantic>=2.7.0",
  "PyYAML>=6.0.1",
  "typer>=0.12.3"
]

[project.scripts]
signalbridge = "signalbridge.cli:app"
'@

Ensure-File (Join-Path $root "requirements.txt") @'
requests>=2.32.0
pydantic>=2.7.0
PyYAML>=6.0.1
typer>=0.12.3
pytest>=8.2.0
'@

Ensure-File (Join-Path $root "docker-compose.yml") @'
version: "3.9"
services:
  signalbridge:
    image: python:3.11-slim
    working_dir: /app
    volumes:
      - ./:/app
    command: bash -c "pip install -r requirements.txt && pytest"
'@

Ensure-File (Join-Path $root ".github/workflows/ci.yml") @'
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install --upgrade pip
      - run: pip install -r requirements.txt
      - run: pytest
'@

Ensure-File (Join-Path $root "docs/architecture.md") @'
# Architecture Overview

1. Connector pulls data from upstream API
2. Normalizer standardizes timestamps and structure
3. Validator applies rules and quality flags
4. Router separates raw, validated, and flagged records
5. Sink writes to storage
'@

Ensure-File (Join-Path $root "docs/roadmap.md") @'
# Roadmap

## v0.1.0
- CLI bootstrap
- YAML config loading
- Generic REST polling connector
- Timestamp normalization
- Basic validation rules
- CSV sink
- Initial tests
'@

Ensure-File (Join-Path $root "examples/config.sample.yaml") @'
api:
  base_url: "https://example.com/api/tags"
  method: "GET"
  headers:
    Authorization: "Bearer your-token-here"
  timeout_seconds: 30

polling:
  interval_seconds: 60

validation:
  min_value: -100.0
  max_value: 1000.0
  allow_negative: true

output:
  csv_path: "output/validated.csv"
'@

Ensure-File (Join-Path $root "examples/sample_payload.json") @'
[
  {
    "tag": "pump_vibration_x",
    "timestamp": "2026-04-06T10:30:00Z",
    "value": 2.15
  }
]
'@

Ensure-File (Join-Path $root "signalbridge/__init__.py") ""
Ensure-File (Join-Path $root "signalbridge/cli.py") @'
import typer

app = typer.Typer()

@app.command()
def info():
    typer.echo("SignalBridge OSS")

if __name__ == "__main__":
    app()
'@

Ensure-File (Join-Path $root "signalbridge/config.py") @'
from pathlib import Path
import yaml
from pydantic import BaseModel

class AppConfig(BaseModel):
    api: dict
    polling: dict
    validation: dict
    output: dict

def load_config(path: str | Path) -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig.model_validate(data)
'@

Ensure-File (Join-Path $root "signalbridge/models.py") @'
from pydantic import BaseModel

class TimeSeriesRecord(BaseModel):
    tag: str
    timestamp: str
    value: float
'@

Ensure-File (Join-Path $root "signalbridge/connectors/__init__.py") ""
Ensure-File (Join-Path $root "signalbridge/connectors/rest_poller.py") @'
import requests

def fetch_json(url: str, headers: dict | None = None, timeout_seconds: int = 30):
    response = requests.get(url, headers=headers or {}, timeout=timeout_seconds)
    response.raise_for_status()
    return response.json()
'@

Ensure-File (Join-Path $root "signalbridge/normalization/__init__.py") ""
Ensure-File (Join-Path $root "signalbridge/normalization/timestamps.py") @'
from datetime import datetime, timezone

def normalize_timestamp(value: str) -> str:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).isoformat()
'@

Ensure-File (Join-Path $root "signalbridge/validation/__init__.py") ""
Ensure-File (Join-Path $root "signalbridge/validation/rules.py") @'
def validate_value(value: float, min_value=None, max_value=None, allow_negative=True):
    issues = []

    if not allow_negative and value < 0:
        issues.append("negative values are not allowed")
    if min_value is not None and value < min_value:
        issues.append(f"value below minimum threshold: {min_value}")
    if max_value is not None and value > max_value:
        issues.append(f"value above maximum threshold: {max_value}")

    return (len(issues) == 0, issues)
'@

Ensure-File (Join-Path $root "signalbridge/sinks/__init__.py") ""
Ensure-File (Join-Path $root "signalbridge/sinks/csv_sink.py") @'
import csv
from pathlib import Path

def write_rows(path: str, rows):
    rows = list(rows)
    if not rows:
        return
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
'@

Ensure-File (Join-Path $root "tests/test_config.py") @'
from signalbridge.config import load_config

def test_load_config():
    config = load_config("examples/config.sample.yaml")
    assert "base_url" in config.api
'@

Ensure-File (Join-Path $root "tests/test_timestamps.py") @'
from signalbridge.normalization.timestamps import normalize_timestamp

def test_normalize_timestamp():
    result = normalize_timestamp("2026-04-06T10:30:00Z")
    assert result.startswith("2026-04-06T10:30:00")
'@

Ensure-File (Join-Path $root "tests/test_rules.py") @'
from signalbridge.validation.rules import validate_value

def test_validate_value():
    ok, issues = validate_value(10.0, min_value=0.0, max_value=100.0, allow_negative=True)
    assert ok is True
    assert issues == []
'@

Write-Host ""
Write-Host "Safe scaffold complete."