from pathlib import Path
import yaml
from pydantic import BaseModel

class AppConfig(BaseModel):
    api: dict
    polling: dict
    validation: dict
    output: dict

def load_config(path: str | Path) -> AppConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return AppConfig.model_validate(data)
