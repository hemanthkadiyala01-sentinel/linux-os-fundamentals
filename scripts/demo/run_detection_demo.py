import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from labs._07_detection_engineering_loader import should_alert

SAMPLES = ROOT / "samples" / "authentication"

APPROVED_COMMANDS = {
    "systemctl status ssh",
    "journalctl -u ssh",
}


def load_events(path):
    events = []

    with path.open("r", encoding="utf-8-sig") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"{path.name}, line {line_number}: invalid JSON"
                ) from exc

            if not isinstance(event, dict):
                raise ValueError(
                    f"{path.name}, line {line_number}: "
                    "each event must be a JSON object"
                )

            events.append(event)

    return events


def run_scenario(name):
    path = SAMPLES / f"{name}.jsonl"
    events = load_events(path)

    alerts = should_alert(
        events,
        baseline=4,
        window_minutes=60,
        approved_commands=APPROVED_COMMANDS,
    )

    return {
        "scenario": name,
        "input_events": len(events),
        "alert_count": len(alerts),
        "alerts": alerts,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run the synthetic sudo detection demonstration."
    )
    parser.add_argument(
        "--scenario",
        choices=["all", "benign", "suspicious-sequence"],
        default="all",
        help="Scenario to evaluate (default: all).",
    )
    args = parser.parse_args()

    scenarios = (
        ["benign", "suspicious-sequence"]
        if args.scenario == "all"
        else [args.scenario]
    )

    try:
        results = [run_scenario(name) for name in scenarios]
    except (OSError, ValueError) as exc:
        print(f"Demo error: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(results, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
