# 🔗 Merge

A CLI tool to merge multiple files into a single text file.

## 📋 Features

- ✅ **One-liner installation** for Windows, Linux, and macOS
- ✅ **Single Binary**: No Python installation required for end-users
- ✅ **Auto-generate configuration** via `merge --generate-config`
- ✅ **Recursive traversal** with smart filtering
- ✅ Filter by **extension**, **prefix**, or **keywords**
- ✅ **Priority Folders**: Force include critical directories
- ✅ **Visual Tree**: Generates a directory structure map at the end of the file

## 🚀 Quick Install

No Python? No problem. Run the command for your system:

### Linux / macOS
```bash
curl -fsSL [https://raw.githubusercontent.com/FranciscoMesquita360/merge-files/main/install.sh](https://raw.githubusercontent.com/FranciscoMesquita360/merge-files/main/install.sh) | bash
```

### Windows (PowerShell)
```powershell
iwr [https://raw.githubusercontent.com/FranciscoMesquita360/merge-files/main/install.ps1](https://raw.githubusercontent.com/FranciscoMesquita360/merge-files/main/install.ps1) | iex
```

---

## 🛠️ Usage

### 1. Generate Configuration File
First, create a template to customize what you want to merge:
```bash
merge --generate-config
```
This creates `merge_config.json`. 

### 2. Run the Merge
Simply type the command in your project root:
```bash
merge
```
**Done!** A file named `merged_output_<folder_name>.txt` will be created.

---

## 📖 Command Line Options

```bash
merge                       # Run with current/default settings
merge --generate-config     # Generate merge_config.json template
merge -g                    # Short form for config generation
merge --help                # Show help message
```

---

## ⚙️ Configuration Structure

The `merge_config.json` allows full control over the process:

| Option | Description |
|--------|-------------|
| `mandatory_dirs` | Folders that ALWAYS bypass exclusion filters (e.g., "src/core") |
| `excluded_dirs` | Folders to ignore (node_modules, .git, etc.) |
| `included_extensions` | Only merge files with these extensions (.rs, .py, .ts) |
| `search_keywords` | Only merge files containing these specific words |
| `project_description` | Custom text header for the output file |
| `tree_settings` | Control how the directory tree is drawn |

---

## 📚 Use Case Examples

### 🌐 Web Development
```json
{
  "project_description": "Fullstack Web Project Analysis",
  "included_extensions": [".js", ".jsx", ".ts", ".tsx", ".css", ".html"],
  "excluded_dirs": ["node_modules", "dist", ".next", "build"]
}
```

### 🦀 Rust Backend
```json
{
  "project_description": "Rust Source and Logic",
  "included_extensions": [".rs", ".toml", ".sql"],
  "excluded_dirs": ["target", ".git"]
}
```

### 🐞 Bug Hunting (Keyword Search)
```json
{
  "project_description": "Searching for Technical Debt",
  "search_keywords": ["TODO", "FIXME", "HACK", "ERROR"],
  "included_extensions": [".py", ".js", ".rs"]
}
```

### 📄 Documentation Only
```json
{
  "project_description": "Project Documentation Audit",
  "included_extensions": [".md", ".txt", ".yaml", "Dockerfile"],
  "excluded_dirs": ["src", "lib", "node_modules"]
}
```

---

## 📂 Output Format

The generated file is structured as follows:
1. **Header**: Project description and active filters.
2. **Files**: Each file starts with a clear separator `// ==================== [path/to/file]`.
3. **Directory Tree**: A visual representation of the scanned project structure.

## 💡 Pro Tips

1. **LLM Context**: This tool is perfect for creating a "Knowledge Base" file for custom GPTs or Claude Projects.
2. **Token Saving**: Use `included_extensions` strictly to avoid sending unnecessary files to the AI.
3. **Tree Mapping**: Even if you don't merge all files, use `tree_settings` to let the AI see your architecture.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or PRs on [GitHub](https://github.com/FranciscoMesquita360/merge-files).

## 📄 License
MIT - Free to use and modify.