from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


def get_required_env(var_name: str) -> str:
    value = os.getenv(var_name)

    if value is None:
        raise ValueError(
            f"Required environment variable '{var_name}' is not set."
        )

    return value


# Required configuration
APP_NAME = get_required_env("APP_NAME")
ENVIRONMENT = get_required_env("ENVIRONMENT")


# Optional configuration
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))


