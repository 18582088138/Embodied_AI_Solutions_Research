"""Regression checks for scoped research registration."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import organize_repository as organizer


class ScopedRegistrationTests(unittest.TestCase):
    def test_support_directory_is_not_a_research_project(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            category = root / '06_Open_Source'
            for name in ('21_LeRobot_SO101', 'research_state', 'assets'):
                (category / name).mkdir(parents=True)
            with patch.object(organizer, 'ROOT', root):
                self.assertEqual([p.name for p in organizer.category_projects('06_Open_Source')], ['21_LeRobot_SO101'])

    def test_scoped_index_preserves_unrelated_content(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / '06_Open_Source/21_LeRobot_SO101'
            (project / 'research_state').mkdir(parents=True)
            (project / 'research_state/progress.json').write_text(json.dumps(dict(completed_dimensions=['01_Product_Research'])), encoding='utf-8')
            (project / '01_Product_Research.md').write_text('# SO-101\n\n研究正文\n', encoding='utf-8')
            (project / 'README.md').write_text('Authored product navigation\n', encoding='utf-8')
            old_entry = dict(project='01_Compute_Chips/01_NVIDIA', path='01_Compute_Chips/01_NVIDIA/01_Hardware_Platform.md', sha256='preserve-existing-index')
            (root / 'research-index.json').write_text(json.dumps([old_entry]), encoding='utf-8')
            original = '# Research\n\n## Existing category\n\nKeep this section.\n\n## 下载与复用\n\nArchive rules.\n'
            (root / 'README.md').write_text(original, encoding='utf-8')
            with patch.object(organizer, 'ROOT', root), patch('prepare_git_sources.prepare'):
                organizer.build_selected_indexes('06_Open_Source')
                first = (root / 'README.md').read_bytes()
                organizer.build_selected_indexes('06_Open_Source')
            entries = json.loads((root / 'research-index.json').read_text(encoding='utf-8'))
            self.assertEqual(entries[0], old_entry)
            self.assertEqual(len(entries), 2)
            self.assertIn('首轮', entries[1]['status'])
            self.assertIn('## Existing category\n\nKeep this section.\n\n', (root / 'README.md').read_text(encoding='utf-8'))
            self.assertEqual((root / 'README.md').read_bytes(), first)
            self.assertEqual((project / 'README.md').read_text(encoding='utf-8'), 'Authored product navigation\n')


if __name__ == '__main__':
    unittest.main()
