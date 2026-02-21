---
title: Git guidelines
---

# Header Heuristic

The header should make a valid sentence once concatenated with
`if applied, this commit will <header>`. For example
`[IMP] base: prevent to archive users linked to active partners`
is correct because it reads as
"if applied, this commit will prevent to archive users…".

# Why Over What

First explain WHY you are modifying code. What matters if someone goes
back to your commit in 4 decades (or 3 days) is the purpose of the
change. The WHAT can be seen in the diff itself. If technical choices
were involved, explain WHY that decision was taken after the rationale.

## Sources

- https://github.com/odoo/documentation/blob/19.0/content/contributing/development/git_guidelines.rst