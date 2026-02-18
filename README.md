# Odoo Commit Message Guidelines Skill

This repository contains a skill that helps draft, rewrite, and validate
Odoo-style commit messages.

## Skill Included

- `odoo-commit-message-guidelines`

Path:

- `skills/odoo-commit-message-guidelines/SKILL.md`

## What This Skill Does

The skill enforces Odoo commit message conventions, including:

- Header format: `[TAG] module: short summary`
- English language only
- Imperative voice (`Fix`, `Add`, `Remove`)
- Short, meaningful subject line (target ~50 chars)
- Body wrapped to about 80 characters per line
- WHY-first body content (rationale before implementation details)
- Correct tag selection (including migration tag `[MIG]`)

## When to Use It

Use this skill when you need to:

- Write a new Odoo commit message
- Improve an existing commit message
- Check compliance with Odoo formatting rules
- Choose the right tag for a change

## Required Inputs

Before generating a message, gather:

- Module name (or `various` for cross-module changes)
- Change intent (fix, refactor, migration, etc.)
- Main rationale (WHY this change is needed)
- Relevant implementation notes (optional)
- References when available (`task-*`, `Fixes #`, `Closes #`, `opw-*`)

## Output Template

```text
[TAG] module: short summary

WHY the change is needed.
WHAT changed and technical choices (if relevant).

task-123
Fixes #123
Closes #456
opw-789
```

## Supported Tags

- `[FIX]` bug fix
- `[REF]` major refactor
- `[ADD]` new module
- `[REM]` code/resource removal
- `[REV]` revert
- `[MOV]` move while preserving intent
- `[REL]` release
- `[IMP]` improvement
- `[MERGE]` merge/forward-port
- `[CLA]` contributor license signature
- `[I18N]` translations
- `[PERF]` performance
- `[CLN]` cleanup
- `[LINT]` linting
- `[MIG]` migration

## Quick Validation Checklist

- Header matches `[TAG] module: summary`
- Summary is concise and meaningful
- Body explains WHY first
- Body lines are around 80 chars max
- Verb tense is imperative present
- Tag and module are accurate
- Scope is one logical change
- References are correctly formatted

## Example

```text
[FIX] website: remove unused alert div

Fix look of input-group-btn.
Bootstrap requires input-group-btn to be the first or last child.
An invisible alert node broke that structure and produced visual issues.

Fixes #22769
Closes #22793
```
