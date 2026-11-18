import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from build_overrides import build

class TestTaxMigration(unittest.TestCase):
    def test_preserves_vanilla_and_reports_comments_and_unknown(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            game = root / 'game'
            src = game / 'in_game' / 'common'
            src.mkdir(parents=True)
            (game / 'main_menu' / 'common').mkdir(parents=True)
            for n in range(60):
                (src / f'f{n}.txt').write_text('# marker\n')
            file = src / 'law.txt'
            raw = b'\xef\xbb\xbfkey = {\r\n    nobles_estate_max_tax = -0.1\r\n    # global_estate_max_tax = 2\r\n    newfolk_estate_max_tax = 0.3\r\n}\r\n'
            file.write_bytes(raw)
            report = build(game, root / 'build')
            self.assertEqual(report['files_scanned'], 61)
            self.assertEqual(report['candidate_assignments'], 1)
            self.assertEqual(report['status_counts']['unknown_modifier'], 1)
            self.assertEqual(report['status_counts']['comment'], 1)
            self.assertEqual(file.read_bytes(), raw)
            out = root / 'build' / 'overrides' / 'in_game' / 'common' / 'law.txt'
            data = out.read_bytes()
            self.assertTrue(data.startswith(b'\xef\xbb\xbf'))
            self.assertIn(b'ec_nobles_acceptable_max_tax = -0.1', data)
            self.assertIn(b'\r\n', data)

    def test_fails_on_missing_game_data(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / 'in_game').mkdir()
            (root / 'main_menu').mkdir()
            with self.assertRaises(ValueError):
                build(root, root.parent / 'out')

if __name__ == '__main__':
    unittest.main()
