"""
Application entry point.
"""

from jobpulse.config import (
    APP_NAME,
    ENVIRONMENT,
    API_TIMEOUT,
)


def main():
    print("=" * 50)
    print(f"Application : {APP_NAME}")
    print(f"Environment : {ENVIRONMENT}")
    print(f"API Timeout : {API_TIMEOUT} seconds")
    print("=" * 50)


if __name__ == "__main__":
    main()