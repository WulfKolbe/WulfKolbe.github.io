# WulfKolbe.github.io

Project homepage for **[pdfdrill](https://github.com/WulfKolbe/pdfdrill)** — a
token-economical drill-down PDF extraction toolkit and PDF→LaTeX OCR
quality-control pipeline.

### 🔗 Live site: **https://wulfkolbe.github.io/**

The site is **plain static HTML** (no Jekyll, no build step — `.nojekyll` is
present so GitHub Pages serves `index.html` verbatim). It loads fonts and KaTeX
from a CDN at runtime; everything else is self-contained.

## Pages

| File | What it is |
|---|---|
| [`index.html`](https://wulfkolbe.github.io/) | The homepage. Explains pdfdrill and the Claude.ai sandbox workflow with live, interactive examples — command catalogue, the QC pipeline (LaTeX │ KaTeX │ MathPix crop), and live-rendered equations pulled from a real extracted model. |

### Demo TiddlyWikis — one per source document

Each is a **single self-contained HTML file**: a TiddlyWiki 5.4.0 + KaTeX
(Gruvbox palette) carrying the *complete* document model `pdfdrill tiddlers`
extracted from the source, plus the matching QC reports.

| Document (bibkey) | Wiki | Reports |
|---|---|---|
| arXiv 2004.05631v1 — *At the Interface of Algebra and Statistics* | [wiki](https://wulfkolbe.github.io/2004.05631v1.html) | [formula report](https://wulfkolbe.github.io/formula-report.html) |
| Burkhard Heim — Unified Field Theory (`heimUFT`) | [wiki](https://wulfkolbe.github.io/heimUFT.html) | [formula](https://wulfkolbe.github.io/heimUFT-formula-report.html) · [compare](https://wulfkolbe.github.io/heimUFT-compare.html) · [tiddlers.json](https://wulfkolbe.github.io/heimUFT.tiddlers.json) |
| Kolbe (2018) — *Korrelation im Hubbard-Modell* (`kolbe2018hubbard`) | [wiki](https://wulfkolbe.github.io/kolbe2018hubbard.html) | [formula](https://wulfkolbe.github.io/kolbe2018hubbard-formula-report.html) · [compare](https://wulfkolbe.github.io/kolbe2018hubbard-compare.html) · [tiddlers.json](https://wulfkolbe.github.io/kolbe2018hubbard.tiddlers.json) |

## How it runs

- The live extraction path is **Python 3**, so it runs inside the Claude.ai
  sandbox (which already ships poppler-utils, pdfplumber, pydantic).
- The end product is a **single self-contained HTML file** that also runs as an
  **HTML tiddler inside any TiddlyWiki server with internet access**, so the
  CDN-hosted KaTeX / MathPix crop links load. (An earlier TypeScript
  implementation transpiled to HTML/JS works the same way in a plain HTML file.)

## Regenerating the artifacts

```bash
# model + reports + tiddler JSON (offline, from an existing lines.json)
pdfdrill model    <pdf>                  # unified document model
pdfdrill report   <pdf> --embed          # → formula-report.html
pdfdrill compare  <pdf> --embed          # → compare.html
pdfdrill tiddlers <pdf> --embed          # → <stem>.tiddlers.json

# build the tiddler JSON into a single-file wiki with the KaTeX plugin
npm i tiddlywiki
tiddlywiki mywiki --init server          # add "tiddlywiki/katex" to plugins
cp <stem>.tiddlers.json mywiki/tiddlers/doc.json
tiddlywiki mywiki --render '$:/core/save/all' <stem>.html text/plain
```
