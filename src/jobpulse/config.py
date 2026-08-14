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
JOB_API_BASE_URL = get_required_env("JOB_API_BASE_URL")
JOB_API_KEY = get_required_env("JOB_API_KEY")

# Optional configuration
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
CONNECT_TIMEOUT = int(os.getenv("CONNECT_TIMEOUT", "3"))
READ_TIMEOUT = int(os.getenv("READ_TIMEOUT", "10"))

