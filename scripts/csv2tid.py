#!/usr/bin/env python3
"""Turn a CSV into tiddlers.

Two shapes, because the useful thing to do with a CSV depends on whether the
rows are data or presentation:

    --per-row (default)  one tiddler per row, columns become tiddler fields,
                         which makes the rows queryable by TiddlyWiki filters
    --table              one tiddler holding a WikiText table, for when you
                         just want to look at it

    ./scripts/csv2tid.py books.csv --title-column Title --tags book
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

import tidlib

# Field names TiddlyWiki assigns meaning to; a CSV column of the same name
# would quietly override the generated value, so they are prefixed instead.
_RESERVED = {"title", "text", "created", "modified", "tags", "type"}


def wikitext_table(rows: list[dict[str, str]], columns: list[str]) -> str:
    header = "|" + "|".join(f"!{c}" for c in columns) + "|"
    body = [
        "|" + "|".join(row.get(c, "").replace("|", "&#124;") for c in columns) + "|"
        for row in rows
    ]
    return "\n".join([header, *body])


def field_name(column: str) -> str:
    slug = "".join(ch if ch.isalnum() else "-" for ch in column.strip().lower()).strip("-")
    return f"csv-{slug}" if slug in _RESERVED else slug


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--title-column", help="column to use as the tiddler title (per-row mode)")
    parser.add_argument("--title", help="title of the table tiddler (--table mode)")
    parser.add_argument("--prefix", default="", help="string prepended to each row title")
    parser.add_argument("--tags", nargs="*", default=[])
    parser.add_argument("--table", action="store_true", help="emit one table tiddler")
    parser.add_argument("--delimiter", default=",")
    parser.add_argument("--out", type=Path, default=tidlib.default_tiddlers_dir())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    with args.csv_file.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter=args.delimiter)
        columns = reader.fieldnames or []
        rows = list(reader)

    if not columns:
        print("error: CSV has no header row", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    tags = tidlib.format_tags(args.tags)

    if args.table:
        title = args.title or args.csv_file.stem
        tiddler = tidlib.stamped(title, wikitext_table(rows, columns), tags=tags)
        print(f"{args.csv_file} -> {tiddler.write(args.out, overwrite=args.force).name}")
        return 0

    title_column = args.title_column or columns[0]
    if title_column not in columns:
        print(f"error: no column {title_column!r}; have {columns}", file=sys.stderr)
        return 1

    for index, row in enumerate(rows, start=1):
        title = args.prefix + (row.get(title_column) or f"row-{index}")
        fields = {
            field_name(column): (row.get(column) or "")
            for column in columns
            if column != title_column
        }
        tiddler = tidlib.stamped(title, "", tags=tags, **fields)
        try:
            written = tiddler.write(args.out, overwrite=args.force)
        except FileExistsError as exc:
            print(f"skip: {exc}", file=sys.stderr)
            continue
        print(f"row {index} -> {written.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
