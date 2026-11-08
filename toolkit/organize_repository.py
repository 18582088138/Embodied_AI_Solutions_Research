"""Normalize research links and metadata; rebuild navigation without downloading."""
import argparse
import hashlib
import json
import os
import re
import shutil
from pathlib import Path
from urllib.parse import unquote, urlsplit, quote
from archive_paths import ROOT, portable

CATEGORIES = {
    '01_Compute_Chips': '算力芯片与计算平台',
    '02_Core_Components': '核心零部件',
    '03_Robot_Manufacturers': '机器人厂商与场景',
    '04_AI_Models': 'AI 模型',
    '05_Software_and_OS': '软件与操作系统',
    '06_Open_Source': '开源具身智能方案',
}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def projects():
    return [p for cat in CATEGORIES if (ROOT / cat).is_dir() for p in category_projects(cat)]


def category_projects(category):
    return [p for p in sorted((ROOT / category).iterdir())
            if p.is_dir() and re.match(r'^\d\d_', p.name)]


def product_summary(state):
    return ('产品级首轮调研已交付；待用户审阅和实机验证'
            if '01_Product_Research' in state.get('completed_dimensions', [])
            else '候选资料已归档；产品报告待编写')


def build_selected_indexes(category):
    """Register one category without rewriting unrelated reports or their indexes."""
    from prepare_git_sources import prepare
    index_path = ROOT / 'research-index.json'
    index = json.loads(index_path.read_text(encoding='utf-8-sig'))
    index = [item for item in index if not item['project'].startswith(category + '/')]
    lines = [f'## [{category} · {CATEGORIES[category]}]({category}/README.md)', '',
             '新增日期：2026-11-08。首轮报告与候选资料分别标记；调研计划和当前核验记录见类别入口。', '']
    for project in category_projects(category):
        prepare(project)
        state_path = project / 'research_state/progress.json'
        state = json.loads(state_path.read_text(encoding='utf-8-sig')) if state_path.exists() else {}
        reports = [p for p in sorted(project.glob('*.md')) if re.match(r'^\d\d[A-Z]?_', p.name) and 'Index' not in p.name]
        lines.append(f'- [{project.name}]({category}/{project.name}/README.md) — {product_summary(state)}；{len(reports)} 份报告。')
        for report in reports:
            title = next((x.lstrip('# ').strip() for x in report.read_text(encoding='utf-8-sig').splitlines() if x.startswith('# ')), report.stem)
            index.append(dict(path=report.relative_to(ROOT).as_posix(), project=project.relative_to(ROOT).as_posix(),
                              title=title, status=product_summary(state), sha256=hashlib.sha256(report.read_bytes()).hexdigest()))
    section = '\n'.join(lines) + '\n\n'
    readme = ROOT / 'README.md'
    text = readme.read_text(encoding='utf-8-sig')
    pattern = rf'^## \[{re.escape(category)} · .*?(?=^## |\Z)'
    if re.search(pattern, text, re.M | re.S):
        text = re.sub(pattern, lambda _: section, text, flags=re.M | re.S)
    else:
        text = text.replace('## 下载与复用', section + '## 下载与复用', 1)
    readme.write_text(text, encoding='utf-8')
    write_json(index_path, index)


def normalize():
    """Edit authored navigation/metadata only, never source response or dependencies."""
    changed = []
    prefix = ROOT.as_posix() + '/'
    for project in projects():
        reports = list(project.glob('*.md'))
        # Freeze hashes of existing reports before the path-only migration.
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in reports}
        write_json(project / 'research_state/organization_before.json', before)
        for base, dirs, files in os.walk(project):
            dirs[:] = [d for d in dirs if d != '__pycache__']
            for name in files:
                p = Path(base) / name
                rel = p.relative_to(project)
                authored_md = p.suffix == '.md' and 'reference_metrial' not in rel.parts
                metadata = (p.suffix == '.json' and
                            ('research_state' in rel.parts or '_registry' in rel.parts or
                             'derived' in rel.parts or name in ('metadata.json', 'collection.json')))
                index_html = name == 'index.html' and p.parent.name in ('reference_metrial', '02_software_depth', '08_core')
                if metadata:
                    try:
                        original = json.loads(p.read_text(encoding='utf-8-sig'))
                        updated = portable(original)
                        if updated != original:
                            write_json(p, updated)
                            changed.append(p.relative_to(ROOT).as_posix())
                    except (ValueError, UnicodeError):
                        continue
                if not (authored_md or index_html):
                    continue
                text = p.read_text(encoding='utf-8-sig')
                def link(match):
                    raw = unquote(match[1].strip('<>'))
                    if raw.casefold().startswith(prefix.casefold()):
                        target = ROOT / raw[len(prefix):]
                        return '](' + quote(Path(os.path.relpath(target, p.parent)).as_posix(), safe='/._-#') + ')'
                    # Make legacy evidence part of this project's own atomic commit.
                    if '_Evidence/' in raw and not urlsplit(raw).scheme:
                        target = (p.parent / raw.split('#')[0]).resolve()
                        if target.is_file() and target.is_relative_to(ROOT / '_Evidence'):
                            dest = project / 'reference_metrial/legacy' / target.name
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            if not dest.exists():
                                shutil.copy2(target, dest)
                            companion = target.with_suffix('.meta.json')
                            if companion.is_file():
                                cp = dest.with_suffix('.meta.json')
                                write_json(cp, portable(json.loads(companion.read_text(encoding='utf-8-sig'))))
                            return '](' + Path(os.path.relpath(dest, p.parent)).as_posix() + ')'
                    return match[0]
                updated = re.sub(r'\]\(([^)]+)\)', link, text)
                if authored_md:
                    updated = updated.replace('本地绝对路径', '仓库内相对路径')
                if updated != text:
                    p.write_text(updated, encoding='utf-8')
                    changed.append(p.relative_to(ROOT).as_posix())
        print('normalized', project.relative_to(ROOT), flush=True)
    return changed


def status_for(project, report, state):
    if state.get('research_type') == 'product_multidimensional':
        return product_summary(state)
    if project.name == '01_NVIDIA':
        return '既有深度报告；保留原核验记录'
    done = state.get('completed_dimensions', [])
    if report.stem in done or report.name[:2] in done:
        return '深度调研已交付；审阅状态见 progress.json'
    if re.match(r'0[28][A-Z]_', report.name) and state:
        return '深度专题；完成与审阅状态见 progress.json'
    return '首轮资料；待后续深度调研'


def build_indexes(category=None):
    if category:
        build_selected_indexes(category)
        return
    from prepare_git_sources import prepare
    index = []
    root_lines = ['# 具身智能解决方案研究', '',
                  '整理日期：2026-11-06（Asia/Shanghai）。收录已有研究报告与参考材料；各原件保留实际采集时间。', '',
                  '从以下类别进入各分项 README，可查阅章节、软件/核心技术专题、原件和核验记录。首轮概览与深度调研分别标记；报告交付不等于用户批准或实机验证。', '',
                  '- [研究方法](METHODOLOGY.md)',
                  '- [持续调研与提交规范](CONTRIBUTING.md)',
                  '- [可复用调研 skill](.agents/skills/embodied-ai-platform-research/SKILL.md)',
                  '- [公共下载与检查工具](toolkit/README.md)',
                  '- [本次整理校验](validation.json)',
                  '- [首轮全景结论（历史快照）](EXECUTIVE_SUMMARY.md)',
                  '- [首轮证据缺口（历史快照）](GAPS_AND_NEXT_STEPS.md)',
                  '- [历史共享证据登记](_Evidence/SOURCE_REGISTER.md)',
                  '- [研究计划与历史索引](docs/history/)', '']
    for cat, title in CATEGORIES.items():
        if not (ROOT / cat).is_dir():
            continue
        lines = [f'# {cat} · {title}', '', '[返回研究首页](../README.md)', '']
        root_lines.append(f'## [{cat} · {title}]({cat}/README.md)')
        root_lines.append('')
        for project in category_projects(cat):
            prepare(project)
            state_path = project / 'research_state/progress.json'
            state = json.loads(state_path.read_text(encoding='utf-8-sig')) if state_path.exists() else {}
            reports = [p for p in sorted(project.glob('*.md')) if re.match(r'^\d\d[A-Z]?_', p.name)
                       and 'Index' not in p.name]
            completed = len(state.get('completed_dimensions', []))
            summary = (product_summary(state) if state.get('research_type') == 'product_multidimensional' else
                       '既有 01—09 深度报告' if project.name == '01_NVIDIA' else
                       '01—02 深度调研；03—09 为首轮简报' if project.name == '07_Cambricon' else
                       '01—09 深度调研已交付，审阅状态见分项记录' if completed >= 9 else
                       '首轮资料，待深度调研')
            entry = f'- [{project.name}]({project.name}/README.md) — {summary}；{len(reports)} 份章节/专题。'
            lines.append(entry)
            root_lines.append(entry.replace(f']({project.name}/', f']({cat}/{project.name}/'))
            readme = [f'# {project.name}', '', f'资料状态：{summary}。', '',
                      f'[返回类别](../README.md) · [研究首页](../../README.md)', '',
                      '## 章节与专题', '']
            for report in reports:
                title_line = next((x.lstrip('# ').strip() for x in report.read_text(encoding='utf-8-sig').splitlines() if x.startswith('# ')), report.stem)
                readme.append(f'- [{report.stem} · {title_line}]({report.name})')
                index.append({'path': report.relative_to(ROOT).as_posix(), 'project': project.relative_to(ROOT).as_posix(),
                              'title': title_line, 'status': status_for(project, report, state),
                              'sha256': hashlib.sha256(report.read_bytes()).hexdigest()})
            readme.extend(['', '## 参考材料与核验', '',
                           '完整原件留在本地 `reference_metrial/`，未上传 GitHub；历史首轮文本在本地 `reference_metrial/legacy/`。来源清单保留官网 URL、本地路径、哈希和归档状态。'])
            archive = project / 'reference_metrial'
            for target, label in [('REFERENCES.md', '参考来源与本地原件清单'),
                                  ('sources.json', '机器可读来源、路径与哈希'),
                                  ('assets/figures/', '报告正文图表'),
                                  ('research_state/archive_qa/', '历史归档核验记录'),
                                  ('research_state/progress.json', '原有调研进度与审阅状态'),
                                  ('research_state/evidence/', '原有逐章证据'),
                                  ('research_state/baselines/', '原有章节基线'),
                                  ('research_state/organization_before.json', '整理前报告哈希（路径变更基线）')]:
                if (project / target).exists():
                    readme.append(f'- [{label}]({target})')
            readme.extend(['', '本次整理仅规范导航、路径与归档管理，不重新认证报告结论。旧基线与原核验记录为历史记录；路径规范化后的新报告哈希见根目录 `research-index.json`。', ''])
            previous = project / 'README.md'
            if previous.exists() and '本次整理仅规范导航' not in previous.read_text(encoding='utf-8-sig'):
                dest = project / 'research_state/revisions/README_before_organization.md'
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(previous, dest)
            if state.get('research_type') != 'product_multidimensional':
                previous.write_text('\n'.join(readme), encoding='utf-8')
        if not (ROOT / cat / 'RESEARCH_PLAN.md').exists():
            (ROOT / cat / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
        root_lines.append('')
    root_lines.extend(['## 下载与复用', '',
                       'GitHub 主仓库保存报告、正文图表、来源清单、skill、工具与核验记录。完整 HTML/PDF 原件、网页依赖和媒体保留本地，不纳入 Git 或 LFS；clone 不会自动取得这些原件。', '',
                       '每个分项的 REFERENCES.md / sources.json 保留官方 URL、本地归档路径与 SHA256。拥有原件的工作目录可继续打开本地 reference_metrial/index.html 并复用下载器；后续可连接外部归档而保留同一来源清单。', '',
                       '原件与网页依赖保留既有字节；JSON 路径以仓库根目录为基准，公共工具在加载时解析。部分静态依赖缺失、动态页面限制及未取得证据继续保留在报告和 metadata 中。', ''])
    (ROOT / 'README.md').write_text('\n'.join(root_lines), encoding='utf-8')
    write_json(ROOT / 'research-index.json', index)


def check(category=None):
    errors = []
    count = 0
    report_count = 0
    selected = category_projects(category) if category else projects()
    navigation = [ROOT / 'README.md']
    navigation += list((ROOT / category).glob('*.md')) if category else [ROOT / cat / 'README.md' for cat in CATEGORIES if (ROOT / cat).is_dir()]
    for folder in selected:
        navigation.extend(folder.glob('*.md'))
    for report in navigation:
        if report.is_file():
            report_count += 1
            for value in re.findall(r'\]\(([^)]+)\)', report.read_text(encoding='utf-8-sig')):
                value = unquote(value.strip('<>'))
                if not value or value.startswith('#') or urlsplit(value).scheme:
                    continue
                count += 1
                target = (report.parent / value.split('#')[0]).resolve()
                if not target.exists() or not target.is_relative_to(ROOT):
                    errors.append({'report': report.relative_to(ROOT).as_posix(), 'link': value})
    result = {'organized_on': '2026-11-08 Asia/Shanghai' if category else '2026-11-06 Asia/Shanghai', 'projects': len(selected),
              'markdown_files_checked': report_count, 'local_links_checked': count,
              'errors': errors, 'outcome': 'pass' if not errors else 'fail',
              'scope': 'Current project Markdown local links and navigation; original research checks remain historical. No new semantic or hardware validation.'}
    write_json(ROOT / category / 'research_state/navigation_quality.json' if category else ROOT / 'validation.json', result)
    print(json.dumps(result, ensure_ascii=False), flush=True)
    return bool(errors)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--normalize', action='store_true', help='One-time absolute-path migration; preserves original response bytes')
    parser.add_argument('--build-indexes', action='store_true')
    parser.add_argument('--category', choices=list(CATEGORIES), help='Update only this category and its root navigation/index entries')
    args = parser.parse_args()
    if args.normalize:
        write_json(ROOT / 'docs/organization/path_changes.json', normalize())
    if args.build_indexes:
        build_indexes(args.category)
    raise SystemExit(check(args.category))
