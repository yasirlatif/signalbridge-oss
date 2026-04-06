import typer

from signalbridge.config import load_config

app = typer.Typer(help="SignalBridge OSS CLI")


@app.command()
def info() -> None:
    """Show basic project info."""
    typer.echo("SignalBridge OSS")
    typer.echo("Resilient time-series API ingestion and validation toolkit.")


@app.command()
def validate(
    config_path: str = typer.Argument(
        "examples/config.sample.yaml",
        help="Path to the YAML configuration file.",
    )
) -> None:
    """Validate a YAML configuration file."""
    config = load_config(config_path)
    typer.echo(f"Configuration is valid: {config_path}")
    typer.echo(f"API URL: {config.api.base_url}")
    typer.echo(f"CSV Output: {config.output.csv_path}")


if __name__ == "__main__":
    app()