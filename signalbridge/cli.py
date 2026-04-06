import json
from pathlib import Path

import typer

from signalbridge.config import load_config
from signalbridge.normalization.timestamps import normalize_timestamp
from signalbridge.sinks.csv_sink import write_rows
from signalbridge.validation.rules import validate_value

app = typer.Typer(help="SignalBridge OSS CLI")


def run_demo(
    payload_path: str | Path,
    config_path: str | Path,
    output_path: str | Path | None = None,
) -> dict[str, int | Path]:
    """Run the local sample flow and return a short execution summary."""
    config = load_config(config_path)
    payload_file = Path(payload_path)

    with payload_file.open("r", encoding="utf-8-sig") as file:
        records = json.load(file)

    valid_rows = []
    flagged_records = 0

    for record in records:
        is_valid, _ = validate_value(
            record["value"],
            min_value=config.validation.min_value,
            max_value=config.validation.max_value,
            allow_negative=config.validation.allow_negative,
        )
        if is_valid:
            valid_rows.append(
                {
                    "tag": record["tag"],
                    "timestamp": normalize_timestamp(record["timestamp"]),
                    "value": record["value"],
                }
            )
        else:
            flagged_records += 1

    destination = Path(output_path) if output_path is not None else config.output.csv_path
    write_rows(destination, valid_rows)

    return {
        "total_records": len(records),
        "valid_records": len(valid_rows),
        "flagged_records": flagged_records,
        "output_path": destination,
    }


@app.command()
def info() -> None:
    """Show a short project description."""
    typer.echo("SignalBridge OSS")
    typer.echo("Resilient time-series API ingestion and validation toolkit.")


@app.command()
def validate(
    config_path: str = typer.Argument(
        "examples/config.sample.yaml",
        help="Path to the YAML configuration file.",
    )
) -> None:
    """Validate a configuration file and show the resolved core settings."""
    config = load_config(config_path)
    typer.echo(f"Configuration is valid: {config_path}")
    typer.echo(f"API URL: {config.api.base_url}")
    typer.echo(f"CSV Output: {config.output.csv_path}")


@app.command("demo-run")
def demo_run(
    payload_path: str = typer.Argument(
        "examples/sample_payload.json",
        help="Path to the sample JSON payload.",
    ),
    config_path: str = typer.Argument(
        "examples/config.sample.yaml",
        help="Path to the YAML configuration file.",
    ),
    output_path: str = typer.Option(
        "",
        "--output",
        help="Optional CSV output path override.",
    ),
) -> None:
    """Run the bundled sample payload through normalization, validation, and CSV output."""
    summary = run_demo(payload_path, config_path, output_path or None)

    typer.echo(f"Demo output: {summary['output_path']}")
    typer.echo(f"Total records: {summary['total_records']}")
    typer.echo(f"Valid records: {summary['valid_records']}")
    typer.echo(f"Flagged records: {summary['flagged_records']}")


if __name__ == "__main__":
    app()
