from typer.testing import CliRunner

from signalbridge.cli import app


runner = CliRunner()


def test_validate_command_loads_sample_config() -> None:
    result = runner.invoke(app, ["validate"])

    assert result.exit_code == 0
    assert "Configuration is valid" in result.stdout
    assert "examples/config.sample.yaml" in result.stdout
