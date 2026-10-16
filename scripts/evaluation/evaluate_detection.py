import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from labs._07_detection_engineering_loader import should_alert

DEFAULT_DATASET = (
    ROOT / "samples" / "evaluation" / "authentication-corpus.json"
)

APPROVED_COMMANDS = {
    "systemctl status ssh",
    "journalctl -u ssh",
}

VALID_LABELS = {"benign", "suspicious", "ambiguous"}


def load_cases(path):
    try:
        cases = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON dataset: {exc}") from exc

    if not isinstance(cases, list) or not cases:
        raise ValueError("Dataset must be a non-empty JSON list.")

    seen = set()

    for index, case in enumerate(cases, start=1):
        if not isinstance(case, dict):
            raise ValueError(f"Scenario {index} must be an object.")

        scenario_id = case.get("scenario_id")
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            raise ValueError(f"Scenario {index} needs a scenario_id.")

        if scenario_id in seen:
            raise ValueError(f"Duplicate scenario_id: {scenario_id}")
        seen.add(scenario_id)

        if not isinstance(case.get("description"), str):
            raise ValueError(f"{scenario_id}: description must be a string.")

        if not isinstance(case.get("labeling_rationale"), str):
            raise ValueError(
                f"{scenario_id}: labeling_rationale must be a string."
            )

        if case.get("activity_label") not in VALID_LABELS:
            raise ValueError(
                f"{scenario_id}: activity_label must be one of "
                f"{sorted(VALID_LABELS)}."
            )

        if type(case.get("expected_alert")) is not bool:
            raise ValueError(
                f"{scenario_id}: expected_alert must be a boolean."
            )

        if not isinstance(case.get("events"), list):
            raise ValueError(f"{scenario_id}: events must be a list.")

    return cases


def evaluate_cases(cases):
    results = []

    for case in cases:
        alerts = should_alert(
            case["events"],
            baseline=4,
            window_minutes=60,
            approved_commands=APPROVED_COMMANDS,
        )
        actual_alert = bool(alerts)

        results.append({
            "scenario_id": case["scenario_id"],
            "category": case.get("category", "unspecified"),
            "activity_label": case["activity_label"],
            "description": case["description"],
            "labeling_rationale": case["labeling_rationale"],
            "expected_alert": case["expected_alert"],
            "actual_alert": actual_alert,
            "rule_match": case["expected_alert"] == actual_alert,
            "alerts": alerts,
        })

    return results


def _ratio(numerator, denominator):
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def calculate_metrics(results):
    """Compare expected_alert to actual_alert, irrespective of activity labels."""
    tp = fp = tn = fn = 0

    for result in results:
        expected = result["expected_alert"]
        actual = result["actual_alert"]

        if type(expected) is not bool or type(actual) is not bool:
            raise ValueError("Expected and actual alert values must be booleans.")

        if expected and actual:
            tp += 1
        elif not expected and actual:
            fp += 1
        elif not expected and not actual:
            tn += 1
        else:
            fn += 1

    total = len(results)

    return {
        "scenario_count": total,
        "confusion_matrix": {
            "true_positive": tp,
            "false_positive": fp,
            "true_negative": tn,
            "false_negative": fn,
        },
        "metrics": {
            "accuracy": _ratio(tp + tn, total),
            "precision": _ratio(tp, tp + fp),
            "recall": _ratio(tp, tp + fn),
            "specificity": _ratio(tn, tn + fp),
            "f1_score": _ratio(2 * tp, 2 * tp + fp + fn),
        },
    }


def calculate_activity_metrics(results):
    """
    Compare actual alerts with scenario activity labels.
    Ambiguous scenarios are deliberately excluded.
    """
    labeled = [
        result for result in results
        if result["activity_label"] in {"benign", "suspicious"}
    ]

    mapped = [
        {
            "expected_alert": result["activity_label"] == "suspicious",
            "actual_alert": result["actual_alert"],
        }
        for result in labeled
    ]

    report = calculate_metrics(mapped)
    report["included_suspicious"] = sum(
        result["activity_label"] == "suspicious" for result in labeled
    )
    report["included_benign"] = sum(
        result["activity_label"] == "benign" for result in labeled
    )
    report["excluded_ambiguous"] = sum(
        result["activity_label"] == "ambiguous" for result in results
    )

    return report


def calculate_rule_agreement(results):
    total = len(results)
    matched = sum(result["rule_match"] for result in results)

    return {
        "scenario_count": total,
        "matched_scenarios": matched,
        "mismatched_scenarios": total - matched,
        "agreement_rate": _ratio(matched, total),
    }


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate the detection rule and compare its alerts against "
            "documented synthetic activity labels."
        )
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=DEFAULT_DATASET,
        help="Path to a labeled JSON evaluation dataset.",
    )
    args = parser.parse_args()

    try:
        cases = load_cases(args.dataset)
        results = evaluate_cases(cases)

        report = {
            "dataset": str(args.dataset),
            "evaluation_scope": (
                "Manually designed synthetic scenarios. Rule agreement "
                "measures regression consistency; activity metrics compare "
                "alerts against documented scenario labels. Neither result "
                "establishes real-world detection performance."
            ),
            "rule_regression": calculate_rule_agreement(results),
            "activity_classification": calculate_activity_metrics(results),
            "scenarios": results,
        }
    except (OSError, ValueError) as exc:
        print(f"Evaluation error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report, indent=2))

    if report["rule_regression"]["mismatched_scenarios"]:
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
