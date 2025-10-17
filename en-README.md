# ptree - Directory Tree Viewer

A simple and efficient directory tree visualization tool with custom depth, exclusion, file filtering, and multi-language support, helping you quickly visualize directory structures.

## Features

- **Multi-language Support**: Built-in Chinese and English, default language can be configured
- **Color Differentiation**: Directories and files displayed in different colors (requires colorama)
- **Flexible Filtering**: Filter files by type (e.g., only show `.txt`, `.py` files)
- **Persistent Configuration**: Saves default color mode and language settings to config file
- **Friendly Interaction**: Ctrl+C interrupt allows continuation or termination, clear error prompts
- **Cross-platform Compatibility**: Automatically adapts to console encoding for Windows, Linux and macOS

## Installation

1. Clone or download this project
2. Install dependencies (required for color display):
   ```bash
   pip install colorama
   ```
   
   >  or use `pip install -r requirements.txt` ,   **Ensure this command is executed in the project directory.** 

## Usage

### Basic Usage

```bash
# Display directory tree of current directory (default depth 3)
python ptree.py

# Display directory tree of specified path
python ptree.py /path/to/directory
```

### Common Parameters

| Parameter         | Description                                 | Example                                              |
| ----------------- | ------------------------------------------- | ---------------------------------------------------- |
| `-d, --depth`     | Set maximum traversal depth                 | `python ptree.py -d 2` (show 2 levels only)          |
| `-e, --exclude`   | Exclude files/directories by name           | `python ptree.py -e __pycache__ .git`                |
| `-t, --types`     | Show only specified file types              | `python ptree.py -t py txt` (show .py and .txt only) |
| `-n, --no-color`  | Disable color display (use text indicators) | `python ptree.py -n`                                 |
| `-c, --set-color` | Set default color mode (on/off)             | `python ptree.py -c off` (disable color by default)  |
| `-l, --set-lang`  | Set default language (zh/en)                | `python ptree.py -l en` (default to English)         |
| `-v, --version`   | Show version information                    | `python ptree.py -v`                                 |

## Configuration File

The config file is located at `~/.ptree/config.json`, example content:

```json
{
  "use_color": true,
  "language": "en"
}
```

Can be modified via `--set-color` and `--set-lang` parameters, or edited directly.

## Notes

- For color display issues on Windows, follow program prompts to modify registry for ANSI support
- Automatically falls back to text indicators ([Dir]/[File]) when colorama is not installed
- Shows `[Permission Denied]` for inaccessible directories without interrupting the program


