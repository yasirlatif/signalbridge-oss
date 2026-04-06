import json
from pathlib import Path

import typer

from signalbridge.config import load_config
from signalbridge.routing import route_records
from signalbridge.sinks.csv_sink import write_rows

app = typer.Typer(help="SignalBridge OSS CLI")


def _resolve_demo_output_paths(output_path: str | Path | None) -> tuple[Path, Path]:
    """Resolve predictable validated and flagged output paths for the demo flow."""
    validated_path = Path(output_path) if output_path is not None else Path("output/validated.csv")
    if validated_path.suffix == "":
        validated_path = validated_path.with_suffix(".csv")

    if validated_path.stem == "validated":
        flagged_path = validated_path.with_name(f"flagged{validated_path.suffix}")
    else:
        flagged_path = validated_path.with_name(f"{validated_path.stem}.flagged{validated_path.suffix}")

    return validated_path, flagged_path


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

    routed = route_records(
        records,
        min_value=config.validation.min_value,
        max_value=config.validation.max_value,
        allow_negative=config.validation.allow_negative,
    )

    validated_output_path, flagged_output_path = _resolve_demo_output_paths(
        output_path if output_path is not None else config.output.csv_path
    )
    write_rows(validated_output_path, routed.validated_records)
    write_rows(flagged_output_path, routed.flagged_records)

    return {
        "total_records": len(routed.raw_records),
        "raw_records": len(routed.raw_records),
        "valid_records": len(routed.validated_records),
        "flagged_records": len(routed.flagged_records),
        "duplicate_records": routed.duplicate_records,
        "out_of_order_records": routed.out_of_order_records,
        "validated_output_path": validated_output_path,
        "flagged_output_path": flagged_output_path,
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

    typer.echo("Execution summary")
    typer.echo(f"Total records: {summary['total_records']}")
    typer.echo(f"Valid records: {summary['valid_records']}")
    typer.echo(f"Flagged records: {summary['flagged_records']}")
    typer.echo(f"Duplicate records: {summary['duplicate_records']}")
    typer.echo(f"Out-of-order records: {summary['out_of_order_records']}")
    typer.echo(f"Validated output: {summary['validated_output_path']}")
    typer.echo(f"Flagged output: {summary['flagged_output_path']}")


@app.command()
def backfill(
    config_path: str = typer.Argument(
        "examples/config.sample.yaml",
        help="Path to the YAML configuration file.",
    ),
    window: str = typer.Argument(
        ...,
        help="Requested time window, for example 2026-04-01T00:00:00Z/2026-04-02T00:00:00Z.",
    ),
) -> None:
    """Show the planned backfill mode inputs."""
    typer.echo("Backfill mode is planned but not implemented yet.")
    typer.echo(f"Config path: {config_path}")
    typer.echo(f"Requested window: {window}")


if __name__ == "__main__":
    app()
