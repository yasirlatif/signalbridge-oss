from pathlib import Path
import yaml
from pydantic import BaseModel, ConfigDict, Field, model_validator

class ApiConfig(BaseModel):
    base_url: str
    method: str = "GET"
    headers: dict[str, str] = Field(default_factory=dict)
    timeout_seconds: int = 30

    model_config = ConfigDict(str_strip_whitespace=True)


class PollingConfig(BaseModel):
    interval_seconds: int = 60


class ValidationConfig(BaseModel):
    min_value: float
    max_value: float
    allow_negative: bool = True

    @model_validator(mode="after")
    def validate_range(self) -> "ValidationConfig":
        if self.min_value > self.max_value:
            raise ValueError("min_value must be less than or equal to max_value")
        return self


class OutputConfig(BaseModel):
    csv_path: Path


class AppConfig(BaseModel):
    api: ApiConfig
    polling: PollingConfig
    validation: ValidationConfig
    output: OutputConfig


def load_config(path: str | Path) -> AppConfig:
    config_path = Path(path)
    with config_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file) or {}
    return AppConfig.model_validate(data)
