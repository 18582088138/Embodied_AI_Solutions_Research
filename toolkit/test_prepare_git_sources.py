import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import prepare_git_sources as catalog


class SourceCatalogTests(unittest.TestCase):
    def test_catalog_links_figures_and_clone_without_raw_archive(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            project = root / '01_Compute_Chips/01_Fixture'
            page = project / 'reference_metrial/webpages/doc'
            page.mkdir(parents=True)
            (page / 'index.html').write_text('<p>official fixture</p>', encoding='utf-8')
            (page / 'figure.png').write_bytes(b'fixture-figure')
            record = {'id': 'fixture', 'url': 'https://example.org/manual', 'archive_status': 'complete_static',
                      'file': (page / 'index.html').relative_to(root).as_posix(), 'sha256': 'original-hash',
                      'original_sha256': 'raw-hash', 'archived_at_utc': '2026-01-01T00:00:00Z'}
            registry = project / 'reference_metrial/_registry'
            registry.mkdir()
            (registry / 'materials.json').write_text(json.dumps({'fixture': record}), encoding='utf-8')
            (page / 'metadata.json').write_text(json.dumps(record), encoding='utf-8')
            report = project / '01_Report.md'
            report.write_text('[source](reference_metrial/webpages/doc/index.html)\n![figure](reference_metrial/webpages/doc/figure.png)', encoding='utf-8')
            with patch.object(catalog, 'ROOT', root):
                catalog.prepare(project)
                text = report.read_text(encoding='utf-8')
                self.assertIn('REFERENCES.md#ref-', text)
                self.assertIn('assets/figures/', text)
                self.assertEqual((page / 'figure.png').read_bytes(), b'fixture-figure')
                self.assertEqual(json.loads((project / 'sources.json').read_text())[0]['sha256'], 'original-hash')
                before = (project / 'sources.json').read_bytes()
                (project / 'reference_metrial').rename(root / 'preserved-raw')
                catalog.prepare(project)
                self.assertEqual((project / 'sources.json').read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
