# JobPulse AI Bootcamp — Session 9 Notes
## HTTP Client & API Layer

**Goal:** Build a production-oriented HTTP abstraction and API client using dependency injection, centralized configuration, retries, connection pooling, timeouts, and structured exception propagation.

---

## 1. Architecture

We established three clear responsibility boundaries:

```text
main.py
   |
   | creates and wires dependencies
   v
JobAPIClient
   |
   | API-specific contract
   v
HTTPClient
   |
   | HTTP transport mechanics
   v
External API
```

### main.py
Responsible for application composition/wiring:
- Load configuration.
- Create `HTTPClient`.
- Create `JobAPIClient`.
- Inject dependencies.

### JobAPIClient
Responsible for the specific Job API:
- Base URL.
- API endpoints.
- API-specific parameters such as `location`, `page`, and `limit`.
- Delegates actual HTTP operations to `HTTPClient`.

### HTTPClient
Responsible for generic HTTP mechanics:
- `requests.Session`.
- Connection pooling.
- `HTTPAdapter`.
- Retry strategy.
- Connect/read timeouts.
- Generic HTTP request execution.
- HTTP-level exception handling/logging.

---

## 2. Dependency Injection

We chose to pass an existing `HTTPClient` into `JobAPIClient` rather than creating one internally.

```python
class JobAPIClient:

    def __init__(self, http_client, base_url):
        self.http_client = http_client
        self.base_url = base_url
```

Why:
- Avoid duplicate `requests.Session` objects.
- Reuse connection pools.
- Centralize HTTP configuration.
- Improve maintainability.
- Make unit testing easier.
- Follow dependency injection principles.

We explicitly avoided:

```python
class JobAPIClient:

    def __init__(self):
        self.http_client = HTTPClient()
```

because that would create infrastructure dependencies internally.

---

## 3. Centralized Configuration

We extended the existing configuration system instead of creating another configuration mechanism.

Required:

```python
JOB_API_BASE_URL = get_required_env("JOB_API_BASE_URL")
```

Optional:

```python
CONNECT_TIMEOUT = int(os.getenv("CONNECT_TIMEOUT", "3"))
READ_TIMEOUT = int(os.getenv("READ_TIMEOUT", "10"))
```

Example `.env`:

```text
JOB_API_BASE_URL=https://api.example.com
CONNECT_TIMEOUT=3
READ_TIMEOUT=10
```

The important principle:

```text
.env
  ↓
config.py
  ↓
main.py
  ↓
JobAPIClient / HTTPClient
```

Configuration is not hardcoded inside the API client.

---

## 4. Separate Connect and Read Timeouts

We rejected one generic timeout because connection establishment and waiting for server data are different operations.

We chose:

```text
Connect timeout = 3 seconds
Read timeout    = 10 seconds
```

Requests accepts this as:

```python
timeout=(3, 10)
```

The mapping is:

```text
First value  → Connect Timeout
Second value → Read Timeout
```

A read timeout is not necessarily a total response-download limit. If a server continuously sends data, individual reads can continue even when the total operation takes longer.

---

## 5. HTTP Session

We use one reusable `requests.Session()`:

```python
self.session = requests.Session()
```

Benefits:
- Connection reuse.
- Connection pooling.
- Reduced TCP/TLS setup overhead.
- Centralized session configuration.

---

## 6. Retry Strategy

Current retry configuration:

```python
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    allowed_methods=["GET"]
)
```

We intentionally restricted automatic retries to `GET`.

Reason:
- Not every HTTP method is safely retryable.
- GET is generally idempotent.
- Retrying POST can potentially create duplicate operations unless the API supports idempotency.

### Backoff

We use:

```python
backoff_factor=1
```

because immediate retries can repeatedly hit an overloaded service.

---

## 7. HTTPAdapter and Connection Pool

Current adapter:

```python
adapter = HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20,
    max_retries=retry_strategy,
    pool_block=True
)
```

The adapter is mounted on both schemes:

```python
self.session.mount("https://", adapter)
self.session.mount("http://", adapter)
```

`mount()` associates the adapter with URLs matching the specified prefix.

We discussed:
- `pool_connections`: number of connection pools maintained by the adapter.
- `pool_maxsize`: maximum connections retained/available per pool.
- `pool_block=True`: callers wait for a connection when the pool is exhausted instead of immediately creating behavior outside the configured pool limit.

---

## 8. HTTPClient GET Method

The current conceptual implementation is:

```python
def get(self, url, params=None):
    response = self.session.get(
        url,
        params=params,
        timeout=(
            self.connect_timeout,
            self.read_timeout,
        ),
    )

    response.raise_for_status()

    return response
```

Important separation:

`JobAPIClient` knows:

```text
/v1/jobs
location
page
limit
```

`HTTPClient` knows:

```text
URL
params dictionary
timeout
retry
session
adapter
connection pool
```

`HTTPClient` does not need to understand what `location`, `page`, or `limit` mean.

---

## 9. Query Parameters

We use:

```python
params={
    "location": "Pune",
    "page": 1,
    "limit": 10,
}
```

instead of manually constructing:

```text
...?location=Pune&page=1&limit=10
```

Benefits:
- Keeps query data separate from URL construction.
- Lets `requests` perform URL encoding.
- Avoids manual query-string errors.
- Provides a clean generic interface.

---

## 10. HTTP Error Handling

`requests` does not automatically raise an exception just because the server returns a 4xx/5xx response.

For example:

```python
response = self.session.get(url)
```

can return:

```text
Response
└── status_code = 404
```

We explicitly call:

```python
response.raise_for_status()
```

to convert unsuccessful HTTP responses into `HTTPError`.

Important distinction:

```text
Network-level failure
    ├── ConnectTimeout
    ├── ReadTimeout
    └── ConnectionError
          ↓
       exception

HTTP response received
    ├── 200
    ├── 404
    └── 500
          ↓
    raise_for_status()
          ↓
      HTTPError
```

---

## 11. Exception Propagation

We decided not to silently catch exceptions and return `None`.

Bad:

```python
except requests.RequestException:
    return None
```

Why this is bad:
- Hides the actual failure.
- Makes debugging difficult.
- Prevents higher-level application logic from deciding how to handle the failure.

Instead:

```python
except requests.exceptions.ConnectTimeout:
    logger.error(...)
    raise
```

The lower-level HTTP layer logs technical HTTP context and re-raises the exception.

### Logging responsibility

`HTTPClient` should log HTTP/transport details.

`JobAPIClient` may add business context only when it provides additional useful information.

Avoid logging the same failure multiple times without adding context.

---

## 12. Centralized Logging

Individual modules obtain a logger:

```python
import logging

logger = logging.getLogger(__name__)
```

They do **not** call `configure_logging()` themselves.

`main.py` configures application logging:

```python
configure_logging()
```

This maintains one centralized logging configuration.

---

## 13. Debugging Lessons

We encountered and fixed several issues:

### Package naming
Changed:

```text
Clients
```

to:

```text
clients
```

to match:

```python
from jobpulse.clients.http_client import HTTPClient
```

and follow standard Python package naming.

### Constructor dependency
Fixed:

```python
def __init__(self, http_client):
    self.base_url = base_url
```

to:

```python
def __init__(self, http_client, base_url):
    self.http_client = http_client
    self.base_url = base_url
```

because `base_url` must be injected.

### Method indentation
`fetch_jobs()` was accidentally nested inside `__init__()`.

Correct structure:

```python
class JobAPIClient:

    def __init__(...):
        ...

    def fetch_jobs(...):
        ...
```

### Scope of parameters
`location`, `page`, and `limit` must be parameters of `fetch_jobs()` and the code using them must remain inside that method.

### Unsaved main.py
We also discovered that the terminal was executing an older saved version of `main.py`. Saving the file with `Ctrl+S` fixed the mismatch.

This is an important practical debugging lesson: always compare the traceback with the code actually saved to disk.

---

## 14. Successful HTTPClient Integration Test

We tested the HTTP infrastructure using:

```text
https://httpbin.io/get
```

with:

```python
response = http_client.get(
    "https://httpbin.io/get",
    params={
        "location": "Pune",
        "page": 1,
        "limit": 10,
    },
)
```

Result:

```text
Response status: 200
```

The response echoed:

```text
location = Pune
page = 1
limit = 10
```

This successfully validated:

- HTTPClient construction.
- Session creation.
- GET request.
- Query parameter handling.
- Connect/read timeout configuration.
- HTTPAdapter integration.
- Connection pool configuration.
- Successful response handling.
- `response.json()` processing.

We also observed:

```text
Connection: keep-alive
```

which is consistent with using a reusable `requests.Session`.

---

## 15. Retry Test Observation

An earlier test accidentally called:

```text
https://api.example.com/v1/jobs
```

which is only a placeholder domain.

The output showed:

```text
Retry(total=2)
Retry(total=1)
Retry(total=0)
```

followed by:

```text
NameResolutionError
MaxRetryError
requests.exceptions.ConnectionError
```

This proved that the configured retry mechanism was actually being exercised.

The failure was DNS/name resolution, not a read timeout or connect timeout.

---

## 16. Current JobAPIClient

Current design:

```python
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
```

This has not yet been tested successfully against a compatible Job API endpoint.

---

## 17. Remaining Work

Next session should continue with controlled failure testing.

Priority order:

1. Test HTTP 404 and verify `response.raise_for_status()`.
2. Verify `HTTPError` logging and propagation.
3. Test retry behavior for 500/502/503/504.
4. Test `ReadTimeout` using a controlled delayed endpoint.
5. Test connection-related exceptions where practical.
6. Add/improve centralized HTTP request logging.
7. Add centralized/default headers.
8. Connect `JobAPIClient` to the test HTTP endpoint.
9. Test the complete chain:

```text
main.py
   ↓
JobAPIClient
   ↓
HTTPClient
   ↓
requests.Session
   ↓
External API
```

10. Add unit tests.
11. Clean up temporary httpbin testing code.
12. Replace placeholder `JOB_API_BASE_URL` before production integration.

---

## Interview Takeaways

Be able to explain these clearly:

### Why use a shared Session?

A shared `requests.Session` enables connection reuse and connection pooling and avoids repeatedly creating HTTP infrastructure.

### Why use an HTTPClient abstraction?

To centralize transport concerns such as:
- Session management.
- Retry.
- Timeout.
- Connection pooling.
- Headers.
- HTTP exception handling.

### Why separate JobAPIClient?

It isolates API-specific knowledge such as endpoints, query parameters, payloads, and business/API contracts from generic HTTP mechanics.

### Why dependency injection?

It avoids tightly coupling `JobAPIClient` to a concrete HTTP implementation, improves testability, and allows the same configured HTTP client to be reused.

### Why separate connect/read timeout?

Connection establishment and waiting for response data are different phases and can have different operational characteristics.

### Why not silently return None?

Because doing so hides failures and prevents higher-level components from making informed decisions.

### Why retry only selected HTTP methods?

Retries can duplicate side effects. GET is generally idempotent, while POST may not be unless an idempotency mechanism is available.

---

## Session Status

**Session 9 — HTTP Client & API Layer: In Progress**

Completed today:
- HTTP client abstraction.
- Shared Session.
- Retry strategy.
- HTTPAdapter.
- Connection pools.
- Dependency injection.
- Base URL configuration.
- Separate connect/read timeouts.
- GET method.
- Query parameters.
- Exception propagation.
- First successful real HTTP integration test.
- Debugging and package structure fixes.

Next session starts with:
**HTTPError and controlled failure testing.**
