# Data Engineering Bootcamp
# Session 02 - Environment Variables & Configuration Management

**Project:** JobPulse AI

**Objective:**
In this session we learned why production applications never hardcode configuration values and how Python applications securely manage configuration using environment variables, `.env` files, `python-dotenv`, and a centralized configuration module.

---

# Session Roadmap

Topics covered:

- What is Configuration?
- Why Hardcoding is Dangerous
- Environment Variables
- .env File
- python-dotenv
- load_dotenv()
- os.getenv()
- os.environ
- pathlib
- Path
- __file__
- resolve()
- parents
- Config Module
- Fail Fast Principle
- get_required_env()
- Best Practices

---

# Why Configuration Exists

Every application contains values that may change depending on where it is deployed.

Examples:

- API Keys
- Database URL
- Username
- Password
- Environment
- Timeout
- File Paths

These values are called **Configuration**.

Business logic should never depend on hardcoded configuration.

---

# The Problem with Hardcoding

Example:

```python
API_KEY = "abc123"
```

Problems:

- Sensitive information is exposed.
- Different developers need different values.
- Production and Development configurations become difficult to manage.
- Every change requires modifying source code.

Professional applications never hardcode secrets.

---

# What are Environment Variables?

Environment variables are key-value pairs provided by the operating system.

Example:

```
API_KEY=abc123

ENVIRONMENT=DEV

API_TIMEOUT=30
```

Applications read these values during startup.

---

# Why Use Environment Variables?

Advantages:

- Secure
- Easy to modify
- No code changes required
- Separate configuration from code
- Different values for Development, Testing and Production

---

# .env File

During development, storing environment variables manually inside the operating system is inconvenient.

Instead, we create:

```
.env
```

Example:

```
APP_NAME=JobPulse AI

ENVIRONMENT=DEV

API_TIMEOUT=30
```

This file contains configuration only.

No application logic.

---

# python-dotenv

Python cannot automatically read a `.env` file.

We install:

```bash
pip install python-dotenv
```

This package reads the `.env` file and loads the values into the application's environment.

---

# load_dotenv()

To load environment variables from the `.env` file:

```python
from dotenv import load_dotenv

load_dotenv()
```

After calling `load_dotenv()`, the variables become available through the `os` module.

---

# os.getenv()

Used to safely retrieve environment variables.

Example:

```python
import os

APP_NAME = os.getenv("APP_NAME")
```

If the variable does not exist, `os.getenv()` returns `None` by default.

It can also accept a default value:

```python
timeout = os.getenv("API_TIMEOUT", "30")
```

---

# os.environ

`os.environ` represents the entire environment as a dictionary-like object.

Example:

```python
import os

print(os.environ["APP_NAME"])
```

Difference:

`os.environ`

- Raises `KeyError` if the variable is missing.

`os.getenv()`

- Returns `None` (or a provided default).

For configuration, `os.getenv()` is generally safer.

---

# Centralized Configuration

Instead of reading environment variables everywhere:

❌

```python
import os

api_key = os.getenv("API_KEY")
```

inside every module,

we created one centralized configuration module.

Example:

```
config.py
```

All configuration is loaded once.

Every module imports configuration from this single location.

Advantages:

- No duplicate code
- Easy maintenance
- Single source of truth

---

# pathlib

Python provides the `pathlib` module for working with file system paths.

Instead of manipulating strings:

```python
"C:\\Users\\Desktop\\Project"
```

we use objects.

Example:

```python
from pathlib import Path
```

Advantages:

- Cross-platform
- Cleaner code
- Easier path operations

---

# __file__

Every Python module automatically knows its own location.

Example:

```python
print(__file__)
```

Possible output:

```
C:\Projects\jobpulse\config.py
```

---

# resolve()

Converts relative paths into absolute paths.

Example:

```python
Path(__file__).resolve()
```

Output:

```
C:\Projects\jobpulse\src\jobpulse\config.py
```

---

# parents

Suppose:

```
C:\Projects\jobpulse\src\jobpulse\config.py
```

Then:

```python
Path(__file__).resolve().parents[0]
```

returns

```
jobpulse
```

parents[1]

returns

```
src
```

parents[2]

returns

```
jobpulse-ai
```

We used this to locate the project root.

---

# Loading .env Correctly

The configuration module determines the project root using `pathlib`.

Then:

```python
load_dotenv(...)
```

loads the `.env` file from that location.

This avoids issues caused by running the application from different directories.

---

# Fail Fast Principle

Suppose:

```
API_KEY
```

is missing.

Should the application continue?

No.

Professional applications should stop immediately.

This principle is called:

**Fail Fast**

Fail early instead of producing unexpected behavior later.

---

# get_required_env()

Instead of repeatedly writing:

```python
os.getenv(...)
```

we designed a helper function.

Purpose:

- Read environment variables.
- Validate required values.
- Raise an error immediately if a required variable is missing.

Advantages:

- Cleaner code.
- Reusable.
- Consistent validation.

---

# Configuration Flow

```
Developer

        │

        ▼

Creates .env

        │

        ▼

load_dotenv()

        │

        ▼

Environment Variables

        │

        ▼

config.py

        │

        ▼

Other Modules
```

Configuration is loaded once.

Every module imports from `config.py`.

---

# Best Practices

✅ Keep secrets in `.env`

✅ Never hardcode passwords

✅ Load configuration once

✅ Centralize configuration

✅ Fail Fast

✅ Validate required variables

---

# Mistakes Encountered During Session

### Mistake 1

Initially there was confusion between:

Environment Variables

and

`.env`

Correction:

`.env` is only a development convenience.

The real configuration exists as environment variables.

---

### Mistake 2

Confusion between:

`os.environ`

and

`os.getenv()`

Correction:

`os.environ`

Raises an exception when missing.

`os.getenv()`

Returns `None` or a default value.

---

### Mistake 3

Initially `pathlib` seemed unnecessary.

Correction:

It provides a cross-platform and robust way to work with file paths without manually manipulating strings.

---

### Mistake 4

There was uncertainty about why we use `Path(__file__).resolve()`.

Correction:

It allows the application to reliably locate the project root and the `.env` file regardless of the current working directory.

---

# Interview Questions

## What is Configuration?

Configuration consists of values that control how an application behaves without changing its source code.

---

## Why should secrets never be hardcoded?

Hardcoding exposes sensitive information, makes deployments difficult, and requires code changes whenever configuration changes.

---

## What is an Environment Variable?

An operating system level key-value pair that applications use to obtain configuration.

---

## Why do we use `.env`?

It provides a convenient way to define environment variables during development.

---

## Difference between `os.getenv()` and `os.environ`?

`os.getenv()`

Returns `None` or a default value if the variable is missing.

`os.environ`

Raises a `KeyError` when a required variable is absent.

---

## Why use `pathlib`?

To work with filesystem paths in a platform-independent and object-oriented way.

---

## What is the Fail Fast principle?

Validate critical configuration at startup and stop the application immediately if required values are missing.

---

# Key Takeaways

- Configuration should never be hardcoded.
- `.env` files simplify local development.
- `python-dotenv` loads `.env` values into the environment.
- `os.getenv()` safely retrieves environment variables.
- `config.py` centralizes configuration.
- `pathlib` simplifies path handling.
- `__file__` identifies the current module's location.
- `resolve()` converts paths to absolute form.
- `parents` helps navigate the project directory structure.
- Fail Fast prevents hidden configuration issues.

---

# Homework

1. Explain the difference between `.env` and environment variables.
2. Describe the difference between `os.getenv()` and `os.environ`.
3. Explain why we centralize configuration in `config.py`.
4. Practice using `Path(__file__).resolve().parents`.
5. Explain the Fail Fast principle without referring to notes.

---

# Project State After Session

```
jobpulse-ai/
│
├── .env
│
├── src/
│   └── jobpulse/
│       ├── config.py
│       ├── constants.py
│       ├── logger.py
│       ├── main.py
│       └── __init__.py
│
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

# Session Summary

This session established the configuration architecture for JobPulse AI. We learned how to separate configuration from business logic using environment variables and `.env` files, how to load them with `python-dotenv`, and why professional applications centralize configuration inside `config.py`. We also introduced `pathlib` for reliable path handling and adopted the **Fail Fast** principle to ensure that missing configuration is detected immediately during application startup.