# JobPulse AI Bootcamp Handbook

## Session 1 (Revised)

### Objectives

-   Understand the JobPulse AI project.
-   Learn the `src` layout.
-   Understand modules, packages and `__init__.py`.

### Key Concepts

-   Module = Python file
-   Package = Directory containing related modules
-   `__init__.py` conventionally marks/initializes a package
-   `src` layout keeps production code separate from project metadata.

### Project Structure

``` text
jobpulse-ai/
├── src/
│   └── jobpulse/
│       ├── __init__.py
│       └── main.py
├── requirements.txt
└── .env
```

### Interview Focus

-   Module vs Package
-   Why `src` layout?
-   Purpose of `__init__.py`

------------------------------------------------------------------------

## Session 2 (Revised)

### Objectives

-   Configuration management
-   Environment variables
-   Production-ready config

### Topics

-   `.env`
-   `load_dotenv()`
-   `os.getenv()`
-   Required vs optional configuration
-   `get_required_env()`
-   `return`
-   `raise`
-   `None`
-   Fail Fast

### Example

``` python
APP_NAME = get_required_env("APP_NAME")
ENVIRONMENT = get_required_env("ENVIRONMENT")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
```

### Key Takeaways

-   Keep secrets out of code.
-   Validate configuration at startup.
-   Stop early when required configuration is missing (Fail Fast).

### Interview Focus

-   `os.getenv()` vs `os.environ`
-   Why use `.env`?
-   Why Fail Fast?
