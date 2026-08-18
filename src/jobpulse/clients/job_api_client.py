import uuid

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

        response = self.http_client.get(
            endpoint,
            params=params,
        )

        data = self.http_client.parse_json(response, endpoint)

        if "jobs" not in data:
            raise ValueError(
                "Invalid job API response: missing 'jobs'"
            )
        
        return data
        

    def create_job(self, payload, idempotency_key=None):
        # endpoint = f"{self.base_url}/v1/jobs"
        endpoint = f"{self.base_url}/post"
        if idempotency_key is None:
            idempotency_key = str(uuid.uuid4())

        return self.http_client.post(
            endpoint,
            json=payload,
            headers={
                "Idempotency-Key": idempotency_key,
            },
        )