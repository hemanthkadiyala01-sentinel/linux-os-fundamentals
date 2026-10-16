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
            raise ValueError(f"Scenario {index} must be a JSON object.")

        scenario_id = case.get("scenario_id")
        if not isinstance(scenario_id, str) or not scenario_id.strip():
            raise ValueError(f"Scenario {index} needs a scenario_id.")

        if scenario_id in seen:
            raise ValueError(f"Duplicate scenario_id: {scenario_id}")
        seen.add(scenario_id)

        if not isinstance(case.get("description"), str):
            raise ValueError(f"{scenario_id}: description must be a string.")

        if type(case.get("expected_alert")) is not bool:
            raise ValueError(
                f"{scenario_id}: expected_alert must be true or false."
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
        expected_alert = case["expected_alert"]

        results.append({
            "scenario_id": case["scenario_id"],
            "description": case["description"],
            "expected_alert": expected_alert,
            "actual_alert": actual_alert,
            "match": expected_alert == actual_alert,
            "alerts": alerts,
        })

    return results


def _ratio(numerator, denominator):
    if denominator == 0:
        return None
    return round(numerator / denominator, 4)


def calculate_metrics(results):
    tp = fp = tn = fn = 0

    for result in results:
        expected = result["expected_alert"]
        actual = result["actual_alert"]

        if type(expected) is not bool or type(actual) is not bool:
            raise ValueError("Expected and actual labels must be booleans.")

        if expected and actual:
            tp += 1
        elif not expected and actual:
            fp += 1
        elif not expected and not actual:
            tn += 1
        else:
            fn += 1

    total = len(results)
    accuracy = _ratio(tp + tn, total)
    precision = _ratio(tp, tp + fp)
    recall = _ratio(tp, tp + fn)
    specificity = _ratio(tn, tn + fp)

    if (
        precision is None
        or recall is None
        or precision + recall == 0
    ):
        f1_score = None
    else:
        f1_score = round(
            2 * precision * recall / (precision + recall),
            4,
        )

    return {
        "scenario_count": total,
        "confusion_matrix": {
            "true_positive": tp,
            "false_positive": fp,
            "true_negative": tn,
            "false_negative": fn,
        },
        "metrics": {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "specificity": specificity,
            "f1_score": f1_score,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate detection logic against labeled synthetic cases."
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
                "Scenario-level evaluation on manually designed synthetic "
                "cases. Results do not represent real-world detection accuracy."
            ),
            **calculate_metrics(results),
            "scenarios": results,
        }
    except (OSError, ValueError) as exc:
        print(f"Evaluation error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(report, indent=2))

    if not all(result["match"] for result in results):
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
