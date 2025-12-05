from pathlib import Path
import yaml

def load_config(path: str = "configs/config.yaml") -> dict:
    """
    Load YAML config file and return as a Python dictionary.
    """
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with config_path.open("r") as f:
        config = yaml.safe_load(f)

    return config
