import typer

from signalbridge.config import load_config


app = typer.Typer(help="SignalBridge OSS CLI")


@app.command()
def info() -> None:
    """Show basic project info."""
    typer.echo("SignalBridge OSS")
    typer.echo("Resilient time-series API ingestion and validation toolkit.")


@app.command()
def validate(config_path: str = "examples/config.sample.yaml") -> None:
    """Validate a configuration file."""
    load_config(config_path)
    typer.echo(f"Configuration is valid: {config_path}")


if __name__ == "__main__":
    app()
