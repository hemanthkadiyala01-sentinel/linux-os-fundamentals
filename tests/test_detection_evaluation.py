import json
import tempfile
import unittest
from pathlib import Path

from scripts.evaluation.evaluate_detection import (
    DEFAULT_DATASET,
    calculate_activity_metrics,
    calculate_metrics,
    calculate_rule_agreement,
    evaluate_cases,
    load_cases,
)


class DetectionEvaluationTests(unittest.TestCase):

    def test_confusion_matrix_and_metrics(self):
        results = [
            {"expected_alert": True, "actual_alert": True},
            {"expected_alert": False, "actual_alert": True},
            {"expected_alert": False, "actual_alert": False},
            {"expected_alert": True, "actual_alert": False},
        ]

        report = calculate_metrics(results)

        self.assertEqual(report["scenario_count"], 4)
        self.assertEqual(
            report["confusion_matrix"],
            {
                "true_positive": 1,
                "false_positive": 1,
                "true_negative": 1,
                "false_negative": 1,
            },
        )
        self.assertEqual(
            report["metrics"],
            {
                "accuracy": 0.5,
                "precision": 0.5,
                "recall": 0.5,
                "specificity": 0.5,
                "f1_score": 0.5,
            },
        )

    def test_zero_denominators_return_none(self):
        report = calculate_metrics([
            {"expected_alert": False, "actual_alert": False}
        ])

        self.assertIsNone(report["metrics"]["precision"])
        self.assertIsNone(report["metrics"]["recall"])
        self.assertIsNone(report["metrics"]["f1_score"])
        self.assertEqual(report["metrics"]["specificity"], 1.0)

    def test_empty_results_have_undefined_metrics(self):
        report = calculate_metrics([])

        self.assertEqual(report["scenario_count"], 0)
        for name in (
            "accuracy", "precision", "recall", "specificity", "f1_score"
        ):
            self.assertIsNone(report["metrics"][name])

    def test_corpus_rule_regression(self):
        cases = load_cases(DEFAULT_DATASET)
        results = evaluate_cases(cases)
        report = calculate_rule_agreement(results)

        self.assertEqual(len(cases), 26)
        self.assertEqual(report["matched_scenarios"], 26)
        self.assertEqual(report["mismatched_scenarios"], 0)
        self.assertEqual(report["agreement_rate"], 1.0)

    def test_activity_metrics_include_known_challenges(self):
        results = evaluate_cases(load_cases(DEFAULT_DATASET))
        report = calculate_activity_metrics(results)

        self.assertEqual(report["scenario_count"], 21)
        self.assertEqual(report["included_suspicious"], 10)
        self.assertEqual(report["included_benign"], 11)
        self.assertEqual(report["excluded_ambiguous"], 5)

        self.assertEqual(
            report["confusion_matrix"],
            {
                "true_positive": 8,
                "false_positive": 1,
                "true_negative": 10,
                "false_negative": 2,
            },
        )
        self.assertEqual(
            report["metrics"],
            {
                "accuracy": 0.8571,
                "precision": 0.8889,
                "recall": 0.8,
                "specificity": 0.9091,
                "f1_score": 0.8421,
            },
        )

    def test_ambiguous_scenarios_are_excluded_from_classification(self):
        results = [
            {
                "activity_label": "suspicious",
                "actual_alert": True,
            },
            {
                "activity_label": "benign",
                "actual_alert": False,
            },
            {
                "activity_label": "ambiguous",
                "actual_alert": True,
            },
        ]

        report = calculate_activity_metrics(results)

        self.assertEqual(report["scenario_count"], 2)
        self.assertEqual(report["excluded_ambiguous"], 1)
        self.assertEqual(
            report["confusion_matrix"],
            {
                "true_positive": 1,
                "false_positive": 0,
                "true_negative": 1,
                "false_negative": 0,
            },
        )

    def test_missing_or_duplicate_labels_are_rejected(self):
        cases = load_cases(DEFAULT_DATASET)

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            duplicate_path = root / "duplicate.json"
            duplicate_path.write_text(
                json.dumps([cases[0], cases[0]]),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "Duplicate scenario_id"):
                load_cases(duplicate_path)

            missing = dict(cases[0])
            missing.pop("labeling_rationale")

            missing_path = root / "missing-rationale.json"
            missing_path.write_text(
                json.dumps([missing]),
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "labeling_rationale"):
                load_cases(missing_path)


if __name__ == "__main__":
    unittest.main()
