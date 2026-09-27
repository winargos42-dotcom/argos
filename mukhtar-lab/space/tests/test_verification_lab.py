import importlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

SPACE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SPACE))


class VerificationLabTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec("verification_lab"),
                             "Recorded verification viewer is not implemented")
        self.lab = importlib.import_module("verification_lab")

    def test_all_recorded_experiments_have_pinned_provenance(self):
        names = self.lab.list_experiments()
        self.assertEqual(len(names), 14)
        for name in names:
            record = self.lab.load_experiment(name)
            self.assertTrue(record["source_revision"].startswith("07c6f55"))
            self.assertEqual(record["checkpoint_validation"], "not_performed")
            self.assertEqual(len(record["sha256"]), 64)
            self.assertTrue(Path(self.lab.raw_path(name)).is_file())

    def test_vision_plot_retains_weaker_fly_result_and_untrained_label(self):
        name = "vision_depth_looming.json"
        record = self.lab.load_experiment(name)
        self.assertEqual(record["data"]["results"]["fly"]["acc"], 0.29)
        self.assertEqual(record["data"]["results"]["twin"]["acc"], 0.53625)
        figure = self.lab.plot_experiment(name)
        heights = [bar.get_height() for bar in figure.axes[0].patches]
        self.assertEqual(heights, [0.84, 0.8375, 0.29, 0.53625, 0.32875])
        summary = self.lab.render_summary(name)
        for text in ("записан", "untrained", "0.29", "0.53625", "не проверен"):
            self.assertIn(text, summary)

    def test_mnist_and_olfaction_use_reported_accuracy(self):
        mnist = self.lab.plot_experiment("vision_phase0_rec20.json")
        self.assertEqual([p.get_height() for p in mnist.axes[0].patches],
                         [0.882, 0.899, 0.874, 0.905])
        olf = self.lab.load_experiment("olfaction_mb_summary.json")["data"]
        self.assertEqual(olf["mean_test_acc"]["backprop"], 0.707)
        self.assertIn("not robot gas-source navigation",
                      self.lab.render_summary("olfaction_mb_summary.json"))

    def test_b09_plot_shows_recorded_repeats_and_t2_parses_only_json_lines(self):
        figure = self.lab.plot_experiment("b09_shadow_results.json")
        self.assertEqual(len(figure.axes[0].lines), 3)
        self.assertEqual(list(figure.axes[0].lines[0].get_ydata()),
                         [0.34, 0.34, 0.36, 0.34, 0.34, 0.4])
        data = self.lab.load_experiment("t2_closed_fresh.txt")["data"]
        trials = [row for row in data if "variant" in row]
        self.assertEqual(len(trials), 12)
        self.assertTrue(all(not row["goal_reached"] for row in trials))

    def test_unknown_and_traversal_names_do_not_read_files(self):
        for name in ("../app.py", "/etc/passwd", "manifest.json", "", None):
            with self.subTest(name=name), self.assertRaises(ValueError):
                self.lab.load_experiment(name)

    def test_changed_bytes_and_external_symlink_are_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "verification"
            shutil.copytree(SPACE / "data/verification", target)
            name = "vision_depth_looming.json"
            (target / name).write_text("{}")
            with patch.object(self.lab, "DATA", target), self.assertRaisesRegex(ValueError, "SHA256"):
                self.lab.load_experiment(name)
            (target / name).unlink()
            (target / name).symlink_to(SPACE / "data/verification" / name)
            with patch.object(self.lab, "DATA", target), self.assertRaises(ValueError):
                self.lab.raw_path(name)


if __name__ == "__main__":
    unittest.main()
