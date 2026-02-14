# 🔗 Merge (Markdown Edition)

A CLI tool to merge multiple files into a single file.md

## 📋 Features

- ✅ **One-liner installation** for Windows, Linux, and macOS
- ✅ **Markdown Output**: Files are wrapped in code blocks with syntax highlighting (`.rs`, `.py`, `.ts`, etc.)
- ✅ **Auto-generate configuration** via `merge --generate-config`
- ✅ **Recursive traversal** with smart filtering
- ✅ Filter by **extension**, **prefix**, or **keywords**
- ✅ **Priority Folders**: Force include critical directories

## 🚀 Quick Install

No Python? No problem. Run the command for your system:

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
**Done!** A file named `merged_output_<folder_name>.md` will be created.

---

## 📖 Command Line Options

| Option | Short | Description |
|--------|-------|-------------|
| --generate-config | -g | Generate merge_config.json template
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
| `tree_settings` | Control how the directory tree is drawn (can differ from file selection) |

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

---

## 📂 Output Format

The generated `.md` file is structured to give LLMs the best possible context:

1. **Header**: Project description.
2. **Directory Tree**: A visual map of the project structure.
   ```text
   my-project/
   ├── src/
   │   ├── main.rs
   │   └── utils.rs
   └── Cargo.toml
   ```
3. **Files**: Each file is clearly separated with Markdown syntax highlighting:
   ```rust
   // ## File: src/main.rs
   fn main() {
       println!("Hello World");
   }
   ```

## 💡 Pro Tips

1. **LLM Context**: This tool is perfect for creating a "Knowledge Base" file for custom GPTs or Claude Projects.
2. **Token Saving**: Use `included_extensions` strictly to avoid sending unnecessary files to the AI.
3. **Tree Mapping**: Even if you don't merge all files, use `tree_settings` to let the AI see your architecture.

## 🤝 Contributing
Contributions are welcome! Feel free to open issues or PRs.

## 📄 License
MIT - Free to use and modify.