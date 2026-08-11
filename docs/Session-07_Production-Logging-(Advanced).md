# Session 7 – Production Logging (Advanced)

**Project:** JobPulse AI

**Date:** 05-Aug-2026

---

# Session Objective

In this session we enhanced our logging system to production standards by introducing persistent log storage, automatic log rotation, and exception logging.

---

# Topics Covered

- FileHandler
- RotatingFileHandler
- Pathlib for log management
- Automatic log directory creation
- Multiple handlers
- Log rotation
- backupCount
- maxBytes
- logger.error()
- logger.exception()
- Production logging practices

---

# Why FileHandler?

Console logs are temporary.

Problems with only using StreamHandler:

- Logs disappear after application exits.
- Difficult to investigate production failures.
- No historical records.
- Impossible to audit previous executions.

Solution

```
Logger
      │
      ├────────► StreamHandler
      │               │
      │               ▼
      │           Console
      │
      └────────► FileHandler
                      │
                      ▼
                  logs/app.log
```

---

# Log Directory Structure

```
jobpulse-ai/

src/
tests/
logs/
    app.log

README.md
pyproject.toml
```

Why?

- Runtime files separated from source code
- Easier maintenance
- Cleaner project structure
- Easy Git ignore

---

# Creating Log Directory

Using pathlib

```python
from pathlib import Path

log_dir = Path("logs")

log_dir.mkdir(exist_ok=True)

log_file = log_dir / "app.log"
```

---

# Why exist_ok=True?

Creates directory if missing.

If directory already exists

↓

Do nothing.

Without it Python raises

```
FileExistsError
```

---

# Why pathlib instead of os?

Advantages

- Modern Python API
- Better readability
- Platform independent
- Object-oriented design
- Cleaner path construction

Example

```python
log_file = log_dir / "app.log"
```

instead of

```python
os.path.join(...)
```

---

# Multiple Handlers

Logger can send one LogRecord to multiple destinations.

```
Logger
      │
      ├────────► StreamHandler
      │               ▼
      │           Console
      │
      └────────► FileHandler
                      ▼
                   app.log
```

One logging statement

```python
logger.info("Application Started")
```

writes to both console and file.

---

# Preventing Duplicate Handlers

```python
if not logger.handlers:
    logger.addHandler(handler)
    logger.addHandler(file_handler)
```

Why?

Without this condition, every call to `configure_logging()` would attach new handlers.

Result

```
INFO Application Started
INFO Application Started
INFO Application Started
```

Duplicate log messages.

---

# RotatingFileHandler

Problem

Single log file grows indefinitely.

Issues

- Difficult debugging
- Large backups
- High disk usage
- Slow searching
- Maintenance problems

Solution

```python
from logging.handlers import RotatingFileHandler

file_handler = RotatingFileHandler(
    filename=log_file,
    maxBytes=5 * 1024 * 1024,
    backupCount=3,
)
```

---

# maxBytes

Defines maximum size of current log file.

Example

```
5 MB
```

When limit is reached

↓

Current log rotates.

---

# backupCount

Defines number of old log files to keep.

Example

```
logs/

app.log
app.log.1
app.log.2
app.log.3
```

Oldest log automatically removed after exceeding retention count.

---

# Log Rotation Process

```
New LogRecord

↓

Check current file size

↓

Size exceeded?

↓

Yes

↓

Rotate existing logs

↓

Create fresh app.log

↓

Write new LogRecord
```

---

# Why RotatingFileHandler?

Without rotation

```
app.log

↓

10 GB

↓

20 GB

↓

50 GB

↓

100 GB
```

Problems

- Slow searching
- Difficult debugging
- Huge backups
- Storage issues
- Poor maintainability

Rotating logs solve all these problems.

---

# logger.error()

Use when reporting an error condition without an active exception.

Example

```python
logger.error("Configuration missing")
```

Logs only the error message.

---

# logger.exception()

Use only inside an except block.

Example

```python
try:
    response = requests.get(url)
except Exception:
    logger.exception("Failed to fetch jobs")
```

Automatically logs

- Custom message
- Exception type
- Complete traceback
- Call stack
- File name
- Line number

---

# logger.error() vs logger.exception()

logger.error()

- Logs only the supplied message.

logger.exception()

- Logs message
- Complete traceback
- Exception details

Should be used only inside an `except` block.

---

# Production Best Practices

- Configure logging once.
- Centralize logger configuration.
- Use module-specific loggers.
- Use multiple handlers.
- Rotate log files.
- Prevent duplicate handlers.
- Never log passwords, tokens or secrets.
- Use `logger.exception()` for exceptions.

---

# Architecture After Session 7

```
Application
      │
      ▼
Root Logger
      │
      ├──────────────► StreamHandler
      │                    │
      │                    ▼
      │                Console
      │
      └──────────────► RotatingFileHandler
                           │
                           ▼
                     logs/app.log
```

---

# Key Learnings

- Persistent logging
- FileHandler
- RotatingFileHandler
- Pathlib
- Runtime directory management
- Multiple handlers
- Log rotation
- Exception logging
- Production diagnostics
- Maintainable logging architecture

---

# Interview Questions Covered

### Why use FileHandler?

To persist logs beyond the application's lifetime.

---

### Why use RotatingFileHandler?

To prevent unlimited log growth.

---

### What is maxBytes?

Maximum size before log rotation.

---

### What is backupCount?

Number of historical log files retained.

---

### Difference between logger.error() and logger.exception()?

`logger.exception()` logs the complete traceback and should be used inside an `except` block.

---

### Why use pathlib?

Cleaner, object-oriented, cross-platform path handling.

---

### Why check if not logger.handlers?

To prevent duplicate handlers and duplicate log messages.

---

# Session Status

✅ Session 7 Completed

---

# Next Session

## Session 8 – HTTP Client & API Layer

Topics

- requests.Session
- Connection Pooling
- HTTP Methods
- HTTP Status Codes
- Timeouts
- Retries
- Headers
- Exception Handling
- Production API Client Design