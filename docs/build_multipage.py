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

import datetime
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
    --font: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    --size: 22px;
    --width: 720px;
    --leading: 1.5;
  }
  /* Reader display options. The defaults above are the original design;
     a small script (see PREFS_SCRIPT / SETTINGS below) sets these
     data-* attributes on <html> from the reader's saved choices. */
  html[data-theme="paper"] {
    --bg: #fdfdf8; --paper: #fdfdf8; --ink: #2e2c26;
    --muted: #8a8574; --accent: #7c5c3b; --rule: #e4dfcd;
  }
  html[data-theme="sepia"] {
    --bg: #eee1c6; --paper: #eee1c6; --ink: #46351d;
    --muted: #a1895e; --accent: #8a5a2b; --rule: #dcc99e;
  }
  html[data-theme="dark"] {
    --bg: #201d18; --paper: #201d18; --ink: #e7ddc8;
    --muted: #9c917b; --accent: #d2a95e; --rule: #3b372e;
    color-scheme: dark;
  }
  html[data-font="palatino"] {
    --font: "Palatino Linotype", "Book Antiqua", Palatino, Georgia, serif;
  }
  html[data-font="sans"] {
    --font: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto,
      "Helvetica Neue", Arial, sans-serif;
  }
  html[data-size="s"] { --size: 19px; }
  html[data-size="l"] { --size: 25px; }
  html[data-size="xl"] { --size: 28px; }
  html[data-width="narrow"] { --width: 620px; }
  html[data-width="wide"] { --width: 880px; }
  html[data-leading="compact"] { --leading: 1.4; }
  html[data-leading="relaxed"] { --leading: 1.75; }
  html[data-align="left"] .chapter p { text-align: left; hyphens: none; }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: var(--font);
    line-height: var(--leading);
    font-size: var(--size);
  }
  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }

  .page {
    max-width: var(--width);
    margin: 0 auto;
    padding: 4vh 28px 6vh;
  }

  header.title-page {
    max-width: var(--width);
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
    max-width: var(--width);
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

  nav.backmatter {
    text-align: center;
    margin-top: 2.5em;
    padding-top: 1.4em;
    border-top: 1px solid var(--rule);
  }
  nav.backmatter a { margin: 0 14px; white-space: nowrap; }

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
    :root { --size: 21px; }
    html[data-size="s"] { --size: 18px; }
    html[data-size="l"] { --size: 24px; }
    html[data-size="xl"] { --size: 27px; }
    header.title-page h1 { font-size: 2rem; }
    .page { padding-left: 22px; padding-right: 22px; }
    .chapter h1 { font-size: 1.8rem; }
  }

  /* Reading-settings control (see SETTINGS below). */
  .reader-settings {
    position: fixed; right: 18px; bottom: 18px; z-index: 50;
    font-size: 15px; line-height: 1.35;
  }
  .rs-toggle {
    width: 46px; height: 46px; border-radius: 50%;
    border: 1px solid var(--rule); background: var(--bg);
    color: var(--accent); font-family: var(--font); font-size: 17px;
    cursor: pointer; box-shadow: 0 4px 18px rgba(0,0,0,.18);
  }
  .rs-panel {
    position: absolute; right: 0; bottom: 56px; width: 248px;
    background: var(--bg); color: var(--ink);
    border: 1px solid var(--rule); border-radius: 10px;
    box-shadow: 0 12px 40px rgba(0,0,0,.25); padding: 14px 16px;
  }
  .rs-panel h2 {
    font-size: .78rem; letter-spacing: 2px; text-transform: uppercase;
    color: var(--muted); margin: 0 0 10px; font-weight: 600;
  }
  .rs-group { margin-bottom: 12px; }
  .rs-group .rs-label { display: block; color: var(--muted);
    font-size: .8rem; margin-bottom: 5px; }
  .rs-opts { display: flex; flex-wrap: wrap; gap: 6px; }
  .rs-opts button {
    border: 1px solid var(--rule); background: transparent;
    color: var(--ink); border-radius: 999px; padding: 4px 11px;
    font: inherit; font-size: .85rem; cursor: pointer;
  }
  .rs-opts button[aria-pressed="true"] {
    background: var(--accent); border-color: var(--accent); color: var(--bg);
  }
  .rs-reset {
    border: none; background: none; color: var(--accent);
    font: inherit; font-size: .85rem; cursor: pointer; padding: 0;
    text-decoration: underline;
  }
"""

# Runs in <head>, before the stylesheet takes effect, so a returning
# reader never sees a flash of the default design: it copies the saved
# choices from localStorage onto <html> as data-* attributes.
PREFS_SCRIPT = """<script>
(function () {
  try {
    var p = JSON.parse(localStorage.getItem("lifelog-prefs") || "{}");
    var d = document.documentElement;
    ["theme", "font", "size", "width", "leading", "align"].forEach(function (k) {
      if (p[k]) d.setAttribute("data-" + k, p[k]);
    });
  } catch (e) {}
})();
</script>"""

# The "Aa" button and its panel, injected at the end of <body> on every
# page. Choices are stored per browser in localStorage ("lifelog-prefs")
# and shared by all pages of the book on that browser.
SETTINGS = """<div class="reader-settings">
  <div class="rs-panel" id="rs-panel" hidden>
    <h2>Reading settings</h2>
    <div class="rs-group"><span class="rs-label">Background</span>
      <div class="rs-opts">
        <button type="button" data-key="theme" data-value="cream">Cream</button>
        <button type="button" data-key="theme" data-value="paper">Paper</button>
        <button type="button" data-key="theme" data-value="sepia">Sepia</button>
        <button type="button" data-key="theme" data-value="dark">Dark</button>
      </div></div>
    <div class="rs-group"><span class="rs-label">Font</span>
      <div class="rs-opts">
        <button type="button" data-key="font" data-value="serif">Serif</button>
        <button type="button" data-key="font" data-value="palatino">Palatino</button>
        <button type="button" data-key="font" data-value="sans">Sans</button>
      </div></div>
    <div class="rs-group"><span class="rs-label">Text size</span>
      <div class="rs-opts">
        <button type="button" data-key="size" data-value="s">Small</button>
        <button type="button" data-key="size" data-value="m">Medium</button>
        <button type="button" data-key="size" data-value="l">Large</button>
        <button type="button" data-key="size" data-value="xl">Extra large</button>
      </div></div>
    <div class="rs-group"><span class="rs-label">Column</span>
      <div class="rs-opts">
        <button type="button" data-key="width" data-value="narrow">Narrow</button>
        <button type="button" data-key="width" data-value="normal">Normal</button>
        <button type="button" data-key="width" data-value="wide">Wide</button>
      </div></div>
    <div class="rs-group"><span class="rs-label">Spacing</span>
      <div class="rs-opts">
        <button type="button" data-key="leading" data-value="compact">Compact</button>
        <button type="button" data-key="leading" data-value="normal">Normal</button>
        <button type="button" data-key="leading" data-value="relaxed">Relaxed</button>
      </div></div>
    <div class="rs-group"><span class="rs-label">Paragraphs</span>
      <div class="rs-opts">
        <button type="button" data-key="align" data-value="justify">Justified</button>
        <button type="button" data-key="align" data-value="left">Left-aligned</button>
      </div></div>
    <button type="button" class="rs-reset" id="rs-reset">Reset to defaults</button>
  </div>
  <button type="button" class="rs-toggle" id="rs-toggle" aria-haspopup="true" aria-expanded="false" title="Reading settings">Aa</button>
</div>
<script>
(function () {
  var KEY = "lifelog-prefs";
  var DEFAULTS = { theme: "cream", font: "serif", size: "m",
                   width: "normal", leading: "normal", align: "justify" };
  function load() {
    try { return JSON.parse(localStorage.getItem(KEY) || "{}"); }
    catch (e) { return {}; }
  }
  function save(p) {
    try { localStorage.setItem(KEY, JSON.stringify(p)); } catch (e) {}
  }
  function apply(p) {
    var d = document.documentElement;
    Object.keys(DEFAULTS).forEach(function (k) {
      if (p[k] && p[k] !== DEFAULTS[k]) d.setAttribute("data-" + k, p[k]);
      else d.removeAttribute("data-" + k);
    });
  }
  var prefs = load();
  var panel = document.getElementById("rs-panel");
  var toggle = document.getElementById("rs-toggle");
  function syncButtons() {
    document.querySelectorAll(".rs-opts button").forEach(function (b) {
      var k = b.getAttribute("data-key");
      var cur = prefs[k] || DEFAULTS[k];
      b.setAttribute("aria-pressed",
                     b.getAttribute("data-value") === cur ? "true" : "false");
    });
  }
  document.querySelectorAll(".rs-opts button").forEach(function (b) {
    b.addEventListener("click", function () {
      prefs[b.getAttribute("data-key")] = b.getAttribute("data-value");
      save(prefs); apply(prefs); syncButtons();
    });
  });
  function setOpen(open) {
    panel.hidden = !open;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
  }
  toggle.addEventListener("click", function () { setOpen(panel.hidden); });
  document.addEventListener("click", function (e) {
    if (!panel.hidden && !e.target.closest(".reader-settings")) setOpen(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setOpen(false);
  });
  document.getElementById("rs-reset").addEventListener("click", function () {
    prefs = {}; save(prefs); apply(prefs); syncButtons();
  });
  syncButtons();
})();
</script>"""

PAGE_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{prefs_script}
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
{settings}
</body>
</html>
"""

INDEX_TMPL = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{prefs_script}
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
{backmatter_html}</div>
<footer>
  <p>&copy; {copyright_holder}</p>
{revision_line}</footer>
{settings}
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


def backnav(position):
    """Contents-only navigation bar for back-matter pages."""
    cls = "pagenav" + (" bottom" if position == "bottom" else "")
    return (f'<nav class="{cls}">\n'
            f'  <span class="prev"></span>\n'
            f'  <span class="home"><a href="index.html">Contents</a></span>\n'
            f'  <span class="next"></span>\n'
            f'</nav>')


def build(contents_path="contents.yaml", out_dir="html"):
    meta, chapters, back_matter = parse_contents(contents_path)

    book_title = meta.get("title", "Untitled")
    author = meta.get("author", "")
    lang = meta.get("language", "en")
    cover = meta.get("cover", "")
    cover_author = meta.get("cover_author", "")
    publication_date = meta.get("publication_date", "")
    copyright_holder = meta.get("copyright", "") or author
    # the revision date is the build date, not a yaml entry
    revision_date = datetime.date.today().strftime("%B %d, %Y")
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

    back_pages = []
    for ch in back_matter:
        fname = ch["file"]
        ctitle = ch.get("title", fname)
        out = os.path.splitext(os.path.basename(fname))[0] + ".html"
        with open(fname, encoding="utf-8") as f:
            md.reset()
            body = md.convert(f.read())
        back_pages.append({"title": ctitle, "out": out, "body": body})

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
            prefs_script=PREFS_SCRIPT,
            settings=SETTINGS,
            topnav=pagenav(pages, i, "top"),
            body=p["body"],
            bottomnav=pagenav(pages, i, "bottom"),
            copyright_holder=html.escape(copyright_holder),
            revision_line=revision_line,
        )
        with open(os.path.join(out_dir, p["out"]), "w", encoding="utf-8") as f:
            f.write(doc)

    # Back-matter pages: standalone, outside the Contents, with a
    # contents-only navigation bar instead of prev/next.
    for p in back_pages:
        doc = PAGE_TMPL.format(
            lang=html.escape(lang),
            meta_tags=meta_tags,
            title=html.escape(p["title"]),
            book_title=html.escape(book_title),
            style=STYLE,
            prefs_script=PREFS_SCRIPT,
            settings=SETTINGS,
            topnav=backnav("top"),
            body=p["body"],
            bottomnav=backnav("bottom"),
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

    backmatter_html = ""
    if back_pages:
        links = "\n".join(
            f'  <a href="{p["out"]}">{html.escape(p["title"])}</a>'
            for p in back_pages)
        backmatter_html = f'<nav class="backmatter">\n{links}\n</nav>\n'

    index_doc = INDEX_TMPL.format(
        lang=html.escape(lang),
        meta_tags=meta_tags,
        book_title=html.escape(book_title),
        style=STYLE,
        prefs_script=PREFS_SCRIPT,
        settings=SETTINGS,
        cover_html=cover_html,
        author=html.escape(author),
        dedication_html=dedication_html,
        toc="\n".join(toc_items),
        backmatter_html=backmatter_html,
        copyright_holder=html.escape(copyright_holder),
        revision_line=revision_line,
    )
    with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_doc)

    print(f"Wrote {out_dir}/ — {len(pages)} chapters + index"
          f" + {len(back_pages)} back-matter, "
          f"{sum(os.path.getsize(os.path.join(out_dir, p['out'])) for p in pages)} bytes")


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "html"
    build(out_dir=out)
