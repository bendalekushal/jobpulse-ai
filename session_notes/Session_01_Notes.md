# JobPulse AI Bootcamp

# Session 1 - Python Project Setup & Configuration Fundamentals

> **Goal:** Build a production-style Python project while understanding
> *why* every file, command and line of code exists.

------------------------------------------------------------------------

# 1. Session Summary

During this session we:

-   Created the project structure.
-   Configured the Python virtual environment.
-   Discussed why modern Python projects use the `src` layout.
-   Learned how to execute packages using `python -m`.
-   Understood how `.env` files work.
-   Learned the difference between `load_dotenv()` and `os.getenv()`.
-   Explored Python's `__file__` variable.
-   Learned `pathlib.Path`.
-   Understood `resolve()`.
-   Understood `.parent` vs `.parents`.
-   Fully decoded:

``` python
BASE_DIR = Path(__file__).resolve().parents[2]
```

------------------------------------------------------------------------

# 2. Concepts Explained

## Virtual Environment

Purpose: - Isolates project dependencies. - Prevents version
conflicts. - Makes projects reproducible.

------------------------------------------------------------------------

## src Layout

Example:

    jobpulse-ai/
    │
    ├── .env
    ├── src/
    │   └── jobpulse/
    │       ├── main.py
    │       └── config.py

Benefits: - Cleaner imports - Prevents accidental imports - Industry
standard

------------------------------------------------------------------------

## Running with Modules

``` bash
python -m jobpulse.main
```

Why?

-   Executes package correctly.
-   Relative imports work.
-   Preferred production practice.

------------------------------------------------------------------------

## Environment Variables

    .env
          ↓
    load_dotenv()
          ↓
    Operating System Environment
          ↓
    os.getenv()

`load_dotenv()` loads values.

`os.getenv()` reads values.

------------------------------------------------------------------------

## **file**

-   Automatically created by Python.
-   Contains the path of the currently executing Python file.
-   Not available inside the Python REPL.

------------------------------------------------------------------------

## pathlib.Path

Converts a string path into a Path object.

Useful methods:

-   name
-   suffix
-   parent
-   parents
-   exists()

------------------------------------------------------------------------

## resolve()

Returns:

-   Absolute path
-   Normalized path

Does **not** print anything.

It returns a Path object.

------------------------------------------------------------------------

## parent vs parents

Given:

    jobpulse-ai/
    └── src/
        └── jobpulse/
            └── config.py

  Expression     Result
  -------------- --------------
  parent         src/jobpulse
  parents\[0\]   src/jobpulse
  parents\[1\]   src
  parents\[2\]   jobpulse-ai

------------------------------------------------------------------------

## BASE_DIR

    __file__
    ↓
    Path(__file__)
    ↓
    resolve()
    ↓
    parents[2]
    ↓
    Project Root

------------------------------------------------------------------------

# 3. Commands Used

Create virtual environment

``` bash
python -m venv .venv
```

Activate

``` powershell
.\.venv\Scripts\Activate.ps1
```

Check interpreter

``` bash
python -c "import sys; print(sys.executable)"
```

Run project

``` bash
cd src
python -m jobpulse.main
```

Deactivate

``` bash
deactivate
```

------------------------------------------------------------------------

# 4. Final Production Code

``` python
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

APP_NAME = os.getenv("APP_NAME")
ENVIRONMENT = os.getenv("ENVIRONMENT")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))
```

------------------------------------------------------------------------

# 5. Common Mistakes Encountered

-   Unsaved file before execution.
-   Wrong Python interpreter selected.
-   Expected `__file__` inside REPL.
-   Confused return values with printed values.
-   Imported `pathlab` instead of `pathlib`.
-   Mixed up `.parent` and `.parents`.

------------------------------------------------------------------------

# 6. Debugging Log

  ----------------------------------------------------------------------------
  Problem                 Diagnosis               Fix
  ----------------------- ----------------------- ----------------------------
  Environment variable    `.env` not loaded       `load_dotenv()`
  returned None                                   

  `__file__` NameError    Running in REPL         Execute from Python file

  Module import typo      Wrong module name       `from pathlib import Path`

  BASE_DIR confusion      Investigated            Broke expression into pieces
                          step-by-step            
  ----------------------------------------------------------------------------

------------------------------------------------------------------------

# 7. Interview Questions

1.  Why use a virtual environment?
2.  Why use the `src` layout?
3.  Why execute using `python -m`?
4.  Difference between `load_dotenv()` and `os.getenv()`.
5.  What does `__file__` contain?
6.  Why use `pathlib`?
7.  What does `resolve()` do?
8.  Difference between `.parent` and `.parents`.
9.  Explain `Path(__file__).resolve().parents[2]`.
10. Why doesn't `__file__` exist in the REPL?

------------------------------------------------------------------------

# 8. Key Takeaways

-   Understand, don't memorize.
-   Every configuration path should be explainable.
-   Debug by breaking complex expressions into smaller parts.
-   Functions may **return** values without **printing** them.
-   Production code values readability and maintainability.

------------------------------------------------------------------------

# 9. Homework / Practice

1.  Explain `Path(__file__).resolve().parents[2]` without notes.
2.  Create a small project with a different folder structure and
    determine the correct `parents[]` index.
3.  Experiment with `.name`, `.suffix`, `.stem`, `.parent`, and
    `.parents`.
4.  Remove one variable from `.env` and observe `os.getenv()` behavior.
5.  Answer all interview questions aloud in under 10 minutes.

------------------------------------------------------------------------

**Status:** Session 1 Complete
