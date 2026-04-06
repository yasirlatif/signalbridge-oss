# Quickstart

## Requirements

- Python 3.11+

## Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .[test]
```

## Validate configuration

```bash
signalbridge validate examples/config.sample.yaml
```

## Run the local demo

```bash
signalbridge demo-run examples/sample_payload.json examples/config.sample.yaml --output output/demo.csv
```

## Run tests

```bash
pytest
```

## What the demo does

- reads `examples/sample_payload.json`
- loads validation settings from `examples/config.sample.yaml`
- normalizes timestamps to UTC ISO format
- validates numeric values against configured thresholds
- routes records into validated and flagged outputs
- writes `output/demo.csv` and `output/demo.flagged.csv`
- prints a short record summary
