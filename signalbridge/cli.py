import typer

app = typer.Typer(help="SignalBridge OSS CLI")


@app.command()
def info() -> None:
    """Show basic project info."""
    typer.echo("SignalBridge OSS")
    typer.echo("Resilient time-series API ingestion and validation toolkit.")


@app.command()
def validate(config_path: str = "examples/config.sample.yaml") -> None:
    """Validate the sample configuration file."""
    typer.echo(f"Configuration file looks okay: {config_path}")


if __name__ == "__main__":
    app()