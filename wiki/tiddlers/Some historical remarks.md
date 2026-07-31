```markdown
Dear User,

After retiring in 2024, I set out to make a series of four German books on a new Quantum Field Theory (written around 1970) more accessible to the scientific community by translating them into English.

The physical books were digitised by a professional scanning service (Iridian.de), which cuts the spine to capture every page without distortion.  
I then evaluated all available OCR tools — both free and commercial — and chose MathPix.com. However, the OCR output contained many math expressions and symbols that were incorrectly converted, incomplete, or replaced with an image link due to low confidence scores.

## Discovering Tiddlywiki and transclusions

While searching for ways to compare, edit, correct, and preview math expressions, I repeatedly encountered KaTeX in combination with HTML. That led me to Tiddlywiki, where I was immediately fascinated by Jeremy Ruston’s JavaScript style and his commitment to simplicity. His concept of **transclusions** instantly made sense to me: with just a single function definition and a CSV-like file of formulas, I had transclusions working in LaTeX.

LaTeX alone, however, could not render the math expressions inline. I therefore started importing formulas into Tiddlywiki and using **templated transclusions** for math. I soon realised that templated transclusions had a much broader application — they could elegantly handle bibliographic references, images, footnotes, and more.

## Background and efficiency

During the three years before my retirement, I spent far too much time “behind the browser” — on the inspection panels of Chrome and Firefox — benchmarking slow, inefficient code written by so‑called full‑stack developers who favoured React and Clojure for data‑intensive tasks. In contrast, the code inside Tiddlywiki and its plugins looked refreshingly efficient to me.

After writing a few simple `gawk` scripts, I had my first table with columns for a link, the LaTeX math expression, and the KaTeX visual — editing was only one click away.

## Large language models and the `lines.json` format

Like many people, I was captivated by the arrival of LLMs and tested every model I had access to by uploading my OCR results.  
Starting with small batches of 10 pages, things evolved quickly and soon 100‑page uploads became possible. Early models (before ChatGPT‑3) essentially ignored math expressions. I experimented extensively with OCR outputs from InftyReader and later tools like LlamaParse, observing gradual progress in understanding and translation quality.

In parallel, I used coding assistants like Cursor.ai to combine all my transclusion ideas into TypeScript code. The key lesson was that the project must be broken into very small, independent pieces to avoid exhausting token limits too early. I achieved this by dynamically loading small modules that always expose the same function names, which are then called in a loop, passing the result from one module to the next. Adding a new module only requires an entry in a `config.json` file (already using Tiddlywiki’s JSON array syntax) and the corresponding code module.

In 2025 I discovered MathPix’s `lines.json` output, available only through their API. This JSON format contains coordinates for every text line and for more complex elements. With these coordinates I can recover the positions of numbered equations (LaTeX expressions) and construct direct links to their CDN images. The result is an equation table that shows the math expression, the KaTeX visual, *and* the source image — with editing just one click away.

## Building a complete pipeline

To obtain real‑world examples of how math expressions are constructed, I turned to LaTeX sources from lecture notes and arXiv.org. This made a **LaTeX‑to‑Tiddlywiki** converter necessary.  
Similarly, because LLMs mostly output Markdown, I needed a **Markdown‑to‑Tiddlywiki** process for corrections.  
Finally, to produce printable versions, a **Tiddlywiki‑to‑LaTeX** exporter proved helpful.

## Advantages of the MathPix CDN and storage optimizations

Using MathPix’s `canonical_uri` to reference images on their CDN allows me to exclude all binary image data from the Tiddlywiki JSON array — dramatically reducing storage size.  
Jeremy Ruston’s “Tiddlyspace” idea can also be adapted: storing only the header fields yields excellent compression.

## Token‑efficient data for LLMs

For LLM processing, I now use a custom format that uses only a single token between records. Standard JSON wastes a token for every quote and colon.  
Instead, I use a delimiter‑based structure:

%%%%
Title
Text
%%%%

This reduces token consumption significantly when passing structured data to a language model.
```