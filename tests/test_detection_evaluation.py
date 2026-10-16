import unittest

from scripts.evaluation.evaluate_detection import (
    DEFAULT_DATASET,
    calculate_metrics,
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
        self.assertIsNone(report["metrics"]["accuracy"])
        self.assertIsNone(report["metrics"]["precision"])
        self.assertIsNone(report["metrics"]["recall"])
        self.assertIsNone(report["metrics"]["specificity"])
        self.assertIsNone(report["metrics"]["f1_score"])

    def test_synthetic_corpus_matches_expected_labels(self):
        cases = load_cases(DEFAULT_DATASET)
        results = evaluate_cases(cases)
        report = calculate_metrics(results)

        self.assertEqual(len(cases), 11)
        self.assertTrue(all(result["match"] for result in results))
        self.assertEqual(
            report["confusion_matrix"],
            {
                "true_positive": 4,
                "false_positive": 0,
                "true_negative": 7,
                "false_negative": 0,
            },
        )


if __name__ == "__main__":
    unittest.main()
