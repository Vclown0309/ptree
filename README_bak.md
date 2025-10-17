# ptree — Python Directory Tree Viewer

`ptree` is a Python script to display directory structures in a tree-like format, similar to the classic `tree` command, with support for excluding files/folders and limiting depth.

> **Note:**
> The command is named `ptree` to avoid conflicts with the built-in Windows `tree` command.

---

## Features

* Recursive directory listing in a tree structure
* Option to exclude specific files or folders
* Limit the maximum depth of directory traversal
* Cross-platform support (Windows CMD, PowerShell, Git Bash, WSL)

---

## Setup

### 1. Clone or download this repository

Place all files into a folder, e.g.:

```plaintext
C:\Users\YourName\Scripts\
```

### 2. Ensure Python is installed and available in your PATH

Check by running:

```bash
python --version
```

---

### 4. Create launcher scripts

* **Windows CMD/PowerShell:** `ptree.bat`

  ```bat
  @echo off
  python "%~dp0ptree.py" %*
  ```

* **Git Bash / WSL:** `ptree`

  ```bash
  #!/bin/bash
  python "$(dirname "$0")/ptree.py" "$@"
  ```

Make sure the `ptree` file has execute permission:

```bash
chmod +x ptree
```

---

### 5. Add the folder to your system `PATH`

* On Windows:
  Add the folder (e.g., `C:\Users\YourName\Scripts`) to your user or system environment variable `PATH`.

* On Linux/macOS (bash):
  Add this line to your `~/.bashrc` or `~/.zshrc`:

  ```bash
  export PATH="$PATH:/path/to/your/scripts"
  ```

---

### 6. Restart your terminal

Open a new terminal window to apply the changes.

---

## Usage

Run the `ptree` command followed by the directory path and optional arguments:

```bash
ptree C:\path\to\directory -d 2 -e __pycache__ .git
```

### Arguments

* `path` — Starting directory path (required)
* `-d`, `--depth` — Maximum depth to traverse (optional)
* `-e`, `--exclude` — List of file or folder names to exclude (optional)

---

## Example

```bash
ptree C:\Users -d 3 -e node_modules .git
```

---

## Notes

* Do **not** use the name `tree` for the command to avoid conflict with Windows' built-in `tree.exe`.
* The launcher scripts (`ptree.bat` and `ptree`) ensure the script works from any terminal.

---

## License

[Walaszek License](https://youtu.be/mUl-D6MATvA)
