import tempfile
import unittest
from pathlib import Path
from archive_paths import portable, restore


class PortablePathsTest(unittest.TestCase):
    def test_round_trip_nested_records_preserves_urls_and_archive_relative_assets(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            path = root / '01_Compute_Chips/01_NVIDIA/reference_metrial/data/content.md'
            obj = {'file': path.as_posix(), 'assets': [{'file': '_registry/assets/a.png'}],
                   'url': 'https://example.org/01_Compute_Chips/manual.pdf', 'baseline': {'report.md': 'hash'}}
            stored = portable(obj, root)
            self.assertEqual(stored['file'], '01_Compute_Chips/01_NVIDIA/reference_metrial/data/content.md')
            self.assertEqual(restore(stored, root), obj)

    def test_relocation_does_not_depend_on_working_directory(self):
        obj = {'file': '01_Compute_Chips/02_Intel/reference_metrial/documents/document.pdf'}
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            self.assertEqual(restore(obj, root)['file'], (root / obj['file']).as_posix())


if __name__ == '__main__':
    unittest.main()
