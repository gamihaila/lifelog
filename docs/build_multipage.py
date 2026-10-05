#!/usr/bin/env python3
"""Generate a multi-page HTML edition of the book.

Reads the book metadata and chapter list from contents.yaml (same format as
build.py) and writes one HTML file per chapter plus a contents page into a
dedicated folder. Each chapter page links to the previous and next chapter
and back to the contents page.

Usage:
    python3 build_multipage.py              # reads ./contents.yaml, writes ./html/
    python3 build_multipage.py outdir/      # writes into ./outdir/
"""

import html
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build import parse_contents  # noqa: E402

import markdown

STYLE = """
  :root {
    --bg: #f6efd8;
    --paper: #f6efd8;
    --ink: #3a3226;
    --muted: #9c8f74;
    --accent: #7c5c3b;
    --rule: #e8dfc4;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    line-height: 1.5;
    font-size: 22px;
  }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }

  .page {
    max-width: 720px;
    margin: 0 auto;
    padding: 4vh 28px 6vh;
  }

  header.title-page {
    max-width: 720px;
    margin: 0 auto;
    padding: 12vh 32px 8vh;
    text-align: center;
  }
  header.title-page .cover {
    max-width: 320px;
    width: 60%;
    height: auto;
    border-radius: 4px;
    box-shadow: 0 12px 40px rgba(0,0,0,.28);
    margin-bottom: 40px;
  }
  header.title-page h1 {
    font-size: 2.6rem;
    line-height: 1.2;
    margin: 0 0 .4em;
    font-weight: 600;
    letter-spacing: .5px;
  }
  header.title-page .author {
    font-size: 1.2rem;
    color: var(--muted);
    font-style: italic;
    margin: 0;
  }
  header.title-page .cover-credit {
    font-size: .8rem;
    color: var(--muted);
    margin: -32px 0 40px;
  }

  section.dedication {
    max-width: 720px;
    margin: 0 auto;
    padding: 4vh 32px 8vh;
    text-align: center;
    font-style: italic;
    color: var(--muted);
  }

  nav.toc h2 {
    text-align: center;
    font-size: 1rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--rule);
    padding-bottom: 16px;
    margin-bottom: 8px;
    font-weight: 600;
  }
  nav.toc ol { list-style: none; margin: 0; padding: 0; }
  nav.toc li a {
    display: flex;
    align-items: baseline;
    gap: 16px;
    padding: 11px 8px;
    border-bottom: 1px solid var(--rule);
    color: var(--ink);
  }
  nav.toc li a:hover { background: rgba(124,92,59,.06); text-decoration: none; }
  nav.toc .toc-num {
    color: var(--accent);
    font-variant-numeric: tabular-nums;
    min-width: 1.8em;
    text-align: right;
    font-size: .95rem;
  }
  nav.toc .toc-title { flex: 1; }

  .chapter h1 {
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 .9em;
  }
  .chapter p { margin: 0 0 .9em; text-align: justify; hyphens: auto; }

  nav.pagenav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 12px;
    padding: 12px 0;
    margin-bottom: 2em;
    border-bottom: 1px solid var(--rule);
    font-size: .9rem;
  }
  nav.pagenav.bottom {
    border-bottom: none;
    border-top: 1px solid var(--rule);
    margin: 3em 0 0;
  }
  nav.pagenav .prev { text-align: left; }
  nav.pagenav .home { text-align: center; white-space: nowrap; }
  nav.pagenav .next { text-align: right; }
  nav.pagenav .disabled { color: var(--muted); opacity: .5; }
  nav.pagenav small { display: block; color: var(--muted); font-size: .8rem; }

  footer {
    text-align: center;
    color: var(--muted);
    font-size: .8rem;
    padding: 4vh 32px 8vh;
  }
  footer .revision { margin-top: .4em; }

  @media (max-width: 600px) {
    body { font-size: 21px; }
    header.title-page h1 { font-size: 2rem; }
    .page { padding-left: 22px; padding-right: 22px; }
    .chapter h1 { font-size: 1.8rem; }
  }
"""

PAGE_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{meta_tags}
<title>{title} &mdash; {book_title}</title>
<style>{style}
</style>
</head>
<body>
<div class="page">
{topnav}
<article class="chapter">
<h1>{title}</h1>
{body}
</article>
{bottomnav}
</div>
<footer>
  <p>&copy; {copyright_holder}</p>
{revision_line}</footer>
</body>
</html>
"""

INDEX_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{meta_tags}
<title>{book_title}</title>
<style>{style}
</style>
</head>
<body>
<header class="title-page">
{cover_html}    <h1>{book_title}</h1>
    <p class="author">{author}</p>
</header>
{dedication_html}
<div class="page">
<nav class="toc">
  <h2>Contents</h2>
  <ol>
{toc}
  </ol>
</nav>
</div>
<footer>
  <p>&copy; {copyright_holder}</p>
{revision_line}</footer>
</body>
</html>
"""


def chapter_filename(i, file):
    stem = os.path.splitext(os.path.basename(file))[0]
    return f"{i:02d}-{stem}.html"


def pagenav(pages, i, position):
    """Prev/contents/next navigation bar for chapter i (0-based)."""
    prev_link = next_link = ""
    if i > 0:
        p = pages[i - 1]
        prev_link = (f'<a href="{p["out"]}">&larr; '
                     f'{html.escape(p["title"])}<small>Previous chapter</small></a>')
    else:
        prev_link = '<span class="disabled">&larr; <small>First chapter</small></span>'
    if i < len(pages) - 1:
        n = pages[i + 1]
        next_link = (f'<a href="{n["out"]}">{html.escape(n["title"])} &rarr;'
                     f'<small>Next chapter</small></a>')
    else:
        next_link = '<span class="disabled"><small>Last chapter</small> &rarr;</span>'
    cls = "pagenav" + (" bottom" if position == "bottom" else "")
    return (f'<nav class="{cls}">\n'
            f'  <span class="prev">{prev_link}</span>\n'
            f'  <span class="home"><a href="index.html">Contents</a></span>\n'
            f'  <span class="next">{next_link}</span>\n'
            f'</nav>')


def build(contents_path="contents.yaml", out_dir="html"):
    meta, chapters = parse_contents(contents_path)

    book_title = meta.get("title", "Untitled")
    author = meta.get("author", "")
    lang = meta.get("language", "en")
    cover = meta.get("cover", "")
    cover_author = meta.get("cover_author", "")
    publication_date = meta.get("publication_date", "")
    copyright_holder = meta.get("copyright", "") or author
    revision_date = meta.get("revision_date", "")
    dedication = meta.get("dedication", "")

    os.makedirs(out_dir, exist_ok=True)

    md = markdown.Markdown(
        extensions=["footnotes", "smarty"],
        extension_configs={"footnotes": {"UNIQUE_IDS": True}},
    )

    pages = []
    for i, ch in enumerate(chapters, 1):
        fname = ch["file"]
        ctitle = ch.get("title", fname)
        out = chapter_filename(i, fname)
        with open(fname, encoding="utf-8") as f:
            md.reset()
            body = md.convert(f.read())
        pages.append({"num": i, "title": ctitle, "out": out, "body": body})

    meta_tag_lines = [f'<meta name="author" content="{html.escape(author)}">']
    if publication_date:
        meta_tag_lines.append(
            f'<meta name="dcterms.date" content="{html.escape(publication_date)}">')
    if revision_date:
        meta_tag_lines.append(
            f'<meta name="dcterms.modified" content="{html.escape(revision_date)}">')
    if copyright_holder:
        meta_tag_lines.append(
            f'<meta name="copyright" content="{html.escape(copyright_holder)}">')
    meta_tags = "\n".join(meta_tag_lines)

    footer_sub = " &middot; ".join(
        part for part in [
            f"Published {html.escape(publication_date)}" if publication_date else "",
            f"Revised {html.escape(revision_date)}" if revision_date else "",
        ] if part)
    revision_line = (f'  <p class="revision">{footer_sub}</p>\n'
                     if footer_sub else "")

    # Chapter pages.
    for i, p in enumerate(pages):
        doc = PAGE_TMPL.format(
            lang=html.escape(lang),
            meta_tags=meta_tags,
            title=html.escape(p["title"]),
            book_title=html.escape(book_title),
            style=STYLE,
            topnav=pagenav(pages, i, "top"),
            body=p["body"],
            bottomnav=pagenav(pages, i, "bottom"),
            copyright_holder=html.escape(copyright_holder),
            revision_line=revision_line,
        )
        with open(os.path.join(out_dir, p["out"]), "w", encoding="utf-8") as f:
            f.write(doc)

    # Contents page.
    toc_items = [
        f'      <li><a href="{p["out"]}"><span class="toc-num">{p["num"]}</span>'
        f'<span class="toc-title">{html.escape(p["title"])}</span></a></li>'
        for p in pages
    ]

    cover_html = ""
    if cover:
        # Cover lives next to contents.yaml, one level above the output dir.
        cover_html = (f'    <img class="cover" src="../{html.escape(cover)}" '
                      f'alt="Cover">\n')
        if cover_author:
            cover_html += (f'    <p class="cover-credit">Cover art by '
                           f'{html.escape(cover_author)}</p>\n')

    dedication_html = ""
    if dedication:
        dedication_html = (f'<section class="dedication">\n'
                           f'  <p>{html.escape(dedication)}</p>\n'
                           f'</section>\n')

    index_doc = INDEX_TMPL.format(
        lang=html.escape(lang),
        meta_tags=meta_tags,
        book_title=html.escape(book_title),
        style=STYLE,
        cover_html=cover_html,
        author=html.escape(author),
        dedication_html=dedication_html,
        toc="\n".join(toc_items),
        copyright_holder=html.escape(copyright_holder),
        revision_line=revision_line,
    )
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_doc)

    print(f"Wrote {out_dir}/ — {len(pages)} chapters + index, "
          f"{sum(os.path.getsize(os.path.join(out_dir, p['out'])) for p in pages)} bytes")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "html"
    build(out_dir=out)
