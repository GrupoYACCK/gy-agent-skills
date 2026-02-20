#!/usr/bin/env python3
import os
import shutil
import re
import sys


MODULE_NAME_RE = re.compile(r"^[a-z0-9_]+$")
ODOO_VERSION_RE = re.compile(r"^\d+\.\d+$")
TEMPLATE_CHOICES = {"1": "basic_module", "2": "advanced_module"}


def print_help():
    print("Usage: scaffold.py [odoo_version] [module_name] [location] [template_choice]")
    print("")
    print("Positional arguments (all optional, in order):")
    print("  odoo_version     Odoo major version in X.Y format (example: 16.0)")
    print("  module_name      Technical module name ([a-z0-9_]+)")
    print("  location         Destination parent path (default: current directory)")
    print("  template_choice  1|2|basic_module|advanced_module")
    print("")
    print("If any argument is missing, it is requested interactively.")
    print("Options:")
    print("  -h, --help       Show this help message and exit")

def prompt_user(prompt_msg, default=""):
    if default:
        res = input(f"{prompt_msg} [{default}]: ").strip()
        return res if res else default
    else:
        while True:
            res = input(f"{prompt_msg}: ").strip()
            if res:
                return res
            print("This field is required.")


def prompt_validated(prompt_msg, validator, error_msg, default=""):
    while True:
        value = prompt_user(prompt_msg, default)
        if validator(value):
            return value
        print(error_msg)


def normalize_template_choice(value):
    if value in TEMPLATE_CHOICES:
        return value
    reverse_map = {name: key for key, name in TEMPLATE_CHOICES.items()}
    return reverse_map.get(value)

def main():
    print("=== Odoo Module Scaffolding ===")

    args = sys.argv[1:]
    if any(arg in {"-h", "--help"} for arg in args):
        print_help()
        return 0

    if len(args) > 4:
        print_help()
        return 1

    odoo_version_arg = args[0] if len(args) > 0 else ""
    module_name_arg = args[1] if len(args) > 1 else ""
    location_arg = args[2] if len(args) > 2 else ""
    template_choice_arg = args[3] if len(args) > 3 else ""
    
    # Prompts
    if odoo_version_arg:
        if not ODOO_VERSION_RE.fullmatch(odoo_version_arg):
            print("Invalid Odoo version. Use format like 16.0")
            return 1
        odoo_version = odoo_version_arg
    else:
        odoo_version = prompt_validated(
            "Odoo Version (e.g., 16.0)",
            lambda value: bool(ODOO_VERSION_RE.fullmatch(value)),
            "Invalid Odoo version. Use format like 16.0",
            "16.0",
        )

    if module_name_arg:
        if not MODULE_NAME_RE.fullmatch(module_name_arg):
            print(
                "Invalid module name. Use only lowercase letters, numbers and underscores."
            )
            return 1
        module_name = module_name_arg
    else:
        module_name = prompt_validated(
            "Module Name (tech name, e.g., my_module)",
            lambda value: bool(MODULE_NAME_RE.fullmatch(value)),
            "Invalid module name. Use only lowercase letters, numbers and underscores.",
        )

    location = location_arg if location_arg else prompt_user("Module Location path", ".")

    print("Available templates:")
    print("  1 - Basic (minimal models and views)")
    print("  2 - Advanced (includes portals, controllers, security, etc.)")

    normalized_choice = normalize_template_choice(template_choice_arg)
    if template_choice_arg and normalized_choice:
        template_name = TEMPLATE_CHOICES[normalized_choice]
    elif template_choice_arg:
        print("Invalid template choice. Use 1, 2, basic_module or advanced_module")
        return 1
    else:
        while True:
            choice = prompt_user("Select template (1/2)", "1")
            normalized_choice = normalize_template_choice(choice)
            if normalized_choice:
                template_name = TEMPLATE_CHOICES[normalized_choice]
                break
            print("Invalid choice.")
        
    human_name = module_name.replace("_", " ").title()

    # Determine paths
    script_dir = os.path.dirname(os.path.realpath(__file__))
    assets_dir = os.path.join(os.path.dirname(script_dir), "assets")
    template_dir = os.path.join(assets_dir, template_name)
    
    if not os.path.exists(template_dir):
        print(f"Error: Template directory {template_dir} does not exist.")
        return

    dest_dir = os.path.join(os.path.abspath(location), module_name)
    
    if os.path.exists(dest_dir):
        print(f"Error: Destination directory {dest_dir} already exists.")
        return
        
    print(f"\nCreating module '{module_name}' in {dest_dir}...")
    shutil.copytree(template_dir, dest_dir)
    
    # Update manifest
    manifest_path = os.path.join(dest_dir, "__manifest__.py")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest_content = f.read()
            
        # Replace versions and names
        manifest_content = re.sub(r'"version"\s*:\s*".*?"', f'"version": "{odoo_version}.1.0.0"', manifest_content)
        manifest_content = re.sub(r'"name"\s*:\s*".*?"', f'"name": "{human_name}"', manifest_content)
        manifest_content = re.sub(r'"summary"\s*:\s*".*?"', f'"summary": "Summary for {human_name}"', manifest_content)
        
        with open(manifest_path, "w", encoding="utf-8") as f:
            f.write(manifest_content)
            
    print("Module created successfully!")
    print("Remember to adjust __manifest__.py (author, depends, data) and rename files to match your model names.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
