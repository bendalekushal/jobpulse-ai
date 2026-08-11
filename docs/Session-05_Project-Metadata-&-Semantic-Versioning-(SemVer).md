# Data Engineering Bootcamp
# Session 05 - Project Metadata & Semantic Versioning (SemVer)

**Project:** JobPulse AI

**Objective:**

In this session we learned how a Python project identifies itself using project metadata, why package identity is different from package evolution, and how Semantic Versioning (SemVer) communicates the maturity and compatibility of software releases.

---

# Session Roadmap

Topics Covered

- Project Metadata
- [project] Section
- Package Identity
- Distribution Name
- Package Name
- Why name is Mandatory
- Versioning
- Semantic Versioning
- Major Version
- Minor Version
- Patch Version
- First Stable Release
- Professional Versioning Strategy

---

# Recap

Current pyproject.toml

```toml
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"
```

Question:

What comes next?

Answer:

```toml
[project]
```

---

# What is [project]?

The

```toml
[project]
```

section contains information describing our application.

Think of it as the identity card of the package.

It contains:

- Name
- Version
- Description
- Authors
- Dependencies
- Python Version

This information is called:

Project Metadata

---

# Difference Between Build System and Project

One important realization.

```
[build-system]
```

describes

How should the package be built?

Whereas

```
[project]
```

describes

What is this package?

These two sections have completely different responsibilities.

---

# First Metadata Property

```toml
[project]
name = "jobpulse-ai"
```

Purpose:

The package's identity.

Package managers use this name to identify the project.

---

# Why is name Mandatory?

Suppose every package had no name.

Would pip know what to install?

No.

Would PyPI know what to publish?

No.

Would users know which package to download?

No.

Therefore,

```
name
```

is mandatory.

---

# Package Identity

The project name represents identity.

Identity usually never changes.

Example

```
jobpulse-ai
```

Even after years of development,

the package identity remains the same.

---

# Distribution Name vs Package Name

Current project

Project Folder

```
jobpulse-ai
```

Python Package

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

Important realization

Distribution Name

↓

Package Installation

Package Name

↓

Python Imports

---

# Why Can Distribution Names Use Hyphens?

Python identifiers cannot contain

```
-
```

Therefore

```python
import jobpulse-ai
```

is invalid.

Instead,

```python
import jobpulse
```

works.

---

# Adding Version

Next property

```toml
version = "0.1.0"
```

Question

Why is version separate from name?

Answer

Because

Name

↓

Identity

Version

↓

Evolution

---

# Identity vs Evolution

Identity

```
JobPulse AI
```

Remains the same.

Evolution

```
0.1.0

↓

0.2.0

↓

0.5.0

↓

1.0.0
```

Represents software growth.

Analogy

Person

↓

Name remains same

↓

Knowledge improves

Likewise,

Package name remains.

Version changes.

---

# What is Semantic Versioning?

Semantic Versioning

(short form)

SemVer

Version Format

```
MAJOR.MINOR.PATCH
```

Example

```
0.1.0
```

---

# Understanding Version Numbers

```
0 . 1 . 0

│   │   │

│   │   └── Patch

│   └────── Minor

└────────── Major
```

---

# Major Version

Represents

Overall maturity

and

Backward compatibility.

Example

```
1.0.0

↓

2.0.0
```

Usually changes when:

Breaking changes occur.

---

# Minor Version

Represents

New Features.

Example

```
1.2.0

↓

1.3.0
```

Existing functionality continues working.

---

# Patch Version

Represents

Small improvements.

Examples

- Bug Fixes
- Documentation Updates
- Performance Improvements
- Logging Improvements
- Internal Refactoring

Example

```
1.2.3

↓

1.2.4
```

---

# Why Start at 0.1.0?

Question

Why not

```
1.0.0
```

immediately?

Answer

Because the project is still under development.

Version

```
0.x.y
```

communicates

- APIs may change.
- Features may change.
- Software is not yet considered stable.

---

# When Should We Release 1.0.0?

Project Evolution

```
0.1.0

↓

0.2.0

↓

0.5.0

↓

0.8.0

↓

0.9.9

↓

1.0.0
```

One important discussion.

Initially it seemed logical that

```
0.10.0
```

should come after

```
0.9.9
```

Although mathematically correct,

SemVer communicates software maturity.

Once software becomes stable,

the first public release should become

```
1.0.0
```

---

# Examples

## Documentation Fix

```
0.1.0

↓

0.1.1
```

Patch

---

## Added Resume Parser

```
0.1.1

↓

0.2.0
```

Minor

---

## Changed Entire API

```
1.2.0

↓

2.0.0
```

Major

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

```
0.10.0
```

should be the first stable release.

Correction

The first stable release should become

```
1.0.0
```

because the major version communicates software stability.

---

## Mistake 2

Initially mixed

Package Name

and

Distribution Name.

Correction

Distribution Name

↓

pip

Package Name

↓

Python Imports

---

## Mistake 3

Initially assumed

Version is just a number.

Correction

Version communicates software maturity and compatibility.

---

# Interview Questions

## What is Project Metadata?

Information describing the project rather than its source code.

---

## Why is name mandatory?

Because it uniquely identifies the package.

---

## Difference between Name and Version?

Name represents identity.

Version represents evolution.

---

## What is Semantic Versioning?

A standardized versioning scheme using

```
MAJOR.MINOR.PATCH
```

to communicate compatibility and software maturity.

---

## Difference between Major, Minor and Patch?

Major

Breaking changes.

Minor

New features without breaking compatibility.

Patch

Bug fixes and small improvements.

---

## Why start at 0.1.0?

Because the software is still under development.

---

## When should a project become 1.0.0?

When maintainers consider it the first stable public release.

---

# Key Takeaways

- Project metadata describes the package.
- Build metadata and project metadata have different responsibilities.
- Package identity is represented by name.
- Package evolution is represented by version.
- Distribution names are used by pip.
- Package names are used by Python imports.
- Semantic Versioning follows MAJOR.MINOR.PATCH.
- 0.x indicates ongoing development.
- 1.0.0 indicates the first stable public release.

---

# Homework

1. Explain why name and version are different.
2. Describe the responsibilities of Major, Minor and Patch versions.
3. Explain why 1.0.0 is considered the first stable release.
4. Give examples of Patch, Minor and Major updates.
5. Explain the difference between Distribution Name and Package Name.

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

This session completed the foundational concepts of Python packaging by introducing project metadata and Semantic Versioning. We learned how the `[project]` section identifies the package, why `name` represents the package's identity while `version` represents its evolution, and how Semantic Versioning communicates the maturity and compatibility of software through the `MAJOR.MINOR.PATCH` format. These concepts provide the basis for releasing and maintaining production-quality Python applications.