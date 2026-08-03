# Data Engineering Bootcamp
# Session 03 - Python Packaging, Module Execution & Editable Installation

**Project:** JobPulse AI

**Objective:**

In this session we learned how Python executes package-based applications, why the `src` layout requires packaging, how editable installations work, and why professional Python projects use `python -m` instead of executing files directly.

---

# Session Roadmap

Topics covered:

- Why Python Packaging Exists
- Project Structure Review
- Running Python Programs
- Module Search Path
- ModuleNotFoundError
- PYTHONPATH
- Editable Installation
- pip install -e .
- What "-e" Means
- Site-Packages
- Project Linking
- Runtime vs Installation
- pyproject.toml Introduction
- Packaging Lifecycle

---

# Recap

Current Project Structure

```

jobpulse-ai/
│
├── src/
│   └── jobpulse/
│       ├── config.py
│       ├── constants.py
│       ├── logger.py
│       ├── main.py
│       └── **init**.py
│
├── .env
├── requirements.txt
└── README.md
