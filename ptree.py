#!/usr/bin/env python3
import os
import argparse

def walk_directory(path, excluded=None, max_depth=None, current_depth=0, prefix=''):
    if excluded is None:
        excluded = []

    if max_depth is not None and current_depth > max_depth:
        return

    try:
        with os.scandir(path) as it:
            entries = [e for e in it if e.name not in excluded]
            count = len(entries)

            for index, entry in enumerate(entries):
                connector = "└───" if index == count - 1 else "├───"
                print(f"{prefix}{connector}{entry.name}")

                if entry.is_dir():
                    extension = "    " if index == count - 1 else "│   "
                    walk_directory(
                        os.path.join(path, entry.name),
                        excluded=excluded,
                        max_depth=max_depth,
                        current_depth=current_depth + 1,
                        prefix=prefix + extension
                    )
    except PermissionError:
        print(f"{prefix} [Permission Denied] {path}")
    except FileNotFoundError:
        print(f"{prefix} [Not Found] {path}")

def main():
    parser = argparse.ArgumentParser(description="Display directory tree structure.")
    parser.add_argument("path", help="Starting directory path")
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=None,
        help="Maximum depth to traverse (optional)"
    )
    parser.add_argument(
        "-e", "--exclude",
        nargs="*",
        default=[],
        help="List of folder or file names to exclude (optional)"
    )

    args = parser.parse_args()
    print(args.path)
    walk_directory(args.path, excluded=args.exclude, max_depth=args.depth)

if __name__ == "__main__":
    main()
