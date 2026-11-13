#!/usr/bin/env python3
"""Shared local/CI quality entry point. Requires Python >= 3.9 and LLVM 18."""

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SUFFIXES = {".c", ".cc", ".cpp", ".cxx"}
HEADER_SUFFIXES = {".h", ".hh", ".hpp", ".hxx"}


def find_tool(name):
    override = os.environ.get(name.upper().replace("-", "_"))
    executable = override or shutil.which(name + "-18") or shutil.which(name)
    if not executable:
        raise ValueError(f"Missing {name} 18; install it or set "
                         f"{name.upper().replace('-', '_')} to its path")
    version = subprocess.check_output([executable, "--version"], text=True)
    if not re.search(r"version\s+18\.", version):
        raise ValueError(f"Expected {name} 18, got: {version.strip()}")
    return executable


def source_files():
    output = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z", "--", "examples"],
        cwd=ROOT,
    )
    return sorted({ROOT / os.fsdecode(name) for name in output.split(b"\0")
                   if name and Path(os.fsdecode(name)).suffix in SOURCE_SUFFIXES | HEADER_SUFFIXES
                   and (ROOT / os.fsdecode(name)).is_file()})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("check", choices=["format", "tidy"])
    parser.add_argument("--fix", action="store_true", help="apply formatting (format only)")
    parser.add_argument("--build-dir", type=Path, default=ROOT / "build/packet-parser")
    args = parser.parse_args()
    if args.fix and args.check != "format":
        parser.error("--fix is supported only for format")
    try:
        files = source_files()
        if not files:
            raise ValueError("No C/C++ example files found")
        if args.check == "format":
            tool = find_tool("clang-format")
            flags = ["-i"] if args.fix else ["--dry-run", "--Werror"]
            subprocess.run([tool, "--style=file", *flags, *map(str, files)],
                           cwd=ROOT, check=True)
        else:
            tool = find_tool("clang-tidy")
            build_dir = args.build_dir.resolve()
            database = build_dir / "compile_commands.json"
            if not database.is_file():
                raise ValueError(f"Missing {database}; configure CMake first "
                                 "with a Makefiles or Ninja generator")
            entries = json.loads(database.read_text())
            compiled = set()
            for entry in entries:
                path = Path(entry["file"])
                if not path.is_absolute():
                    path = Path(entry["directory"]) / path
                compiled.add(path.resolve())
            sources = [path for path in files if path.suffix in SOURCE_SUFFIXES]
            if not sources:
                raise ValueError("No C/C++ translation units found")
            missing = [str(path) for path in sources if path.resolve() not in compiled]
            if missing:
                raise ValueError("Sources missing from compile_commands.json: " + ", ".join(missing))
            subprocess.run([tool, "-p", str(build_dir), *map(str, sources)],
                           cwd=ROOT, check=True)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"Quality check failed: {error}", file=sys.stderr)
        return 1
    print(f"{args.check}: passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
