---
title: OCA Contributing Guidelines (OCA-Specific Conventions)
---

# OCA Guidelines

> For general Odoo coding conventions (module structure, file naming, XML format,
> XML ID naming, Python imports/idioms, model attribute order, field naming,
> SQL injection, ORM bypass, cr.commit rules), see `coding_guidelines.md`.
> For security topics, see `backend/security.rst`.
> This file covers **OCA-specific** conventions only.

## Modules

### Naming

- Singular form (except when the Odoo object is already plural, e.g. `mrp_operations_...`).
- `base_` prefix if the module serves as a base for others (e.g. `base_location_nuts`).
- `l10n_CC_` prefix for localization modules (`CC` = country code, e.g. `l10n_es_pos`).
- When extending an Odoo module, prefix with that module's name (e.g. `mail_forward`).
- Combining Odoo + OCA modules: Odoo's name first (e.g. `crm_partner_firstname` for Odoo's `crm` + OCA's `partner_firstname`).

### Manifest (`__manifest__.py`)

- Avoid empty keys.
- Must have `license` and `images` keys.
- Append `,Odoo Community Association (OCA)` to `author`.
- `website`: `https://github.com/OCA/<repo>` (or `.../tree/<branch>/<addon>`).
- No company logos or corporate branding.

## Version Numbers

Format: `<odoo_major>.0.x.y.z` (e.g. `12.0.1.0.0`).

The `x.y.z` part is **major.minor.patch**:

- **x**: Significant data model or view changes. May require migration.
- **y**: New features, backward compatible. Module upgrade likely needed.
- **z**: Bug fixes. Server restart typically needed.

Breaking changes must include migration instructions or scripts. See [SemVer](https://semver.org/).

## Migrations

Breaking changes **must** include a migration script. For major Odoo version migrations, scripts are appreciated; at minimum document changes in the README.

Reference: <https://github.com/OCA/maintainer-tools/wiki#migration>

## Installation Hooks

Hooks go in **`hooks.py`** at the module root: `pre_init_hook`, `post_init_hook`, `uninstall_hook`, `post_load`.

Manifest:

```python
{
    'pre_init_hook': 'pre_init_hook',
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'post_load': 'post_load',
}
```

In `__init__.py`:

```python
from .hooks import pre_init_hook, post_init_hook, uninstall_hook, post_load
```

Use `post_load` for monkey patches (applied only when module is installed).

## OCA Module Structure

```
addons/<my_module_name>/
|-- controllers/
|   |-- __init__.py
|   `-- main.py
|-- data/
|   `-- <main_model>.xml
|-- demo/
|   `-- <inherited_model>.xml
|-- examples/
|   `-- my_example.csv
|-- i18n/
|   |-- en_GB.po
|   |-- es.po
|   `-- module_name.pot
|-- migrations/
|   `-- 16.0.x.y.z/
|       |-- pre-migration.py
|       `-- post-migration.py
|-- models/
|   |-- __init__.py
|   |-- <main_model>.py
|   `-- <inherited_model>.py
|-- readme/
|   |-- CONTRIBUTORS.rst
|   |-- DESCRIPTION.rst
|   `-- USAGE.rst
|-- reports/
|   |-- __init__.py
|   |-- reports.xml
|   `-- <bi_reporting_model>.py
|-- security/
|   |-- ir.model.access.csv
|   `-- <main_model>_security.xml
|-- static/
|   |-- img/
|   |-- lib/
|   `-- src/
|       |-- js/
|       |-- css/
|       `-- xml/
|-- templates/
|   `-- <main_model>.xml
|-- tests/
|   |-- __init__.py
|   `-- <test_file>.py
|-- views/
|   |-- <main_model>_views.xml
|   `-- report_<qweb_report>.xml
|-- wizards/
|   |-- __init__.py
|   |-- <wizard_model>.py
|   `-- <wizard_model>.xml
|-- README.rst
|-- __init__.py
|-- __manifest__.py
|-- exceptions.py
`-- hooks.py
```

OCA-specific vs standard Odoo: `readme/`, `examples/`, `hooks.py`, separate `data/` and `demo/` folders.

Filenames: `[a-z0-9_]` only. Permissions: folders 755, files 644.

## External Dependencies

### Manifest

```python
{
    'external_dependencies': {
        'bin': ['wkhtmltopdf'],
        'python': ['phonenumbers'],
    },
}
```

**Pinning:** No exact pins. Lower bound only for recent features (`lib>1.4`). Upper bound only for known incompatibilities.

### ImportError Handling

```python
try:
    import external_dependency_python_N
    EXTERNAL_DEPENDENCY_BINARY_N_PATH = tools.find_in_path('external_dependency_binary_N')
except (ImportError, IOError) as err:
    _logger.debug(err)
```

Not needed in test files. Not needed for Odoo >= v12 (unmet deps in uninstalled modules don't block).

Document install instructions in `README.rst` under `Installation`.

### oca_dependencies.txt

One OCA dependency per line:

```
sale-workflow
sale-workflow https://github.com/OCA/sale-workflow
sale-workflow https://github.com/OCA/sale-workflow branchname
sale-workflow https://github.com/OCA/sale-workflow branchname f848e37
```

## Tests

Bug fixes should include a test that fails without the fix. New modules should test all defined functions.

**Example modules** for feature showcases: name `module_name_example` — coverage analysis ignores them.

### Test with Lowest Permissions

Use `new_test_user` and `@users` to test under constrained permissions:

```python
from odoo.tests import TransactionCase, users, new_test_user

class TestSomething(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        new_test_user(cls.env, "test_portal", groups="base.group_portal")

    @users("test_portal")
    def test_something(self):
        ...
```

### Avoid Flaky Tests

**subTest pollution:** DB transaction and env cache aren't reset between subtests.

```python
# BAD: 2nd run fails with duplicate key
@users('admin', 'demo')
def test_something(self):
    self.env["res.users"].create({"name": "Foo", "login": "foo"})
```

**Env metadata on stored records:** Records in class/instance vars carry `.env` with cursor, uid, sudo, context that won't change when switching test users:

```python
# BAD: self.partner.env.uid != self.uid
self.assertRaises(AccessError, self.partner.read)

# GOOD: re-bind to current env
partner = self.partner.with_env(self.env)
self.assertRaises(AccessError, partner.read)
```

**Dynamic dates:** Use `freezegun` (Odoo dependency since 14.0):

```python
from freezegun import freeze_time

@freeze_time("2024-01-01 10:10:10")
def test_creation_time(self):
    partner = self.env["res.partner"].create({"name": "Foo"})
    self.assertEqual(partner.create_date, datetime(2024, 1, 1, 10, 10, 10))
```

**Mock external services:** Use `unittest.mock`, `cls.classPatch()`, `self.patch()`, or `self.startPatcher()`:

```python
from unittest.mock import patch

class TestSomething(TransactionCase):
    @patch("my_module.external_service")
    def test_something(self, mock_external_service):
        mock_external_service.return_value = "Some response"
        ...
```

For real service tests, tag with `-standard` and `external` (or `external_l10n`).

**Demo data:** Create test data within your suite; don't rely on demo data.

## Git Commit Messages

- Short summary ≤50 chars, no prefix: `This is a commit message`
- Body: specify module, reason. Lines ≤80 chars.
- English, present imperative (`Fix formatting`, not `Fixes`).
- One commit per logical change. No fix-up commits.
- Avoid commits spanning many modules; split by module.
- OCA-specific tag: **[MIG]** for module migration.
- If GitHub truncates with `[...]`, shorten it.

## Differences With Odoo Guidelines

- **Module Structure**: One file per model; separate `data/`/`demo/`; don't change xml_ids while inheriting; external deps handling; `hooks.py`.
- **XML**: Avoid current module name in xml_id; explicit `user_id` for `ir.filters`.
- **Python**: Fuller PEP8; relative imports; long comma-separated line breaks; no CamelCase model variables; uppercase constants.
- **SQL**: Don't bypass ORM; never commit transaction.
- **Fields**: Lambda defaults; default label string; inverse method pattern.
- **Tests**: Full section added.
- **Git**: No commit prefixing; squash in PRs; present imperative.

## Sources

- [OCA Contributing Guidelines](https://github.com/OCA/odoo-community.org/blob/master/website/Contribution/CONTRIBUTING.rst)
- [OCA Module Template](https://github.com/OCA/maintainer-tools/tree/master/template/module)
