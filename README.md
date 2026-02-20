# Agent Skills Repository

This repository contains specialized skills designed to extend the capabilities of AI agents. Each skill provides specific knowledge, workflows, and tools for particular domains.

## Available Skills

### [Odoo Dev](skills/odoo-dev/SKILL.md)
**Description:** Senior Odoo developer skill focused on Odoo/OCA standards, secure code patterns, and module scaffolding workflows.
**Key Features:**
- Enforces Odoo and OCA coding/contribution guidelines from local references.
- Reviews code for common framework risks (SQL injection patterns, unsafe commits, fragile XML inheritance).
- Supports module scaffolding with `scripts/scaffold.py` in interactive mode or positional-argument mode.
- Includes script usage documentation in `skills/odoo-dev/scripts/README.md`.

### [Odoo Commit Message Guidelines](skills/odoo-commit-message-guidelines/SKILL.md)
**Description:** comprehensive guide for drafting, rewriting, and validating Odoo-style commit messages.
**Key Features:**
- Enforces Odoo's specific commit message format (Tag + Module + Summary).
- Provides guidelines for content (WHY vs WHAT).
- Includes validation checklists and examples.

### [Python PEP 8 Coach](skills/python-pep8-coach/SKILL.md)
**Description:** A skill to review and verify Python code compliance with PEP 8 standards.
**Key Features:**
- Uses `flake8` for linting and `black` for safe formatting.
- Designed to be interactive, asking for user confirmation before applying fixes.
- Focuses on safety and code quality.

## Repository Structure

```
skills/
├── odoo-dev/
│   ├── SKILL.md
│   ├── assets/
│   ├── references/
│   └── scripts/
│       ├── scaffold.py
│       └── README.md
├── odoo-commit-message-guidelines/
│   ├── SKILL.md
│   └── references/
│       ├── CONTRIBUTING.md
│       └── git_guidelines.md
└── python-pep8-coach/
    ├── SKILL.md
    └── references/
        └── pep-0008.md
```

## Usage

To use a skill, an agent should read the corresponding `SKILL.md` file to understand the instructions and capabilities.
