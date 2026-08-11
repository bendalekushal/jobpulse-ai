# Session 6 - Python Logging & Production Environment Setup

**Project:** JobPulse AI

**Date:** 04-Aug-2026

---

# Session Objective

In this session we learned:

- Python Logging Architecture
- Root Logger vs Module Logger
- Logger, Handler, Formatter & LogRecord
- Centralized Logging
- StreamHandler Configuration
- Formatter Design
- Production Logging Principles
- Python Virtual Environment Troubleshooting
- Production Python Environment Setup
- pyproject.toml Dependency Management
- Successfully Tested JobPulse AI Logger

---

# Part 1 - Python Logging Architecture

Python logging consists of four major components.

```
Application
      │
      ▼
Logger
      │
      ▼
Handler
      │
      ▼
Formatter
      │
      ▼
Destination
```

---

# Logger

Responsible for deciding:

> Should this log message be processed?

Example

```python
logger.info("Application Started")
```

The logger checks the configured logging level.

Example:

```
Logger Level = INFO

DEBUG -> Ignored

INFO -> Processed

WARNING -> Processed

ERROR -> Processed

CRITICAL -> Processed
```

---

# Handler

Responsible for deciding:

> Where should the log message be sent?

Examples

- Console
- File
- Cloud Logging
- Database
- Remote Logging Server

Current Project

```
StreamHandler()
```

Destination

```
Console (stderr)
```

---

# Formatter

Responsible for deciding:

> How should the log message look?

Current Formatter

```python
"%(asctime)s | %(levelname)-8s | %(name)s | Line:%(lineno)d | %(message)s"
```

Generated Output

```
2026-08-04 09:51:50 | INFO | __main__ | Line:19 | Application Started
```

---

# LogRecord

Python automatically creates a LogRecord object whenever logging methods are called.

Example

```python
logger.info("Application Started")
```

Internally Python stores

```
Timestamp

Level

Logger Name

Line Number

Function Name

File Name

Thread ID

Process ID

Message
```

Formatter reads these attributes.

---

# Root Logger

Configured only once.

```python
logging.getLogger()
```

Responsibilities

- Configure Log Level
- Configure Handler
- Configure Formatter

Acts as the parent logger.

---

# Module Logger

Created inside every module.

```python
logger = logging.getLogger(__name__)
```

Examples

```
jobpulse.main

jobpulse.database

jobpulse.scraper
```

Each module has its own logger while inheriting the root logger configuration.

---

# Why Configure Root Logger?

Instead of configuring every module individually

```
database.py

scraper.py

main.py
```

We configure once.

Advantages

- Centralized configuration
- Easy maintenance
- No code duplication
- Single Responsibility Principle
- DRY Principle
- Consistent logging across application

---

# Why Only main.py Calls configure_logging()

Only the application entry point should initialize logging.

```
main.py

↓

configure_logging()
```

Other modules simply create module-specific loggers.

```
logging.getLogger(__name__)
```

---

# Logger Configuration

logger.py

```python
import logging


def configure_logging():

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | Line:%(lineno)d | %(message)s"
    )

    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)
```

---

# Why logger.handlers Check?

Without

```python
if not logger.handlers
```

Calling configure_logging() multiple times would attach multiple handlers.

Result

Duplicate log messages.

Current implementation avoids duplicate handlers.

---

# Why StreamHandler()

```
logging.StreamHandler()
```

Default Stream

```
sys.stderr
```

Therefore logs appear in the terminal.

---

# Why Formatter?

Without

```python
handler.setFormatter(formatter)
```

Python uses the default formatter.

Result

Logs still work but are not displayed in the required format.

---

# Why Include Line Number?

```
%(lineno)d
```

Advantages

- Faster debugging
- Exact source location
- Easier issue investigation

---

# Propagation

Meaning

Should child loggers pass log records to the parent logger?

Default

```
propagate = True
```

Current project relies on propagation.

Therefore module loggers automatically use the root logger's configuration.

---

# Production Logging Principles Learned

- Configure logging once
- Create logger per module
- Avoid code duplication
- Keep configuration centralized
- Avoid import-time side effects
- Initialize resources only when required

---

# Part 2 - Project Integration

main.py

```python
import logging

from jobpulse.logger import configure_logging

configure_logging()

logger = logging.getLogger(__name__)
```

Inside main()

```python
logger.info("Application Started")
```

---

# Logger Output

```
2026-08-04 09:51:50 | INFO | __main__ | Line:19 | Application Started
```

Explanation

```
Timestamp

↓

Log Level

↓

Module Name

↓

Line Number

↓

Actual Message
```

---

# Why __main__ Appeared?

Application executed using

```bash
python -m jobpulse.main
```

Therefore

```
__name__ == "__main__"
```

Hence

```python
logging.getLogger(__name__)
```

becomes

```
logging.getLogger("__main__")
```

---

# Part 3 - Python Environment Troubleshooting

Initial Issue

```
ModuleNotFoundError

No module named jobpulse
```

Reason

Project not installed.

Solution

```
pip install -e .
```

---

# Second Issue

```
ImportError

_ssl DLL missing
```

Investigation

Verified

```
Python Version

Virtual Environment

SSL

sys.path

pyvenv.cfg
```

Found

Current virtual environment depended on Conda DLLs.

---

# Production Decision

Instead of relying on

```
(.venv) (base)
```

Installed

Official Python 3.11

Reason

- Production standard
- Independent virtual environment
- Better package compatibility
- Cleaner architecture

---

# New Environment

Installed

```
Python 3.11.6
```

Created

```
python -m venv .venv
```

Activated

```
.venv\Scripts\Activate.ps1
```

---

# pyproject.toml Improvements

Added

```toml
description

readme

requires-python

authors

dependencies
```

Configured

```
python-dotenv

requests
```

Also configured setuptools package discovery for src layout.

---

# Final Verification

Application executed successfully.

```
python -m jobpulse.main
```

Output

```
Application Started

Application : JobPulse AI

Environment : development

API Timeout : 30 seconds
```

Logger working successfully.

---

# Key Learnings

- Python logging architecture
- Root logger
- Module logger
- Handler
- Formatter
- LogRecord
- StreamHandler
- Logger inheritance
- Centralized configuration
- Propagation
- Production environment setup
- Official Python installation
- Virtual environment management
- pyproject.toml dependency management
- Editable package installation
- Production debugging mindset

---

# Interview Questions Covered

### Why use centralized logging?

Avoid duplicate configuration and improve maintainability.

---

### Why configure the root logger?

To provide common configuration inherited by all module loggers.

---

### Why use logging.getLogger(__name__)?

Each module gets its own logger while inheriting the root configuration.

---

### Why use if not logger.handlers?

Prevents duplicate handlers and duplicate log messages.

---

### Why include line numbers in logs?

Makes debugging significantly easier.

---

### Why should only main.py call configure_logging()?

Application initialization should happen only once from the entry point.

---

# Session Status

Session 6 Completed Successfully

Next Session

- FileHandler
- RotatingFileHandler
- TimedRotatingFileHandler
- Exception Logging
- Production Logging Best Practices
- Logging Configuration Improvements