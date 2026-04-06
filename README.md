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
