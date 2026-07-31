# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`WulfKolbe/WulfKolbe.github.io` is a GitHub Pages **user site** — the repo name is what binds it to `https://wulfkolbe.github.io/`. It publishes a **single-file TiddlyWiki**.

The important thing to understand is that there are two representations of the same wiki, and only one of them is the source:

- **`wiki/`** is the source of truth — a TiddlyWiki *folder* edition. Every tiddler is a separate `.tid` file under `wiki/tiddlers/`, which is what makes the content diffable and reviewable in git.
- **`index.html`** at the repo root is a 3.6 MB **generated artifact** — the whole wiki rendered into one self-contained file. It is committed (GitHub Pages has no build step and serves it verbatim), but it must never be hand-edited. Any manual change to it is destroyed by the next `./build`.

So: edit `wiki/tiddlers/`, then rebuild. Never edit `index.html`.

## Commands

```bash
./setup          # vendor bun into .bun/, install node + python deps (idempotent)
./serve          # TiddlyWiki node server on http://127.0.0.1:8080 (PORT=… to override)
./build          # render wiki/ → index.html at the repo root
```

A fresh clone needs **no** global toolchain — `./serve` and `./build` both run `./setup` first if `.bun/bin/bun` or `node_modules/tiddlywiki` is missing, so cloning and running `./build` is enough. There is no lint or test tooling; do not invent commands for these.

Everything runs through the **vendored** `.bun/bin/bun`, never a system bun, so the toolchain is identical everywhere the repo is cloned.

The editing loop is: run `./serve`, edit in the browser, and the **filesystem plugin writes each change straight back to `wiki/tiddlers/*.tid`** as you save — no export step, no manual file juggling. When you're happy, `./build` and commit both the changed `.tid` files and the regenerated `index.html`.

Both scripts invoke TiddlyWiki through **bun** (`bun node_modules/tiddlywiki/tiddlywiki.js`) rather than the `tiddlywiki` bin stub, which would pick up system node instead.

## The vendored toolchain (`setup`)

`.bun/` holds a project-local bun, downloaded rather than committed. The binary is ~94 MB and platform-specific, so committing it would bloat every clone *and* still hand a macOS machine a Linux binary — fetching per-platform is what actually makes an arbitrary clone work. `setup` maps `uname` to a release triple (linux/darwin × x64/aarch64) and unpacks the GitHub release archive directly, deliberately **not** piping through bun's official install script, which edits your shell rc files. If the standard x64 build won't execute — pre-AVX2 CPUs get SIGILL — it retries with bun's `-baseline` variant.

**`BUN_VERSION` in `setup` is pinned on purpose.** An unpinned `latest` means two clones taken weeks apart resolve different bun versions and write different `bun.lockb`, so every fresh clone starts with a dirty tree. Bumping bun is therefore a deliberate commit: edit the pin, run `./setup && .bun/bin/bun install`, and commit the resulting `bun.lockb`.

The Python venv is best-effort: `uv sync` when uv is present, otherwise a `python3 -m venv` + pip fallback, and a warning if neither exists. The wiki builds fine without it — only `scripts/` needs it.

## tiddlywiki.info

`wiki/tiddlywiki.info` declares the plugin set; adding a plugin means adding its name here and rebuilding.

- `tiddlywiki/filesystem` + `tiddlywiki/tiddlyweb` are a **pair** — filesystem does the server-side `.tid` writing, tiddlyweb is the browser-side sync adaptor that talks to it. Removing either breaks the edit-saves-to-disk loop.
- `tiddlywiki/markdown` — set a tiddler's `type:` to `text/markdown` to author in Markdown instead of WikiText.
- `tiddlywiki/katex` — `$…$` inline and `$$…$$` display maths.
- `tiddlywiki/highlight` — syntax highlighting in code blocks.

The `index` build target renders `$:/plugins/tiddlywiki/tiddlyweb/save/offline`, **not** the more commonly seen `$:/core/save/all`. This matters: because tiddlyweb is installed, `save/all` would bake the server sync machinery into the published file, and the wiki would sit there trying to sync against a server that doesn't exist on GitHub Pages. The `offline` template strips it out.

`HelloThere` and `MarkdownExample` double as a plugin smoke test — they exercise KaTeX and Markdown rendering, so if either looks wrong after a plugin change, that's the signal.

## Python authoring scripts

`scripts/` generates `.tid` files from other formats. The venv is uv-managed (`uv sync`); run them as `.venv/bin/python scripts/<name>.py`.

- **`tidlib.py`** — the shared `.tid` reader/writer everything else builds on. Its `Tiddler.filename` deliberately reproduces TiddlyWiki's own character-swapping rule (`$:/StoryList` → `$__StoryList.tid`) so generated files are indistinguishable from ones the server wrote, and the server won't create a duplicate alongside yours.
- **`md2tid.py`** — wraps Markdown as `type: text/markdown`. There is no Markdown→WikiText conversion and there should not be: the markdown plugin renders it natively, so the body is copied byte for byte and nothing is lost in translation. A leading `# H1` is promoted to the title and dropped from the body (`--keep-heading` to retain it).
- **`csv2tid.py`** — `--per-row` (default) makes each row a tiddler with columns as fields, which is what you want if the rows should be reachable by TiddlyWiki filters; `--table` makes a single WikiText table, for when you only want to look at it.
- **`bib2tid.py`** — one tiddler per BibTeX entry, titled by cite key so `[[knuth1984]]` just links. Fields are kept as `bib-*` and a formatted citation goes in the body.

Two conventions worth preserving when extending these: CSV columns colliding with TiddlyWiki's own field names (`text`, `tags`, `created`, …) are prefixed rather than allowed to silently override the generated value, and every script refuses to clobber an existing tiddler without `--force`.

Generated tiddlers land in `wiki/tiddlers/` and are picked up by the next `./build` like any other. Pinned to `bibtexparser~=1.4` — the v2 API is incompatible.

## Repo hygiene

- **`.nojekyll` must stay.** It disables Jekyll preprocessing on GitHub Pages; without it, paths beginning with `_` are silently dropped.
- `$:/StoryList` records which tiddlers are open in the browser. TiddlyWiki rewrites it on every serve and build, so it is gitignored to keep that churn out of diffs.
- `.bun/`, `node_modules/`, `.venv/`, `.codegraph/`, `.cursor/`, and `resume.sh` (a local relaunch wrapper) are all untracked by design — `./setup` reconstructs the first three.
- `index.html` is not byte-reproducible across machines: TiddlyWiki serialises the tiddlers inside a plugin in filesystem read order, so a rebuild elsewhere shuffles a few hundred bytes without changing content. Don't chase that diff.
- **CodeGraph MCP** is initialized here, but the tracked source is `.tid` files and shell scripts, which it doesn't usefully index — plain Read/Grep is the faster route in this repo.
