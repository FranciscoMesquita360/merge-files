# 🔗 Merge Files

A powerful CLI tool to merge multiple project files into a single Markdown file with **built-in secret sanitization** for safe sharing with LLMs.

## ✨ Key Features

- 🔐 **Secret Sanitization**: Automatically detects and replaces 25+ types of credentials (API keys, passwords, tokens)
- 📝 **Markdown Output**: Files wrapped in syntax-highlighted code blocks (`.rs`, `.py`, `.ts`, etc.)
- ⚡ **One-liner Installation** for Windows, Linux, and macOS
- 🎯 **Smart Filtering**: By extension, prefix, keywords, or priority folders
- 🌳 **Directory Tree**: Visual project structure in the output
- ⚙️ **Configurable**: Full control via JSON config file
- 🏷️ **File Tagging**: Optional source path comments in original files

## 🚀 Quick Install

No Python required. Run the command for your system:

### Linux / macOS
```bash
curl -fsSL https://raw.githubusercontent.com/FranciscoMesquita360/merge-files/main/install.sh | bash
```

### Windows (PowerShell)
```powershell
iwr https://raw.githubusercontent.com/FranciscoMesquita360/merge-files/main/install.ps1 | iex
```

---

## 🛠️ Usage

### Quick Start

```bash
# 1. Navigate to your project
cd my-project/

# 2. Run merge (uses smart defaults)
merge

# Output: merged_output_my-project.md
```

### Generate Custom Configuration

```bash
merge --generate-config
```

This creates `merge_config.json` with all available options. Edit it to customize:
- Which files to include/exclude
- Directory filters
- **Secret sanitization patterns** (enabled by default)
- Project description

Then run:
```bash
merge
```

---

## 📖 Command Line Options

| Command | Description |
|---------|-------------|
| `merge` | Merge files in current directory |
| `merge -g` / `merge --generate-config` | Generate `merge_config.json` template |
| `merge -c custom.json` | Use specific configuration file |
| `merge -t` / `merge --tag-files` | Add source path comments to original files |
| `merge --help` | Show all available options |

---

## 🔐 Secret Sanitization (Security First!)

**Enabled by default** to protect your credentials when sharing code with LLMs or teammates.

### Automatically Detects & Sanitizes:

✅ **API Keys**: OpenAI, Anthropic, AWS, Stripe, Google, etc.  
✅ **Passwords**: Database passwords, admin credentials, SMTP passwords  
✅ **Tokens**: JWT, Bearer, GitHub, OAuth tokens  
✅ **Database URLs**: PostgreSQL, MongoDB, MySQL, Redis (with credentials)  
✅ **Private Keys**: RSA, SSH, PEM keys  
✅ **Message Brokers**: Kafka SASL, RabbitMQ, MQTT credentials  
✅ **URLs with Auth**: `https://user:pass@api.com` → `https://USERNAME:********@api.com`  

### Example:

**Before sanitization:**
```python
DATABASE_URL = "postgresql://admin:MyP@ssw0rd@db.prod.com:5432/main"
OPENAI_API_KEY = "sk-proj-AbCdEf..."
stripe_key = "sk_live_51H8K9L..."
```

**After sanitization:**
```python
DATABASE_URL = "postgresql://USERNAME:********@db.prod.com:5432/main"
OPENAI_API_KEY = "********"
stripe_key = "sk_live_********"
```

### Sanitization Patterns Included:

- 13+ regex patterns for common credentials
- 30+ keyword monitors (OPENAI_API_KEY, DATABASE_PASSWORD, etc.)
- Kafka/RabbitMQ/MQTT specific patterns
- Even detects credentials in **commented code**!

### Disable (if needed):

Edit `merge_config.json`:
```json
{
  "sanitize_secrets": {
    "enabled": false
  }
}
```

⚠️ **Not recommended** - always review output before sharing!

---

## ⚙️ Configuration Structure

The `merge_config.json` provides full control:

| Option | Description |
|--------|-------------|
| `mandatory_dirs` | Folders that ALWAYS bypass filters (e.g., `"src/core"`) |
| `excluded_dirs` | Folders to ignore (`node_modules`, `.git`, `__pycache__`, etc.) |
| `excluded_file_prefixes` | Skip files starting with these (e.g., `"test_"`, `"README"`) |
| `included_extensions` | Only include files with these extensions (`.py`, `.js`, `.rs`) |
| `search_keywords` | Only merge files containing specific words |
| `project_description` | Custom header text for the output file |
| `sanitize_secrets` | Configure secret detection patterns (25 patterns by default) |
| `tree_settings` | Control directory tree display independently |

---

## 📚 Use Case Examples

### 🌐 Web Development (Frontend + Backend)
```json
{
  "project_description": "Fullstack Web Application",
  "included_extensions": [".js", ".jsx", ".ts", ".tsx", ".css", ".html"],
  "excluded_dirs": ["node_modules", "dist", ".next", "build"],
  "sanitize_secrets": {
    "enabled": true
  }
}
```

### 🦀 Rust Backend
```json
{
  "project_description": "Rust Microservice - Source and Config",
  "included_extensions": [".rs", ".toml", ".sql"],
  "excluded_dirs": ["target", ".git"],
  "mandatory_dirs": ["src/core"]
}
```

### 🐍 Python Data Pipeline
```json
{
  "project_description": "ETL Pipeline with Kafka Integration",
  "included_extensions": [".py", ".sql", ".yaml"],
  "excluded_dirs": ["venv", "__pycache__", "data"],
  "search_keywords": ["kafka", "database", "transform"]
}
```

### 🐞 Security Audit / Bug Hunting
```json
{
  "project_description": "Security Review - Technical Debt Search",
  "search_keywords": ["TODO", "FIXME", "HACK", "XXX", "password", "secret"],
  "included_extensions": [".py", ".js", ".rs", ".go"]
}
```

### 🔐 Share Code Safely with LLM
```json
{
  "project_description": "Project Context for Claude/ChatGPT",
  "included_extensions": [".py", ".js", ".md"],
  "excluded_dirs": ["tests", "docs", ".git"],
  "sanitize_secrets": {
    "enabled": true,
    "custom_keywords": [
      "COMPANY_API_KEY",
      "INTERNAL_TOKEN"
    ]
  }
}
```

---

## 📂 Output Format

The generated `.md` file is optimized for LLM context:

### 1. **Project Header**
```markdown
# PROJECT DESCRIPTION

Your custom project description here
```

### 2. **Directory Tree**
```text
my-project/
├── src/
│   ├── main.rs
│   ├── lib.rs
│   └── utils/
│       └── helpers.rs
├── Cargo.toml
└── README.md
```

### 3. **Security Notice** (if sanitization enabled)
```markdown
> 🔐 SECURITY NOTICE
> This document has been processed with secret sanitization.
> Sensitive information has been replaced with `********`.
```

### 4. **File Contents** (with syntax highlighting)
```markdown
## File: `src/main.rs`

> 🔐 Sanitized: Database URLs (1x), API Keys (2x)

```rust
fn main() {
    let db_url = "postgresql://USERNAME:********@localhost/db";
    println!("Server starting...");
}
```
```

---

## 💡 Pro Tips

### 🤖 LLM Integration
This tool is perfect for creating context files for:
- **Custom GPTs** (ChatGPT)
- **Claude Projects** (Anthropic)
- **Code Reviews** with AI assistants
- **Documentation Generation**

Just upload the generated `.md` file and the AI has your entire codebase context!

### 🔒 Security Best Practices
1. ✅ **Always keep sanitization enabled** when sharing code
2. ✅ **Review the output** before uploading to AI services
3. ✅ **Add custom keywords** for company-specific secrets
4. ✅ **Use `.gitignore`** to exclude `merged_output_*.md` from commits

### ⚡ Performance Tips
1. Use `included_extensions` to reduce token count
2. Use `mandatory_dirs` for critical folders only
3. Exclude test/mock data directories
4. Use `search_keywords` for targeted analysis

### 🏷️ File Tagging
Use `merge -t` to add source path comments to your original files:
```python
# src/utils/helpers.py  ← Auto-added by merge tool
def my_function():
    pass
```

Useful for tracking file origins when refactoring!

---

## 🛡️ Supported Secret Types

The sanitization engine detects **25+ patterns**, including:

**Cloud & Infrastructure:**
- AWS Access Keys & Secret Keys
- Google Cloud API Keys
- Azure Connection Strings

**APIs & Services:**
- OpenAI API Keys (`sk-...`, `sk-proj-...`)
- Anthropic API Keys (`sk-ant-...`)
- Stripe Keys (test & live)
- GitHub Tokens (`ghp_...`, `gho_...`)
- SendGrid, Twilio, Mailgun keys

**Databases:**
- PostgreSQL URLs with credentials
- MongoDB connection strings
- MySQL, Redis, MariaDB URLs
- MSSQL connection strings

**Message Brokers:**
- Kafka SASL username/password
- RabbitMQ credentials
- MQTT credentials

**General:**
- JWT tokens
- Bearer tokens
- Private Keys (RSA, SSH)
- Password fields in dicts/configs
- URLs with basic auth

Full list in the generated `merge_config.json`!

---

## 🔧 Advanced Configuration

### Add Custom Sanitization Patterns

Edit `merge_config.json`:

```json
{
  "sanitize_secrets": {
    "enabled": true,
    "patterns": [
      {
        "name": "Company Internal Token",
        "regex": "(COMPANY_TOKEN)\\s*=\\s*['\"]([^'\"]+)['\"]",
        "replacement": "\\1 = \"********\""
      }
    ],
    "custom_keywords": [
      "COMPANY_API_KEY",
      "INTERNAL_SECRET"
    ]
  }
}
```

### Multiple Configurations

Keep different configs for different purposes:

```bash
merge -c config-frontend.json   # Frontend only
merge -c config-backend.json    # Backend only
merge -c config-full.json       # Everything
```

---



## 🤝 Contributing

Contributions welcome! Areas of interest:

- 🔐 Additional secret patterns
- 📝 Documentation improvements
- 🐛 Bug fixes
- ✨ Feature requests

Feel free to open issues or PRs at: https://github.com/FranciscoMesquita360/merge-files

---

## 📄 License

MIT License - Free to use and modify.

---

## 🙏 Acknowledgments

Built to solve the "share my code with AI safely" problem. Inspired by the need to:
- Give LLMs full project context
- Protect sensitive credentials
- Make code sharing effortless

**Stay secure! 🔐**