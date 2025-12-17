# 🔗 Merge Project Files v3.0

A tool to merge multiple project code/configuration files into a single text file. Ideal for feeding LLMs (ChatGPT, Claude, Gemini) with your code's context.

## 📋 Features

- ✅ **External configuration** via JSON file
- ✅ Recursively traverses project directories
- ✅ Filters by file **extension** (.rs, .py, .ts, etc.)
- ✅ Filters by file **prefix**
- ✅ Searches for **keywords** within files
- ✅ Automatically excludes system directories and files
- ✅ Generates a visual directory tree structure

## 🚀 How to Use

1. **(Optional) Create the configuration file:**
   Create a file named `merge_config.json` in the same directory as the script. If not created, the script will use default values.

   *(You can copy the example below)*:

   ```json
   {
     "project_description": "My awesome project",
     "just_file_prefixes": [],
     "included_extensions": [".rs", ".ts", ".py", ".json"],
     "excluded_dirs": ["node_modules", "target", "dist", ".git"]
   }
   ```

2. **Run the script:**

   ```bash
   python merge_files.py
   ```

3. **Done!** The file `merged_output_<folder_name>.txt` will be generated containing the code and the directory tree.

# 📚 Configuration Examples (merge_config.json)

This document lists various usage scenarios for the `merge_config.json` file. Copy the content of the desired scenario to your configuration file.

---

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

## 📂 Generated Output

The output file contains:
1. **Project Description** (defined in JSON)
2. **Visual directory tree**
3. **Content** of all found files (separated by comments)

Perfect for analysis, AI refactoring, or documentation.

## 📋 Requirements

- Python 3.6+

## 📄 License

Free to use and modify.