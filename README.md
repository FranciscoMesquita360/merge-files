# 🔗 Merge Project Files

A tool to merge multiple project code/configuration files into a single text file. Ideal for feeding LLMs (ChatGPT, Claude, Gemini) with your code's context.

## 📋 Features

- ✅ **Auto-generate configuration file** via command line
- ✅ **External configuration** via JSON file
- ✅ Recursively traverses project directories
- ✅ Filters by file **extension** (.rs, .py, .ts, etc.)
- ✅ Filters by file **prefix**
- ✅ Searches for **keywords** within files
- ✅ Automatically excludes system directories and files
- ✅ Generates a visual directory tree structure

## 🚀 Quick Start

### 1. Generate Configuration File

```bash
python merge_files.py --generate-config
```

Or use the short form:

```bash
python merge_files.py -g
```

This will create a `merge_config.json` file with all default settings that you can customize.

### 2. Customize Your Configuration (Optional)

Edit the generated `merge_config.json` file:

```json
{
  "project_description": "My awesome project",
  "included_extensions": [".rs", ".ts", ".py", ".json"],
  "excluded_dirs": ["node_modules", "target", "dist", ".git"],
  "search_keywords": [],
  "just_file_prefixes": []
}
```

### 3. Run the Merge

```bash
python merge_files.py
```

**Done!** The file `merged_output_<folder_name>.txt` will be generated containing the code and the directory tree.

## 🆕 What's New

- 🎉 **Auto-generate config**: Use `--generate-config` or `-g` to create `merge_config.json`
- 🛡️ **Safety check**: Confirms before overwriting existing config files
- 📖 **Better help**: Enhanced command-line help with examples
- 🔧 **Improved UX**: Clear messages and instructions throughout

## 📖 Command Line Options

```bash
python merge_files.py                    # Run merge with current/default settings
python merge_files.py --generate-config  # Generate merge_config.json template
python merge_files.py -g                 # Short form to generate config
python merge_files.py --help             # Show help message
```

## ⚙️ Configuration File Structure

When you run `--generate-config`, a `merge_config.json` file is created with this structure:

```json
{
  "mandatory_dirs": [],
  "excluded_dirs": ["target", ".git", "node_modules", "__pycache__", ...],
  "excluded_file_prefixes": ["log", "Cargo.lock", "package-lock", ...],
  "just_file_prefixes": [],
  "search_keywords": [],
  "included_extensions": [".rs", ".ts", ".py", ".json", ...],
  "project_description": "Default project description",
  "inline_comment_symbol": "//",
  "tree_settings": {
    "excluded_dirs": [...],
    "excluded_prefixes": [...],
    "just_prefixes": [],
    "included_extensions": [...]
  }
}
```

### Configuration Options Explained

| Option | Description |
|--------|-------------|
| `mandatory_dirs` | Directories that will ALWAYS be included (highest priority) |
| `excluded_dirs` | Directories to ignore during scanning |
| `excluded_file_prefixes` | File prefixes to exclude (e.g., "test_", "backup_") |
| `just_file_prefixes` | If set, ONLY files with these prefixes are included |
| `search_keywords` | Only include files containing these keywords |
| `included_extensions` | File extensions to include (e.g., ".py", ".js") |
| `project_description` | Description shown at the top of output file |
| `inline_comment_symbol` | Symbol used for comments in output (default: "//") |
| `tree_settings` | Specific settings for the directory tree visualization |

---

# 📚 Configuration Examples (merge_config.json)

Copy and paste these examples into your `merge_config.json` file based on your use case.

## 1. 🌐 Web Development (Frontend & Backend)
Focused on Fullstack projects (React/Node, Vue/Python), ignoring build files and heavy dependencies.

```json
{
  "project_description": "Fullstack Web Project - Component and API Analysis",
  "included_extensions": [".js", ".jsx", ".ts", ".tsx", ".css", ".html", ".py", ".json"],
  "excluded_dirs": ["node_modules", "dist", "build", ".next", "coverage", "__pycache__", ".venv"],
  "excluded_file_prefixes": ["package-lock", "yarn.lock", "tsconfig"],
  "just_file_prefixes": []
}
```

---

## 2. 🦀 Rust Backend (High Performance)
Clean configuration for Rust projects, focusing only on source code and cargo settings, ignoring build artifacts.

```json
{
  "project_description": "High-Performance Rust Backend",
  "included_extensions": [".rs", ".toml", ".proto", ".sql"],
  "excluded_dirs": ["target", ".git", "migrations"],
  "excluded_file_prefixes": ["Cargo.lock"],
  "tree_settings": {
    "excluded_dirs": ["target", ".git"]
  }
}
```

---

## 3. 🎯 Focus on Specific Module (Prefixes)
Useful when you want to send the AI only the files related to a specific feature (e.g., "Auth" or "Payments"), without sending the entire project.

```json
{
  "project_description": "Refactoring the Auth Module",
  "just_file_prefixes": ["auth", "login", "user_session", "guard", "middleware_auth"],
  "included_extensions": [".ts", ".js", ".py", ".rs"],
  "excluded_dirs": ["node_modules", "tests"]
}
```

---

## 4. 🐞 Bug Hunting (Keyword Search)
Ignores standard structure and searches only for files containing technical debt comments or specific errors.

```json
{
  "project_description": "Technical Debt Assessment (TODOs and FIXMEs)",
  "search_keywords": ["TODO", "FIXME", "DEPRECATED", "HACK", "unwrap()"],
  "included_extensions": [".rs", ".ts", ".py", ".js", ".java", ".cpp"],
  "excluded_dirs": ["node_modules", ".git"],
  "tree_settings": {
    "excluded_dirs": ["node_modules"]
  }
}
```

---

## 5. 🚨 Mandatory Directories (Critical Path)
This scenario forces the inclusion of critical folders (like 'core' or 'shared'), ignoring default exclusion filters for these folders, while filtering the rest normally.

```json
{
  "project_description": "Core System Analysis",
  "mandatory_dirs": ["src/core", "src/shared/types"],
  "excluded_dirs": ["test", "docs", "scripts", "legacy"],
  "included_extensions": [".ts", ".rs"],
  "just_file_prefixes": []
}
```

---

## 6. 📄 Documentation & Configuration Only
Useful for asking AI to analyze project structure, READMEs, and config files (Docker, CI/CD), without reading heavy source code.

```json
{
  "project_description": "Documentation and DevOps Audit",
  "included_extensions": [".md", ".txt", ".json", ".yaml", ".yml", ".toml", "Dockerfile"],
  "excluded_dirs": ["src", "app", "lib", "node_modules", "target"],
  "excluded_file_prefixes": ["package-lock"]
}
```

---

## 7. 🌳 Detailed Tree, Summarized Code
In this scenario, you exclude almost all code from reading (to save tokens), but keep the full directory tree to understand the architecture.

```json
{
  "project_description": "Directory Tree Only (Minimal Content)",
  "included_extensions": [".md"], 
  "excluded_dirs": ["node_modules", ".git"],
  "tree_settings": {
    "excluded_dirs": [".git"],
    "included_extensions": [".rs", ".ts", ".js", ".py", ".css", ".html"]
  }
}
```
*Note: The `tree_settings` key controls what appears in the tree drawing, while `included_extensions` at the root controls what content is read.*

---

## 8. 🐍 Data Science & Python Scripts
Focused on notebooks, Python scripts, and SQL queries.

```json
{
  "project_description": "Data Pipeline and Analysis",
  "included_extensions": [".py", ".ipynb", ".sql", ".r", ".csv"],
  "excluded_dirs": [".venv", "env", "data_raw", "logs", "__pycache__"],
  "excluded_file_prefixes": ["temp_", "backup_"],
  "inline_comment_symbol": "#"
}
```

---

## 9. 🔍 Mobile Development (React Native / Flutter)
Focus on mobile app source code, ignoring platform-specific build directories.

```json
{
  "project_description": "Mobile App Development",
  "included_extensions": [".js", ".jsx", ".ts", ".tsx", ".dart", ".java", ".kt", ".swift"],
  "excluded_dirs": ["node_modules", "android/build", "ios/Pods", "build", ".gradle"],
  "excluded_file_prefixes": ["pod", "gradle"],
  "just_file_prefixes": []
}
```

---

## 10. 🎮 Game Development (Unity/Unreal)
Focused on game scripts and configurations, excluding large asset files and build artifacts.

```json
{
  "project_description": "Game Logic and Systems",
  "included_extensions": [".cs", ".cpp", ".h", ".lua", ".json", ".xml"],
  "excluded_dirs": ["Library", "Temp", "Build", "Builds", "obj", "Binaries"],
  "excluded_file_prefixes": ["meta", "asset"],
  "just_file_prefixes": []
}
```

---

## 📂 Generated Output

The output file (`merged_output_<folder_name>.txt`) contains:

1. **Project Description** (defined in your config)
2. **Keyword Filter Info** (if using search_keywords)
3. **Content of All Matched Files** (with clear file path separators)
4. **Visual Directory Tree** (at the end, showing project structure)

Perfect for:
- 🤖 Feeding context to LLMs (ChatGPT, Claude, Gemini)
- 📊 Code analysis and refactoring
- 📚 Documentation generation
- 🔍 Code review preparation

## 💡 Pro Tips

1. **Start with `--generate-config`**: Always generate the config file first and customize it for your needs
2. **Use `mandatory_dirs` for critical code**: Ensure important modules are always included
3. **Combine filters**: Use `search_keywords` + `included_extensions` for laser-focused searches
4. **Save token costs**: Use `tree_settings` to show structure without including all file contents
5. **Test incrementally**: Start with strict filters, then gradually expand if needed

## 📋 Requirements

- Python 3.6+
- No external dependencies required!

## 🤝 Contributing

Feel free to open issues or submit pull requests with improvements!

## 📄 License

Free to use and modify.

---