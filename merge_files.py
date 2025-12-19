#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 MERGE PROJECT FILES
================================================================================
Tool to merge multiple project code/configuration files into a single file.
================================================================================
"""

import os
import sys
import json
import argparse

# ═══════════════════════════════════════════════════════════════════════════
# ⚙️ DEFAULT CONFIGURATION (FALLBACK)
# ═══════════════════════════════════════════════════════════════════════════
# These settings will only be used if the 'merge_config.json' file
# is NOT found in the same directory.

DEFAULT_CONFIG = {
    "mandatory_dirs": [],
    "excluded_dirs": [
        'target', 'target-app', '.git', '.vscode', '__pycache__', 
        'node_modules', 'build', '.venv', 'windows-schema', 'gen'
    ],
    "excluded_file_prefixes": [
        'Insomnia', 'log', 'merge_files', 'merged_output', 
        'Cargo.lock', 'package-lock', 'data', 'mod', 
        'mock_bundle_registry', '.git', '.DS_Store'
    ],
    "just_file_prefixes": [],
    "search_keywords": [],
    "included_extensions": [
        '.rs', '.ts', '.tsx', '.css', '.json', '.toml', 
        '.html', '.py', '.txt', '.proto', '.lua', '.js'
    ],
    "project_description": "Default project description (Create merge_config.json to change).",
    "inline_comment_symbol": "//",
    "tree_settings": {
        "excluded_dirs": [
            'target', '.git', '.vscode', '__pycache__', 
            'node_modules', 'build', '.venv', 'windows-schema', 'gen', 'icons', 'data'
        ],
        "excluded_prefixes": [
            'gitignore', 'package-lock', 'merge_files', 'merged_output',
            'README', 'tauri_studio_structure', 'Cargo.lock', '.git'
        ],
        "just_prefixes": [],
        "included_extensions": [
             '.rs', '.ts', '.tsx', '.css', '.json', '.toml', '.html', '.py', '.txt', '.proto', '.js'
        ]
    }
}

CONFIG_FILENAME = "merge_config.json"

# ═══════════════════════════════════════════════════════════════════════════
# 🔧 HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def generate_config_file(output_path=None):
    """Generates a merge_config.json file with default settings."""
    if output_path is None:
        output_path = os.path.join(os.getcwd(), CONFIG_FILENAME)
    
    if os.path.exists(output_path):
        response = input(f"⚠️  File '{CONFIG_FILENAME}' already exists. Overwrite? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operation cancelled.")
            return False
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Configuration file generated successfully: {CONFIG_FILENAME}")
        print(f"📝 Edit this file to customize your merge settings.")
        return True
    except Exception as e:
        print(f"❌ Error generating configuration file: {e}")
        return False

def load_configuration(current_dir):
    """Loads config from JSON or returns default."""
    config_path = os.path.join(current_dir, CONFIG_FILENAME)
    
    if not os.path.exists(config_path):
        print(f"⚠️  File '{CONFIG_FILENAME}' not found. Using default script settings.")
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            print(f"📄 Loading configuration from: {CONFIG_FILENAME}")
            user_config = json.load(f)
            
            # Simple merge to ensure keys missing in JSON pick up the default
            final_config = DEFAULT_CONFIG.copy()
            final_config.update(user_config)
            
            # Specific merge for nested dictionary 'tree_settings'
            if 'tree_settings' in user_config:
                final_config['tree_settings'] = DEFAULT_CONFIG['tree_settings'].copy()
                final_config['tree_settings'].update(user_config['tree_settings'])
                
            return final_config
    except Exception as e:
        print(f"❌ Error reading '{CONFIG_FILENAME}': {e}")
        print("⚠️  Using default settings.")
        return DEFAULT_CONFIG

def _parse_prefixes(prefixes_input):
    """Converts different input formats (list or string) to a set."""
    if not prefixes_input:
        return None
    
    if isinstance(prefixes_input, list):
        # If coming from JSON as a list
        return set([os.path.normpath(p.strip()) for p in prefixes_input if p.strip()])
    elif isinstance(prefixes_input, str):
        # If coming as a comma-separated string
        prefixes = [os.path.normpath(p.strip()) for p in prefixes_input.split(',') if p.strip()]
        return set(prefixes) if prefixes else None
    else:
        return set([os.path.normpath(p) for p in prefixes_input]) if prefixes_input else None

def _ensure_tuple(data):
    """Ensures JSON lists become tuples for startswith/endswith checks."""
    if isinstance(data, list):
        return tuple(data)
    return data if data else ()

def _file_contains_keywords(file_path, keywords_set):
    """Checks if the file contains at least one of the keywords."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            return any(keyword.lower() in content for keyword in keywords_set)
    except Exception:
        return False

def _get_keywords_in_file(file_path, keywords_set):
    """Returns the list of keywords found in the file."""
    found_keywords = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            for keyword in keywords_set:
                if keyword.lower() in content:
                    found_keywords.append(keyword)
    except Exception:
        pass
    return sorted(found_keywords)


def merge_project_files(directory, output_file, config):
    output_filename = os.path.basename(output_file)
    script_filename = os.path.basename(__file__)
    
    print(f"🔍 Searching for files in: {directory}")
    print(f"📝 Output will be saved to: {output_filename}\n")

    # Extracting config to local variables for readability
    mandatory_dirs = _parse_prefixes(config.get('mandatory_dirs'))
    excluded_dirs = set(config.get('excluded_dirs', []))
    excluded_prefixes = _ensure_tuple(config.get('excluded_file_prefixes'))
    just_prefixes_set = _parse_prefixes(config.get('just_file_prefixes'))
    keywords_set = _parse_prefixes(config.get('search_keywords'))
    included_extensions = _ensure_tuple(config.get('included_extensions'))
    
    inline_comment = config.get('inline_comment_symbol', '//')
    proj_desc = config.get('project_description', '')

    # ─────────────────────────────────────────────────────────────────────
    # PHASE 1: Collecting files to merge
    # ─────────────────────────────────────────────────────────────────────
    found_files = []

    if mandatory_dirs:
        print(f"🚨 Mandatory Directories (Priority): {', '.join(sorted(mandatory_dirs))}")

    if keywords_set:
        print(f"🔍 Keyword filter active: {', '.join(sorted(keywords_set))}")
    
    skipped_by_keywords = 0
    
    for root, dirs, files in os.walk(directory, topdown=True):
        # Filters default excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        
        root_normalized = os.path.normpath(root)
        
        is_mandatory_path = False
        if mandatory_dirs:
            for m_dir in mandatory_dirs:
                if m_dir in root_normalized:
                    is_mandatory_path = True
                    break

        for file in files:
            # ✗ Always exclude: current script, output file, and config json
            if file == script_filename or file == output_filename or file == CONFIG_FILENAME:
                continue
            
            full_path = os.path.join(root, file)

            # 🚨 PRIORITY CHECK: If it is a mandatory directory
            if is_mandatory_path:
                if not file.startswith(('.DS_Store', '.git')): 
                    found_files.append(full_path)
                    continue 

            # --- NORMAL FILTERS ---

            # ✗ Exclude: prefixes
            if file.startswith(excluded_prefixes):
                continue
            
            # ✗ Exclude: extensions
            if not file.endswith(included_extensions):
                continue
            
            # ✗ Exclude: positive prefix filter
            if just_prefixes_set and not any(file.startswith(prefix) for prefix in just_prefixes_set):
                continue
            
            # ✗ Exclude: keyword filter
            if keywords_set:
                if not _file_contains_keywords(full_path, keywords_set):
                    skipped_by_keywords += 1
                    continue
            
            # ✅ File passed
            found_files.append(full_path)
    
    found_files.sort()
    
    print(f"✅ Found {len(found_files)} files to merge")
    if keywords_set and skipped_by_keywords > 0:
        print(f"   ({skipped_by_keywords} files ignored because they don't contain keywords)")
    print()

    # ─────────────────────────────────────────────────────────────────────
    # PHASE 2: Writing output file
    # ─────────────────────────────────────────────────────────────────────
    with open(output_file, 'w', encoding='utf-8') as outfile:
        
        if proj_desc:
            outfile.write(inline_comment + " PROJECT DESCRIPTION\n")
            outfile.write(inline_comment + "-" * 50 + "\n")
            for line in proj_desc.strip().splitlines():
                outfile.write(inline_comment + " " + line + "\n")
            outfile.write("\n" + inline_comment + "=" * 50 + "\n\n\n")
        
        if keywords_set:
            outfile.write(inline_comment + " KEYWORD FILTER ACTIVE\n")
            outfile.write(inline_comment + "-" * 50 + "\n")
            outfile.write(inline_comment + " Searching for: " + ", ".join(sorted(keywords_set)) + "\n")
            outfile.write("\n" + inline_comment + "=" * 50 + "\n\n\n")

        for file_path in found_files:
            relative_path = os.path.relpath(file_path, directory)
            
            outfile.write(inline_comment + "=" * 50 + "\n")
            outfile.write(inline_comment + relative_path + "\n")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    outfile.write(infile.read())
            except Exception as e:
                outfile.write(inline_comment + f" [ERROR READING FILE (Binary?): {e}]\n")
            
            outfile.write("\n\n")

        # ─────────────────────────────────────────────────────────────────
        # PHASE 3: Directory Tree
        # ─────────────────────────────────────────────────────────────────
        outfile.write(inline_comment + " PROJECT DIRECTORY TREE\n")
        outfile.write(inline_comment + "-" * 50 + "\n")
        
        tree = {}
        files_keywords_map = {}
        
        # Tree settings
        tree_conf = config.get('tree_settings', {})
        excl_dirs_tree = set(tree_conf.get('excluded_dirs', []))
        excl_prefixes_tree = _ensure_tuple(tree_conf.get('excluded_prefixes'))
        just_prefixes_tree = _parse_prefixes(tree_conf.get('just_prefixes'))
        incl_ext_tree = _ensure_tuple(tree_conf.get('included_extensions'))

        for root, dirs, files in os.walk(directory, topdown=True):
            dirs[:] = [d for d in dirs if d not in excl_dirs_tree]
            
            relative_root = os.path.relpath(root, directory)
            current_node = tree
            if relative_root != ".":
                parts = relative_root.split(os.sep)
                for part in parts:
                    current_node = current_node.setdefault(part, {})
            
            for d in dirs:
                current_node.setdefault(d, {})
            
            for file in files:
                if file == script_filename or file == output_filename or file == CONFIG_FILENAME:
                    continue
                
                # Tree filters
                if file.startswith(excl_prefixes_tree):
                    continue
                if incl_ext_tree and not file.endswith(incl_ext_tree):
                    continue
                if just_prefixes_tree and not any(file.startswith(prefix) for prefix in just_prefixes_tree):
                    continue
                
                current_node[file] = None
                
                if keywords_set:
                    full_path = os.path.join(root, file)
                    found_keywords = _get_keywords_in_file(full_path, keywords_set)
                    if found_keywords:
                        rel_path = os.path.relpath(full_path, directory)
                        files_keywords_map[rel_path] = found_keywords

        def print_tree(node, prefix, current_path=""):
            keys = sorted(node.keys())
            for i, key in enumerate(keys):
                is_last = i == (len(keys) - 1)
                connector = "└── " if is_last else "├── "
                
                is_directory = (node[key] is not None)
                
                if not is_directory:
                    file_path = os.path.join(current_path, key) if current_path else key
                    if file_path in files_keywords_map:
                        keywords_str = ",".join(files_keywords_map[file_path])
                        marker = f"  ({keywords_str})"
                    else:
                        marker = ""
                    
                    outfile.write(inline_comment + " " + prefix + connector + key + marker + "\n")
                else:
                    outfile.write(inline_comment + " " + prefix + connector + key + "/\n")
                    if node[key] != {}:
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        next_path = os.path.join(current_path, key) if current_path else key
                        print_tree(node[key], next_prefix, next_path)

        root_name = os.path.basename(os.path.abspath(directory))
        outfile.write(inline_comment + " " + root_name + "/\n")
        print_tree(tree, "", "")
        outfile.write("\n" + inline_comment + "=" * 50 + "\n\n")
    
    print(f"✅ File generated successfully: {output_filename}")
    print(f"📊 Size: {os.path.getsize(output_file) / 1024:.2f} KB")


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='🔗 Merge Project Files - Combine multiple project files into a single output',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python merge_files.py                    # Run merge with current settings
  python merge_files.py --generate-config  # Generate merge_config.json template
  python merge_files.py -g                 # Short form to generate config
        """
    )
    
    parser.add_argument(
        '-g', '--generate-config',
        action='store_true',
        help='Generate a merge_config.json file with default settings'
    )
    
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    # If user wants to generate config file
    if args.generate_config:
        print("=" * 70)
        print("⚙️  GENERATING CONFIGURATION FILE")
        print("=" * 70 + "\n")
        generate_config_file()
        sys.exit(0)
    
    # Normal merge operation
    current_dir = os.getcwd()
    dir_name = os.path.basename(current_dir)
    output_name = f"merged_output_{dir_name}.txt"
    output_path = os.path.join(current_dir, output_name)
    
    try:
        print("=" * 70)
        print("🔗 MERGE PROJECT FILES v3.1.0")
        print("=" * 70 + "\n")

        # 1. Load configuration
        config = load_configuration(current_dir)

        if os.path.exists(output_path):
            print(f"🧹 Removing previous output file: {output_name}")
            os.remove(output_path)
        
        # 2. Execute merge passing config object
        merge_project_files(current_dir, output_path, config)
        
        print("\n" + "=" * 70)
        print("✅ Process completed successfully!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}", file=sys.stderr)
        sys.exit(1)