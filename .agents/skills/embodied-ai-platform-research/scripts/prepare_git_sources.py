"""Publish source catalogs and report figures while keeping full archives local."""
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit
from archive_paths import ROOT, portable


def prepare(project):
    archive = project / 'reference_metrial'
    registry = archive / '_registry/materials.json'
    if not archive.exists() and (project / 'sources.json').exists():
        return  # A clone carries the catalog; never erase it when raw archives are absent.
    sources = []
    file_anchors = {}
    if registry.exists():
        data = json.loads(registry.read_text(encoding='utf-8-sig'))
        records = {r.get('url', name): r for name, r in data.items()}
        for url, rec in sorted(records.items()):
            anchor = 'ref-' + hashlib.sha256(url.encode()).hexdigest()[:16]
            keep = ('id', 'aliases', 'url', 'final_url', 'archive_status', 'archived_at_utc',
                    'fetched_at_utc', 'retrieved_at_utc', 'time_utc', 'status', 'content_type', 'sha256', 'original_sha256',
                    'file', 'original_file', 'used_by', 'visible_text_unchanged', 'error')
            entry = {k: rec[k] for k in keep if k in rec}
            entry.update(catalog_anchor=anchor, assets_count=len(rec.get('assets', [])),
                         unavailable_assets_count=len(rec.get('unavailable_assets', {})),
                         unavailable_presentation_assets_count=len(rec.get('unavailable_presentation_assets', {})))
            for k in ('file', 'original_file'):
                if rec.get(k):
                    file_anchors[(ROOT / rec[k]).resolve()] = anchor
            sources.append(portable(entry))
    legacy = archive / 'legacy'
    for meta in sorted(legacy.glob('*.meta.json')):
        rec = json.loads(meta.read_text(encoding='utf-8-sig'))
        url = rec.get('url', rec.get('requested_url', ''))
        name = meta.name.removesuffix('.meta.json')
        anchor = 'legacy-' + hashlib.sha256(name.encode()).hexdigest()[:16]
        entry = dict(catalog_anchor=anchor, id=name, url=url, legacy=True,
                     archive_status=rec.get('content_review', rec.get('status', 'historical_snapshot')),
                     local_file=(legacy / (name + '.txt')).relative_to(ROOT).as_posix(), metadata=portable(rec))
        sources.append(entry)
        for p in legacy.glob(name + '.*'):
            file_anchors[p.resolve()] = anchor
    # An unexpanded first-round project can still use this catalog without downloads.
    (project / 'sources.json').write_text(json.dumps(sources, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    text = ['# 参考来源清单', '', '[返回本分项](README.md)', '',
            '完整参考原件保留在本地 `reference_metrial/`，未上传 GitHub。下方提供官方 URL、原始采集记录、哈希与本地路径；本地路径以仓库根为基准。', '',
            'GitHub 可直接阅读报告及正文图表。需要核验 HTML/PDF 原件时，在拥有本地归档的工作目录打开原件；clone 本仓库不会自动得到完整原件。后续可在保持 SHA256 清单不变的情况下连接外部归档。', '',
            '- [机器可读完整清单](sources.json)',
            '- [本地归档管理方式](../../CONTRIBUTING.md)', '']
    for rec in sources:
        text.extend([f'<a id="{rec["catalog_anchor"]}"></a>', '', f'## {rec.get("id", rec.get("url", "历史资料"))}', ''])
        if rec.get('url'):
            text.append(f'- [官方/原始来源]({rec["url"]})')
        for k in ('archive_status', 'archived_at_utc', 'fetched_at_utc', 'time_utc', 'sha256', 'original_sha256', 'file', 'original_file', 'local_file'):
            if k in rec:
                text.append(f'- `{k}`：`{rec[k]}`')
        if rec.get('unavailable_assets_count'):
            text.append(f'- 未取得依赖：{rec["unavailable_assets_count"]} 项；详见本地 metadata。')
        text.append('')
    (project / 'REFERENCES.md').write_text('\n'.join(text), encoding='utf-8')
    # Preserve useful old archive QA records in the tracked state directory.
    qa = archive / 'derived/qa'
    if qa.exists():
        shutil.copytree(qa, project / 'research_state/archive_qa', dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns('*.png', '*.jpg', '*.jpeg', '*.pdf', '*.html', '*.css', '*.js'))
    figure_manifest = []
    for report in project.glob('*.md'):
        if report.name == 'REFERENCES.md':
            continue
        text = report.read_text(encoding='utf-8-sig')
        def replace(match):
            is_image, label, raw = match.groups()
            value = unquote(raw.strip('<>'))
            if urlsplit(value).scheme or value.startswith('#'):
                return match[0]
            target = (report.parent / value.split('#')[0]).resolve()
            if target.is_relative_to(project / 'research_state/archive_qa') and target.suffix == '.html':
                return f'[{label}](REFERENCES.md)'
            if not target.is_relative_to(archive):
                return match[0]
            if is_image and target.is_file():
                sha = hashlib.sha256(target.read_bytes()).hexdigest()
                dest = project / 'assets/figures' / (target.stem[:65] + '--' + sha[:12] + target.suffix)
                dest.parent.mkdir(parents=True, exist_ok=True)
                if not dest.exists():
                    shutil.copy2(target, dest)
                figure_manifest.append({'report': report.name, 'figure': dest.relative_to(project).as_posix(),
                                        'local_original': target.relative_to(ROOT).as_posix(), 'sha256': sha})
                return f'![{label}]({quote(dest.relative_to(project).as_posix(), safe="/._-")})'
            if target.is_relative_to(qa):
                dest = project / 'research_state/archive_qa' / target.relative_to(qa)
                if dest.exists():
                    return f'[{label}]({quote(dest.relative_to(project).as_posix(), safe="/._-")})'
            anchor = file_anchors.get(target)
            if not anchor:
                meta = target.parent / 'metadata.json'
                if meta.exists():
                    rec = json.loads(meta.read_text(encoding='utf-8-sig'))
                    if rec.get('url'):
                        anchor = 'ref-' + hashlib.sha256(rec['url'].encode()).hexdigest()[:16]
                        if not any(x['catalog_anchor'] == anchor for x in sources):
                            anchor = None
            return f'[{label}](REFERENCES.md' + (f'#{anchor}' if anchor else '') + ')'
        updated = re.sub(r'(!?)\[([^\]]*)\]\(([^)]+)\)', replace, text)
        if updated != text:
            report.write_text(updated, encoding='utf-8')
    figures_path = project / 'research_state/organization_figures.json'
    if figure_manifest:
        figures_path.parent.mkdir(parents=True, exist_ok=True)
        previous = json.loads(figures_path.read_text(encoding='utf-8-sig')) if figures_path.exists() else []
        merged = {(x['report'], x['figure']): x for x in previous + figure_manifest}
        figure_manifest = list(merged.values())
        figures_path.write_text(json.dumps(figure_manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print('source catalog', project.relative_to(ROOT), len(sources), 'sources; figures copied', len(figure_manifest), flush=True)


if __name__ == '__main__':
    for project in sorted(ROOT.glob('[0-9][0-9]_*/*')):
        if project.is_dir():
            prepare(project)
