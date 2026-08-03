# Data Engineering Bootcamp
# Session 01 - Python Project Structure, Modules & Packages

**Project:** JobPulse AI

**Objective:**
To understand how professional Python projects are organized before writing any business logic. In this session we learned how Python identifies modules, packages, and the project structure that will be used throughout the JobPulse AI application.

---

# Session Roadmap

In this session we covered:

- Why we are building JobPulse AI
- Why production projects are structured differently from beginner projects
- Python Modules
- Python Packages
- __init__.py
- __name__
- __main__
- Module Execution
- Import System
- src Layout
- Absolute Imports
- Project Folder Structure
- python -m
- Interview Questions

---

# Why JobPulse AI?

Instead of learning isolated Python concepts, we decided to build one complete production-style application.

The goal is not only to learn Python syntax but also to understand how real software projects are designed.

Throughout the bootcamp this project will gradually evolve into a complete Data Engineering application containing:

- Configuration Management
- Logging
- API Integration
- Web Scraping
- Data Cleaning
- SQL
- Pandas
- PySpark
- Airflow
- AWS
- Docker
- Testing
- CI/CD

Every topic will be added naturally into this project.

---

# Why Not Write Everything in One File?

A beginner project usually looks like this:

```python
import requests

print("Start")

# scraping

# cleaning

# database

# logging

# api

print("Done")
```

This becomes impossible to maintain.

Professional projects separate responsibilities.

Instead of one file, we create multiple modules.

---

# Professional Project Structure

```
jobpulse-ai/

│
├── src/
│   │
│   └── jobpulse/
│       │
│       ├── config.py
│       ├── constants.py
│       ├── logger.py
│       ├── main.py
│       └── __init__.py
│
├── tests/
│
├── docs/
│
├── pyproject.toml
│
└── README.md
```

Each file has one responsibility.

---

# What is a Module?

A module is simply a Python file.

Examples:

```
config.py

logger.py

database.py

main.py
```

Every `.py` file is a module.

Reason:

Python imports modules, not folders.

---

# Advantages of Modules

- Better organization
- Reusability
- Easy testing
- Less duplication
- Better maintenance
- Easier debugging

---

# Example

config.py

```python
APP_NAME = "JobPulse AI"

API_TIMEOUT = 30
```

main.py

```python
from jobpulse.config import APP_NAME

print(APP_NAME)
```

Instead of rewriting values everywhere, we reuse them.

---

# What is a Package?

A package is a folder containing one or more Python modules.

Example:

```
jobpulse/

│
├── config.py
├── logger.py
├── constants.py
├── main.py
└── __init__.py
```

Here:

```
jobpulse
```

is a package.

Everything inside it becomes part of the package.

---

# Difference Between Module and Package

| Module | Package |
|---------|----------|
| Python file | Folder |
| Ends with .py | Contains multiple modules |
| Holds code | Organizes modules |

Example:

```
logger.py
```

Module

Example:

```
jobpulse/
```

Package

---

# Why __init__.py?

This file tells Python:

> "Treat this directory as a Python package."

Without it (especially for beginners and many tooling scenarios), the intent of the directory being a package is less explicit.

Usually:

```python
__init__.py
```

contains:

- Nothing
- Version information
- Package exports

Initially ours remains empty.

---

# Your Understanding

You correctly answered:

> "__init__.py indicates that this folder should act as a package."

That understanding is correct.

---

# What is __name__?

Every Python module automatically receives a variable called:

```python
__name__
```

Python creates it automatically.

We never create it ourselves.

---

# Important Realization

Initially asked:

"Does Python create __name__ automatically?"

Your Answer:

> Yes.

Correct.

---

# Value of __name__

Suppose:

```
main.py
```

runs directly.

Then:

```python
__name__
```

becomes:

```
__main__
```

Suppose:

```
config.py
```

is imported.

Then:

```
config
```

Suppose:

```
logger.py
```

is imported.

Then:

```
logger
```

Python sets these values automatically.

---

# Why __main__ Exists

Suppose:

```
main.py
```

contains:

```python
print(__name__)
```

Running:

```
python main.py
```

prints

```
__main__
```

Python uses this to identify the entry point.

---

# The Most Important Condition

```python
if __name__ == "__main__":
    main()
```

Meaning:

Execute this block only when this file is run directly.

Do not execute it when imported.

---

# Practical Example

hello.py

```python
print("Top")

if __name__ == "__main__":
    print("Inside If")

print("Bottom")
```

Running directly:

```
Top

Inside If

Bottom
```

Importing:

```
Top

Bottom
```

Reason:

The condition becomes False.

---

# Your Answers During Practice

Question:

What prints when file runs directly?

Your Answer:

```
Top

Inside If

Bottom
```

Correct.

---

Question:

What prints when imported?

Your Answer:

```
Top

Bottom
```

Correct.

---

# Common Mistake We Corrected

Initially there was confusion between:

```
__main__
```

and

```
"main"
```

You later correctly understood:

```
__main__
```

is a special value automatically created by Python.

It is different from the filename.

---

# Module Execution

Python executes code from top to bottom.

Importing a module also executes top-level code.

Function bodies execute only when called.

---

# Absolute Imports

We used:

```python
from jobpulse.config import APP_NAME
```

Advantages:

- Explicit
- Easy to understand
- Production standard

---

# src Layout

Instead of:

```
project/

config.py
```

we use:

```
src/

jobpulse/

config.py
```

Advantages:

- Cleaner imports
- Prevents accidental imports
- Matches professional Python packaging practices

---

# Running Modules

Instead of:

```
python main.py
```

we learned:

```
python -m jobpulse.main
```

Why?

Python first searches for the package:

```
jobpulse
```

Then:

```
main.py
```

inside it.

This is the preferred approach for package-based projects.

---

# Mistakes Encountered During Session

### Mistake 1

Initially confused module with package.

Correction:

Module = Python file

Package = Folder containing modules.

---

### Mistake 2

Thought Python might create packages based on extensions.

Correction:

Folders become packages through package structure (and `__init__.py` in our project), not because of a `.py` extension on the folder.

---

### Mistake 3

Confused

```
__main__
```

with

```
main
```

Correction:

`__main__` is a special runtime value automatically assigned to the entry-point module.

---

# Interview Questions

## What is a module?

A Python file containing code.

---

## What is a package?

A directory containing Python modules that are organized together.

---

## Why use packages?

To organize related modules, improve maintainability, and enable reusable imports.

---

## What is __name__?

A special variable automatically created by Python for every module.

---

## When does __name__ become "__main__"?

When the file is executed directly.

---

## Why do we use

```python
if __name__ == "__main__":
```

To ensure certain code executes only when the file is run directly, not when it is imported as a module.

---

## Key Takeaways

- Every `.py` file is a module.
- A package groups related modules.
- `__init__.py` marks and initializes a package.
- Python automatically creates `__name__`.
- The entry-point module receives `__name__ == "__main__"`.
- Top-level code executes during import.
- Functions execute only when called.
- Professional projects use the `src` layout.
- `python -m` runs modules within a package correctly.

---

# Homework

1. Explain the difference between a module and a package without referring to notes.
2. Explain why `__name__` exists.
3. Describe what happens when a module is imported versus executed directly.
4. Practice using `python -m` with a simple package.
5. Draw the JobPulse AI project structure from memory.

---

# Project State After Session

```
jobpulse-ai/
│
├── src/
│   └── jobpulse/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       ├── logger.py
│       └── constants.py
│
├── tests/
│
└── README.md
```

---

# Session Summary

This session established the architectural foundation of the entire JobPulse AI project. We learned how Python organizes code into modules and packages, how the `__name__` variable behaves during execution and import, the purpose of `__init__.py`, and why professional projects adopt a `src` layout. These concepts form the basis for everything that follows, including configuration management, packaging, logging, and large-scale application development.