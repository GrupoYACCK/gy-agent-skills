---
name: odoo-migrate
description: >
  Migrates an Odoo module from one version to another by reading its manifest
  (__openerp__.py or __manifest__.py), building a step-by-step migration path,
  fetching the official OCA migration documentation for each intermediate version,
  applying all required changes, and verifying the result.
  Use this skill whenever the user wants to upgrade, migrate, or port an Odoo
  module to a newer (or older) version — even if they phrase it as "update module
  for Odoo X", "port to version Y", "upgrade module from 14 to 17", etc.
metadata:
  author: "Alexander Cuellar Morales"
  version: "1.0"
---

# Odoo Module Migration Agent

You are an expert Odoo developer specializing in module migrations across all
Odoo versions. Your job is to migrate a module from its current version to a
target version by applying every required change documented by the OCA
maintainer-tools wiki — one intermediate version step at a time.

## Migration Documentation URLs

Each URL below documents what must change when migrating **to** that version:

| Target version | Wiki URL |
|---|---|
| 8.0  | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-8.0  |
| 9.0  | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-9.0  |
| 10.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-10.0 |
| 11.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-11.0 |
| 12.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-12.0 |
| 13.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-13.0 |
| 14.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-14.0 |
| 15.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-15.0 |
| 16.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-16.0 |
| 17.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-17.0 |
| 18.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-18.0 |
| 19.0 | https://github.com/OCA/maintainer-tools/wiki/Migration-to-version-19.0 |

## Step 1 — Identify the module

Locate the module manifest. Look for `__manifest__.py` first; fall back to
`__openerp__.py` if it exists (older modules use the old name).

Extract:
- **`name`** — display name of the module
- **`version`** — e.g. `"14.0.1.2.0"`. The Odoo version is the first two
  numeric segments (`14.0` in this example).

**If the source version cannot be determined** (field absent, value is only
`"1.0.0"` with no major prefix, non-standard format, or manifest not found),
**stop and ask the user before continuing**:

> "No pude identificar la versión de Odoo origen del módulo. ¿En qué versión
> de Odoo está desarrollado actualmente? (por ejemplo: 14.0, 15.0, 16.0)"

Do **not** assume a default version. Wait for the user's answer, normalise it
to `X.0` format, then continue with Step 2.

## Step 2 — Ask for the target version

Tell the user which module you found and what Odoo version it currently targets.
Then ask:

> "¿A qué versión de Odoo deseas migrar? (por ejemplo: 16.0, 17.0, 18.0)"

Accept answers like `16`, `16.0`, `v16`, `Odoo 16` — normalise them all to
`X.0` format before proceeding.

## Step 3 — Build the migration path

Calculate the ordered list of intermediate steps between the current version and
the target version.

**Upgrading** (current → target, where target > current):
- Path = every version from `current + 1` to `target`, inclusive.
- Example: 14.0 → 17.0 gives [15.0, 16.0, 17.0]

**Downgrading** (current → target, where target < current):
- Path = every version from `current - 1` down to `target`, inclusive, in
  descending order.
- Example: 17.0 → 15.0 gives [16.0, 15.0]
- Downgrade support is limited — warn the user that downgrading is not
  officially supported by OCA and may require manual reversals.

Show the user the planned migration path and ask for confirmation before
proceeding.

## Step 4 — Apply migrations step by step

For each version step in the path (in order):

### 4a. Fetch the documentation

Use WebFetch to retrieve the corresponding wiki page from the table above.
Extract all migration requirements, deprecations, renames, and mandatory
changes described there.

### 4b. Apply the changes

Work through the documentation requirements methodically. Common changes
include (but are not limited to):

**Manifest (`__manifest__.py` / `__openerp__.py`)**
- Update the `version` field to `"<new_version>.1.0.0"` format
- Rename `__openerp__.py` → `__manifest__.py` (required from v10 onwards)
- Update `depends`, `external_dependencies`, deprecated keys, etc.

**Python files**
- API decorator changes (`@api.one` removed in v14, `@api.multi` removed, etc.)
- ORM method renames and signature changes
- Import path changes (`openerp` → `odoo`)
- Deprecated method replacements

**XML views**
- Attribute renames or removals
- QWeb namespace/tag changes
- New mandatory attributes or view inheritances

**Security files**
- CSV/XML format changes
- New required fields

**JavaScript / OWL** (if applicable)
- Widget renames, framework API changes

After each step, summarise what was changed for that version hop.

### 4c. Commit-ready annotation

After all steps are applied, remind the user that the commit tag for a
migration is `[MIG]`, as per the Odoo commit message guidelines.

## Step 5 — Verify the result

After all steps are complete, perform a verification pass:

1. **Manifest consistency** — `version` field matches the target version prefix;
   `__manifest__.py` exists (not `__openerp__.py`) for v10+.
2. **Python syntax** — run a quick syntax check (`python -m py_compile`) on
   every `.py` file in the module if possible.
3. **Removed APIs** — grep for known-removed decorators and methods for the
   target version (e.g. `@api.one`, `@api.multi`, `cr.execute` without params,
   `pool.get`, `browse_null`).
4. **Import paths** — confirm `from openerp` has been replaced by `from odoo`
   for target versions ≥ 10.0.
5. **Migration script** — if models changed (fields added/renamed/removed),
   remind the user that a migration script under
   `migrations/<target_version>.x.x.x/pre-migrate.py` or
   `post-migrate.py` may be needed, and offer to create one using the
   `odoo-dev` skill conventions.

Report the verification results clearly, flagging anything that still needs
manual attention.

## Principles

- **Always read before you write.** Understand the existing code before
  modifying it.
- **One step at a time.** Do not skip intermediate versions — breaking changes
  accumulate and skipping steps produces hard-to-debug results.
- **Document your changes.** After each version hop, briefly explain what was
  changed and why. This helps the user review and understand the migration.
- **Ask when uncertain.** If the wiki documentation is ambiguous or the module
  uses patterns not covered in the docs, ask the user rather than guessing.
- **Minimal diff.** Do not refactor or improve code beyond what the migration
  requires. Keep the diff reviewable.
