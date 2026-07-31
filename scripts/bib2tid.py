#!/usr/bin/env python3
"""Turn a BibTeX file into one tiddler per entry.

The cite key becomes the title, so `[[knuth1984]]` links resolve straight to
the reference. BibTeX fields are kept as tiddler fields (prefixed `bib-`) so
they stay queryable, and a readable citation goes in the body.

    ./scripts/bib2tid.py refs.bib --tags reference
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import bibtexparser
from bibtexparser.bparser import BibTexParser

import tidlib

_WHITESPACE = re.compile(r"\s+")

# Braces protect capitalisation in BibTeX; they are noise once rendered.
_BRACES = re.compile(r"[{}]")


def clean(value: str) -> str:
    return _WHITESPACE.sub(" ", _BRACES.sub("", value)).strip()


def format_authors(raw: str) -> str:
    """BibTeX 'Last, First and Last, First' -> 'First Last, First Last'."""
    people = []
    for person in raw.split(" and "):
        person = clean(person)
        if "," in person:
            last, _, first = person.partition(",")
            person = f"{first.strip()} {last.strip()}".strip()
        people.append(person)
    return ", ".join(people)


def citation(entry: dict[str, str]) -> str:
    authors = format_authors(entry.get("author") or entry.get("editor", ""))
    title = clean(entry.get("title", ""))
    venue = clean(entry.get("journal") or entry.get("booktitle") or entry.get("publisher", ""))
    year = clean(entry.get("year", ""))

    parts = [p for p in (authors, f"''{title}''" if title else "", venue, year) if p]
    lines = [". ".join(parts) + ("." if parts else "")]

    if doi := clean(entry.get("doi", "")):
        lines.append(f"\nDOI: [[{doi}|https://doi.org/{doi}]]")
    elif url := clean(entry.get("url", "")):
        lines.append(f"\n[[{url}|{url}]]")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("bib_file", type=Path)
    parser.add_argument("--tags", nargs="*", default=["reference"])
    parser.add_argument(
        "--tag-by-type",
        action="store_true",
        help="also tag each tiddler with its BibTeX entry type (article, book, ...)",
    )
    parser.add_argument("--out", type=Path, default=tidlib.default_tiddlers_dir())
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    bib_parser = BibTexParser(common_strings=True)
    bib_parser.ignore_nonstandard_types = False
    database = bibtexparser.loads(args.bib_file.read_text(encoding="utf-8"), bib_parser)

    if not database.entries:
        print(f"error: no entries found in {args.bib_file}", file=sys.stderr)
        return 1

    args.out.mkdir(parents=True, exist_ok=True)
    for entry in database.entries:
        key = entry.get("ID") or ""
        if not key:
            print("skip: entry without a cite key", file=sys.stderr)
            continue

        entry_type = entry.get("ENTRYTYPE", "misc")
        tags = list(args.tags) + ([entry_type] if args.tag_by_type else [])
        fields = {
            f"bib-{name}": clean(value)
            for name, value in entry.items()
            if name not in ("ID", "ENTRYTYPE")
        }

        tiddler = tidlib.stamped(
            key,
            citation(entry),
            tags=tidlib.format_tags(tags),
            **{"bib-type": entry_type, **fields},
        )
        try:
            written = tiddler.write(args.out, overwrite=args.force)
        except FileExistsError as exc:
            print(f"skip: {exc}", file=sys.stderr)
            continue
        print(f"{key} -> {written.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
