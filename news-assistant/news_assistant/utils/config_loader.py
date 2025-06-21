import yaml
from pathlib import Path


def get_config() -> dict:
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent.parent
    config_path = parent_dir / "config.yaml"
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with config_path.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
