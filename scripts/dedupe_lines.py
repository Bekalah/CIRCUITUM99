#!/usr/bin/env python3
"""Remove consecutive duplicate lines from text files.

Memory lapses sometimes append the same block twice.
This tiny tool keeps files trimmed without any network calls.
"""

from __future__ import annotations

import argparse
import pathlib
import subprocess


def dedupe_file(path: pathlib.Path) -> int:
    """Collapse runs of identical lines. Return count removed."""
    data = path.read_text(encoding="utf-8")
    lines = data.splitlines()
    cleaned: list[str] = []
    removed = 0
    prev: str | None = None
    for line in lines:
        if line == prev:
            removed += 1
            continue
        cleaned.append(line)
        prev = line
    tail = "\n" if data.endswith("\n") else ""
    path.write_text("\n".join(cleaned) + tail, encoding="utf-8")
    return removed


def tracked_files() -> list[pathlib.Path]:
    """List repo-tracked files using git."""
    res = subprocess.run([
        "git",
        "ls-files",
    ], check=True, text=True, capture_output=True)
    return [pathlib.Path(line) for line in res.stdout.splitlines()]


def main() -> None:
    p = argparse.ArgumentParser(description="Remove consecutive duplicate lines")
    p.add_argument("files", nargs="*", type=pathlib.Path, help="Targets")
    p.add_argument("--all", action="store_true", help="Process all tracked files")
    args = p.parse_args()

    targets = args.files or []
    if args.all:
        targets = tracked_files()
    if not targets:
        p.error("no files given")

    for path in targets:
        removed = dedupe_file(path)
        if removed:
            print(f"{path}: removed {removed} duplicate line(s)")


if __name__ == "__main__":
    main()

