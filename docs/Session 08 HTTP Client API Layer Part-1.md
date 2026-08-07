# Session 08 – HTTP Client & API Layer (Part 1)

**Date:** 07-Aug-2026

---

# Objective

Build a reusable production-grade HTTP Client instead of calling `requests.get()` throughout the application.

The goal is to centralize:

- HTTP Session
- Retry Strategy
- Connection Pooling
- HTTP Adapter
- Future Headers
- Future Timeouts
- Logging
- Exception Handling

---

# Why not use requests.get() everywhere?

Problems:

- Duplicate timeout configuration
- Duplicate retry configuration
- Duplicate headers
- No connection reuse
- Hard to maintain
- Difficult to extend

Solution:

Create one reusable `HTTPClient`.

---

# Architecture

```
Application
      │
      ▼
LinkedInClient
      │
      ▼
HTTPClient
      │
      ▼
requests.Session
      │
      ▼
HTTPAdapter
      │
      ▼
Retry Strategy
      │
      ▼
Connection Pool
      │
      ▼
Internet
```

---

# requests.Session()

## Why use Session?

Without Session

```
Request
↓

Open TCP Connection

↓

Receive Response

↓

Close TCP Connection
```

Every request creates a new TCP connection.

---

With Session

```
Request

↓

Existing TCP Connection

↓

Receive Response

↓

Keep Connection Alive

↓

Reuse Connection
```

Benefits

- Faster requests
- Connection Pooling
- Lower latency
- Less TCP overhead
- Shared configuration

---

# Retry Strategy

```
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[
        500,
        502,
        503,
        504,
    ],
    allowed_methods=["GET"],
)
```

---

## total

Maximum retry attempts after the original request fails.

Example

```
Original Request

↓

Retry 1

↓

Retry 2

↓

Retry 3

↓

Raise Exception
```

Total Requests = 4

---

## backoff_factor

Controls waiting time between retries.

Purpose

Avoid retry storms and give the server time to recover.

Example

```
Retry 1 → Immediate / negligible delay

Retry 2 → 2 sec

Retry 3 → 4 sec

Retry 4 → 8 sec
```

---

## status_forcelist

Retry only for temporary server failures.

```
500 Internal Server Error

502 Bad Gateway

503 Service Unavailable

504 Gateway Timeout
```

Possible production addition

```
429 Too Many Requests
```

Reason

Respect rate limiting instead of retrying immediately.

---

## allowed_methods

Retry only safe HTTP methods.

Example

```
GET
```

Reason

Retrying POST may create duplicate business operations such as:

- Duplicate Payments
- Duplicate Orders
- Duplicate Emails

POST should only be retried when the API supports idempotency.

---

# HTTPAdapter

Purpose

Acts as the transport layer between `Session` and the network.

Responsibilities

- Applies Retry Strategy
- Manages Connection Pools
- Handles HTTP Transport
- Controls Pool Behaviour

Configuration

```python
adapter = HTTPAdapter(
    max_retries=retry_strategy
)
```

---

# session.mount()

Registers an adapter for matching URL prefixes.

```python
self.session.mount(
    "https://",
    adapter
)

self.session.mount(
    "http://",
    adapter
)
```

Meaning

```
https://

↓

Use Custom Adapter

------------------------

http://

↓

Use Same Adapter
```

Without mount

Retry Strategy is never used.

---

# Connection Pooling

Connection Pool

```
LinkedIn Pool

Connection 1

Connection 2

Connection 3

...
```

Connections are reused instead of recreated.

---

## pool_connections

Maximum number of connection pools.

Think

```
One Pool

↓

One Host
```

Example

```
LinkedIn

GitHub

Greenhouse

Workday
```

Four Hosts

↓

Need four pools.

---

## pool_maxsize

Maximum reusable connections inside one pool.

Example

```
LinkedIn Pool

↓

Connection 1

Connection 2

...

Connection 20
```

---

## pool_block

```
pool_block=True
```

If all pooled connections are busy

```
Wait

↓

Reuse Existing Connection
```

instead of

```
Create Unlimited Temporary Connections
```

Benefits

- Predictable resource usage
- Better concurrency control
- Protect downstream services

---

# Final Configuration

```python
retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[
        500,
        502,
        503,
        504,
    ],
    allowed_methods=["GET"],
)

adapter = HTTPAdapter(
    max_retries=retry_strategy
)

self.session.mount(
    "https://",
    adapter
)

self.session.mount(
    "http://",
    adapter
)
```

---

# Software Engineering Principles

- Single Responsibility Principle (SRP)
- Separation of Concerns
- DRY (Don't Repeat Yourself)
- Reusability
- Single Source of Truth
- Production-first Design

---

# Interview Questions Covered

1. Why use `requests.Session()` instead of `requests.get()`?
2. Why create an `HTTPClient`?
3. Why does `Retry` come from `urllib3`?
4. Why doesn't `Retry` work by itself?
5. What does `HTTPAdapter` do?
6. Why use `session.mount()`?
7. What is exponential backoff?
8. Why retry only temporary failures?
9. Why not retry `404` and `401`?
10. When should `429` be retried?
11. Difference between `pool_connections` and `pool_maxsize`.
12. What does `pool_block=True` do?

---

# Current Project Status

Completed

- HTTP Session
- Retry Strategy
- HTTP Adapter
- Connection Pool Configuration

Pending

- Default Headers
- Timeout Configuration
- Generic GET Method
- Generic POST Method
- Exception Handling
- Logging
- Unit Testing

---

# Key Takeaways

- Always reuse `requests.Session()`.
- `Retry` only defines the retry policy.
- `HTTPAdapter` applies the retry policy.
- `mount()` registers adapters for URL prefixes.
- Connection pooling improves performance by reusing TCP connections.
- Retry only transient failures.
- Use exponential backoff to avoid retry storms.
- Design infrastructure components for reuse and maintainability.