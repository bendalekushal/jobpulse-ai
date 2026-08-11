class JobAPIClient:

    def __init__(self, http_client, base_url):
        self.http_client = http_client
        self.base_url = base_url

    def fetch_jobs(self, location, page=1, limit=50):
        endpoint = f"{self.base_url}/v1/jobs"

        params = {
            "location": location,
            "page": page,
            "limit": limit,
        }

        return self.http_client.get(
            endpoint,
            params=params,
        )