#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🔗 MERGE PROJECT FILES
================================================================================
A CLI tool to merge multiple files into a single file.md
================================================================================
"""

import os
import sys
import json
import argparse
import re

# ═══════════════════════════════════════════════════════════════════════════
# ⚙️ DEFAULT CONFIGURATION (FALLBACK)
# ═══════════════════════════════════════════════════════════════════════════

DEFAULT_CONFIG = {
    "mandatory_dirs": [],
    "excluded_dirs": [
        "target",
        "target-app",
        ".git",
        ".vscode",
        "__pycache__",
        "node_modules",
        "build",
        ".venv",
        "windows-schema",
        "gen",
        "dist",
        "coverage"
    ],
    "excluded_file_prefixes": [
        "merged_output",
        "Cargo.lock",
        "package-lock",
        "yarn.lock",
        "pnpm-lock",
        "data",
        "mock_bundle_registry",
        ".git",
        ".DS_Store",
        "readme",
        "README"
    ],
    "just_file_prefixes": [],
    "just_file_contain": [],
    "any_file_prefixes": [],
    "any_file_contain": [],
    "search_keywords": [],
    "included_extensions": [
        ".rs",
        ".ts",
        ".tsx",
        ".css",
        ".scss",
        ".json",
        ".toml",
        ".yaml",
        ".yml",
        ".html",
        ".py",
        ".txt",
        ".proto",
        ".lua",
        ".js",
        ".jsx",
        ".sql",
        ".sh",
        ".ps1"
    ],
    "project_description": "Default project description",
    "sanitize_secrets": {
        "enabled": True,
        "patterns": [
            {
                "name": "API Keys (generic)",
                "regex": "(api[_-]?key|apikey|api[_-]?secret)\\s*[:=]\\s*['\"]([^'\"]{8,})['\"]",
                "replacement": "\\1 = \"********\""
            },
            {
                "name": "Tokens & Bearer",
                "regex": "(token|bearer|jwt|auth[_-]?token|access[_-]?token)\\s*[:=]\\s*['\"]([^'\"]{8,})['\"]",
                "replacement": "\\1 = \"********\""
            },
            {
                "name": "Passwords",
                "regex": "(password|passwd|pwd|secret|pass)\\s*[:=]\\s*['\"]([^'\"]+)['\"]",
                "replacement": "\\1 = \"********\""
            },
            {
                "name": "AWS Keys",
                "regex": "(aws[_-]?access[_-]?key[_-]?id|aws[_-]?secret[_-]?access[_-]?key)\\s*[:=]\\s*['\"]([^'\"]+)['\"]",
                "replacement": "\\1 = \"********\""
            },
            {
                "name": "Database URLs with credentials",
                "regex": "(mongodb|postgres|mysql|redis|mariadb)://([^:]+):([^@]+)@",
                "replacement": "\\1://USERNAME:********@"
            },
            {
                "name": "Connection Strings",
                "regex": "(connection[_-]?string|database[_-]?url|db[_-]?url)\\s*[:=]\\s*['\"]([^'\"]+)['\"]",
                "replacement": "\\1 = \"********\""
            },
            {
                "name": "Private Keys",
                "regex": "-----BEGIN[\\s\\S]*?PRIVATE KEY-----[\\s\\S]*?-----END[\\s\\S]*?PRIVATE KEY-----",
                "replacement": "-----BEGIN PRIVATE KEY-----\\n[REDACTED]\\n-----END PRIVATE KEY-----"
            },
            {
                "name": "GitHub Tokens",
                "regex": "(ghp|gho|ghu|ghs|ghr)_[a-zA-Z0-9]{36,}",
                "replacement": "gh*_********"
            },
            {
                "name": "Stripe Keys",
                "regex": "(sk|pk)_(test|live)_[a-zA-Z0-9]{24,}",
                "replacement": "\\1_\\2_********"
            },
            {
                "name": "OpenAI API Keys",
                "regex": "sk-[a-zA-Z0-9]{48,}",
                "replacement": "sk-********"
            },
            {
                "name": "Generic Secrets in ENV format",
                "regex": "^([A-Z_]+_(?:SECRET|KEY|TOKEN|PASSWORD|PASS))\\s*=\\s*(.+)$",
                "replacement": "\\1=********"
            },
            {
                "name": "JWT Tokens",
                "regex": "eyJ[a-zA-Z0-9_-]{10,}\\.[a-zA-Z0-9_-]{10,}\\.[a-zA-Z0-9_-]{10,}",
                "replacement": "eyJ******.*******.******"
            },
            {
                "name": "URLs with Basic Auth",
                "regex": "https?://([^:]+):([^@]+)@",
                "replacement": "https://USERNAME:********@"
            },
            {
                "name": "Kafka SASL Username",
                "regex": "(['\"]sasl\\.username['\"]\\s*:\\s*['\"])([^'\"]+)(['\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "Kafka SASL Password",
                "regex": "(['\"]sasl\\.password['\"]\\s*:\\s*['\"])([^'\"]+)(['\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "Generic username in dict",
                "regex": "(['\"]username['\"]\\s*:\\s*['\"])([^'\"]+)(['\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "Generic password in dict",
                "regex": "(['\"]password['\"]\\s*:\\s*['\"])([^'\"]+)(['\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "Token assignments (short tokens)",
                "regex": "(token_?\\s*=\\s*[\\(\\'\"])([a-zA-Z0-9]{8,})([\\)\\'\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "RabbitMQ credentials",
                "regex": "(['\"](?:username|password)['\"]\\s*:\\s*['\"])([^'\"]+)(['\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "MQTT credentials",
                "regex": "(['\"](?:username|password)['\"]\\s*:\\s*['\"])([^'\"]+)(['\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "HTTP Auth tuples",
                "regex": "http_auth[\\s]*=[\\s]*\\([\\s]*['\"]([^'\"]+)['\"][\\s]*,[\\s]*['\"]([^'\"]+)['\"][\\s]*\\)",
                "replacement": "http_auth = ('USERNAME', '********')"
            },
            {
                "name": "Auth Provider tuples",
                "regex": "auth_provider[\\s]*=[\\s]*\\([\\s]*['\"]([^'\"]+)['\"][\\s]*,[\\s]*['\"]([^'\"]+)['\"][\\s]*\\)",
                "replacement": "auth_provider = ('USERNAME', '********')"
            },
            {
                "name": "Client Secret in dict",
                "regex": "(['\"]client_secret['\"]\\s*:\\s*['\"])([^'\"]+)(['\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "User field in dict",
                "regex": "(['\"]user['\"]\\s*:\\s*['\"])([^'\"]+)(['\"])",
                "replacement": "\\1********\\3"
            },
            {
                "name": "Commented credentials (still visible)",
                "regex": "#\\s*(sasl\\.(username|password)|password|api[_-]?key)\\s*[=:]\\s*['\"]([^'\"]+)['\"]",
                "replacement": "# \\1 = '********'"
            }
        ],
        "custom_keywords": [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "STRIPE_SECRET_KEY",
            "STRIPE_PUBLISHABLE_KEY",
            "DATABASE_PASSWORD",
            "DB_PASSWORD",
            "POSTGRES_PASSWORD",
            "MYSQL_PASSWORD",
            "REDIS_PASSWORD",
            "JWT_SECRET",
            "SESSION_SECRET",
            "ENCRYPTION_KEY",
            "PRIVATE_KEY",
            "CLIENT_SECRET",
            "MASTER_KEY",
            "ADMIN_PASSWORD",
            "KAFKA_USERNAME",
            "KAFKA_PASSWORD",
            "SASL_USERNAME",
            "SASL_PASSWORD",
            "RABBITMQ_USER",
            "RABBITMQ_PASS",
            "MQTT_USERNAME",
            "MQTT_PASSWORD",
            "ELASTIC_USER",
            "ELASTIC_PASSWORD",
            "INFLUX_USER",
            "INFLUX_PASSWORD",
            "CASSANDRA_USER",
            "CASSANDRA_PASSWORD"
        ]
    },
    "tree_settings": {
        "excluded_dirs": [
            "target",
            ".git",
            ".vscode",
            "__pycache__",
            "node_modules",
            "build",
            ".venv",
            "windows-schema",
            "gen",
            "icons",
            "data"
        ],
        "excluded_prefixes": [
            "gitignore",
            "package-lock",
            "merge_files",
            "merged_output",
            "README",
            "tauri_studio_structure",
            "Cargo.lock",
            ".git"
        ],
        "just_prefixes": [],
        "just_file_contain": [],
        "any_file_prefixes": [],
        "any_file_contain": [],
        "included_extensions": [
            ".rs",
            ".ts",
            ".tsx",
            ".css",
            ".scss",
            ".json",
            ".toml",
            ".yaml",
            ".yml",
            ".html",
            ".py",
            ".txt",
            ".proto",
            ".lua",
            ".js",
            ".jsx",
            ".md",
            ".sql",
            ".sh",
            ".ps1"
        ]
    }
}

CONFIG_FILENAME = "merge_config.json"

COMMENT_MAP = {
    # Scripts & Configs
    '.py': '# {}',
    '.sh': '# {}',
    '.ps1': '# {}',
    '.yaml': '# {}',
    '.yml': '# {}',
    '.toml': '# {}',
    '.rb': '# {}',
    '.dockerfile': '# {}',
    
    # C-Style Languages
    '.rs': '// {}',
    '.js': '// {}',
    '.jsx': '// {}',
    '.ts': '// {}',
    '.tsx': '// {}',
    '.go': '// {}',
    '.c': '// {}',
    '.cpp': '// {}',
    '.h': '// {}',
    '.java': '// {}',
    '.kt': '// {}',
    '.kts': '// {}',
    '.swift': '// {}',
    '.proto': '// {}',
    '.php': '// {}',
    '.dart': '// {}',
    '.cs': '// {}',
    '.scala': '// {}',
    
    # Infrastructure & Data
    '.tf': '# {}',
    '.tfvars': '# {}',
    '.lua': '-- {}',
    '.sql': '-- {}',
    '.hs': '-- {}',
    
    # Styling (CSS/Sass use /* */ for safety in minifiers)
    '.css': '/* {} */',
    '.scss': '/* {} */',
    '.sass': '/* {} */',
    '.less': '/* {} */',
    
    # Specialized
    '.vue': '',
    '.html': '',
    '.xml': '',
    '.md': '[//]: # ({})',
}

# ═══════════════════════════════════════════════════════════════════════════
# 🔧 HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════════

def sanitize_content(content, sanitize_config, file_path=""):
    """
    🔐 Remove sensitive information from content.
    Returns: (sanitized_content, list_of_replacements_made)
    """
    if not sanitize_config.get('enabled', False):
        return content, []
    
    sanitized = content
    replacements_made = []
    
    # 1. Apply regex patterns
    for pattern_config in sanitize_config.get('patterns', []):
        try:
            pattern = pattern_config['regex']
            replacement = pattern_config['replacement']
            name = pattern_config.get('name', 'Unknown pattern')
            
            # Count matches before replacement
            matches = re.findall(pattern, sanitized, re.IGNORECASE | re.MULTILINE)
            if matches:
                sanitized = re.sub(pattern, replacement, sanitized, flags=re.IGNORECASE | re.MULTILINE)
                count = len(matches) if isinstance(matches[0], str) else len(matches)
                replacements_made.append(f"{name} ({count}x)")
        except re.error as e:
            print(f"⚠️  Invalid regex in pattern '{pattern_config.get('name')}': {e}")
            continue
    
    # 2. Apply custom keywords (simple value replacement)
    for keyword in sanitize_config.get('custom_keywords', []):
        pattern = f'({re.escape(keyword)})\\s*[:=]\\s*["\']([^"\']+)["\']'
        matches = re.findall(pattern, sanitized, re.IGNORECASE)
        if matches:
            sanitized = re.sub(pattern, r'\1 = "********"', sanitized, flags=re.IGNORECASE)
            replacements_made.append(f"Keyword '{keyword}'")
    
    return sanitized, replacements_made

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
        print(f"🔐 Secret sanitization is ENABLED by default for security.")
        return True
    except Exception as e:
        print(f"❌ Error generating configuration file: {e}")
        return False

def load_configuration(current_dir, custom_config_path=None):
    """Loads config from JSON or returns default."""
    if custom_config_path:
        config_path = custom_config_path
    else:
        config_path = os.path.join(current_dir, CONFIG_FILENAME)
    
    if not os.path.exists(config_path):
        if custom_config_path:
            print(f"❌ Custom config file '{custom_config_path}' not found!")
            sys.exit(1)
        print(f"⚠️  File '{CONFIG_FILENAME}' not found. Using default script settings.")
        return DEFAULT_CONFIG
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            print(f"📄 Loading configuration from: {config_path}")
            user_config = json.load(f)
            
            final_config = DEFAULT_CONFIG.copy()
            final_config.update(user_config)
            
            if 'tree_settings' in user_config:
                final_config['tree_settings'] = DEFAULT_CONFIG['tree_settings'].copy()
                final_config['tree_settings'].update(user_config['tree_settings'])
            
            # Merge sanitize_secrets to preserve default patterns
            if 'sanitize_secrets' in user_config:
                default_sanitize = DEFAULT_CONFIG['sanitize_secrets'].copy()
                user_sanitize = user_config['sanitize_secrets']
                
                if 'enabled' in user_sanitize:
                    default_sanitize['enabled'] = user_sanitize['enabled']
                
                if 'patterns' in user_sanitize:
                    default_sanitize['patterns'].extend(user_sanitize['patterns'])
                
                if 'custom_keywords' in user_sanitize:
                    default_sanitize['custom_keywords'].extend(user_sanitize['custom_keywords'])
                    default_sanitize['custom_keywords'] = list(set(default_sanitize['custom_keywords']))
                
                final_config['sanitize_secrets'] = default_sanitize
                
            return final_config
    except Exception as e:
        print(f"❌ Error reading '{config_path}': {e}")
        print("⚠️  Using default settings.")
        return DEFAULT_CONFIG

def _parse_prefixes(prefixes_input):
    if not prefixes_input: return None
    if isinstance(prefixes_input, list):
        return set([os.path.normpath(p.strip()) for p in prefixes_input if p.strip()])
    elif isinstance(prefixes_input, str):
        prefixes = [os.path.normpath(p.strip()) for p in prefixes_input.split(',') if p.strip()]
        return set(prefixes) if prefixes else None
    else:
        return set([os.path.normpath(p) for p in prefixes_input]) if prefixes_input else None

def _ensure_tuple(data):
    if isinstance(data, list): return tuple(data)
    return data if data else ()

def _file_contains_keywords(file_path, keywords_set):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            return any(keyword.lower() in content for keyword in keywords_set)
    except Exception:
        return False

def _get_keywords_in_file(file_path, keywords_set):
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

def _get_markdown_language(filename):
    """Maps file extension to Markdown language identifier for syntax highlighting."""
    ext = os.path.splitext(filename)[1].lower()
    mapping = {
        '.py': 'python',
        '.rs': 'rust',
        '.js': 'javascript', '.jsx': 'javascript',
        '.ts': 'typescript', '.tsx': 'typescript',
        '.html': 'html',
        '.css': 'css', '.scss': 'scss',
        '.json': 'json',
        '.md': 'markdown',
        '.yaml': 'yaml', '.yml': 'yaml',
        '.toml': 'toml',
        '.sh': 'bash', '.zsh': 'bash', '.bat': 'batch',
        '.lua': 'lua',
        '.c': 'c', '.cpp': 'cpp', '.h': 'cpp',
        '.sql': 'sql',
        '.java': 'java',
        '.go': 'go',
        '.rb': 'ruby',
        '.php': 'php',
        '.xml': 'xml',
        '.proto': 'protobuf',
        '.dockerfile': 'dockerfile',
        '.txt': 'text',
        '.tf': 'terraform', '.tfvars': 'terraform',
        '.kt': 'kotlin', '.kts': 'kotlin',
        '.swift': 'swift',
        '.dart': 'dart',
        '.cs': 'csharp',
        '.vue': 'vue'
    }
    # Special case for files like 'Dockerfile' with no extension
    if filename.lower() == 'dockerfile': return 'dockerfile'
    if filename.lower() == 'makefile': return 'makefile'
    
    return mapping.get(ext, '')


def tag_original_files(file_list, base_directory):
    """
    Adiciona ou atualiza um comentário com o caminho relativo no topo dos arquivos.
    - Ignora arquivos com Shebang (#!).
    - Substitui tags antigas se o arquivo foi renomeado.
    """
    print(f"🏷️  Tagging/Updating {len(file_list)} original files...")
    tagged_count = 0
    ignored_shebang = 0
    
    for file_path in file_list:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in COMMENT_MAP:
            continue
            
        rel_path = os.path.relpath(file_path, base_directory)
        comment_template = COMMENT_MAP[ext]
        
        # Cria um Regex para detectar se a primeira linha já é uma tag (independente do caminho)
        # Ex: se o template é "// {}", o regex vira "^// .*"
        regex_tag_pattern = "^" + re.escape(comment_template).replace(r'\{\}', r'.*') + "$"
        tag_line = comment_template.format(rel_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content_lines = f.readlines()
            
            if not content_lines:
                continue

            first_line = content_lines[0].strip()

            # 1. Ignorar se houver Shebang
            if first_line.startswith("#!"):
                ignored_shebang += 1
                continue

            # 2. Verificar se a primeira linha já é uma tag deste script
            is_old_tag = re.match(regex_tag_pattern, first_line)
            
            if is_old_tag:
                # Se a tag já está correta, não faz nada
                if first_line == tag_line:
                    continue
                # Se a tag existe mas o caminho mudou, removemos a linha antiga
                remaining_content = "".join(content_lines[1:])
            else:
                # Se não tem tag, preservamos o arquivo todo
                remaining_content = "".join(content_lines)

            # Escrever a nova tag e o conteúdo
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(tag_line + "\n" + remaining_content)
            
            tagged_count += 1
            
        except Exception as e:
            print(f"⚠️  Could not tag file {rel_path}: {e}")
            
    if ignored_shebang > 0:
        print(f"ℹ️  Ignored {ignored_shebang} files with Shebang (#!).")
    print(f"✅ Tagging complete. {tagged_count} files updated/corrected.\n")

# ═══════════════════════════════════════════════════════════════════════════
# 🚀 MAIN MERGE FUNCTION
# ═══════════════════════════════════════════════════════════════════════════

def merge_project_files(directory, output_file, config, tag_files=False):
    output_filename = os.path.basename(output_file)
    script_filename = os.path.basename(__file__)
    
    print(f"🔍 Searching for files in: {directory}")
    print(f"📝 Output will be saved to: {output_filename}\n")

    # Config extraction
    mandatory_dirs = _parse_prefixes(config.get('mandatory_dirs'))
    excluded_dirs = set(config.get('excluded_dirs', []))
    excluded_prefixes = _ensure_tuple(config.get('excluded_file_prefixes'))
    just_prefixes_set = _parse_prefixes(config.get('just_file_prefixes'))
    just_contain_set = _parse_prefixes(config.get('just_file_contain'))
    any_prefixes_set = _parse_prefixes(config.get('any_file_prefixes'))
    any_contain_set = _parse_prefixes(config.get('any_file_contain'))
    keywords_set = _parse_prefixes(config.get('search_keywords'))
    included_extensions = _ensure_tuple(config.get('included_extensions'))
    proj_desc = config.get('project_description', '')
    sanitize_config = config.get('sanitize_secrets', {})

    # Show sanitization status
    if sanitize_config.get('enabled', False):
        print("🔐 Secret sanitization: ENABLED")
        print(f"   - {len(sanitize_config.get('patterns', []))} regex patterns active")
        print(f"   - {len(sanitize_config.get('custom_keywords', []))} custom keywords monitored\n")
    else:
        print("⚠️  Secret sanitization: DISABLED\n")

    # PHASE 1: Collecting files
    # ─────────────────────────────────────────────────────────────────────
    found_files = []

    if mandatory_dirs:
        print(f"🚨 Mandatory Directories (Priority): {', '.join(sorted(mandatory_dirs))}")
    if keywords_set:
        print(f"🔍 Keyword filter active: {', '.join(sorted(keywords_set))}")
    
    skipped_by_keywords = 0
    
    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in excluded_dirs]
        root_normalized = os.path.normpath(root)
        
        is_mandatory_path = False
        if mandatory_dirs:
            for m_dir in mandatory_dirs:
                if m_dir in root_normalized:
                    is_mandatory_path = True
                    break

        for file in files:
            if file == script_filename or file == output_filename or file == CONFIG_FILENAME:
                continue
            
            full_path = os.path.join(root, file)

            # Priority Check
            if is_mandatory_path:
                found_files.append(full_path)
                continue 

            # Normal Filters
            if file.startswith(excluded_prefixes): continue
            if not file.endswith(included_extensions): continue
            
            # Logic for JUST filters (High Priority)
            if (just_prefixes_set or just_contain_set):
                match_just = False
                if just_prefixes_set and any(file.startswith(prefix) for prefix in just_prefixes_set):
                    match_just = True
                if just_contain_set and any(sub.lower() in file.lower() for sub in just_contain_set):
                    match_just = True
                
                if not match_just:
                    continue
            
            # Logic for ANY filters (Lower Priority)
            elif (any_prefixes_set or any_contain_set):
                match_any = False
                if any_prefixes_set and any(file.startswith(prefix) for prefix in any_prefixes_set):
                    match_any = True
                if any_contain_set and any(sub.lower() in file.lower() for sub in any_contain_set):
                    match_any = True
                
                if not match_any:
                    continue
            
            if keywords_set:
                if not _file_contains_keywords(full_path, keywords_set):
                    skipped_by_keywords += 1
                    continue
            
            found_files.append(full_path)
    
    found_files.sort()
    
    print(f"✅ Found {len(found_files)} files to merge")
    if keywords_set and skipped_by_keywords > 0:
        print(f"   ({skipped_by_keywords} files ignored because they don't contain keywords)")
    print()

    if tag_files:
        tag_original_files(found_files, directory)

    # ─────────────────────────────────────────────────────────────────────
    # PHASE 2: Writing output file (MARKDOWN FORMAT)
    # ─────────────────────────────────────────────────────────────────────
    total_sanitized_files = 0
    total_replacements = 0
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        
        # 1. Project Header
        if proj_desc:
            outfile.write(f"# PROJECT DESCRIPTION\n\n")
            outfile.write(f"{proj_desc.strip()}\n\n")
            outfile.write("---\n\n")

        # ─────────────────────────────────────────────────────────────────
        # 2. Directory Tree
        # ─────────────────────────────────────────────────────────────────
        outfile.write("# PROJECT DIRECTORY TREE\n\n")
        outfile.write("```text\n") # Start text block for tree
        
        tree = {}
        files_keywords_map = {}
        
        tree_conf = config.get('tree_settings', {})
        excl_dirs_tree = set(tree_conf.get('excluded_dirs', []))
        excl_prefixes_tree = _ensure_tuple(tree_conf.get('excluded_prefixes'))
        just_prefixes_tree = _parse_prefixes(tree_conf.get('just_prefixes'))
        just_contain_tree = _parse_prefixes(tree_conf.get('just_file_contain'))
        any_prefixes_tree = _parse_prefixes(tree_conf.get('any_file_prefixes'))
        any_contain_tree = _parse_prefixes(tree_conf.get('any_file_contain'))
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
                
                if file.startswith(excl_prefixes_tree): continue
                if incl_ext_tree and not file.endswith(incl_ext_tree): continue
                
                # Tree Filter Logic (Matching main merge logic)
                if (just_prefixes_tree or just_contain_tree):
                    match_just = False
                    if just_prefixes_tree and any(file.startswith(prefix) for prefix in just_prefixes_tree):
                        match_just = True
                    if just_contain_tree and any(sub.lower() in file.lower() for sub in just_contain_tree):
                        match_just = True
                    if not match_just: continue
                
                elif (any_prefixes_tree or any_contain_tree):
                    match_any = False
                    if any_prefixes_tree and any(file.startswith(prefix) for prefix in any_prefixes_tree):
                        match_any = True
                    if any_contain_tree and any(sub.lower() in file.lower() for sub in any_contain_tree):
                        match_any = True
                    if not match_any: continue

                current_node[file] = None
                
                if keywords_set:
                    full_path = os.path.join(root, file)
                    found_keywords = _get_keywords_in_file(full_path, keywords_set)
                    if found_keywords:
                        rel_path = os.path.relpath(full_path, directory)
                        files_keywords_map[rel_path] = found_keywords

        def print_tree(node, prefix, current_path=""):
            keys = sorted(node.keys())
            # Cleanup empty directory nodes after filtering
            keys = [k for k in keys if node[k] is not None or (node[k] is None)]
            
            for i, key in enumerate(keys):
                is_last = i == (len(keys) - 1)
                connector = "└── " if is_last else "├── "
                
                is_directory = (node[key] is not None)
                
                if not is_directory:
                    file_path = os.path.join(current_path, key) if current_path else key
                    marker = ""
                    if file_path in files_keywords_map:
                        keywords_str = ",".join(files_keywords_map[file_path])
                        marker = f"  (* {keywords_str})"
                    
                    outfile.write(f"{prefix}{connector}{key}{marker}\n")
                else:
                    if node[key] == {} and (just_prefixes_tree or just_contain_tree or any_prefixes_tree or any_contain_tree):
                        # Skip empty folders when filtering files
                        continue
                        
                    outfile.write(f"{prefix}{connector}{key}/\n")
                    if node[key] != {}:
                        next_prefix = prefix + ("    " if is_last else "│   ")
                        next_path = os.path.join(current_path, key) if current_path else key
                        print_tree(node[key], next_prefix, next_path)

        root_name = os.path.basename(os.path.abspath(directory))
        outfile.write(f"{root_name}/\n")
        print_tree(tree, "", "")
        outfile.write("```\n\n") # End text block
        outfile.write("---\n\n")
        
        # 3. Security Notice
        if sanitize_config.get('enabled', False):
            outfile.write("> 🔐 **SECURITY NOTICE**\n")
            outfile.write("> This document has been processed with secret sanitization.\n")
            outfile.write("> Sensitive information (passwords, API keys, tokens) has been replaced with `********`.\n\n")
            outfile.write("---\n\n")
        
        # 4. Keyword Info
        if keywords_set:
            outfile.write("> ⚠️ **KEYWORD FILTER ACTIVE**\n")
            outfile.write(f"> Searching for: `{', '.join(sorted(keywords_set))}`\n\n")
            outfile.write("---\n\n")
        
        # 5. Files Content
        for file_path in found_files:
            relative_path = os.path.relpath(file_path, directory)
            filename = os.path.basename(file_path)
            lang = _get_markdown_language(filename)
            
            outfile.write(f"## File: `{relative_path}`\n\n")
            
            try:
                with open(file_path, 'r', encoding='utf-8') as infile:
                    content = infile.read()
                    
                    # 🔐 SANITIZE SECRETS
                    sanitized_content, replacements = sanitize_content(content, sanitize_config, relative_path)
                    
                    if replacements:
                        total_sanitized_files += 1
                        total_replacements += len(replacements)
                        outfile.write(f"> 🔐 **Sanitized**: {', '.join(replacements)}\n\n")
                    
                    outfile.write(f"```{lang}\n")
                    outfile.write(sanitized_content)
                    if not sanitized_content.endswith('\n'):
                        outfile.write("\n")
                    outfile.write("```\n\n")
            except Exception as e:
                outfile.write(f"> ❌ [ERROR READING FILE]: {e}\n\n")

    print(f"✅ File generated successfully: {output_filename}")
    print(f"📊 Size: {os.path.getsize(output_file) / 1024:.2f} KB")
    
    if sanitize_config.get('enabled') and total_sanitized_files > 0:
        print(f"🔐 Sanitized {total_replacements} secrets in {total_sanitized_files} files")
    elif sanitize_config.get('enabled'):
        print(f"🔐 No secrets detected in scanned files")


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='🔗 Merge Project Files (Markdown) - Combine project files for LLM Context',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('-g', '--generate-config', action='store_true', help='Generate default config')
    parser.add_argument('-c', '--config', type=str, help='Path to a custom merge_config.json file')
    parser.add_argument('-t', '--tag-files', action='store_true', help='Add relative path as comment to the top of original files')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    
    if args.generate_config:
        print("=" * 70)
        print("⚙️  GENERATING CONFIGURATION FILE")
        print("=" * 70 + "\n")
        generate_config_file()
        sys.exit(0)
    
    current_dir = os.getcwd()
    dir_name = os.path.basename(current_dir)
    output_name = f"merged_output_{dir_name}.md"
    output_path = os.path.join(current_dir, output_name)
    
    try:
        print("=" * 70)
        print("🔗 MERGE PROJECT FILES")
        print("=" * 70 + "\n")

        config = load_configuration(current_dir, args.config)

        if os.path.exists(output_path):
            print(f"🧹 Removing previous output file: {output_name}")
            os.remove(output_path)
        
        merge_project_files(current_dir, output_path, config, tag_files=args.tag_files)
        
        print("\n" + "=" * 70)
        print("✅ Process completed successfully!")
        print("=" * 70)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ FATAL ERROR: {e}", file=sys.stderr)
        sys.exit(1)