"""Offline, report-scoped evidence and sequential change checks for NVIDIA."""
import argparse
import hashlib
import json
import pathlib
import re
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import unquote, urlsplit

from download_materials import VisibleText, charset, decode_body

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = ROOT / 'Embodied_AI_Solutions_Research'
PROJECT = BASE / '01_Compute_Chips/01_NVIDIA'
ARCHIVE = PROJECT / 'reference_metrial'


def verify(stem, allowed):
    errors = []
    report = PROJECT / (stem + '.md')
    text = report.read_text(encoding='utf-8')
    body = text.split('## 参考资料与本地原文')[0]
    han = len(re.findall(r'[\u4e00-\u9fff]', body))
    if han < 1500:
        errors.append('Body has fewer than 1500 Han characters')
    if re.search(r'\{\{|<a\s+id=|\]\(#|\bTODO\b|待填写|此处填写', text):
        errors.append('Placeholder or anchor present')
    tables = []
    rows = []
    for line in body.splitlines() + ['']:
        if line.startswith('|'):
            rows.append(line)
        elif rows:
            tables.append(rows)
            rows = []
    if not tables:
        errors.append('Missing comparison tables')
    for i, table in enumerate(tables):
        counts = [len(re.split(r'(?<!\\)\|', row.strip())) - 2 for row in table]
        if len(table) < 3 or len(set(counts)) != 1 or max(counts) > 8:
            errors.append('Invalid table ' + str(i + 1))
    headings = list(re.finditer(r'^#{1,6} .+$', body, re.M))
    for left, right in zip(headings, headings[1:]):
        if not body[left.end():right.start()].strip() and right[0].count('#') <= left[0].count('#'):
            errors.append('Empty section ' + left[0])
    local_links = 0
    for link in re.findall(r'\]\(([^)]+)\)', text):
        if link.startswith(('https://', 'http://')):
            continue
        local_links += 1
        if not re.match(r'^[A-Z]:/', link) or not pathlib.Path(link).is_file():
            errors.append('Invalid report file link: ' + link)

    records = json.loads((ARCHIVE / '_registry/materials.json').read_text(encoding='utf-8'))
    trace = json.loads((ARCHIVE / 'derived/qa/directions' / (stem + '_sources.json')).read_text(encoding='utf-8'))
    page_links = 0
    hash_checks = 0
    html_equal = 0
    assets = set()
    states = Counter()
    missing = set()

    def dependency(value, base, page_dir):
        nonlocal page_links
        if not value or value.startswith(('#', 'data:', 'blob:', 'javascript:')) or urlsplit(value).scheme:
            return
        target = (base / unquote(urlsplit(value).path)).resolve()
        page_links += 1
        if not target.is_relative_to(page_dir) or not target.is_file():
            errors.append('Invalid local dependency: ' + str(target))

    def css(content, base, page_dir):
        for m in re.finditer(r'url\(\s*(?:"([^"]*)"|\'([^\']*)\'|([^)]*?))\s*\)', content, re.I):
            dependency(next(v for v in m.groups() if v is not None).strip(), base, page_dir)
        for m in re.finditer(r'@import\s+["\']([^"\']+)["\']', content, re.I):
            dependency(m[1], base, page_dir)

    class Page(HTMLParser):
        def __init__(self, page_dir):
            super().__init__()
            self.page_dir = page_dir
            self.style = False

        def handle_starttag(self, tag, attrs):
            values = dict(attrs)
            for key, value in attrs:
                if not value:
                    continue
                is_resource = (key == 'src' and tag in ('img', 'script', 'source', 'video', 'audio', 'input')) or (key == 'poster' and tag == 'video') or (tag == 'link' and key == 'href' and set(values.get('rel', '').lower().split()) & {'stylesheet', 'icon', 'preload', 'modulepreload', 'apple-touch-icon'})
                if is_resource:
                    dependency(value, self.page_dir, self.page_dir)
                if key in ('srcset', 'data-srcset') and 'data:' not in value:
                    for part in value.split(','):
                        if part.strip():
                            dependency(part.strip().split()[0], self.page_dir, self.page_dir)
                if key == 'style':
                    css(value, self.page_dir, self.page_dir)
            if tag == 'style':
                self.style = True

        def handle_endtag(self, tag):
            if tag == 'style':
                self.style = False

        def handle_data(self, data):
            if self.style:
                css(data, self.page_dir, self.page_dir)

    def check_hash(path, expected, label):
        nonlocal hash_checks
        hash_checks += 1
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            errors.append('File/hash mismatch: ' + label)

    for name in trace['source_ids']:
        rec = records[name]
        states[rec['archive_status']] += 1
        if rec.get('status') != 200 or rec['archive_status'] == 'failed':
            errors.append('Invalid adopted source: ' + name)
            continue
        if stem not in rec.get('used_by', []):
            errors.append('Missing dimension registration: ' + name)
        for k, h in [('file', 'sha256'), ('original_file', 'original_sha256')]:
            check_hash(pathlib.Path(rec[k]), rec[h], name + ':' + k)
        main = pathlib.Path(rec['file'])
        for a in rec.get('assets', []):
            path = ARCHIVE / a.get('local_file', a['file'])
            check_hash(path, a['sha256'], name + ':' + a['url'])
            assets.add(a['url'])
            if path.suffix == '.css' and path.exists():
                css(path.read_text(encoding='utf-8'), path.parent, main.parent)
        missing.update(rec.get('unavailable_presentation_assets', {}).keys())
        if main.suffix == '.html':
            raw = decode_body(pathlib.Path(rec['original_file']).read_bytes(), rec['headers'])
            before = VisibleText()
            before.feed(raw.decode(charset(raw, rec['content_type'])))
            after = VisibleText()
            after.feed(main.read_text(encoding='utf-8'))
            if before.value() != after.value():
                errors.append('Visible text mismatch: ' + name)
            else:
                html_equal += 1
            Page(main.parent).feed(main.read_text(encoding='utf-8'))
    for figure in trace['figures']:
        from PIL import Image
        path = pathlib.Path(figure['file'])
        if not path.is_file():
            errors.append('Missing figure: ' + str(path))
        else:
            with Image.open(path) as im:
                im.verify()

    baseline = json.loads((BASE / 'toolkit/audit/NVIDIA_next_directions_baseline.json').read_text(encoding='utf-8'))
    changes = []
    for rel, sha in baseline.items():
        path = BASE / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != sha:
            changes.append(rel)
    permitted = {'01_Compute_Chips/01_NVIDIA/' + s + '.md' for s in allowed}
    if set(changes) - permitted:
        errors.append('Unrelated report changes: ' + repr(set(changes) - permitted))
    result = dict(report=report.as_posix(), body_han_chars=han, tables=len(tables),
                  report_local_links=local_links, sources=len(trace['source_ids']),
                  status_counts=dict(states), html_visible_text_equal=html_equal,
                  unique_asset_urls=len(assets), unavailable_presentation_urls=len(missing), file_hash_checks=hash_checks,
                  page_local_dependencies_checked=page_links, changed_reports=changes,
                  errors=errors, outcome='pass' if not errors else 'fail',
                  limits='Offline archive and structure checks; facts manually reviewed; no hardware tests.')
    output = ARCHIVE / 'derived/qa/directions' / (stem + '_quality.json')
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('stem')
    parser.add_argument('--allow-report', action='append', default=[])
    args = parser.parse_args()
    raise SystemExit(verify(args.stem, args.allow_report or [args.stem]))
