import hashlib
import importlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch


SPACE = Path(__file__).resolve().parents[1]
FIXTURE = SPACE / "data" / "schema2"
sys.path.insert(0, str(SPACE))


class BenchmarkDataTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec("benchmark_data"),
                             "Schema 2 reader is not implemented")
        self.reader = importlib.import_module("benchmark_data").BenchmarkData

    def copied_bundle(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name) / "schema2"
        shutil.copytree(FIXTURE, root)
        return root

    def test_useful_obstacle_events_are_not_false_positives(self):
        data = self.reader(FIXTURE)
        row = data.result("B02-footcatch12", "R1b")
        self.assertEqual(row["trigger_count"], 9)
        self.assertIsNone(row["false_events"])
        self.assertEqual(len(data.events("B02-footcatch12", "R1b")), 9)
        self.assertIsNone(data.result("B99-missing", "BASE"))

    def test_r4_episode_starts_differ_from_active_ticks(self):
        row = self.reader(FIXTURE).result("B01-flat", "R4")
        self.assertEqual(row["trigger_count"], 108)
        self.assertEqual(row["active_tick_count"], 10544)
        self.assertEqual(row["false_events"], 108)

    def test_peak_drop_is_not_replaced_with_final_drop(self):
        data = self.reader(FIXTURE)
        baseline = data.result("B03-gap20", "BASE")
        reflex = data.result("B03-gap20", "R3v2")
        self.assertEqual(baseline["peak_body_drop_mm"], 156.0)
        self.assertEqual(reflex["peak_body_drop_mm"], 24.6)
        self.assertEqual(reflex["final_body_drop_mm"], 19.1)

    def test_tampered_artifact_is_rejected(self):
        root = self.copied_bundle()
        with (root / "B02-footcatch12_R1b_events.jsonl").open("a") as stream:
            stream.write("{}\n")
        with self.assertRaisesRegex(ValueError, "SHA256"):
            self.reader(root)

    def test_manifest_and_summary_schema_must_be_compatible(self):
        root = self.copied_bundle()
        manifest_path = root / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["schema_version"] = 1
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "schema"):
            self.reader(root)
        manifest["schema_version"] = 2
        summary_path = root / "summary.json"
        summary = json.loads(summary_path.read_text())
        summary["schema_version"] = 1
        summary_path.write_text(json.dumps(summary))
        manifest["artifacts"]["summary.json"] = hashlib.sha256(
            summary_path.read_bytes()).hexdigest()
        manifest_path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "schema"):
            self.reader(root)

    def test_source_digest_is_checked(self):
        root = self.copied_bundle()
        path = root / "manifest.json"
        manifest = json.loads(path.read_text())
        manifest["source_sha256"] = "0" * 64
        path.write_text(json.dumps(manifest))
        with self.assertRaisesRegex(ValueError, "source_sha256"):
            self.reader(root)

    def test_raw_allowlist_excludes_unlisted_files_and_traversal(self):
        root = self.copied_bundle()
        (root / "unlisted.json").write_text('{"private": true}')
        (root / "directory.json").mkdir()
        data = self.reader(root)
        self.assertIn("manifest.json", data.raw_files)
        self.assertIn("summary.json", data.raw_files)
        self.assertEqual(len(data.raw_files), 20)
        for name in ("../manifest.json", "/etc/passwd", "unlisted.json",
                     "directory.json", ".", "", None):
            with self.subTest(name=name), self.assertRaises(ValueError):
                data.read_raw(name)
        self.assertEqual(json.loads(data.read_raw("manifest.json"))[
            "schema_version"], 2)

    def test_manifest_cannot_allowlist_an_external_symlink(self):
        root = self.copied_bundle()
        external = root.parent / "external.json"
        external.write_text("{}")
        (root / "external.json").symlink_to(external)
        path = root / "manifest.json"
        manifest = json.loads(path.read_text())
        manifest["artifacts"]["external.json"] = hashlib.sha256(b"{}").hexdigest()
        path.write_text(json.dumps(manifest))
        with self.assertRaises(ValueError):
            self.reader(root)


class SpaceIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
        cls.app = importlib.import_module("app")

    @staticmethod
    def table(markdown):
        return {parts[0].strip(): parts[1].strip()
                for line in markdown.splitlines()
                if line.startswith("|") and len(parts := line.strip("|").split("|")) == 2}

    def test_locomotion_displays_schema2_event_meanings(self):
        useful = self.table(self.app.loco_metrics("B02-footcatch12", "R1b"))
        self.assertEqual(useful.get("Начала эпизодов"), "9")
        self.assertEqual(useful.get("Ложные срабатывания"), "не оценено")
        r4 = self.table(self.app.loco_metrics("B01-flat", "R4"))
        self.assertEqual(r4.get("Начала эпизодов"), "108")
        self.assertEqual(r4.get("Активные записи"), "10544")

    def test_locomotion_displays_peak_and_final_drop_separately(self):
        baseline = self.table(self.app.loco_metrics("B03-gap20", "BASE"))
        reflex = self.table(self.app.loco_metrics("B03-gap20", "R3v2"))
        self.assertEqual(baseline.get("Просадка: пик, мм"), "156.0")
        self.assertEqual(reflex.get("Просадка: пик, мм"), "24.6")
        self.assertEqual(reflex.get("Просадка: итог, мм"), "19.1")
        self.assertIsNotNone(reflex.get("Наклон: максимум, °"))

    def test_unknown_run_has_clear_missing_data_message(self):
        self.assertIn("Нет данных", self.app.loco_metrics("B99", "BASE"))

    def test_missing_verified_data_does_not_show_reflex_success(self):
        self.assertTrue(hasattr(self.app, "reflex_summary"),
                        "Reflex evidence must use the verified bundle")
        with patch.object(self.app, "BENCH", None), patch.object(
                self.app, "BENCH_ERROR", "missing manifest"):
            self.assertIn("недоступны", self.app.reflex_summary())
            self.assertIn("недоступны", self.app.loco_metrics("B02-footcatch12", "R1b"))
            self.assertIn("недоступны", self.app.provenance_markdown())
            self.assertTrue(all(row[2] == "нет данных"
                                for row in self.app.benchmark_table()[:3]))

    def test_raw_ui_returns_schema2_manifest_and_rejects_directories(self):
        self.assertEqual(json.loads(self.app.view_raw("summary.json")).get(
            "schema_version"), 2)
        self.assertEqual(json.loads(self.app.view_raw("manifest.json"))[
            "git_revision"], "62ce2a97eb44c3a06cdd4172591eb2e724684bbc")
        for name in ("cpg_m0", "../app.py", "/etc/passwd", "schema2"):
            self.assertIn("Недоступный файл", self.app.view_raw(name))

    def test_ui_provenance_and_raw_selector_use_verified_bundle(self):
        self.assertTrue(hasattr(self.app, "provenance_markdown"),
                        "UI must show the recorded provenance")
        provenance = self.app.provenance_markdown()
        for value in ("62ce2a97eb44c3a06cdd4172591eb2e724684bbc",
                      "31e7b9f231e39881fa40860e05a21f45d1aa6acd978ccae6f02c583cd13b52d8",
                      "20.0", "3.14.0", "2.4.6", "3.11.16"):
            self.assertIn(value, provenance)
        selectors = [component for component in self.app.demo.config["components"]
                     if component.get("props", {}).get("label") == "Файл"]
        self.assertEqual(len(selectors), 1)
        choices = [choice[1] if isinstance(choice, (tuple, list)) else choice
                   for choice in selectors[0]["props"]["choices"]]
        self.assertIn("manifest.json", choices)
        self.assertNotIn("cpg_m0", choices)
        self.assertEqual(len(choices), 20)

    def test_cpg_still_uses_saved_data_and_live_knockout(self):
        figure, text = self.app.cpg_view("normal", 0.8)
        self.assertIsNotNone(figure)
        self.assertIn("normal, drive=0.8", text)
        self.assertEqual(self.app.sim_cpg(ko=("DgR",)).sum(), 0)
        self.assertGreater(self.app.sim_cpg().sum(), 0)


if __name__ == "__main__":
    unittest.main()
