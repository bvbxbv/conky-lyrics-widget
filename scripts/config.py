try:
    import tomllib
except ModuleNotFoundError:  # for python 3.10.12
    import tomli as tomllib

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

with open(BASE_DIR / "configs" / "settings.toml", "rb") as f:
    settings = tomllib.load(f)

with open(BASE_DIR / "configs" / "secret.toml", "rb") as f:
    secrets = tomllib.load(f)
