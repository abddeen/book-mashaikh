#!/usr/bin/env python3
"""Parse markdown content files into structured JSON for the React site."""

import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
CONTENT = BASE / "content"
DATA = BASE / "src" / "data"

PARTS = [
    (1, "Seeds of Tasawwuf", "1st\u20132nd Century AH", "600\u2013820 CE", "Ch. 1\u20139"),
    (2, "Crystallization of Sufi Thought", "3rd\u20134th Century AH", "820\u20131000 CE", "Ch. 10\u201320"),
    (3, "Age of Systematization", "5th\u20136th Century AH", "1000\u20131200 CE", "Ch. 21\u201335"),
    (4, "The Golden Age", "7th\u20138th Century AH", "1097\u20131400 CE", "Ch. 36\u201350, 101\u2013102"),
    (5, "Age of Expansion", "9th\u201311th Century AH", "1199\u20131650 CE", "Ch. 51\u201365, 103\u2013106"),
    (6, "Era of Revival", "12th\u201313th Century AH", "1641\u20131900 CE", "Ch. 66\u201380, 107\u2013114, 126"),
    (7, "The Modern Era", "14th Century AH", "1847\u2013Present", "Ch. 81\u2013100, 115\u2013127"),
]


def parse_ce_year(s):
    m = re.search(r'pre-(\d{3,4})\s*CE', s)
    if m:
        return int(m.group(1)) - 15
    m = re.search(r'(\d{3,4})[\u2013\-](\d{3,4})\s*CE', s)
    if m:
        return (int(m.group(1)) + int(m.group(2))) // 2
    m = re.search(r'(\d{3,4})\s*CE', s)
    if m:
        return int(m.group(1))
    m = re.search(r'(\d+)(?:st|nd|rd|th)\s+century\s+AH', s)
    if m:
        return 622 + (int(m.group(1)) - 1) * 97 + 48
    return 0


def slugify(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def parse_paragraphs(text):
    result = []
    for block in re.split(r'\n{2,}', text.strip()):
        block = block.strip()
        if not block or re.match(r'^-{3,}$', block):
            continue
        para = ' '.join(l.strip() for l in block.split('\n') if l.strip())
        if para:
            result.append(para)
    return result


def parse_stories(text):
    stories = []
    for block in re.split(r'\n{2,}', text.strip()):
        block = block.strip()
        if not block:
            continue
        m = re.match(r'\*\*(.+?):\*\*\s*(.*)', block, re.DOTALL)
        if m:
            content = ' '.join(m.group(2).split())
            stories.append({"title": m.group(1).strip(), "content": content})
    return stories


def parse_works_list(text):
    works = []
    for line in text.split('\n'):
        line = line.strip()
        if not line.startswith('-'):
            continue
        line = line[1:].strip()
        m = re.match(r'\*\*(.+?)\*\*[:\s]*(.*)', line, re.DOTALL)
        if m:
            works.append({
                "title": m.group(1).strip().rstrip(':'),
                "description": m.group(2).strip()
            })
    return works


def parse_sources(text):
    sources = []
    for line in text.split('\n'):
        line = line.strip()
        if not line.startswith('-'):
            continue
        line = line[1:].strip()
        unverified = '[UNVERIFIED]' in line
        line = re.sub(r'\[UNVERIFIED\]\s*', '', line).strip()

        lm = re.match(r'\*\*(.+?)\*\*\s*(.*)', line, re.DOTALL)
        if not lm:
            continue
        label = lm.group(1).rstrip(':').strip()
        rest = lm.group(2).strip()

        um = re.search(r'(https?://\S+)', rest)
        if um:
            url = um.group(1)
            after = rest[um.end():].strip()
            dm = re.match(r'^[\u2014\u2013]\s*(.*)', after, re.DOTALL)
            desc = dm.group(1).strip() if dm else after
        else:
            url = None
            dm = re.search(r'\s[\u2014\u2013]\s+(.*)', rest, re.DOTALL)
            desc = dm.group(1).strip() if dm else rest.strip()

        sources.append({
            "label": label,
            "url": url,
            "description": desc,
            "unverified": unverified
        })
    return sources


META_KEY_MAP = {
    'Full Name': 'fullName',
    'Born': 'born',
    'Died': 'died',
    'Sufi Order': 'sufiOrder',
    'Titles': 'titles',
    'Teachers': 'teachers',
    'Notable Students': 'notableStudents',
    'Major Works': 'majorWorks',
    'Burial': 'burial',
}


def parse_chapter(heading, body, part_num):
    m = re.match(r'## Chapter (\d+): (.+)\s*$', heading.strip())
    if not m:
        return None

    ch_num = int(m.group(1))
    full_title = m.group(2).strip()

    am = re.search(r'\(([^)]+)\)\s*$', full_title)
    arabic = am.group(1) if am else ''
    name = full_title[:am.start()].strip() if am else full_title

    first = re.search(r'\n### ', body)
    meta_text = body[:first.start()] if first else body
    sec_text = body[first.start():] if first else ''

    # Check for afterword appended after this chapter
    afterword = None
    aw = re.search(r'\n## Afterword', sec_text)
    if aw:
        aw_lines = sec_text[aw.start():].strip().split('\n')
        afterword = {
            "title": aw_lines[0].lstrip('#').strip(),
            "paragraphs": parse_paragraphs('\n'.join(aw_lines[1:]))
        }
        sec_text = sec_text[:aw.start()]

    metadata = {}
    for line in meta_text.split('\n'):
        mm = re.match(r'^\*\*(.+?):\*\*\s*(.*)', line.strip())
        if mm:
            k, v = mm.group(1).strip(), mm.group(2).strip()
            metadata[META_KEY_MAP.get(k, k)] = v

    chapter = {
        "number": ch_num,
        "part": part_num,
        "slug": slugify(name),
        "name": name,
        "arabicName": arabic,
        "metadata": metadata,
        "ceYear": parse_ce_year(metadata.get('born', '')),
    }

    for sec in re.split(r'\n### ', '\n' + sec_text):
        sec = sec.strip()
        if not sec:
            continue
        head, _, content = sec.partition('\n')
        head = head.strip()
        content = content.strip()

        if head == 'Biography':
            chapter['biography'] = parse_paragraphs(content)
        elif head == 'Key Teachings':
            chapter['keyTeachings'] = parse_paragraphs(content)
        elif head == 'Famous Stories':
            chapter['famousStories'] = parse_stories(content)
        elif head == 'Major Works':
            if re.search(r'^\s*[-*]\s', content, re.MULTILINE):
                chapter['majorWorksList'] = parse_works_list(content)
            else:
                chapter['majorWorksText'] = parse_paragraphs(content)
        elif head == 'Legacy':
            chapter['legacy'] = parse_paragraphs(content)
        elif head == 'Sources':
            chapter['sources'] = parse_sources(content)

    if afterword:
        chapter['afterword'] = afterword

    return chapter


def parse_part(num):
    md = (CONTENT / f'part{num}.md').read_text('utf-8')
    chunks = re.split(r'\n(?=## Chapter \d+)', md)
    intro = chunks[0]
    ch_chunks = chunks[1:]

    hc_match = re.search(r'^## Historical Context\s*$', intro, re.MULTILINE)
    hist_ctx = []
    if hc_match:
        ctx_text = intro[hc_match.end():].strip()
        ctx_text = re.sub(r'^-{3,}\s*$', '', ctx_text, flags=re.MULTILINE).strip()
        hist_ctx = parse_paragraphs(ctx_text)

    chapters = []
    for chunk in ch_chunks:
        heading, _, body = chunk.partition('\n')
        ch = parse_chapter(heading, body, num)
        if ch:
            chapters.append(ch)

    return hist_ctx, chapters


def parse_index():
    md = (CONTENT / 'index.md').read_text('utf-8')
    WORDS = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7}
    part = 0
    figures = []

    for line in md.split('\n'):
        m = re.match(r'^## Part (\w+):', line)
        if m:
            part = WORDS.get(m.group(1), 0)
            continue
        if not (line.startswith('|') and line.endswith('|')):
            continue
        cells = [c.strip() for c in line[1:-1].split('|')]
        if len(cells) < 5:
            continue
        ch, name_full, born, place, tariqah = cells[:5]
        if not re.match(r'^\d+$', ch):
            continue

        am = re.search(r'\(([^)]+)\)\s*$', name_full)
        arabic = am.group(1) if am else ''
        name = name_full[:am.start()].strip() if am else name_full.strip()
        tariqah_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', tariqah)

        figures.append({
            "chapterNumber": int(ch),
            "name": name,
            "arabicName": arabic,
            "born": born,
            "ceYear": parse_ce_year(born),
            "birthplace": place,
            "tariqah": tariqah_clean,
            "part": part,
        })

    return sorted(figures, key=lambda f: (f['part'], f['ceYear']))


def parse_relationships():
    md = (CONTENT / 'relationships.md').read_text('utf-8')
    sections = []
    current = None

    for line in md.split('\n'):
        if line.startswith('## '):
            if current:
                sections.append(current)
            current = {"title": line[3:].strip(), "raw": []}
        elif current is not None:
            current['raw'].append(line)

    if current:
        sections.append(current)

    result = []
    for sec in sections:
        raw = '\n'.join(sec['raw'])
        diagrams = [m.group(1).strip() for m in re.finditer(r'```mermaid\n(.*?)```', raw, re.DOTALL)]
        text = re.sub(r'```mermaid\n.*?```', '', raw, flags=re.DOTALL)
        notes = [l.strip() for l in text.split('\n')
                 if l.strip() and not l.strip().startswith('---') and not l.strip().startswith('#')]
        result.append({
            "title": sec['title'],
            "mermaidDiagrams": diagrams,
            "notes": notes,
        })

    return result


def main():
    DATA.mkdir(parents=True, exist_ok=True)

    parts_meta = []
    for num, name, period, dates, ch_range in PARTS:
        hist_ctx, chapters = parse_part(num)

        # Check for afterword in last chapter
        afterword = None
        if chapters and 'afterword' in chapters[-1]:
            afterword = chapters[-1].pop('afterword')

        out = DATA / f'part{num}.json'
        with open(out, 'w', encoding='utf-8') as f:
            json.dump(chapters, f, ensure_ascii=False, indent=2)
        print(f'  {out.name}: {len(chapters)} chapters')

        parts_meta.append({
            "number": num,
            "name": name,
            "period": period,
            "dates": dates,
            "chapterRange": ch_range,
            "historicalContext": hist_ctx,
            "chapters": [
                {"number": ch['number'], "name": ch['name'], "arabicName": ch['arabicName']}
                for ch in chapters
            ],
            "afterword": afterword,
        })

    with open(DATA / 'parts.json', 'w', encoding='utf-8') as f:
        json.dump(parts_meta, f, ensure_ascii=False, indent=2)
    print('  parts.json')

    index = parse_index()
    with open(DATA / 'chapters-index.json', 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print(f'  chapters-index.json: {len(index)} figures')

    rels = parse_relationships()
    with open(DATA / 'relationships.json', 'w', encoding='utf-8') as f:
        json.dump(rels, f, ensure_ascii=False, indent=2)
    print('  relationships.json')

    print('\nDone!')


if __name__ == '__main__':
    main()
