import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class HTTPClient:
    """
    Reusable HTTP client for managing 
    sessions, retry, headers and timeouts.
    """


    def __init__(self):
        self.session = requests.Session()
        self._configure_session()

    def _configure_session(self):
        """
        Configure the request session with production 
        settings such as retries, headers and adapters.
        """
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
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