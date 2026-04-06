# SignalBridge OSS

**Resilient time-series API ingestion, validation, anomaly preservation, and analytics-ready storage.**

SignalBridge OSS is an open-source toolkit for engineering teams that need to ingest operational or industrial time-series data from imperfect upstream APIs and store it in a form that is usable for analytics, profiling, and machine learning.

Many real-world APIs return inconsistent timestamps, partial payloads, missing intervals, duplicate records, or values that fall outside expected operating ranges. SignalBridge OSS is designed to handle those realities without silently dropping important data.

## Why this project exists

Most ingestion examples assume that upstream systems behave cleanly and consistently. In practice, engineering teams often face:

- out-of-order timestamps
- irregular polling intervals
- duplicate records
- incomplete or partially invalid responses
- values outside expected thresholds
- the need to preserve anomalies for audit, debugging, and model training

SignalBridge OSS treats these as first-class engineering concerns.

## Core goals

- Poll time-series data from REST-style APIs
- Normalize and validate incoming records
- Preserve anomalous data instead of discarding it
- Separate raw, validated, and flagged records
- Store outputs in analytics-ready sinks
- Provide a reusable foundation for downstream profiling and ML workflows

## Current scope

The current repository provides a small but working local flow:

- load YAML configuration
- fetch JSON from REST endpoints
- normalize timestamps to UTC ISO format
- validate numeric values with simple rule checks
- write accepted records to CSV
- run a local demo without external services

## Quickstart

### Requirements

- Python 3.11+

### Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .[test]
```

### Run the local demo

```bash
signalbridge validate
signalbridge demo-run
pytest
```

The demo command reads the sample payload in `examples/sample_payload.json`, applies validation settings from `examples/config.sample.yaml`, and writes valid records to the configured CSV path.

## Minimal architecture overview

SignalBridge OSS is organized as a small ingestion pipeline with explicit stages:

- `signalbridge/connectors/`: data acquisition from upstream systems
- `signalbridge/normalization/`: timestamp and record-shape cleanup
- `signalbridge/validation/`: rule checks and quality decisions
- `signalbridge/sinks/`: output adapters such as CSV
- `signalbridge/cli.py`: local operational entry points for validation and demo execution

In the current flow, a payload is read from a source, timestamps are normalized, values are checked against validation rules, accepted rows are written to a sink, and invalid records are counted rather than silently ignored.

## Record states

SignalBridge OSS treats record state as an explicit part of the pipeline:

- Raw records: input data exactly as received from the source system before normalization or rule evaluation.
- Validated records: records that passed normalization and configured validation checks and are safe to write to downstream sinks.
- Flagged records: records that were parsed successfully but failed one or more checks and should remain visible for audit, debugging, or future review.

This separation is important for operational transparency. A data pipeline should not make anomalous inputs disappear without leaving a trace.

## Example command sequence

```bash
signalbridge validate examples/config.sample.yaml
signalbridge demo-run examples/sample_payload.json examples/config.sample.yaml --output output/demo.csv
type output\demo.csv
```

## Planned features

### Connectors
- Generic REST polling connector
- Configurable polling intervals
- API key / bearer token authentication
- Retry and backoff support

### Normalization
- Timestamp normalization
- Duplicate detection
- Out-of-order detection
- Missing interval detection

### Validation
- Rule-based min/max checks
- Warning / alarm / trip style thresholds
- Support for negative values where valid
- Quality flags instead of silent drops

### Outputs
- Raw stream output
- Validated stream output
- Anomaly / flagged output
- CSV sink
- Future support for time-series databases

## Architecture principles

- Preserve data lineage
- Prefer explicit flags over destructive filtering
- Keep configuration simple and auditable
- Make imperfect upstream behavior visible
- Support analytics and ML readiness from the start

## Quickstart

Coming in the first release.

## Roadmap

See `docs/roadmap.md`.

## Contributing

Contributions, issue reports, and design feedback are welcome. Contribution guidelines will be added as the project matures.

## License

Apache-2.0
