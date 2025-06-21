import yaml
from pathlib import Path


def get_config(path: str = "../config.yaml") -> dict:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {path}")

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
