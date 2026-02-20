# Scaffold script usage

The module scaffolder supports both interactive and non-interactive execution.

## Interactive mode

```bash
python3 scripts/scaffold.py
```

If no positional arguments are provided, the script asks for all required values.

## Positional arguments (optional)

```bash
python3 scripts/scaffold.py [odoo_version] [module_name] [location] [template_choice]
```

Order is fixed:
1. `odoo_version` (format: `X.Y`, example: `16.0`)
2. `module_name` (technical name, regex: `[a-z0-9_]+`)
3. `location` (destination parent directory)
4. `template_choice` (`1`, `2`, `basic_module`, or `advanced_module`)

If any trailing argument is missing, the script requests it interactively.

## Help

```bash
python3 scripts/scaffold.py --help
```

Shows command usage and accepted values.

## Examples

```bash
# Full non-interactive execution
python3 scripts/scaffold.py 16.0 my_custom_module . 1

# Using template name instead of number
python3 scripts/scaffold.py 16.0 my_custom_module /opt/odoo/addons advanced_module

# Partial args (prompts for missing values)
python3 scripts/scaffold.py 16.0 my_custom_module
```
