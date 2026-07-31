"""Read and write TiddlyWiki .tid files.

A .tid file is a block of `field: value` lines, a blank line, then the body:

    title: HelloThere
    type: text/markdown
    tags: intro [[two words]]

    body text

Field values are single-line by definition, so the blank line is the only
separator that matters. Everything after it is the body verbatim.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

# TiddlyWiki's filesystem adaptor swaps characters that are illegal or awkward
# in a filename for underscores -- which is why $:/StoryList lands on disk as
# $__StoryList.tid. Mirroring that here keeps generated files indistinguishable
# from ones the server itself wrote.
_UNSAFE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')

# Field order in the file is cosmetic, but a stable order keeps git diffs clean.
_FIELD_ORDER = ["title", "type", "tags", "created", "modified"]


def tw_timestamp(when: datetime | None = None) -> str:
    """TiddlyWiki's UTC timestamp format: YYYYMMDDhhmmssSSS."""
    when = (when or datetime.now(timezone.utc)).astimezone(timezone.utc)
    return when.strftime("%Y%m%d%H%M%S") + f"{when.microsecond // 1000:03d}"


def format_tags(tags: list[str]) -> str:
    """Join tags, bracketing any that contain spaces."""
    return " ".join(f"[[{t}]]" if " " in t else t for t in tags)


def parse_tags(value: str) -> list[str]:
    """Split a tags field, honouring [[bracketed tags]]."""
    return [a or b for a, b in re.findall(r"\[\[(.+?)\]\]|(\S+)", value)]


@dataclass
class Tiddler:
    title: str
    text: str = ""
    fields: dict[str, str] = field(default_factory=dict)

    @property
    def filename(self) -> str:
        return _UNSAFE.sub("_", self.title) + ".tid"

    def serialize(self) -> str:
        fields = {"title": self.title, **self.fields}
        ordered = sorted(
            fields.items(),
            key=lambda kv: (
                _FIELD_ORDER.index(kv[0]) if kv[0] in _FIELD_ORDER else len(_FIELD_ORDER),
                kv[0],
            ),
        )
        header = "".join(f"{k}: {v}\n" for k, v in ordered)
        return f"{header}\n{self.text.rstrip()}\n"

    def write(self, tiddlers_dir: Path, *, overwrite: bool = False) -> Path:
        path = tiddlers_dir / self.filename
        if path.exists() and not overwrite:
            raise FileExistsError(f"{path} exists (pass --force to overwrite)")
        path.write_text(self.serialize(), encoding="utf-8")
        return path


def parse(text: str) -> Tiddler:
    head, _, body = text.partition("\n\n")
    fields: dict[str, str] = {}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip()
    title = fields.pop("title", "")
    return Tiddler(title=title, text=body, fields=fields)


def read(path: Path) -> Tiddler:
    return parse(path.read_text(encoding="utf-8"))


def stamped(title: str, text: str, **fields: str) -> Tiddler:
    """Build a Tiddler with created/modified set to now."""
    now = tw_timestamp()
    return Tiddler(
        title=title,
        text=text,
        fields={"created": now, "modified": now, **{k: v for k, v in fields.items() if v}},
    )


def default_tiddlers_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "wiki" / "tiddlers"
