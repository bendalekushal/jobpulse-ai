import logging
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

class AuthenticationError(Exception):
    """Raised when API authentication fails."""
    pass


class AuthorizationError(Exception):
    """Raised when the authenticated client is not allowed to perform an operation."""
    pass

class HTTPClient:
    """
    Reusable HTTP client for managing 
    sessions, retry, headers and timeouts.
    """


    def __init__(self, connect_timeout, read_timeout, api_key):
        self.session = requests.Session()
        self.connect_timeout = connect_timeout
        self.read_timeout = read_timeout
        self.api_key = api_key
        self._configure_session()

        self.default_headers = {
            "Accept": "application/json",
            "User-Agent": "JobPulse/1.0",
            "X-API-Key": self.api_key,
        }

    def _configure_session(self):
        """
        Configure the request session with production 
        settings such as retries, headers and adapters.
        """
        retry_strategy = Retry(
            total=3,
            connect=3,
            read=0,
            status=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=retry_strategy,
            pool_block=True
        )

        self.session.mount(
            "https://",
            adapter
        )

        self.session.mount(
                "http://",
                adapter
        )

    def _validate_response(self, response, url):
        if response.status_code == 401:
            raise AuthenticationError(
                f"Authentication failed for {url}"
            )
        if response.status_code == 403:
            raise AuthorizationError(
                f"Authorization failed for {url}"
            )

        response.raise_for_status()

    def parse_json(self, response, url):
        try:
            return response.json()

        except requests.exceptions.JSONDecodeError:
            logger.error(
                "Invalid JSON response from %s",
                url,
                exc_info=True,
            )
            raise

    def get(self, url, params=None, headers=None):
        try:

            request_headers = self.default_headers.copy()
            if headers:
                request_headers.update(headers)

            response = self.session.get(
                url,
                params=params,
                headers=request_headers,
                timeout=(
                    self.connect_timeout,
                    self.read_timeout,
                ),
            )


            self._validate_response(response, url)

            return response

        except requests.exceptions.ConnectTimeout:
            logger.error(
                "Connection timeout while calling %s",
                url,
                exc_info=True,
            )
            raise

        except requests.exceptions.ReadTimeout:
            logger.error(
                "Read timeout while calling %s",
                url,
                exc_info=True,
            )
            raise

        except requests.exceptions.ConnectionError:
            logger.error(
                "Connection error while calling %s",
                url,
                exc_info=True,
            )
            raise

        except AuthenticationError:
            logger.error(
                "Authentication error while calling %s",
                url,
                exc_info=True,
            )
            raise

        except AuthorizationError:
            logger.error(
                "Authorization error while calling %s",
                url,
                exc_info=True,
            )
            raise

        except requests.exceptions.HTTPError:
            logger.error(
                "HTTP error while calling %s",
                url,
                exc_info=True,
            )
            raise

    def post(self, url, params=None, json=None, headers=None):
        try:

            request_headers = self.default_headers.copy()

            if headers:
                request_headers.update(headers)
            # logger.info(
            #     "Request header names: %s",
            #     list(request_headers.keys()),
            # )

            response = self.session.post(
                url,
                params=params,
                json=json,
                headers=request_headers,
                timeout=(
                    self.connect_timeout,
                    self.read_timeout,
                ),
            )

            self._validate_response(response, url)

            return response

        except requests.exceptions.ConnectTimeout:
            logger.error(
                "Connection timeout while calling %s",
                url,
                exc_info=True,
            )
            raise

        except requests.exceptions.ReadTimeout:
            logger.error(
                "Read timeout while calling %s",
                url,
                exc_info=True,
            )
            raise

        except requests.exceptions.ConnectionError:
            logger.error(
                "Connection error while calling %s",
                url,
                exc_info=True,
            )
            raise

        except AuthenticationError:
            logger.error(
                "Authentication error while calling %s",
                url,
                exc_info=True,
            )
            raise

        except AuthorizationError:
            logger.error(
                "Authorization error while calling %s",
                url,
                exc_info=True,
            )
            raise

        except requests.exceptions.HTTPError:
            logger.error(
                "HTTP error while calling %s",
                url,
                exc_info=True,
            )
            raise
