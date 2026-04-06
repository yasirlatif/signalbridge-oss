# Contributing

## Scope

SignalBridge OSS is currently a small Python project focused on ingestion, normalization, validation, and local sink behavior. Contributions should keep that scope clear and avoid introducing unnecessary framework or deployment complexity.

## Before opening a change

- Check existing issues or open one for larger changes.
- Prefer small, reviewable pull requests.
- Keep behavior explicit and easy to test.

## Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -e .[test]
pytest
```

## Coding guidance

- Target Python 3.11+.
- Keep modules small and production-minded.
- Prefer clear functions over abstraction-heavy designs.
- Preserve raw and flagged data paths where relevant.
- Update or add focused tests with code changes.

## Pull requests

Include:

- a short problem statement
- the change made
- any user-facing or CLI impact
- test coverage notes

If a change affects configuration, CLI behavior, or pipeline semantics, update the relevant documentation.
