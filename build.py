#!/usr/bin/env python3
"""Build The Book of the Mashaikh website.

Usage:  python3 build.py
Output: ./site/
Serve:  cd site && python3 -m http.server 8000
"""

import re
import shutil
from html import escape
from pathlib import Path

BASE_DIR = Path(__file__).parent
SITE_DIR = BASE_DIR / "site"

PARTS = [
    (1, "Seeds of Tasawwuf",               "1st–2nd Century AH",   "Ch. 1–9"),
    (2, "Crystallization of Sufi Thought", "3rd–4th Century AH",   "Ch. 10–20"),
    (3, "Age of Systematization",          "5th–6th Century AH",   "Ch. 21–35"),
    (4, "The Golden Age",                  "7th–8th Century AH",   "Ch. 36–50, 101–102"),
    (5, "Age of Expansion",                "9th–11th Century AH",  "Ch. 51–65, 103–106"),
    (6, "Era of Revival",                  "12th–13th Century AH", "Ch. 66–80, 107–114, 126"),
    (7, "The Modern Era",                  "14th Century AH",      "Ch. 81–100, 115–127"),
]

PART_ERA_DATES = {
    1: ("600–820 CE",   "1st–2nd Century AH"),
    2: ("820–1000 CE",  "3rd–4th Century AH"),
    3: ("1000–1200 CE", "5th–6th Century AH"),
    4: ("1097–1400 CE", "7th–8th Century AH"),
    5: ("1199–1650 CE", "9th–11th Century AH"),
    6: ("1641–1900 CE", "12th–13th Century AH"),
    7: ("1847–Present", "14th Century AH"),
}

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS = """\
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400;1,500&family=Amiri:ital,wght@0,400;0,700;1,400&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:     #f9f5eb;
  --bg-alt: #f1e8d3;
  --border: #d8c8a4;
  --text:   #1e1609;
  --muted:  #6b5438;
  --accent: #7a1a1a;
  --gold:   #9a7010;
  --sid:    #17110a;
  --sid-t:  #e8d4b0;
  --sid-a:  #c8980e;
}

html { scroll-behavior: smooth; font-size: 16px; }

body {
  font-family: 'EB Garamond', Georgia, 'Times New Roman', serif;
  font-size: 1.125rem;
  line-height: 1.85;
  color: var(--text);
  background: var(--bg);
}

a { color: var(--accent); }
a:hover { color: var(--gold); }

/* ── Layout ── */

.layout {
  display: grid;
  grid-template-columns: 265px 1fr;
  min-height: 100vh;
}

/* ── Sidebar ── */

.sidebar {
  background: var(--sid);
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
  scrollbar-width: thin;
  scrollbar-color: rgba(200,152,14,.3) transparent;
}
.sidebar-inner { padding-bottom: 3rem; }
.sidebar-brand {
  padding: 1.75rem 1.5rem 1.25rem;
  border-bottom: 1px solid rgba(200,152,14,.18);
}
.sidebar-brand a {
  display: block;
  color: var(--sid-a);
  text-decoration: none;
  font-size: .7rem;
  text-transform: uppercase;
  letter-spacing: .15em;
  margin-bottom: .6rem;
}
.sidebar-brand .brand-title {
  display: block;
  color: var(--sid-t);
  font-size: .95rem;
  line-height: 1.45;
}
.sidebar nav { padding: .75rem 0; }
.nav-section {
  display: block;
  font-size: .68rem;
  text-transform: uppercase;
  letter-spacing: .18em;
  color: rgba(200,152,14,.6);
  padding: 1rem 1.5rem .3rem;
}
.sidebar nav a {
  display: block;
  padding: .28rem 1.5rem .28rem 1.75rem;
  color: #b09060;
  text-decoration: none;
  font-size: .9rem;
  line-height: 1.45;
  border-left: 3px solid transparent;
  transition: color .15s, border-color .15s, background .15s;
}
.sidebar nav a:hover,
.sidebar nav a.active {
  color: var(--sid-t);
  border-left-color: var(--sid-a);
  background: rgba(200,152,14,.08);
}
.sidebar nav a.nav-part { padding-left: 1.5rem; color: #a08050; }
.sidebar nav a.nav-ch   { padding-left: 2.5rem; color: #8a6840; font-size: .82rem; }

/* ── Main ── */

.main {
  padding: 4.5rem 5.5rem 7rem;
  max-width: 820px;
}

/* ── Cover / Index ── */

.cover {
  text-align: center;
  padding: 4rem 1rem 3.5rem;
  border-bottom: 1px solid var(--border);
  margin-bottom: 4rem;
}
.cover .bismillah {
  font-family: 'Amiri', serif;
  font-size: 2.2rem;
  color: var(--muted);
  display: block;
  margin-bottom: 2rem;
  direction: rtl;
}
.cover h1 { font-size: 3.1rem; font-weight: 400; line-height: 1.15; color: var(--text); }
.cover .arabic-title {
  font-family: 'Amiri', serif;
  font-size: 1.9rem;
  color: var(--muted);
  display: block;
  margin-top: .4rem;
  direction: rtl;
}
.cover .ornament { display: block; color: var(--gold); font-size: 1.4rem; margin: 1.5rem 0; letter-spacing: .4em; }
.cover .subtitle { font-size: 1.05rem; color: var(--muted); font-style: italic; max-width: 480px; margin: 0 auto; }

.toc h2 {
  font-size: .75rem;
  text-transform: uppercase;
  letter-spacing: .15em;
  color: var(--muted);
  font-weight: 400;
  margin-bottom: 1.5rem;
}
.toc-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(295px, 1fr));
  gap: 1rem;
  margin-bottom: 1.25rem;
}
.toc-card {
  display: block;
  padding: 1.2rem 1.5rem;
  border: 1px solid var(--border);
  text-decoration: none;
  color: inherit;
  background: var(--bg);
  position: relative;
  transition: border-color .18s, background .18s, box-shadow .18s;
}
.toc-card::after {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 3px;
  background: var(--accent);
  opacity: 0;
  transition: opacity .18s;
}
.toc-card:hover { background: var(--bg-alt); border-color: #c8a080; box-shadow: 0 2px 10px rgba(0,0,0,.07); }
.toc-card:hover::after { opacity: 1; }
.toc-card .part-num { font-size: .68rem; text-transform: uppercase; letter-spacing: .14em; color: var(--accent); display: block; margin-bottom: .3rem; }
.toc-card .part-name { font-size: 1.1rem; color: var(--text); display: block; line-height: 1.3; }
.toc-card .part-detail { font-size: .8rem; color: var(--muted); font-style: italic; display: block; margin-top: .2rem; }
.toc-ref-links { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: .75rem; }
.toc-rel {
  display: block;
  padding: .85rem 1.5rem;
  border: 1px solid var(--border);
  text-decoration: none;
  color: var(--muted);
  font-style: italic;
  font-size: .93rem;
  text-align: center;
  transition: border-color .18s, color .18s;
}
.toc-rel:hover { border-color: var(--gold); color: var(--gold); }

/* ── Part header ── */

.part-header {
  margin-bottom: 3.5rem;
  padding-bottom: 2rem;
  border-bottom: 2px solid var(--accent);
}
.part-header .part-label {
  font-size: .7rem;
  text-transform: uppercase;
  letter-spacing: .16em;
  color: var(--accent);
  display: block;
  margin-bottom: .7rem;
}
.part-header h1 { font-size: 2.5rem; font-weight: 400; line-height: 1.2; color: var(--text); margin-bottom: .4rem; }
.part-header .part-sub { font-size: 1rem; color: var(--muted); font-style: italic; }

/* ── Historical Context ── */

.context-section { margin-bottom: 4rem; }
.context-section h2 {
  font-size: 1.05rem;
  font-weight: 400;
  font-style: italic;
  color: var(--muted);
  margin-bottom: 1.2rem;
  padding-bottom: .35rem;
  border-bottom: 1px solid var(--border);
}
.context-section p { margin-bottom: 1rem; }
.context-section p:last-child { margin-bottom: 0; }

/* ── Chapter ── */

.chapter { margin-bottom: 6rem; padding-top: 1.5rem; }
.chapter-header { margin-bottom: 1.75rem; }
.chapter-header .ch-label {
  font-size: .68rem;
  text-transform: uppercase;
  letter-spacing: .16em;
  color: var(--accent);
  display: block;
  margin-bottom: .5rem;
}
.chapter-header h2 { font-size: 1.95rem; font-weight: 400; line-height: 1.25; color: var(--text); }
.chapter-header .ch-arabic {
  font-family: 'Amiri', serif;
  font-size: 1.4rem;
  color: var(--muted);
  display: block;
  direction: rtl;
  text-align: right;
  margin-top: .3rem;
}

/* ── Metadata ── */

.metadata {
  margin: 1.75rem 0 2.25rem;
  padding: 1.2rem 1.75rem;
  background: var(--bg-alt);
  border-left: 3px solid var(--gold);
  font-size: .9rem;
}
.meta-row {
  display: grid;
  grid-template-columns: 150px 1fr;
  gap: .15rem .75rem;
  padding: .17rem 0;
  line-height: 1.6;
}
.meta-key {
  font-weight: 600;
  color: var(--muted);
  font-size: .78rem;
  text-transform: uppercase;
  letter-spacing: .04em;
  padding-top: .1rem;
}
.meta-val { color: var(--text); }

/* ── Sections ── */

.section-heading {
  font-size: 1.08rem;
  font-weight: 400;
  font-style: italic;
  color: var(--accent);
  margin: 2.5rem 0 1rem;
  padding-bottom: .3rem;
  border-bottom: 1px solid var(--border);
}
.chapter p { margin-bottom: 1rem; }
.chapter p:last-child { margin-bottom: 0; }
.chapter ul { margin: .5rem 0 1rem 1.5rem; }
.chapter li { margin-bottom: .3rem; }

.story-block {
  margin: 1.25rem 0;
  padding: 1rem 1.5rem 1rem 1.25rem;
  background: rgba(154,112,16,.05);
  border-left: 2px solid var(--gold);
}
.story-block p { margin-bottom: 0; }

.chapter-rule { border: none; border-top: 1px solid var(--border); margin: 5rem 0 0; }

/* ── Afterword ── */

.afterword { margin-top: 4rem; padding-top: 2.5rem; border-top: 2px solid var(--accent); }
.afterword h2 { font-size: 1.8rem; font-weight: 400; margin-bottom: 1.5rem; }
.afterword p { margin-bottom: 1rem; }

/* ── Relationships page ── */

.rel-page h1 { font-size: 2.3rem; font-weight: 400; margin-bottom: .75rem; }
.rel-intro { color: var(--muted); font-style: italic; margin-bottom: 3rem; padding-bottom: 2rem; border-bottom: 1px solid var(--border); }
.era-heading {
  font-size: 1.45rem;
  font-weight: 400;
  color: var(--text);
  margin: 3.5rem 0 1.25rem;
  padding-bottom: .5rem;
  border-bottom: 1px solid var(--border);
}
.mermaid {
  background: var(--bg-alt);
  border: 1px solid var(--border);
  border-radius: 2px;
  padding: 1.5rem;
  overflow-x: auto;
  margin: .75rem 0;
  font-size: .875rem;
}
.era-note { font-size: .88rem; color: var(--muted); margin-top: .5rem; line-height: 1.65; }
.era-note strong { color: var(--text); font-weight: 600; }

/* ── Tables ── */

.summary-table {
  width: 100%;
  border-collapse: collapse;
  font-size: .9rem;
  margin-top: 1rem;
}
.summary-table th {
  text-align: left;
  padding: .6rem 1rem;
  background: var(--bg-alt);
  border-bottom: 2px solid var(--border);
  color: var(--muted);
  font-weight: 600;
  font-size: .72rem;
  text-transform: uppercase;
  letter-spacing: .09em;
}
.summary-table td { padding: .55rem 1rem; border-bottom: 1px solid var(--border); vertical-align: top; }
.summary-table tr:last-child td { border-bottom: none; }
.summary-table tr:hover td { background: var(--bg-alt); }

/* ── Full index ── */

.full-index h1 { font-size: 2.3rem; font-weight: 400; margin-bottom: 2rem; padding-bottom: 1.5rem; border-bottom: 2px solid var(--accent); }
.full-index .era-heading { font-size: 1.2rem; margin: 2.5rem 0 .75rem; }
.full-index .summary-table { font-size: .82rem; }
.full-index .summary-table td:first-child { font-weight: 600; white-space: nowrap; }

/* ── Page nav ── */

.page-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 5rem;
  padding-top: 1.75rem;
  border-top: 1px solid var(--border);
  font-size: .875rem;
}
.page-nav a { color: var(--accent); text-decoration: none; }
.page-nav a:hover { text-decoration: underline; color: var(--gold); }

/* ── Timeline ── */

.tl-page h1 { font-size: 2.3rem; font-weight: 400; margin-bottom: .75rem; }
.tl-intro {
  color: var(--muted);
  font-style: italic;
  margin-bottom: 2rem;
  padding-bottom: 1.75rem;
  border-bottom: 1px solid var(--border);
  font-size: .95rem;
}

.tl-legend {
  display: flex;
  flex-wrap: wrap;
  gap: .4rem .75rem;
  margin-bottom: 2.5rem;
  padding: .9rem 1.25rem;
  background: var(--bg-alt);
  border: 1px solid var(--border);
  font-size: .78rem;
}
.tl-legend-item {
  display: flex;
  align-items: center;
  gap: .35rem;
  color: var(--muted);
}
.tl-legend-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}

.tl-wrap {
  position: relative;
  padding-left: 115px;
}
/* The spine */
.tl-wrap::before {
  content: '';
  position: absolute;
  left: 107px;
  top: 0; bottom: 0;
  width: 2px;
  background: linear-gradient(to bottom, var(--accent) 0%, var(--border) 60%, rgba(200,152,14,.4) 100%);
}

/* Era banner */
.tl-era {
  position: relative;
  margin: 2.75rem 0 .6rem -115px;
  padding-left: 0;
}
.tl-era-inner {
  display: inline-flex;
  align-items: baseline;
  gap: .65rem;
  background: var(--bg-alt);
  border: 1px solid var(--border);
  border-left: 3px solid var(--accent);
  padding: .45rem 1rem .45rem .9rem;
  position: relative;
  z-index: 1;
}
.tl-era-inner::after {
  content: '';
  position: absolute;
  right: -9999px;
  left: 100%;
  top: 50%;
  height: 1px;
  background: var(--border);
  opacity: .5;
}
.tl-era-num {
  font-size: .65rem;
  text-transform: uppercase;
  letter-spacing: .14em;
  color: var(--accent);
  font-weight: 600;
}
.tl-era-name {
  font-size: .95rem;
  color: var(--text);
  font-style: italic;
}
.tl-era-dates {
  font-size: .73rem;
  color: var(--muted);
}

/* Entry row */
.tl-entry {
  display: grid;
  grid-template-columns: 103px 14px 1fr;
  gap: 0 10px;
  align-items: start;
  padding: 3px 0;
}
.tl-year {
  text-align: right;
  font-size: .7rem;
  color: var(--muted);
  padding-top: 5px;
  font-variant-numeric: tabular-nums;
  letter-spacing: -.01em;
}
.tl-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
  position: relative;
  top: 5px;
  z-index: 2;
  border: 2px solid var(--bg);
}
.tl-card {
  padding: 2px 0 7px 10px;
  border-left: 2px solid var(--border);
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: .15rem .45rem;
}
.tl-name {
  font-size: .92rem;
  color: var(--text);
  text-decoration: none;
  font-weight: 500;
}
.tl-name:hover { color: var(--accent); text-decoration: underline; }
.tl-arabic {
  font-family: 'Amiri', serif;
  font-size: .82rem;
  color: var(--muted);
}
.tl-place {
  font-size: .72rem;
  color: var(--muted);
  font-style: italic;
  white-space: nowrap;
}
.tl-place::before { content: '\00b7\0020'; }
.tl-order {
  font-size: .65rem;
  padding: 1px 7px 1px 6px;
  border-radius: 10px;
  border: 1px solid;
  white-space: nowrap;
  margin-top: 2px;
}

/* ── By-Order page ── */

.order-page h1 { font-size: 2.3rem; font-weight: 400; margin-bottom: .75rem; }
.order-intro {
  color: var(--muted);
  font-style: italic;
  margin-bottom: 2.5rem;
  padding-bottom: 1.75rem;
  border-bottom: 1px solid var(--border);
  font-size: .95rem;
}
.order-section { margin-bottom: 3.5rem; }
.order-section-head {
  display: flex;
  align-items: baseline;
  gap: .75rem;
  margin-bottom: 1rem;
  padding: .5rem .9rem;
  background: var(--bg-alt);
  border-left: 4px solid;
  border-bottom: 1px solid var(--border);
}
.order-section-name { font-size: 1.2rem; font-weight: 400; color: var(--text); }
.order-section-count { font-size: .78rem; color: var(--muted); font-style: italic; }
.order-fig-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: .5rem;
}
.order-fig-card {
  padding: .65rem .9rem;
  border: 1px solid var(--border);
  background: var(--bg);
  display: flex;
  flex-direction: column;
  gap: .15rem;
  transition: background .15s, border-color .15s;
}
.order-fig-card:hover { background: var(--bg-alt); border-color: #c8a080; }
.order-fig-ch {
  font-size: .62rem;
  text-transform: uppercase;
  letter-spacing: .1em;
  color: var(--accent);
}
.order-fig-name {
  font-size: .92rem;
  font-weight: 500;
  color: var(--text);
  text-decoration: none;
  line-height: 1.3;
}
.order-fig-name:hover { color: var(--accent); }
.order-fig-arabic {
  font-family: 'Amiri', serif;
  font-size: .82rem;
  color: var(--muted);
  direction: rtl;
  text-align: left;
}
.order-fig-born { font-size: .72rem; color: var(--muted); font-style: italic; }

/* ── Mobile ── */

@media (max-width: 900px) {
  .layout { grid-template-columns: 1fr; }
  .sidebar { position: static; height: auto; }
  .sidebar nav { display: none; }
  .main { padding: 2rem 1.5rem 4rem; }
  .cover h1 { font-size: 2.25rem; }
  .chapter-header h2 { font-size: 1.6rem; }
  .meta-row { grid-template-columns: 1fr; gap: 0; }
  .meta-key { padding-top: .5rem; }
  .tl-wrap { padding-left: 75px; }
  .tl-wrap::before { left: 67px; }
  .tl-era { margin-left: -75px; }
  .tl-entry { grid-template-columns: 63px 12px 1fr; }
  .tl-year { font-size: .62rem; }
}
@media (max-width: 600px) {
  .toc-grid { grid-template-columns: 1fr; }
  .cover .bismillah { font-size: 1.75rem; }
  .tl-place, .tl-arabic { display: none; }
}
"""

# ── Markdown helpers ──────────────────────────────────────────────────────────

def inline(text):
    """HTML-escape then convert **bold** and *italic* markdown."""
    text = escape(text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'(?<!\*)\*([^*\n]+?)\*(?!\*)', r'<em>\1</em>', text)
    return text


def blocks_to_html(text):
    """Convert a block of markdown body text to HTML paragraphs/lists."""
    if not text:
        return ''
    text = re.sub(r'^---+\s*$', '', text, flags=re.MULTILINE)
    text = text.strip()
    if not text:
        return ''

    parts = []
    for block in re.split(r'\n{2,}', text):
        block = block.strip()
        if not block or re.match(r'^---+$', block):
            continue

        lines = [l for l in block.split('\n') if l.strip()]
        if not lines:
            continue

        # Unordered list
        if all(re.match(r'^\s*[-*]\s', l) for l in lines):
            items = [inline(re.sub(r'^\s*[-*]\s+', '', l)) for l in lines]
            parts.append('<ul>' + ''.join(f'<li>{it}</li>' for it in items) + '</ul>')
        # Named / story block: **Title:** text
        elif re.match(r'^\*\*[^\n*]+:\*\*', block):
            para = ' '.join(l.strip() for l in lines)
            parts.append(f'<div class="story-block"><p>{inline(para)}</p></div>')
        # Regular paragraph
        else:
            para = ' '.join(l.strip() for l in lines)
            parts.append(f'<p>{inline(para)}</p>')

    return '\n'.join(parts)


# ── Chapter rendering ─────────────────────────────────────────────────────────

def render_chapter(heading_line, body):
    heading_line = heading_line.strip()
    m = re.match(r'^## Chapter (\d+): (.+)\s*$', heading_line)
    if not m:
        return ''

    ch_num     = m.group(1)
    full_title = m.group(2).strip()

    arabic_m = re.search(r'\(([^)]+)\)\s*$', full_title)
    if arabic_m:
        ch_arabic = arabic_m.group(1)
        ch_title  = full_title[:arabic_m.start()].strip()
    else:
        ch_arabic = ''
        ch_title  = full_title

    ch_id = f'ch-{ch_num}'

    first_sec = re.search(r'\n### ', body)
    if first_sec:
        meta_text     = body[:first_sec.start()]
        sections_text = body[first_sec.start():]
    else:
        meta_text     = body
        sections_text = ''

    afterword_html = ''
    aw = re.search(r'\n## Afterword', sections_text)
    if aw:
        afterword_html = render_afterword(sections_text[aw.start():])
        sections_text  = sections_text[:aw.start()]

    meta_rows = []
    for line in meta_text.split('\n'):
        mm = re.match(r'^\*\*([^*]+):\*\*\s*(.*)', line.strip())
        if mm:
            meta_rows.append((mm.group(1), mm.group(2).strip()))

    sections = []
    for sec in re.split(r'\n### ', '\n' + sections_text):
        sec = sec.strip()
        if not sec:
            continue
        head, _, content = sec.partition('\n')
        sections.append((head.strip(), content.strip()))

    arabic_html = (
        f'<span class="ch-arabic">{escape(ch_arabic)}</span>'
        if ch_arabic else ''
    )

    meta_html = ''
    if meta_rows:
        rows_html = ''.join(
            f'<div class="meta-row">'
            f'<span class="meta-key">{escape(k)}</span>'
            f'<span class="meta-val">{inline(v)}</span>'
            f'</div>'
            for k, v in meta_rows
        )
        meta_html = f'<div class="metadata">{rows_html}</div>'

    sections_html = ''.join(
        f'<h3 class="section-heading">{escape(h)}</h3>\n{blocks_to_html(c)}\n'
        for h, c in sections
    )

    return (
        f'<div class="chapter" id="{ch_id}">\n'
        f'  <div class="chapter-header">\n'
        f'    <span class="ch-label">Chapter {ch_num}</span>\n'
        f'    <h2>{inline(ch_title)}</h2>\n'
        f'    {arabic_html}\n'
        f'  </div>\n'
        f'  {meta_html}\n'
        f'  {sections_html}\n'
        f'</div>\n'
        f'<hr class="chapter-rule">\n'
        f'{afterword_html}'
    )


def render_afterword(md_text):
    lines   = md_text.strip().split('\n')
    heading = lines[0].lstrip('#').strip()
    content = '\n'.join(lines[1:]).strip()
    return (
        f'<div class="afterword">\n'
        f'  <h2>{inline(heading)}</h2>\n'
        f'  {blocks_to_html(content)}\n'
        f'</div>\n'
    )


def render_part_intro(intro_text):
    m = re.search(r'^## Historical Context\s*$', intro_text, re.MULTILINE)
    if not m:
        return ''
    content = intro_text[m.end():].strip()
    content = re.sub(r'^---+\s*$', '', content, flags=re.MULTILINE).strip()
    return (
        f'<div class="context-section">\n'
        f'  <h2>Historical Context</h2>\n'
        f'  {blocks_to_html(content)}\n'
        f'</div>\n'
    )


# ── Relationships page helpers ────────────────────────────────────────────────

def render_rel_text(text):
    if not text.strip():
        return ''

    out        = []
    table_rows = []
    para_lines = []

    def flush_para():
        if para_lines:
            joined = ' '.join(para_lines).strip()
            if joined:
                out.append(f'<p class="era-note">{inline(joined)}</p>')
            para_lines.clear()

    def flush_table():
        if len(table_rows) < 2:
            table_rows.clear()
            return
        th = ''.join(f'<th>{inline(c.strip())}</th>' for c in table_rows[0])
        trs = []
        for row in table_rows[2:]:
            if not any(c.strip() for c in row):
                continue
            td = ''.join(f'<td>{inline(c.strip())}</td>' for c in row)
            trs.append(f'<tr>{td}</tr>')
        out.append(
            f'<table class="summary-table">'
            f'<thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(trs)}</tbody>'
            f'</table>'
        )
        table_rows.clear()

    for line in text.split('\n'):
        s = line.strip()

        if s.startswith('|') and s.endswith('|'):
            flush_para()
            table_rows.append([c for c in s[1:-1].split('|')])
            continue

        if table_rows and not (s.startswith('|') and s.endswith('|')):
            flush_table()

        if re.match(r'^-{3,}$', s):
            flush_para()
            continue

        if re.match(r'^# [^#]', s):
            flush_para()
            continue

        if s.startswith('## '):
            flush_para()
            out.append(f'<h2 class="era-heading">{inline(s[3:].strip())}</h2>')
            continue

        if not s:
            flush_para()
            continue

        para_lines.append(s)

    flush_para()
    if table_rows:
        flush_table()

    return '\n'.join(h for h in out if h)


def render_rel_page(md_text):
    parts = re.split(r'```mermaid\n(.*?)```', md_text, flags=re.DOTALL)
    out = []
    for i, part in enumerate(parts):
        if i % 2 == 1:
            out.append(f'<div class="mermaid">\n{escape(part.strip())}\n</div>')
        else:
            rendered = render_rel_text(part)
            if rendered.strip():
                out.append(rendered)
    return '\n'.join(out)


# ── Timeline helpers ──────────────────────────────────────────────────────────

# Color per order family (keyword → hex)
_ORDER_COLORS = [
    ('pre-tariqa',    '#7a6248'),
    ('qadiri',        '#2d6a4f'),
    ('chishti',       '#c07030'),
    ('naqshbandi',    '#2c5f8a'),
    ('shadhili',      '#3a7878'),
    ('alawi',         '#7a1a1a'),
    ("ba'alawi",      '#7a1a1a'),
    ('tijani',        '#9a7010'),
    ('mourid',        '#1a6b42'),
    ('mevlevi',       '#b86820'),
    ("rifa'i",        '#5a7030'),
    ('rifa',          '#5a7030'),
    ('kubra',         '#5a3d7a'),
    ('suhrawardi',    '#7a4a8a'),
    ('khalwati',      '#2d4a70'),
    ('yasawi',        '#8b5a2b'),
    ('sanusi',        '#4a6b8a'),
    ('inayati',       '#8a3d6b'),
    ('maryami',       '#3d5a8a'),
    ('universal',     '#8a3d6b'),
]

LEGEND_ENTRIES = [
    ('Pre-tariqa era',          '#7a6248'),
    ('Qadiriyya',               '#2d6a4f'),
    ('Chishtiyya',              '#c07030'),
    ('Naqshbandiyya',           '#2c5f8a'),
    ('Shadhiliyya / Alawiyya',  '#3a7878'),
    ("Ba'alawiyya",             '#7a1a1a'),
    ('Tijaniyya',               '#9a7010'),
    ('Mouridiyya',              '#1a6b42'),
    ('Mevleviyya / Rifa\'iyya', '#b86820'),
    ('Suhrawardiyya / Kubrawiyya', '#7a4a8a'),
    ('Khalwatiyya',             '#2d4a70'),
    ('Others',                  '#8a6840'),
]


# Canonical order families for the By-Order page
_CANONICAL_ORDERS = [
    ('Pre-Tariqa Era',             '#7a6248', ['pre-tariqa']),
    ('Qadiriyya',                  '#2d6a4f', ['qadiri']),
    ('Chishtiyya',                 '#c07030', ['chishti']),
    ('Naqshbandiyya',              '#2c5f8a', ['naqshbandi']),
    ('Shadhiliyya / Alawiyya',     '#3a7878', ['shadhili']),
    ("Ba'alawiyya",                '#7a1a1a', ["ba'alawi", 'alawi']),
    ('Suhrawardiyya / Kubrawiyya', '#7a4a8a', ['suhrawardi', 'kubra']),
    ('Khalwatiyya',                '#2d4a70', ['khalwati']),
    ("Rifa'iyya",                  '#5a7030', ["rifa'i", 'rifa']),
    ('Mevleviyya',                 '#b86820', ['mevlevi']),
    ('Yasawiyya',                  '#8b5a2b', ['yasawi']),
    ('Tijaniyya',                  '#9a7010', ['tijani']),
    ('Mouridiyya',                 '#1a6b42', ['mourid']),
    ('Sanusiyya',                  '#4a6b8a', ['sanusi']),
    ('Universal Sufi / Inayati',   '#8a3d6b', ['inayati', 'maryami', 'universal']),
]


def order_color(tariqah):
    t = tariqah.lower()
    for key, color in _ORDER_COLORS:
        if key in t:
            return color
    return '#8a6840'


def order_family(tariqah):
    """Return (display_name, color) for the canonical order family."""
    t = tariqah.lower()
    for name, color, keywords in _CANONICAL_ORDERS:
        if any(kw in t for kw in keywords):
            return name, color
    return 'Independent / Other', '#8a6840'


def parse_ce_year(born_str):
    """Extract the approximate CE birth year from a Born string."""
    s = born_str

    # "pre-NNN CE"
    m = re.search(r'pre-(\d{3,4})\s*CE', s)
    if m:
        return int(m.group(1)) - 15

    # Range "NNN–NNN CE"
    m = re.search(r'(\d{3,4})[–\-](\d{3,4})\s*CE', s)
    if m:
        return (int(m.group(1)) + int(m.group(2))) // 2

    # Single CE year
    m = re.search(r'(\d{3,4})\s*CE', s)
    if m:
        return int(m.group(1))

    # "Nth century AH" without CE
    m = re.search(r'(\d+)(?:st|nd|rd|th)\s+century\s+AH', s)
    if m:
        n = int(m.group(1))
        return 622 + (n - 1) * 97 + 48   # mid-century estimate

    return 0


def parse_index_figures():
    """Parse all figures from index.md, return list of dicts sorted by (part, ce_year)."""
    md = (BASE_DIR / 'index.md').read_text(encoding='utf-8')

    PART_WORDS = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7}
    current_part = 0
    figures = []

    for line in md.split('\n'):
        # Part heading
        m = re.match(r'^## Part (\w+):', line)
        if m:
            current_part = PART_WORDS.get(m.group(1), 0)
            continue

        # Table data row
        if not (line.startswith('|') and line.endswith('|')):
            continue
        cells = [c.strip() for c in line[1:-1].split('|')]
        if len(cells) < 5:
            continue
        ch_str, name_full, born_str, place, tariqah = cells[:5]
        if ch_str in ('#', '---', '') or not re.match(r'^\d+$', ch_str):
            continue

        # Separate English name from Arabic
        am = re.search(r'\(([^)]+)\)\s*$', name_full)
        arabic  = am.group(1) if am else ''
        name_en = name_full[:am.start()].strip() if am else name_full.strip()

        # Clean tariqah for display
        tariqah_disp = re.sub(r'\*\*([^*]+)\*\*', r'\1', tariqah)
        tariqah_disp = re.sub(
            r'\s*\((founder|systematizer|consolidating founder|established in India|'
            r'founder of branch|founder of sub-branch|key link[^)]*|'
            r'uncle and teacher[^)]*|student of[^)]*|'
            r'Sayyid al-Ta\'ifa[^)]*|nearly all[^)]*|virtually all[^)]*|'
            r'ancestor of[^)]*|Uwaysi[^)]*|Mujaddid[^)]*|author of[^)]*|'
            r'Junaidi[^)]*|Hanbali[^)]*|Akbarian[^)]*)\)',
            '', tariqah_disp, flags=re.IGNORECASE
        ).strip()
        if len(tariqah_disp) > 48:
            tariqah_disp = tariqah_disp[:45] + '\u2026'

        figures.append({
            'ch_num':   int(ch_str),
            'name':     name_en,
            'arabic':   arabic,
            'born_str': born_str,
            'ce_year':  parse_ce_year(born_str),
            'place':    place,
            'tariqah':  tariqah,
            'tariqah_disp': tariqah_disp,
            'part':     current_part,
        })

    return sorted(figures, key=lambda f: (f['part'], f['ce_year']))


# ── HTML scaffolding ──────────────────────────────────────────────────────────

def make_sidebar(current, chapter_anchors=None):
    lines = ['<span class="nav-section">Parts</span>']
    for n, name, period, chrange in PARTS:
        cls = 'nav-part active' if current == f'part{n}' else 'nav-part'
        lines.append(f'<a href="part{n}.html" class="{cls}">Part {n}: {escape(name)}</a>')
        if current == f'part{n}' and chapter_anchors:
            for ch_num, ch_short, ch_id in chapter_anchors:
                lines.append(
                    f'<a href="#{ch_id}" class="nav-ch">'
                    f'Ch.{ch_num} &middot; {escape(ch_short)}</a>'
                )
    lines.append('<span class="nav-section">Reference</span>')
    for page, label in [
        ('relationships', 'Relationship Graphs'),
        ('timeline',      'Timeline'),
        ('by-order',      'By Sufi Order'),
        ('full-index',    'Full Index'),
    ]:
        cls = 'nav-part active' if current == page else 'nav-part'
        lines.append(f'<a href="{page}.html" class="{cls}">{label}</a>')

    nav_html = '\n'.join(lines)
    return (
        f'<div class="sidebar-inner">'
        f'<div class="sidebar-brand">'
        f'<a href="index.html">← Home</a>'
        f'<span class="brand-title">The Book of<br>the Mashaikh</span>'
        f'</div>'
        f'<nav>{nav_html}</nav>'
        f'</div>'
    )


def page_shell(title, sidebar, main_content, extra_foot=''):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{escape(title)}</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="layout">
  <aside class="sidebar">{sidebar}</aside>
  <main class="main">{main_content}</main>
</div>
{extra_foot}
</body>
</html>"""


# ── Page builders ─────────────────────────────────────────────────────────────

def build_index():
    cards = ''.join(
        f'<a href="part{n}.html" class="toc-card">'
        f'<span class="part-num">Part {n}</span>'
        f'<span class="part-name">{escape(name)}</span>'
        f'<span class="part-detail">{escape(period)} &middot; {escape(chrange)}</span>'
        f'</a>\n'
        for n, name, period, chrange in PARTS
    )
    main = (
        '<div class="cover">'
        '<span class="bismillah">بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ</span>'
        '<h1>The Book of the Mashaikh</h1>'
        '<span class="arabic-title">كِتَابُ الْمَشَايِخ</span>'
        '<span class="ornament">❦ ❦ ❦</span>'
        '<p class="subtitle">A comprehensive guide to one hundred luminaries of Tasawwuf, arranged by era</p>'
        '</div>'
        '<div class="toc"><h2>Contents</h2>'
        f'<div class="toc-grid">{cards}</div>'
        '<div class="toc-ref-links">'
        '<a href="relationships.html" class="toc-rel">Relationship Graphs by Era</a>'
        '<a href="timeline.html" class="toc-rel">Timeline of All 126 Figures</a>'
        '<a href="by-order.html" class="toc-rel">Figures by Sufi Order</a>'
        '<a href="full-index.html" class="toc-rel">Complete Index</a>'
        '</div>'
        '</div>'
    )
    return page_shell('The Book of the Mashaikh', make_sidebar('index'), main)


def build_part(n):
    _, name, period, chrange = PARTS[n - 1]
    md_text = (BASE_DIR / f'part{n}.md').read_text(encoding='utf-8')

    chunks         = re.split(r'\n(?=## Chapter \d+)', md_text)
    intro_text     = chunks[0]
    chapter_chunks = chunks[1:]

    part_header = (
        f'<header class="part-header">'
        f'<span class="part-label">Part {n}</span>'
        f'<h1>{escape(name)}</h1>'
        f'<p class="part-sub">{escape(period)} &middot; {escape(chrange)}</p>'
        f'</header>'
    )

    context_html  = render_part_intro(intro_text)
    chapters_html = ''
    anchors       = []

    for chunk in chapter_chunks:
        heading_line, _, body = chunk.partition('\n')
        m = re.match(r'^## Chapter (\d+): (.+?)(?:\s+\([^)]+\))?\s*$', heading_line.strip())
        if m:
            ch_num   = m.group(1)
            ch_title = m.group(2).strip()
            short    = ch_title[:38] + '\u2026' if len(ch_title) > 38 else ch_title
            anchors.append((ch_num, short, f'ch-{ch_num}'))
        chapters_html += render_chapter(heading_line, body)

    prev = (f'<a href="part{n-1}.html">&larr; Part {n-1}</a>'
            if n > 1 else '<a href="index.html">&larr; Contents</a>')
    nxt  = (f'<a href="part{n+1}.html">Part {n+1} &rarr;</a>'
            if n < 7 else '<a href="relationships.html">Relationship Graphs &rarr;</a>')
    page_nav = f'<nav class="page-nav"><span>{prev}</span><span>{nxt}</span></nav>'

    main    = part_header + context_html + chapters_html + page_nav
    sidebar = make_sidebar(f'part{n}', anchors)
    return page_shell(f'Part {n}: {name} — The Book of the Mashaikh', sidebar, main)


def build_relationships():
    md   = (BASE_DIR / 'relationships.md').read_text(encoding='utf-8')
    body = render_rel_page(md)
    main = f'<div class="rel-page"><h1>Relationship Graphs by Era</h1>\n{body}</div>'

    mermaid_init = (
        '<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>\n'
        '<script>\n'
        'mermaid.initialize({\n'
        '  startOnLoad: true, theme: "base",\n'
        '  themeVariables: {\n'
        '    primaryColor: "#f1e8d3", primaryTextColor: "#1e1609",\n'
        '    primaryBorderColor: "#c8a890", lineColor: "#9a7010",\n'
        '    secondaryColor: "#f9f5eb", tertiaryColor: "#f1e8d3",\n'
        '    clusterBkg: "#faf7f0", clusterBorder: "#d8c8a4",\n'
        '    edgeLabelBackground: "#f9f5eb", titleColor: "#1e1609",\n'
        '    fontFamily: "EB Garamond, Georgia, serif", fontSize: "15px"\n'
        '  }\n'
        '});\n'
        '</script>'
    )
    return page_shell(
        'Relationship Graphs — The Book of the Mashaikh',
        make_sidebar('relationships'), main, extra_foot=mermaid_init
    )


def build_timeline():
    figures = parse_index_figures()

    # Legend
    legend_html = ''.join(
        f'<span class="tl-legend-item">'
        f'<span class="tl-legend-dot" style="background:{color}"></span>'
        f'{escape(label)}'
        f'</span>'
        for label, color in LEGEND_ENTRIES
    )

    # Group by part
    by_part = {}
    for fig in figures:
        by_part.setdefault(fig['part'], []).append(fig)

    rows = []
    for n, name, period, chrange in PARTS:
        dates, ah = PART_ERA_DATES[n]
        rows.append(
            f'<div class="tl-era" id="tl-part{n}">'
            f'<div class="tl-era-inner">'
            f'<span class="tl-era-num">Part {n}</span>'
            f'<span class="tl-era-name">{escape(name)}</span>'
            f'<span class="tl-era-dates">{escape(dates)}</span>'
            f'</div></div>'
        )
        for fig in by_part.get(n, []):
            color = order_color(fig['tariqah'])
            ce    = fig['ce_year']
            if ce:
                # Show "c." only when the source string implies approximation
                approx = 'c.\u202f' if re.search(r'\bc\.', fig['born_str']) else ''
                year_disp = f'{approx}{ce} CE'
            else:
                year_disp = '?'

            rows.append(
                f'<div class="tl-entry">'
                f'<span class="tl-year">{year_disp}</span>'
                f'<span class="tl-dot" style="background:{color}"></span>'
                f'<div class="tl-card">'
                f'<a href="part{fig["part"]}.html#ch-{fig["ch_num"]}" class="tl-name">'
                f'{inline(fig["name"])}</a>'
                f'<span class="tl-arabic" dir="rtl">{escape(fig["arabic"])}</span>'
                f'<span class="tl-place">{escape(fig["place"])}</span>'
                f'<span class="tl-order" style="border-color:{color};color:{color}">'
                f'{escape(fig["tariqah_disp"])}</span>'
                f'</div></div>'
            )

    main = (
        f'<div class="tl-page">'
        f'<h1>Timeline of the Mashaikh</h1>'
        f'<p class="tl-intro">126 luminaries arranged chronologically across 14 centuries. '
        f'Each name links to its chapter.</p>'
        f'<div class="tl-legend">{legend_html}</div>'
        f'<div class="tl-wrap">{"".join(rows)}</div>'
        f'</div>'
    )
    return page_shell(
        'Timeline — The Book of the Mashaikh',
        make_sidebar('timeline'), main
    )


def build_by_order():
    figures = parse_index_figures()

    # Group by canonical order family, preserving canonical sort order
    order_index = {name: i for i, (name, _, _) in enumerate(_CANONICAL_ORDERS)}
    order_index['Independent / Other'] = len(_CANONICAL_ORDERS)

    groups = {}
    for fig in figures:
        fam_name, _ = order_family(fig['tariqah'])
        groups.setdefault(fam_name, []).append(fig)

    sorted_groups = sorted(
        groups.items(),
        key=lambda kv: order_index.get(kv[0], 999)
    )

    sections = []
    for fam_name, figs in sorted_groups:
        _, color = order_family(figs[0]['tariqah'])
        slug = re.sub(r'[^a-z0-9]+', '-', fam_name.lower()).strip('-')
        count = len(figs)

        cards = []
        for fig in figs:
            born_disp = fig['born_str']
            if len(born_disp) > 42:
                born_disp = born_disp[:39] + '\u2026'
            cards.append(
                f'<div class="order-fig-card">'
                f'<span class="order-fig-ch">Ch.\u202f{fig["ch_num"]}</span>'
                f'<a href="part{fig["part"]}.html#ch-{fig["ch_num"]}" class="order-fig-name">'
                f'{inline(fig["name"])}</a>'
                f'<span class="order-fig-arabic" dir="rtl">{escape(fig["arabic"])}</span>'
                f'<span class="order-fig-born">{escape(born_disp)}</span>'
                f'</div>'
            )

        sections.append(
            f'<div class="order-section" id="order-{slug}">'
            f'<div class="order-section-head" style="border-left-color:{color}">'
            f'<span class="order-section-name">{escape(fam_name)}</span>'
            f'<span class="order-section-count">'
            f'{count}\u202ffigure{"s" if count != 1 else ""}</span>'
            f'</div>'
            f'<div class="order-fig-grid">{"".join(cards)}</div>'
            f'</div>'
        )

    main = (
        f'<div class="order-page">'
        f'<h1>By Sufi Order</h1>'
        f'<p class="order-intro">126 luminaries of Tasawwuf grouped by their primary spiritual '
        f'affiliation, ordered from earliest to most recent order. '
        f'Each name links to its chapter.</p>'
        f'{"".join(sections)}'
        f'</div>'
    )
    return page_shell(
        'By Sufi Order \u2014 The Book of the Mashaikh',
        make_sidebar('by-order'), main
    )


def build_full_index():
    md   = (BASE_DIR / 'index.md').read_text(encoding='utf-8')
    body = render_rel_text(md)
    main = f'<div class="full-index"><h1>Complete Index</h1>\n{body}</div>'
    return page_shell(
        'Complete Index — The Book of the Mashaikh',
        make_sidebar('full-index'), main
    )


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if SITE_DIR.exists():
        shutil.rmtree(SITE_DIR)
    SITE_DIR.mkdir()

    (SITE_DIR / 'style.css').write_text(CSS, encoding='utf-8')
    print('  style.css')

    (SITE_DIR / 'index.html').write_text(build_index(), encoding='utf-8')
    print('  index.html')

    for n, name, _, _ in PARTS:
        (SITE_DIR / f'part{n}.html').write_text(build_part(n), encoding='utf-8')
        print(f'  part{n}.html  ({name})')

    (SITE_DIR / 'relationships.html').write_text(build_relationships(), encoding='utf-8')
    print('  relationships.html')

    (SITE_DIR / 'timeline.html').write_text(build_timeline(), encoding='utf-8')
    print('  timeline.html')

    (SITE_DIR / 'by-order.html').write_text(build_by_order(), encoding='utf-8')
    print('  by-order.html')

    (SITE_DIR / 'full-index.html').write_text(build_full_index(), encoding='utf-8')
    print('  full-index.html')

    print(f'\nBuilt to: {SITE_DIR}')
    print('Serve:    cd site && python3 -m http.server 8000')


if __name__ == '__main__':
    main()
