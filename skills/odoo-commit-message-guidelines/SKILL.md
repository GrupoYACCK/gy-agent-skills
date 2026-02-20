---
name: odoo-commit-message-guidelines
description: "Draft, rewrite, and validate Odoo-style commit messages using [TAG] module: summary format, 50/80 length limits, imperative English, WHY-first body, and correct tag selection including [MIG]. Use when a user asks to write or fix a commit message for Odoo repositories."
---

# Odoo Commit Message Guidelines

## Purpose

Use this skill to produce high-quality Odoo commit messages that are consistent,
reviewable, and easy to revert.

## When To Use

Use this skill when the user asks to:

- write a new commit message for Odoo code
- rewrite or improve an existing commit message
- validate whether a commit message follows Odoo rules
- choose the correct Odoo tag, including migration cases (`[MIG]`)

## Required Inputs

Before drafting, collect:

- modified module name (or `various` for cross-module commits)
- change type and intent (bug fix, refactor, migration, etc.)
- core rationale (WHY the change is needed)
- notable implementation choices (only if relevant)
- references (`task-*`, `Fixes #`, `Closes #`, `opw-*`) when available

If required inputs are missing, ask only the minimum concise follow-up questions.

## Output Format

Use this structure:

```text
[TAG] module: short summary (ideally < 50 chars)

WHY the change is needed.
WHAT changed and technical choices (only if useful).

task-123
Fixes #123
Closes #456
opw-789
```

Rules:

- Commit message must be in English.
- Keep header concise; target about 50 characters in the summary part.
- Body must be multiline and wrapped to about 80 characters per line.
- Use imperative present voice: `Fix`, `Remove`, `Add` (not `Fixes`, `Removes`).
- Make the header meaningful; avoid generic summaries like `bugfix`.
- Prioritize WHY over WHAT in the body.

## Tag Selection Rules

Choose exactly one main tag for the commit:

- `[FIX]` bug fix
- `[REF]` major refactor / heavy rewrite
- `[ADD]` add a new module
- `[REM]` remove dead code/resources/modules
- `[REV]` revert an earlier commit
- `[MOV]` move files/code while preserving history intent
- `[REL]` release commit
- `[IMP]` incremental improvement
- `[MERGE]` merge / forward-port integration commit
- `[CLA]` individual contributor license signature
- `[I18N]` translation updates
- `[PERF]` performance improvement
- `[CLN]` cleanup
- `[LINT]` linting pass
- `[MIG]` module migration

Decision guidance:

- Prefer the tag that best captures intent, not file type.
- If it is clearly a migration, use `[MIG]`.
- If it fixes a regression while migrating, split into two commits when possible.
- Avoid stacking multiple tags in one header.

## Module Naming Rules

- Use technical module name, not marketing/functional display names.
- If multiple modules are touched, list them briefly or use `various`.
- Prefer one logical change per commit and avoid large cross-module commits.

## Writing Workflow

1. Identify the smallest logical change set.
2. Choose the module scope.
3. Select the tag from the rule set above.
4. Draft header: `[TAG] module: imperative summary`.
5. Draft body with WHY first, then concise WHAT if needed.
6. Add references at the end using canonical formats.
7. Validate against checklist before returning.

## Validation Checklist

Confirm all items:

- Header follows `[TAG] module: summary`.
- Summary is concise and not truncated with ellipsis in PR UI.
- Body lines are about 80 characters max.
- Rationale (WHY) is explicit.
- Verb tense is imperative present.
- Tag matches change intent.
- Module naming is technical and accurate.
- Commit scope is a single logical change set.
- References are formatted correctly when present.

If any check fails, rewrite the message before returning.

## Good Examples

```text
[FIX] website: remove unused alert div

Fix look of input-group-btn.
Bootstrap requires input-group-btn to be the first or last child.
An invisible alert node broke that structure and produced visual issues.

Fixes #22769
Closes #22793
```

```text
[IMP] web: add module system to web client

Introduce a module system for JavaScript code to improve isolation,
load order control, and maintainability as the client grows.
```

```text
[MIG] stock_account: migrate valuation hooks to 19.0

Align valuation hook signatures with 19.0 API to preserve extension
compatibility and avoid runtime errors during upgrade.

task-8421
```

## Anti-Patterns To Reject

Reject and rewrite messages with:

- generic headers (`bugfix`, `improvements`)
- missing module name
- missing rationale
- past tense or third-person verbs in header
- oversized multi-topic commits in one message
- truncated first line (`...`) caused by long header

## Response Behavior

When asked to produce a commit message:

1. Return only the raw commit message (no code fences) unless the user asks for explanation.
2. If info is missing, ask only the minimum necessary clarifying questions.
3. If user provides a draft, return a corrected Odoo-compliant version.

## Usage Examples

### Scenario 1: Create a new commit message

**User:** "Write an Odoo commit message for a bug fix in `sale_stock` where delivered qty was computed twice. Reference task-9123."

**Agent behavior:**

1. Identify tag as `[FIX]` and module as `sale_stock`.
2. Draft concise header in imperative form.
3. Explain WHY first in body, then concise WHAT.
4. Append `task-9123` as reference.

### Scenario 2: Rewrite an existing draft

**User:** "Improve this commit message: `fixed stuff in stock module`"

**Agent behavior:**

1. Reject generic summary and missing rationale.
2. Ask minimum questions if context is missing (what bug, why needed).
3. Return corrected message in Odoo format.

### Scenario 3: Validate tag choice

**User:** "I changed API hooks for 19.0 migration and also fixed a small bug. Should I use `[MIG]` or `[FIX]`?"

**Agent behavior:**

1. Prefer `[MIG]` for migration intent.
2. Recommend splitting migration and bug fix into separate commits when possible.
3. Provide one valid commit message for each resulting commit if requested.

## Sources

This documentation was obtained from:

- https://github.com/odoo/documentation/blob/19.0/content/contributing/development/git_guidelines.rst
- https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst#git
