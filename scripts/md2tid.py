#!/usr/bin/env python3
"""Wrap Markdown files as .tid tiddlers.

The markdown plugin renders `type: text/markdown` natively, so there is no
conversion to WikiText here and nothing to lose in translation -- the body is
copied through byte for byte.

    ./scripts/md2tid.py notes/*.md --tags reading
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import tidlib

_H1 = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


def title_and_body(source: str, fallback: str, *, keep_heading: bool) -> tuple[str, str]:
    """Take the title from a leading H1 if there is one, else the filename."""
    match = _H1.search(source)
    if not match or source[: match.start()].strip():
        return fallback, source
    if keep_heading:
        return match.group(1), source
    return match.group(1), source[match.end() :].lstrip("\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("files", nargs="+", type=Path, help="Markdown files")
    parser.add_argument("--tags", nargs="*", default=[], help="tags for every tiddler")
    parser.add_argument("--out", type=Path, default=tidlib.default_tiddlers_dir())
    parser.add_argument("--force", action="store_true", help="overwrite existing tiddlers")
    parser.add_argument(
        "--keep-heading",
        action="store_true",
        help="keep the H1 in the body instead of promoting it to the title only",
    )
    args = parser.parse_args(argv)

    args.out.mkdir(parents=True, exist_ok=True)
    for path in args.files:
        source = path.read_text(encoding="utf-8")
        title, body = title_and_body(source, path.stem, keep_heading=args.keep_heading)
        tiddler = tidlib.stamped(
            title,
            body,
            type="text/markdown",
            tags=tidlib.format_tags(args.tags),
        )
        try:
            written = tiddler.write(args.out, overwrite=args.force)
        except FileExistsError as exc:
            print(f"skip: {exc}", file=sys.stderr)
            continue
        print(f"{path} -> {written.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
