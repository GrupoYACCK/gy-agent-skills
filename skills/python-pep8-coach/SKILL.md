---
name: python-pep8-coach
description: "Review and verify Python code against PEP 8 using flake8/black/pre-commit. Use when users ask to check style compliance, lint Python files, or fix PEP 8 issues."
---

# Python PEP 8 Coach

## Purpose

Audit and improve Python style compliance with PEP 8.

Tools: `flake8` (diagnostics), `black` (formatting), `pre-commit` (automation).

## Local References

- `references/pep-0008.md` — condensed PEP 8 rules requiring human judgment
  (naming, comments, programming recommendations). Consult only for
  style disputes or edge cases not covered by tooling.

## When To Use

- Review Python code for PEP 8 compliance
- Identify or fix style violations in files or folders
- Set up automated style enforcement via pre-commit

## Default Behavior

- Run checks first, report findings, then ask confirmation before edits.
- Never auto-edit without explicit user approval.
- Never apply semantic refactors — only formatting and whitespace.
- Exclude `.venv`, `build`, `dist`, `__pycache__` from scans.
- If scope is repository root, confirm before scanning broadly.
- Re-run checks after formatting and report remaining issues.

## Mode Detection

Detect mode from project config (`pyproject.toml`, `setup.cfg`, `.flake8`,
`tox.ini`, `.pre-commit-config.yaml`) or user instruction:

| Mode | Line length | flake8 flags | Formatter |
|---|---|---|---|
| **Strict PEP 8** (default) | 79 | — | manual edits |
| **Black-compatible** | 88 | `--extend-ignore=E203,W503` | `black` |
| **pre-commit** | from config | from config | `pre-commit run` |

## Workflow

1. Confirm target path from user input.
2. Check for `.pre-commit-config.yaml` in the project root.
   - **If present**: prefer `pre-commit run --files <target>` (or
     `pre-commit run --all-files` for full repo). This respects the
     project's configured hooks (flake8, black, isort, etc.) and avoids
     conflicting with established team workflows.
   - **If absent**: detect mode and run flake8/black directly.
3. Summarize results by file and error code.
4. Ask confirmation before edits.
5. If approved, apply fixes (pre-commit auto-fixes, or black, or
   manual edits depending on mode).
6. Re-run checks and report remaining issues.

## pre-commit Integration

When `.pre-commit-config.yaml` exists:

- Use `pre-commit run --files <target>` for scoped checks.
- Use `pre-commit run --all-files` for full repo checks.
- Do not override hook configurations with manual flake8/black flags.
- If pre-commit is not installed, offer: `pip install pre-commit`
  then `pre-commit install`.

When user asks to set up pre-commit for a project that lacks it:

- Generate a `.pre-commit-config.yaml` with standard Python hooks:
  ```yaml
  repos:
    - repo: https://github.com/pre-commit/pre-commit-hooks
      rev: v5.0.0
      hooks:
        - id: trailing-whitespace
        - id: end-of-file-fixer
    - repo: https://github.com/psf/black
      rev: 25.1.0
      hooks:
        - id: black
    - repo: https://github.com/pycqa/flake8
      rev: 7.1.2
      hooks:
        - id: flake8
    - repo: https://github.com/pycqa/isort
      rev: 6.0.1
      hooks:
        - id: isort
  ```
- Ask confirmation before creating the file.
- Run `pre-commit install` to enable git hooks.

## Missing Dependency Handling

If a required tool is missing:

1. Inform user which tool is unavailable.
2. Ask permission to install (`pip install <tool>`).
3. If declined, provide manual install command and stop.

## Output Expectations

Report: scope analyzed, command(s) run, file count, key violation
categories, fixes applied, remaining issues. If clean, return a short
success summary.