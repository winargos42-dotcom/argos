"""Test the trusted proposal pipeline; NEVER run generated code."""
import json
import os
from pathlib import Path
import tempfile
import unittest
import autodev

GOOD = "def classify_node_state(heartbeat: dict) -> str:\n    return 'confirmed' if heartbeat.get('remote_verified') else 'unknown'\n"


class AutoDevTest(unittest.TestCase):
    def test_candidate_written_but_not_executed(self):
        with tempfile.TemporaryDirectory() as t:
            r = autodev.generate_proposal(
                "Create pure function classifying remote node health",
                root=Path(t), generate=lambda _: json.dumps({"code": GOOD}))
            result = json.loads(r)
            self.assertEqual(result["status"], "NEEDS_REVIEW")
            self.assertFalse(result["tests_executed"])
            dest = next(Path(t).iterdir())
            self.assertEqual((dest / "candidate.py").read_text(), GOOD)
            self.assertEqual((dest / "candidate.py").stat().st_mode & 0o777, 0o600)
            self.assertEqual(json.loads((dest / "report.json").read_text())["report"]["syntax"], "pass")

    def test_import_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(ValueError):
                autodev.generate_proposal("Create pure node classifier function",
                    root=Path(t), generate=lambda _: json.dumps({"code": "import os\n" + GOOD}))
            self.assertFalse(list(Path(t).iterdir()))

    def test_side_effects_rejected(self):
        with self.assertRaises(ValueError):
            autodev.validate_code("def risky(x):\n    return open('secret').read()\n")

    def test_syntax_does_not_mean_correct_behavior(self):
        # A model may generate valid Python but inverted semantics. The system
        # must never label such code as tested or safe to deploy.
        incorrect = "def classify_node_state(h):\n    return 'unknown' if h.get('remote_verified') else 'confirmed'\n"
        report = autodev.validate_code(incorrect)
        self.assertEqual(report["syntax"], "pass")
        self.assertFalse(report["tests_executed"])

    def test_develop_router_does_not_call_original_master(self):
        import ast
        path = Path(__file__).with_name("agent_pool.py")
        tree = ast.parse(path.read_text())
        route = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "route")
        sandbox = {"ArgosMasterCore": object, "SHELL_PREFIXES": (),
                   "OPERATOR": "test", "autodev": autodev}
        # The imported module is part of the static trusted repository, not
        # generated code. No generated content is executed.
        exec(compile(ast.fix_missing_locations(ast.Module(body=[route],type_ignores=[])),
                     str(path),"exec"), sandbox)
        class DummyMaster:
            def execute(self,*args,**kwargs):
                raise AssertionError("direct ARGOS execution not allowed")
        orig = autodev.generate_proposal
        try:
            autodev.generate_proposal=lambda goal: "NEEDS_REVIEW_MOCK"
            mode, output = sandbox["route"](DummyMaster(),"develop: Write a pure function to summarize tasks")
            self.assertEqual(mode,"develop")
            self.assertEqual(output,"NEEDS_REVIEW_MOCK")
        finally:
            autodev.generate_proposal=orig

    def test_daily_queue(self):
        class Memory:
            def __init__(self): self.goals = []
            def add_goal(self, text, priority): self.goals.append((text, priority));return len(self.goals)
            def log_event(self, *args): pass
        cm = Memory(); state = {}
        old = os.environ.get("ARGOS_AUTODEV_ENABLED")
        os.environ["ARGOS_AUTODEV_ENABLED"] = "1"
        try:
            self.assertTrue(autodev.schedule_one(cm,state,at=200000)["queued"])
            self.assertFalse(autodev.schedule_one(cm,state,at=200100)["queued"])
            self.assertTrue(autodev.schedule_one(cm,state,at=200000+86401)["queued"])
            self.assertEqual(len(cm.goals),2)
        finally:
            if old is None:os.environ.pop("ARGOS_AUTODEV_ENABLED")
            else:os.environ["ARGOS_AUTODEV_ENABLED"]=old

if __name__ == "__main__":
    unittest.main()
