"""
Application entry point.
"""
import logging
# from urllib import response
from jobpulse.clients.http_client import HTTPClient
from jobpulse.clients.job_api_client import JobAPIClient
from jobpulse.logger import configure_logging
from jobpulse.config import (
    APP_NAME,
    ENVIRONMENT,
    CONNECT_TIMEOUT,
    READ_TIMEOUT,
    JOB_API_BASE_URL,
)

configure_logging()

logger = logging.getLogger(__name__)

def main():

    logger.info("Application Started")

    http_client = HTTPClient(
        connect_timeout=CONNECT_TIMEOUT,
        read_timeout=READ_TIMEOUT,
    )

    job_client = JobAPIClient(
        http_client=http_client,
        base_url=JOB_API_BASE_URL,
    )

    # Temporary HTTPClient integration test
    response = http_client.get(
        "http://localhost:8000",
        # params={
        #     "location": "Pune",
        #     "page": 1,
        #     "limit": 10,
        # },
    )

    logger.info(
        "Response status: %s",
        response.status_code,
    )

    logger.info(
        "Response body: %s",
        response.json(),
    )


    print("=" * 50)
    print(f"Application : {APP_NAME}")
    print(f"Environment : {ENVIRONMENT}")
    print(f"Connect Timeout : {CONNECT_TIMEOUT} seconds")
    print(f"Read Timeout : {READ_TIMEOUT} seconds")
    print(f"job API Base URL : {JOB_API_BASE_URL}")
    print("=" * 50)

    # response = job_client.fetch_jobs(
    #     location="Pune",
    #     page=1,
    #     limit=10,
    # )

    # logger.info(
    #     "Received response with status code: %s",
    #     response.status_code,
    # )

if __name__ == "__main__":
    main()



