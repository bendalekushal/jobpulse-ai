# Data Engineering Bootcamp
# Session 04 - Modern Python Packaging & pyproject.toml

**Project:** JobPulse AI

**Objective:**

In this session we learned how modern Python projects describe themselves using `pyproject.toml`, how packaging tools build projects, the purpose of the build system, and the difference between build-time and runtime dependencies.

---

# Session Roadmap

Topics Covered

- Why Python Packaging Exists
- Introduction to pyproject.toml
- Build System
- Build Backend
- setuptools
- Build Dependencies
- Runtime Dependencies
- Project Metadata
- Package Identity
- Installation Lifecycle
- Build Phase vs Runtime Phase

---

# Recap

Previous session we learned:

```
pip install -e .
```

Question:

How does pip know:

- Project Name?
- Dependencies?
- Python Version?
- Build Tool?
- Source Package?

Answer:

```
pyproject.toml
```

---

# What is pyproject.toml?

`pyproject.toml` is the standard configuration file used by modern Python projects.

It tells packaging tools how to build and package the project.

Think of it as the **identity card** of the project.

It contains information such as:

- Project Name
- Version
- Description
- Dependencies
- Python Version
- Build System
- Package Metadata

---

# Who Reads pyproject.toml?

One of the biggest concepts from today's session.

Question:

Does Python Interpreter read this file while running our program?

Answer:

**No.**

Python executes only Python code.

Instead,

Packaging tools read this file.

Examples:

- pip
- setuptools
- hatchling
- poetry

---

# When is pyproject.toml Read?

Application Lifecycle

```
Developer

      │

      ▼

Writes pyproject.toml

      │

      ▼

pip install -e .

      │

      ▼

pip reads pyproject.toml

      │

      ▼

Package Installed

      │

      ▼

python -m jobpulse.main

      │

      ▼

Python Executes Program
```

Important realization:

After installation,

Python no longer reads this file.

---

# Build System

We created:

```toml
[build-system]
```

Question:

What is a Build System?

Answer:

A build system is the software responsible for converting our project into an installable Python package.

Examples:

- setuptools
- hatchling
- poetry-core
- flit

---

# Analogy

Imagine building a house.

```
House

↓

Construction Company

↓

Completed House
```

Our Project

↓

Build System

↓

Python Package

The build system constructs the package.

---

# Why Multiple Build Systems?

Initially Python used mainly:

```
setup.py

+

setuptools
```

Modern Python allows different build systems because different projects have different requirements.

This makes packaging standardized and flexible.

---

# First Section

```toml
[build-system]
```

This section describes:

How should this project be built?

---

# requires

```toml
requires = ["setuptools>=61.0"]
```

Meaning:

Before building this project,

install setuptools version 61 or newer.

These are called:

Build Dependencies

---

# build-backend

```toml
build-backend = "setuptools.build_meta"
```

Meaning:

Use setuptools' build logic for packaging this project.

---

# Build Dependencies vs Runtime Dependencies

Initially there was confusion.

Question:

Should packages like:

- pandas
- requests
- pyspark
- python-dotenv

go inside:

```toml
[build-system]
requires
```

Answer:

No.

---

# Build Dependencies

Needed only while building the package.

Examples:

- setuptools
- hatchling
- flit

---

# Runtime Dependencies

Needed when the application executes.

Examples:

- pandas
- requests
- pyspark
- python-dotenv

These belong inside:

```
[project]
dependencies
```

---

# Python Executes Sequentially

Example

```python
if False:
    import pandas

print("Hello")
```

Output

```
Hello
```

Reason:

Python never enters the if block.

Import is never executed.

---

# Another Example

```python
def load_data():
    import pandas

print("Program Started")
```

Output

```
Program Started
```

Reason:

Function body executes only when the function is called.

---

# Another Example

```python
def load_data():
    import pandas

print("Program Started")

load_data()

print("Finished")
```

If pandas is missing:

Output

```
Program Started

ModuleNotFoundError
```

Reason:

Import executes only during function execution.

---

# Project Metadata

After build-system,

we introduced

```toml
[project]
```

Purpose:

Describe our application.

Metadata includes:

- Name
- Version
- Description
- Dependencies
- Authors
- Python Version

---

# Project Identity

First property:

```toml
name = "jobpulse-ai"
```

Purpose:

Unique identity of the package.

Package managers like pip and repositories like PyPI use this name.

---

# Distribution Name vs Package Name

Project Folder

```
jobpulse-ai
```

Package

```
jobpulse
```

Installation

```bash
pip install jobpulse-ai
```

Import

```python
import jobpulse
```

Important:

Distribution Name

↓

Used by pip

Package Name

↓

Used by Python

---

# Why is name Mandatory?

Without a name:

- pip cannot identify the project.
- PyPI cannot publish it.
- Users cannot install it.

The name acts as the package's identity.

---

# Version

Next property:

```toml
version = "0.1.0"
```

Purpose:

Represents the evolution of the project.

Unlike the project name,

the version changes over time.

---

# Identity vs Evolution

Identity

```
name
```

Usually remains constant.

Evolution

```
version
```

Changes whenever the project changes.

Analogy:

Person

↓

Name remains same

↓

Skills improve

Likewise,

Package Name remains.

Version changes.

---

# Current pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "jobpulse-ai"
version = "0.1.0"
```

---

# Mistakes Encountered

## Mistake 1

Initially thought

Python Interpreter reads

```
pyproject.toml
```

Correction:

Packaging tools read it.

Python executes only Python files.

---

## Mistake 2

Initially assumed

Build Dependencies

and

Runtime Dependencies

are identical.

Correction:

Build dependencies build the package.

Runtime dependencies execute the application.

---

## Mistake 3

Initially thought

Project Name

and

Package Name

must always be identical.

Correction:

They serve different purposes.

Distribution Name

↓

Installation

Package Name

↓

Import

---

## Mistake 4

Initially unsure why

```
name
```

is mandatory.

Correction:

It uniquely identifies the package.

---

# Interview Questions

## What is pyproject.toml?

A standardized configuration file describing how a Python project should be built and packaged.

---

## Who reads pyproject.toml?

Packaging tools like pip and setuptools.

Not the Python interpreter.

---

## What is a Build System?

Software responsible for building Python packages.

---

## Difference between Build Dependency and Runtime Dependency?

Build Dependency:

Needed only during packaging.

Runtime Dependency:

Needed when the application executes.

---

## Difference between Distribution Name and Package Name?

Distribution Name:

Used by pip installation.

Package Name:

Used during Python imports.

---

## Why is name mandatory?

Because package managers and repositories use it as the package's unique identity.

---

# Key Takeaways

- `pyproject.toml` is the standard configuration file for modern Python projects.
- Packaging tools read `pyproject.toml`.
- Python interpreter does not.
- Build systems create installable packages.
- `setuptools` is a build backend.
- Build dependencies differ from runtime dependencies.
- Project metadata describes the application.
- Package identity is represented by `name`.
- Package evolution is represented by `version`.

---

# Homework

1. Explain who reads `pyproject.toml`.
2. Explain why build dependencies differ from runtime dependencies.
3. Explain the difference between distribution name and package name.
4. Draw the complete package installation lifecycle.
5. Explain why `name` and `version` are separate properties.

---

# Project State After Session

```
jobpulse-ai/
│
├── pyproject.toml
│
├── .env
│
├── requirements.txt
│
├── src/
│   └── jobpulse/
│       ├── config.py
│       ├── constants.py
│       ├── logger.py
│       ├── main.py
│       └── __init__.py
│
└── README.md
```

---

# Session Summary

This session introduced the foundation of modern Python packaging. We learned how `pyproject.toml` describes a project, how packaging tools such as `pip` and `setuptools` use it during installation, and why build-time concepts differ from runtime concepts. We also created the initial project metadata, established the package identity with `name`, introduced versioning with `version`, and understood the distinction between distribution names used by package managers and package names used by Python imports.