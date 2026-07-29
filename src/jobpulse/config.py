from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

print(f"BASE_DIR = {BASE_DIR}")

loaded = load_dotenv(BASE_DIR / ".env")
print(f".env loaded = {loaded}")

APP_NAME = os.getenv("APP_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))

print(APP_NAME)