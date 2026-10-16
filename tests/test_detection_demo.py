import json
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEMO = ROOT / "scripts" / "demo" / "run_detection_demo.py"


class DetectionDemoTests(unittest.TestCase):
    def run_demo(self, *args):
        return subprocess.run(
            [sys.executable, str(DEMO), *args],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_all_scenarios_have_expected_results(self):
        result = self.run_demo()

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)

        self.assertEqual(
            [item["scenario"] for item in output],
            ["benign", "suspicious-sequence"],
        )
        self.assertEqual(
            [item["alert_count"] for item in output],
            [0, 1],
        )

    def test_benign_scenario_generates_no_alert(self):
        result = self.run_demo("--scenario", "benign")

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["alert_count"], 0)
        self.assertEqual(output[0]["alerts"], [])

    def test_suspicious_scenario_contains_expected_alert(self):
        result = self.run_demo(
            "--scenario", "suspicious-sequence"
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)

        self.assertEqual(len(output), 1)
        self.assertEqual(output[0]["alert_count"], 1)

        alert = output[0]["alerts"][0]
        self.assertEqual(alert["account"], "analyst1")
        self.assertEqual(alert["failure_count"], 5)
        self.assertEqual(alert["command"], "unknown-command")


if __name__ == "__main__":
    unittest.main()
