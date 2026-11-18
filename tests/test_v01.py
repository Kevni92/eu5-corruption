"""Build-tool and static script checks; no access to the running EU5 engine."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from build_release import release

class TestReleaseCandidate(unittest.TestCase):
    def make_game(self, root):
        game = root / "game"
        folder = game / "in_game" / "common" / "auto_modifiers"
        folder.mkdir(parents=True)
        (game / "main_menu" / "common").mkdir(parents=True)
        (folder / "country.txt").write_text(
            "country_base_values = {\n  global_estate_max_tax = 0.35\n}\n")
        for i in range(61):
            (game / "in_game" / f"dummy_{i}.txt").write_text("# stub\n")
        laws = game / "in_game" / "common" / "laws"
        laws.mkdir(parents=True)
        (laws / "test.txt").write_text(
            "test_policy = {\n country_modifier = {\n nobles_estate_max_tax = -0.1\n }\n}\n")
        return game

    def test_build_and_migrate(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = self.make_game(root)
            out = root / "dist" / "EstateCorruption"
            report = release(ROOT, source, out, "1.4.9")
            self.assertEqual(report["assignments_migrated"], 2)
            self.assertIn("ec_global_acceptable_max_tax = 0.35",
                          (out / "in_game/common/auto_modifiers/country.txt").read_text())
            self.assertIn("global_estate_max_tax = 1.0",
                          (out / "in_game/common/auto_modifiers/ec_tax_ceiling.txt").read_text())
            self.assertTrue((out / "in_game/common/scripted_effects/ec_corruption_monthly.txt").is_file())
            self.assertFalse((out / "docs").exists())
            self.assertFalse((out / "tools").exists())
            metadata = json.loads((out / ".metadata/metadata.json").read_text())
            self.assertEqual(metadata["version"], "0.1.0-rc1")
            self.assertEqual(metadata["game_id"], "eu5")
            self.assertFalse(report["version_verified_by_engine"])

    def test_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            source = self.make_game(root)
            out = root / "dist" / "EstateCorruption"
            with self.assertRaises(ValueError):
                release(ROOT, source, out, "1.4.3")
            (source / "in_game" / "unknown.txt").write_text("newfolk_estate_max_tax = 0.2\n")
            with self.assertRaises(RuntimeError):
                release(ROOT, source, out, "1.4.9")
            self.assertFalse(out.exists())

    def test_independent_estate_effects_and_braces(self):
        effect = (ROOT / "in_game/common/scripted_effects/ec_corruption_monthly.txt").read_text()
        impacts = (ROOT / "main_menu/common/static_modifiers/ec_corruption_impact.txt").read_text()
        for estate in ("nobles","clergy","burghers","peasants","tribes","cossacks","dhimmi","crown"):
            self.assertIn(f"clamp_variable = {{ name = ec_{estate}_corruption min = 0 max = 100 }}", effect)
            self.assertIn(f"ec_{estate}_corruption_impact", impacts)
            self.assertIn(f"ec_{estate}_corruption = 100", impacts)
            self.assertIn(f"ec_{estate}_corruption_impact", effect)
        for filename in list((ROOT / "in_game").rglob("*.txt")) + list((ROOT / "main_menu/common").rglob("*.txt")):
            data = filename.read_text(encoding="utf-8-sig")
            self.assertEqual(data.count("{"), data.count("}"), str(filename))

if __name__ == "__main__":
    unittest.main()
