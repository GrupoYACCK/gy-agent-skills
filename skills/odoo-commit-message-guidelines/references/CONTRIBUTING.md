---
title: OCA Guidelines — Commit Message Extensions
---

# OCA Commit Message Extensions

The OCA follows the same commit message conventions as Odoo with the
following additions:

- **[MIG]** tag for migrating a module to a new Odoo version.

## Header Truncation Check

When you open a PR, verify the commit message is not cut with ellipsis:

```
[FIX] module_foo: and this is my very long m[...]
```

If truncated, shorten the summary. Keep detailed explanation in the
body.

## Sources

- https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst#git
