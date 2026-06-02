# WulfKolbe.github.io

Project homepage for **[pdfdrill](https://github.com/WulfKolbe/pdfdrill)** — a
token-economical drill-down PDF extraction toolkit and PDF→LaTeX OCR
quality-control pipeline.

The site is **plain static HTML** (no Jekyll, no build step — `.nojekyll` is
present so GitHub Pages serves `index.html` verbatim). It loads fonts and KaTeX
from a CDN at runtime; everything else is self-contained.

## Pages

| File | What it is |
|---|---|
| `index.html` | The homepage. Explains pdfdrill and the Claude.ai sandbox workflow with live, interactive examples — command catalogue, the QC pipeline (LaTeX │ KaTeX │ MathPix crop), and live-rendered equations pulled from a real extracted model. |
| `2004.05631v1.html` | A **self-hosted TiddlyWiki** (TiddlyWiki 5.4.0 + the official KaTeX plugin) carrying the *complete* document model `pdfdrill tiddlers` extracted from arXiv 2004.05631v1 — 2618 tiddlers: sections, equations, formulas, sidenotes, footnotes, references. Equation tiddlers render live. |
| `formula-report.html` | The actual `pdfdrill report` output for the same paper: 1116 inline formulas + 254 display equations, each as LaTeX source │ KaTeX render │ MathPix CDN crop. |

## Regenerating the artifacts

```bash
# formula report + tiddlers (offline, from an existing lines.json)
pdfdrill report   2004.05631v1.pdf --embed     # → formula-report.html
pdfdrill tiddlers 2004.05631v1.pdf             # → 2004_05631v1_tiddlers.json

# build the tiddler JSON into a single-file wiki with the KaTeX plugin
npm i tiddlywiki
tiddlywiki mywiki --init server                # add "tiddlywiki/katex" to plugins
cp 2004_05631v1_tiddlers.json mywiki/tiddlers/doc.json
tiddlywiki mywiki --render '$:/core/save/all' 2004.05631v1.html text/plain
```
