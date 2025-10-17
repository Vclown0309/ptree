#!/usr/bin/env python3
import os
import argparse
import sys
import io
import signal
import json
from pathlib import Path

# -------------------------- 配置文件处理 --------------------------
CONFIG_DIR = Path.home() / ".ptree"
CONFIG_FILE = CONFIG_DIR / "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "use_color": True,
    "language": "zh"  # "zh" 或 "en"
}


def load_config():
    """加载用户配置"""
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # 确保配置完整
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
    except Exception as e:
        print(f"加载配置文件失败: {e}，使用默认配置", file=sys.stderr)
        return DEFAULT_CONFIG.copy()


def save_config(config):
    """保存用户配置"""
    try:
        CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置文件失败: {e}", file=sys.stderr)
        return False


# 加载配置
config = load_config()

# -------------------------- 颜色配置与导入容错 --------------------------
# 初始化颜色和文本标识变量
COLOR_DIR = ""
COLOR_FILE = ""
RESET_ALL = ""
USE_COLOR = config["use_color"]  # 从配置获取默认值

# 语言相关文本
lang = config["language"]
TEXTS = {
    "zh": {
        "color_import_warn": r"""
        [提示] 未检测到colorama库，颜色显示可能异常。

        # 推荐的解决办法（按照优先级排序）
        1. 安装依赖（最有效）
           - 终端执行命令: pip install -r requirements.txt

        2. 手动启用ANSI支持（仅对Windows而言）
           - 步骤1: 打开注册表编辑器
             按Win+R输入regedit，打开注册表
           - 步骤2: 导航到路径
             地址: HKEY_CURRENT_USER\Console
           - 步骤3: 创建并设置DWORD值
             1. 右键空白处 → 新建 → DWORD (32位)值
             2. 命名为: VirtualTerminalLevel
             3. 双击它 → 设置"数值数据"为1 → 点击"确定"

        3. 禁用颜色输出（快速解决）
           - 运行程序时加--no-color(-n)参数禁用颜色，示例: python 脚本名.py --no-color
        """,
        "interrupt_prompt_win": "\n是否终止批处理作业? (是/否): ",
        "interrupt_prompt_other": "\n是否终止程序? (是/否): ",
        "program_terminated": "\n程序已终止。",
        "continue_running": "\n继续运行...",
        "error_handler_interrupt": "\n处理中断时出错: {e}",
        "permission_denied": "[权限不足] {name}",
        "file_not_found": "[未找到] {name}",
        "error_generic": "[错误] {name}: {msg}",
        "description": "显示清晰的目录树结构，支持自定义深度、排除选项和文件类型筛选。",
        "path_help": "起始目录路径（默认：当前工作目录）",
        "depth_help": "最大遍历深度",
        "exclude_help": "要排除的文件夹或文件名称列表",
        "types_help": "要显示的文件类型（不带点，如: txt py）",
        "no_color_help": "禁用颜色显示，使用文本标识（[目录]/[文件]）",
        "set_color_help": "设置默认颜色显示模式（on/off）",
        "set_lang_help": "设置默认语言（zh/en）",
        "version_help": "显示版本信息",
        "error_path_not_exists": "错误：路径 '{path}' 不存在。",
        "error_not_directory": "错误：'{path}' 不是一个目录。",
        "error_depth_negative": "错误：深度不能为负数，得到 {depth}。",
        "directory_tree": "目录树: {path}",
        "filter_types": "筛选类型: {types}",
        "dir_indicator": "[目录] ",
        "file_indicator": "[文件] "
    },
    "en": {
        "color_import_warn": r"""
        [Hint] colorama library not found, color display may be abnormal.

        # Recommended Solutions (Priority Order)
        1. Install Dependencies (Most Effective)
           - Run command in terminal: pip install -r requirements.txt

        2. Manually Enable ANSI Support (For Windows Only)
           - Step 1: Open Registry Editor 
             Press `Win + R`, type `regedit`, then press Enter.
           - Step 2: Navigate to the path 
             Address: HKEY_CURRENT_USER\Console
           - Step 3: Create and set a DWORD value
             1. Right-click empty space → New → DWORD (32-bit) Value
             2. Name it: VirtualTerminalLevel
             3. Double-click it → Set "Value data" to 1 → Click "OK"

        3. Disable Color Output (Quick Workaround)
           - Add the `--no-color(-n)` parameter when running the program.
             Example: python your_script.py --no-color
        """,
        "interrupt_prompt_win": "\nTerminate batch job? (yes/no): ",
        "interrupt_prompt_other": "\nTerminate program? (yes/no): ",
        "program_terminated": "\nProgram terminated.",
        "continue_running": "\nContinuing running...",
        "error_handler_interrupt": "\nError handling interrupt: {e}",
        "permission_denied": "[Permission Denied] {name}",
        "file_not_found": "[Not Found] {name}",
        "error_generic": "[Error] {name}: {msg}",
        "description": "Display a clear directory tree with custom depth, exclusion, and file type filtering.",
        "path_help": "Starting directory path (default: current working directory)",
        "depth_help": "Maximum traversal depth",
        "exclude_help": "List of folder/file names to exclude",
        "types_help": "File types to display (without dot, e.g., txt py)",
        "no_color_help": "Disable color, use text indicators ([Dir]/[File])",
        "set_color_help": "Set default color display mode (on/off)",
        "set_lang_help": "Set default language (zh/en)",
        "version_help": "Show version information",
        "error_path_not_exists": "Error: Path '{path}' does not exist.",
        "error_not_directory": "Error: '{path}' is not a directory.",
        "error_depth_negative": "Error: Depth cannot be negative, got {depth}.",
        "directory_tree": "Directory tree: {path}",
        "filter_types": "Filter types: {types}",
        "dir_indicator": "[Dir] ",
        "file_indicator": "[File] "
    }
}

# 尝试导入colorama，失败时给出提示
try:
    from colorama import init, Fore, Style

    init(autoreset=True)
    COLOR_DIR = Fore.GREEN
    COLOR_FILE = Fore.YELLOW
    RESET_ALL = Style.RESET_ALL
except ImportError:
    # 颜色库导入失败时的提示
    print(TEXTS[lang]["color_import_warn"], file=sys.stderr)


def set_console_encoding():
    """设置控制台编码以支持中文显示（Set console encoding for Chinese support）"""
    try:
        if sys.platform.startswith('win'):
            import ctypes
            ctypes.windll.kernel32.SetConsoleOutputCP(65001)
            ctypes.windll.kernel32.SetConsoleCP(65001)
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass


def handle_interrupt(signal, frame):
    """自定义中断处理（Ctrl+C）（Custom interrupt handler）"""
    try:
        # 中断提示（根据系统和语言适配）
        if sys.platform.startswith('win'):
            prompt = f"{RESET_ALL}{TEXTS[lang]['interrupt_prompt_win']}" if USE_COLOR else TEXTS[lang][
                'interrupt_prompt_win']
        else:
            prompt = f"{RESET_ALL}{TEXTS[lang]['interrupt_prompt_other']}" if USE_COLOR else TEXTS[lang][
                'interrupt_prompt_other']

        response = input(prompt).strip().lower()
        if response in ['是', 'y', 'yes']:
            msg = f"{RESET_ALL}{TEXTS[lang]['program_terminated']}" if USE_COLOR else TEXTS[lang]['program_terminated']
            print(msg)
            sys.exit(0)
        else:
            msg = f"{RESET_ALL}{TEXTS[lang]['continue_running']}" if USE_COLOR else TEXTS[lang]['continue_running']
            print(msg)
    except Exception as e:
        err_msg = f"{RESET_ALL}{TEXTS[lang]['error_handler_interrupt'].format(e=e)}" if USE_COLOR else TEXTS[lang][
            'error_handler_interrupt'].format(e=e)
        print(err_msg)
        sys.exit(1)


signal.signal(signal.SIGINT, handle_interrupt)


def walk_directory(path, excluded=None, max_depth=None, file_types=None, current_depth=0, prefix=''):
    """递归遍历目录（非目录即文件，无漏判）（Recursive directory traversal）"""
    if excluded is None:
        excluded = []
    if file_types is None:
        file_types = []

    if max_depth is not None and current_depth > max_depth:
        return

    try:
        with os.scandir(path) as it:
            entries = [
                e for e in it
                if e.name not in excluded
                   and (e.is_dir() or not file_types or any(e.name.endswith(f'.{t}') for t in file_types))
            ]
            entries.sort(key=lambda x: (not x.is_dir(), x.name.lower()))
            count = len(entries)

            for index, entry in enumerate(entries):
                connector = "└── " if index == count - 1 else "├── "
                is_dir = entry.is_dir()

                # 处理显示内容：颜色或文本标识（Color or text indicator）
                if USE_COLOR:
                    color = COLOR_DIR if is_dir else COLOR_FILE
                    display_text = f"{color}{entry.name}{'/' if is_dir else ''}"
                else:
                    # 无颜色时用文本标识（Text indicator when no color）
                    indicator = TEXTS[lang]["dir_indicator"] if is_dir else TEXTS[lang]["file_indicator"]
                    display_text = f"{indicator}{entry.name}"

                # 打印目录项（Print entry）
                print(f"{RESET_ALL if USE_COLOR else ''}{prefix}{connector}{display_text}")

                if is_dir:
                    sub_prefix = prefix + ("    " if index == count - 1 else "│   ")
                    walk_directory(
                        os.path.join(path, entry.name),
                        excluded=excluded,
                        max_depth=max_depth,
                        file_types=file_types,
                        current_depth=current_depth + 1,
                        prefix=sub_prefix
                    )

    except PermissionError:
        err = TEXTS[lang]["permission_denied"].format(name=os.path.basename(path))
        print(f"{RESET_ALL if USE_COLOR else ''}{prefix}├── {err}")
    except FileNotFoundError:
        err = TEXTS[lang]["file_not_found"].format(name=os.path.basename(path))
        print(f"{RESET_ALL if USE_COLOR else ''}{prefix}├── {err}")
    except Exception as e:
        err = TEXTS[lang]["error_generic"].format(name=os.path.basename(path), msg=str(e))
        print(f"{RESET_ALL if USE_COLOR else ''}{prefix}├── {err}")


def main():
    global USE_COLOR, lang, config  # 全局控制是否启用颜色和语言
    set_console_encoding()

    # 命令行参数解析
    parser = argparse.ArgumentParser(
        description=TEXTS[lang]["description"],
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="ptree"
    )
    parser.add_argument(
        "path",
        nargs='?',
        default=os.getcwd(),
        help=TEXTS[lang]["path_help"]
    )
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=3,
        help=TEXTS[lang]["depth_help"]
    )
    parser.add_argument(
        "-e", "--exclude",
        nargs="*",
        default=[],
        help=TEXTS[lang]["exclude_help"]
    )
    parser.add_argument(
        "-t", "--types",
        nargs="*",
        default=[],
        help=TEXTS[lang]["types_help"]
    )
    parser.add_argument(
        "-n", "--no-color",
        action="store_true",
        help=TEXTS[lang]["no_color_help"]
    )
    parser.add_argument(
        "-c", "--set-color",
        choices=['on', 'off'],
        help=TEXTS[lang]["set_color_help"]
    )
    parser.add_argument(
        "-l", "--set-lang",
        choices=['zh', 'en'],
        help=TEXTS[lang]["set_lang_help"]
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version="ptree 1.1"
    )

    args = parser.parse_args()

    # 处理配置设置
    if args.set_color is not None:
        config["use_color"] = (args.set_color == 'on')
        if save_config(config):
            print(f"默认颜色设置已更新为: {'启用' if config['use_color'] else '禁用'}")
        return  # 设置后退出，不执行目录树显示

    if args.set_lang is not None:
        config["language"] = args.set_lang
        if save_config(config):
            print(f"默认语言已更新为: {args.set_lang}")
        return  # 设置后退出，不执行目录树显示

    # 更新运行时设置
    USE_COLOR = not args.no_color and config["use_color"]
    lang = config["language"]

    # 参数校验（Parameter validation）
    if not os.path.exists(args.path):
        err = TEXTS[lang]["error_path_not_exists"].format(path=args.path)
        print(f"{RESET_ALL if USE_COLOR else ''}{err}", file=sys.stderr)
        sys.exit(1)
    if not os.path.isdir(args.path):
        err = TEXTS[lang]["error_not_directory"].format(path=args.path)
        print(f"{RESET_ALL if USE_COLOR else ''}{err}", file=sys.stderr)
        sys.exit(1)
    if args.depth < 0:
        err = TEXTS[lang]["error_depth_negative"].format(depth=args.depth)
        print(f"{RESET_ALL if USE_COLOR else ''}{err}", file=sys.stderr)
        sys.exit(1)

    # 打印标题（Print header）
    header = f"{RESET_ALL if USE_COLOR else ''}{TEXTS[lang]['directory_tree'].format(path=args.path)}"
    print(header)
    if args.types:
        types_msg = TEXTS[lang]["filter_types"].format(types=', '.join(args.types))
        print(types_msg)
    print()

    # 遍历目录（Traverse directory）
    walk_directory(
        args.path,
        excluded=args.exclude,
        max_depth=args.depth,
        file_types=args.types
    )

    # 结束时重置（Reset on exit）
    if USE_COLOR:
        print(RESET_ALL, end='')


if __name__ == "__main__":
    main()