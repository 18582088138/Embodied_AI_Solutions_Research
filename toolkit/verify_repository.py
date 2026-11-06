"""Verify stored source and asset hashes offline, deduplicating hard-linked reads."""
import hashlib
import json
from pathlib import Path
from archive_paths import ROOT, load_json


def main():
    cache = {}
    errors = []
    projects = []
    checks = 0
    for registry in sorted(ROOT.glob('[0-9][0-9]_*/*/reference_metrial/_registry/materials.json')):
        archive = registry.parents[1]
        project = archive.parent
        records = load_json(registry)
        unique_records = {r.get('url', name): r for name, r in records.items()}
        original_checks = checks
        failed_candidates = 0
        def verify(path, expected):
            nonlocal checks
            p = Path(path)
            if not p.is_absolute():
                p = archive / p
            if not p.is_file() or not p.resolve().is_relative_to(ROOT):
                errors.append({'project': project.relative_to(ROOT).as_posix(), 'missing_or_external': str(path)})
                return
            if not expected:
                errors.append({'file': p.relative_to(ROOT).as_posix(), 'error': 'missing sha256'})
                return
            stat = p.stat()
            key = (stat.st_dev, stat.st_ino, stat.st_size, stat.st_mtime_ns)
            if key not in cache:
                h = hashlib.sha256()
                with p.open('rb') as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b''):
                        h.update(block)
                cache[key] = h.hexdigest()
            checks += 1
            if cache[key] != expected:
                errors.append({'file': p.relative_to(ROOT).as_posix(), 'error': 'sha256 mismatch'})
        for record in unique_records.values():
            if record.get('archive_status') == 'failed':
                failed_candidates += 1
                continue
            for key, hash_key in [('file', 'sha256'), ('original_file', 'original_sha256')]:
                if record.get(key):
                    verify(record[key], record.get(hash_key))
            for asset in record.get('assets', []):
                verify(asset.get('local_file', asset.get('file')), asset.get('sha256'))
        assets_file = registry.with_name('assets.json')
        if assets_file.is_file():
            for record in load_json(assets_file).values():
                if record.get('file') and record.get('sha256'):
                    verify(record['file'], record['sha256'])
        entry = {'project': project.relative_to(ROOT).as_posix(), 'unique_sources': len(unique_records),
                 'hash_checks': checks - original_checks, 'failed_candidates_preserved': failed_candidates}
        projects.append(entry)
        print(json.dumps(entry), flush=True)
    result = {'organized_on': '2026-11-06 Asia/Shanghai', 'projects': projects,
              'hash_checks': checks, 'unique_files_hashed': len(cache), 'errors': errors,
              'outcome': 'pass' if not errors else 'fail',
              'scope': 'Stored successful source/original/dependency byte hashes; failed candidates preserved, not promoted to evidence.'}
    out = ROOT / 'docs/organization/archive_integrity.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('archive integrity', result['outcome'], 'checks', checks, 'errors', len(errors), flush=True)
    return bool(errors)


if __name__ == '__main__':
    raise SystemExit(main())
