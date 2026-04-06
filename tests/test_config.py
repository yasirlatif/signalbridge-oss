from signalbridge.config import load_config

from io import StringIO
from unittest.mock import patch

import pytest
from pydantic import ValidationError


def test_load_config() -> None:
    config = load_config("examples/config.sample.yaml")

    assert config.api.base_url == "https://example.com/api/tags"
    assert config.api.method == "GET"
    assert config.polling.interval_seconds == 60
    assert config.validation.max_value == 1000.0
    assert config.output.csv_path.name == "validated.csv"


def test_load_config_rejects_invalid_validation_range() -> None:
    invalid_config = "\n".join(
        [
            "api:",
            '  base_url: "https://example.com/api/tags"',
            "polling:",
            "  interval_seconds: 60",
            "validation:",
            "  min_value: 10",
            "  max_value: 1",
            "output:",
            '  csv_path: "output/validated.csv"',
        ]
    )

    with patch("pathlib.Path.open", return_value=StringIO(invalid_config)):
        with pytest.raises(ValidationError):
            load_config("ignored.yaml")
