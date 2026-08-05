"""
Application entry point.
"""
import logging

from jobpulse.logger import configure_logging
from jobpulse.config import (
    APP_NAME,
    ENVIRONMENT,
    API_TIMEOUT,
)

configure_logging()

logger = logging.getLogger(__name__)

def main():

    logger.info("Application Started")
    
    print("=" * 50)
    print(f"Application : {APP_NAME}")
    print(f"Environment : {ENVIRONMENT}")
    print(f"API Timeout : {API_TIMEOUT} seconds")
    print("=" * 50)


if __name__ == "__main__":
    main()

for i in range(100):
    logger.info(f"Log Message {i}")

