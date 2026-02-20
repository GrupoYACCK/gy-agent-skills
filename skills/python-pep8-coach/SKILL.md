---
name: python-pep8-coach
description: "Review and verify Python code against PEP 8 using flake8, then apply safe formatting fixes with black after explicit user confirmation. Use when users ask to check style compliance, lint Python files, or fix PEP 8 issues in a target folder."
---

# Python PEP 8 Coach

## Purpose

Use this skill to audit and improve Python style compliance with PEP 8.

Primary tools:

- `flake8` for lint diagnostics
- `black` for safe, automated formatting fixes

## When To Use

Use this skill when the user asks to:

- review Python code for PEP 8 compliance
- identify style violations in one file or folder
- apply style fixes while minimizing manual edits
- standardize formatting consistently across Python files

## Default Behavior

- Scope defaults to a user-specified folder.
- Do not change code outside the requested path.
- If the requested scope is repository root, confirm before scanning/editing broadly.
- Run checks first and report findings before editing.
- Ask for explicit confirmation before applying fixes.
- Apply automatic fixes with `black` only.
- Re-run format and lint checks after formatting and report remaining issues.

## Workflow

1. Confirm target path (file or folder) from user input.
2. Verify tool availability (`flake8 --version`, `black --version`).
3. Run diagnostics:
    - `black --check --line-length 88 <target>`
    - `flake8 <target> --max-line-length 88 --extend-ignore=E203,W503 --exclude=.venv,build,dist,__pycache__`
4. Summarize results by file and error code.
5. Ask for confirmation before edits.
6. If approved, apply formatting:
   - `black --line-length 88 <target>`
7. Re-run:
    - `black --check --line-length 88 <target>`
    - `flake8 <target> --max-line-length 88 --extend-ignore=E203,W503 --exclude=.venv,build,dist,__pycache__`

## Style Policy

- Line length: 88 characters.
- Black-compatible lint policy:
  - ignore `E203`
  - ignore `W503`
  - set max line length to 88

## Safety Rules

- Never auto-edit without explicit user confirmation.
- Never apply semantic refactors as part of auto-fix.
- Keep changes limited to formatting and whitespace normalization.
- Exclude obvious non-target paths when needed (`.venv`, `build`, `dist`, caches).

## Missing Dependency Handling

If `flake8` or `black` is missing:

1. Inform the user exactly which tool is unavailable.
2. Ask permission to install with pip in the active environment.
3. If user declines, provide manual install commands and stop safely.
4. If user approves, install only the missing tool(s) and re-run diagnostics.

## Output Expectations

When reporting, provide:

- analyzed scope
- command(s) run
- number of files checked
- key lint categories found
- whether fixes were applied
- post-fix remaining issues (if any)

If no violations are found, return a short success summary.

## Examples

### Scenario 1: Auditing a single file

**User:** "Can you check `script.py` for style issues?"

**Agent Reference:**

1.  Check diagnostics:
    ```bash
    flake8 script.py --max-line-length 88 --extend-ignore=E203,W503
    black --check --line-length 88 script.py
    ```
2.  Report: "Found 3 issues in `script.py`: E231 missing whitespace, E302 expected 2 blank lines. Would you like me to fix them?"
3.  User: "Yes."
4.  Fix:
    ```bash
    black --line-length 88 script.py
    ```

### Scenario 2: Fixing a directory

**User:** "Fix all PEP 8 errors in the `src/` folder."

**Agent Reference:**

1.  Check and report summary first.
    ```bash
    flake8 src/ --max-line-length 88 ...
    ```
2.  "Checked 12 files. Found 45 violations. Proceed with formatting?"
3.  User: "Go ahead."
4.  Apply fixes:
    ```bash
    black --line-length 88 src/
    ```