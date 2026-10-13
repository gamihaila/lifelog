#!/usr/bin/env python3
"""Generate a self-contained index.html from contents.yaml.

Reads the book metadata and chapter list from contents.yaml, then embeds each
chapter's markdown (plain paragraph text) directly into a single styled HTML
file. The output works fully offline (no CDN, no fetch) and opens from file://.

Usage:
    python3 build.py            # reads ./contents.yaml, writes ./index.html
"""

import datetime
import html
import re
import markdown


def parse_contents(path='contents.yaml'):
    """Parse the simple, tailored contents.yaml into (meta, chapters).

    The `metadata:` block is a list of single-key items (`- key: value`)
    rather than nested mappings, so its entries are flattened straight
    into the same `meta` dict as the top-level `title`/`author`/etc. keys.
    """
    meta = {}
    chapters = []
    cur = None
    section = None  # None | 'metadata' | 'chapters'
    with open(path, encoding='utf-8') as f:
        for raw in f:
            line = raw.rstrip('\n')
            if not line.strip():
                continue
            if line.startswith('metadata:'):
                section = 'metadata'
                continue
            if line.startswith('chapters:'):
                section = 'chapters'
                continue
            if section == 'metadata':
                m = re.match(r'\s*-\s*(\w+):\s*(.*)', line)
                if m:
                    meta[m.group(1).strip()] = m.group(2).strip()
            elif section == 'chapters':
                m = re.match(r'\s*-\s*file:\s*(.+)', line)
                if m:
                    if cur:
                        chapters.append(cur)
                    cur = {'file': m.group(1).strip()}
                else:
                    m2 = re.match(r'\s*title:\s*(.+)', line)
                    if m2 and cur is not None:
                        cur['title'] = m2.group(1).strip()
            elif ':' in line:
                k, v = line.split(':', 1)
                meta[k.strip()] = v.strip()
        if cur:
            chapters.append(cur)
    return meta, chapters

def build(contents_path='contents.yaml', out_path='index.html'):
    meta, chapters = parse_contents(contents_path)

    title = meta.get('title', 'Untitled')
    author = meta.get('author', '')
    lang = meta.get('language', 'en')
    cover = meta.get('cover', '')
    cover_author = meta.get('cover_author', '')
    publication_date = meta.get('publication_date', '')
    copyright_holder = meta.get('copyright', '') or author
    # the revision date is the build date, not a yaml entry:
    # the HTML always shows when it was rendered
    revision_date = datetime.date.today().strftime('%B %d, %Y')
    dedication = meta.get('dedication', '')

    # Reuse a single Markdown instance and reset() per chapter with UNIQUE_IDS
    # so footnote ids (fn:1, fnref:1, ...) get a per-chapter prefix. Otherwise
    # every chapter restarts numbering at 1 and the ids collide, making all
    # footnote links jump to the first chapter's footnotes.
    md = markdown.Markdown(
        extensions=['footnotes', 'smarty'],
        extension_configs={'footnotes': {'UNIQUE_IDS': True}},
    )

    toc_items = []
    chapter_html = []
    for i, ch in enumerate(chapters, 1):
        fname = ch['file']
        ctitle = ch.get('title', fname)
        cid = 'ch' + str(i)
        with open(fname, encoding='utf-8') as f:
            md.reset()
            body = md.convert(f.read())
        toc_items.append(
            f'      <li><a href="#{cid}"><span class="toc-num">{i}</span>'
            f'<span class="toc-title">{html.escape(ctitle)}</span></a></li>')
        chapter_html.append(f'''    <section class="chapter" id="{cid}">
      <p class="chapter-num">Chapter {i}</p>
      <h2>{html.escape(ctitle)}</h2>
{body}
      <p class="top-link"><a href="#top">&uarr; Contents</a></p>
    </section>''')

            
    toc = '\n'.join(toc_items)
    chapters_joined = '\n'.join(chapter_html)

    cover_html = ''
    if cover:
        cover_html = f'    <img class="cover" src="{html.escape(cover)}" alt="Cover">\n'
        if cover_author:
            cover_html += (
                f'    <p class="cover-credit">Cover art by '
                f'{html.escape(cover_author)}</p>\n')

    dedication_html = ''
    if dedication:
        dedication_html = f'''
<section class="dedication">
  <p>{html.escape(dedication)}</p>
</section>
'''

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
    meta_tags = '\n'.join(meta_tag_lines)

    footer_sub = ' &middot; '.join(
        part for part in [
            f'Published {html.escape(publication_date)}' if publication_date else '',
            f'Revised {html.escape(revision_date)}' if revision_date else '',
        ] if part)

    doc = f'''<!DOCTYPE html>
<html lang="{html.escape(lang)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{meta_tags}
<title>{html.escape(title)}</title>
<style>
  :root {{
    --bg: #f6efd8;
    --paper: #f6efd8;
    --ink: #3a3226;
    --muted: #9c8f74;
    --accent: #7c5c3b;
    --rule: #e8dfc4;
  }}
  * {{ box-sizing: border-box; }}
  html {{ scroll-behavior: smooth; }}
  body {{
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
    line-height: 1.5;
    font-size: 22px;
  }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}

  header.title-page {{
    max-width: 720px;
    margin: 0 auto;
    padding: 12vh 32px 8vh;
    text-align: center;
  }}
  header.title-page .cover {{
    max-width: 320px;
    width: 60%;
    height: auto;
    border-radius: 4px;
    box-shadow: 0 12px 40px rgba(0,0,0,.28);
    margin-bottom: 40px;
  }}
  header.title-page h1 {{
    font-size: 2.6rem;
    line-height: 1.2;
    margin: 0 0 .4em;
    font-weight: 600;
    letter-spacing: .5px;
  }}
  header.title-page .author {{
    font-size: 1.2rem;
    color: var(--muted);
    font-style: italic;
    margin: 0;
  }}
  header.title-page .cover-credit {{
    font-size: .8rem;
    color: var(--muted);
    margin: -32px 0 40px;
  }}

  section.dedication {{
    max-width: 720px;
    margin: 0 auto;
    padding: 4vh 32px 8vh;
    text-align: center;
    font-style: italic;
    color: var(--muted);
  }}

  nav.toc {{
    max-width: 720px;
    margin: 0 auto;
    padding: 0 32px 6vh;
  }}
  nav.toc h2 {{
    text-align: center;
    font-size: 1rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--muted);
    border-bottom: 1px solid var(--rule);
    padding-bottom: 16px;
    margin-bottom: 8px;
    font-weight: 600;
  }}
  nav.toc ol {{ list-style: none; margin: 0; padding: 0; }}
  nav.toc li a {{
    display: flex;
    align-items: baseline;
    gap: 16px;
    padding: 11px 8px;
    border-bottom: 1px solid var(--rule);
    color: var(--ink);
  }}
  nav.toc li a:hover {{ background: rgba(124,92,59,.06); text-decoration: none; }}
  nav.toc .toc-num {{
    color: var(--accent);
    font-variant-numeric: tabular-nums;
    min-width: 1.8em;
    text-align: right;
    font-size: .95rem;
  }}
  nav.toc .toc-title {{ flex: 1; }}

  main {{
    max-width: 720px;
    margin: 0 auto;
    padding: 0 28px;
  }}
  section.chapter {{
    background: var(--bg);
    padding: 4vh 0 3vh;
    margin: 0;
    border-radius: 0;
    box-shadow: none;
  }}
  section.chapter .chapter-num {{
    display: none;
  }}
  section.chapter h2 {{
    text-align: left;
    font-size: 2.4rem;
    font-weight: 700;
    margin: 0 0 .9em;
    padding-bottom: 0;
    border-bottom: none;
  }}
  section.chapter p {{ margin: 0 0 .9em; text-align: justify; hyphens: auto; }}
  .top-link {{
    text-align: center;
    margin-top: 3em !important;
    font-size: .85rem;
  }}
  .top-link a {{ color: var(--muted); }}

  footer {{
    text-align: center;
    color: var(--muted);
    font-size: .8rem;
    padding: 4vh 32px 8vh;
  }}
  footer .revision {{
    margin-top: .4em;
  }}

  @media (max-width: 600px) {{
    body {{ font-size: 21px; }}
    header.title-page h1 {{ font-size: 2rem; }}
    main {{ padding: 0 22px; }}
    section.chapter {{ padding: 4vh 0 3vh; }}
  }}
</style>
</head>
<body>
<a id="top"></a>
<header class="title-page">
{cover_html}    <h1>{html.escape(title)}</h1>
    <p class="author">{html.escape(author)}</p>
</header>
{dedication_html}
<nav class="toc">
  <h2>Contents</h2>
  <ol>
{toc}
  </ol>
</nav>

<main>
{chapters_joined}
</main>

<footer>
  <p>&copy; {html.escape(copyright_holder)}</p>
{f'  <p class="revision">{footer_sub}</p>' if footer_sub else ''}
</footer>
</body>
</html>
'''

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(doc)

    print(f"Wrote {out_path} — {len(chapters)} chapters, {len(doc)} bytes")


if __name__ == '__main__':
    build()
