
import unittest
from datetime import datetime, timedelta

from labs._07_detection_engineering_loader import should_alert


APPROVED_COMMANDS = {
    "systemctl status ssh",
    "journalctl -u ssh",
}


def make_event(
    timestamp,
    outcome="failure",
    account="bunny",
    event_text="authentication failure",
    command=None,
):
    event = {
        "timestamp": timestamp,
        "account": account,
        "process": "sudo",
        "outcome": outcome,
        "event_text": event_text,
    }

    if command is not None:
        event["command"] = command

    return event


def make_failures(
    count,
    start="2026-09-22T10:00:00",
    account="bunny",
    interval_minutes=1,
):
    start_time = datetime.fromisoformat(start)

    return [
        make_event(
            (
                start_time
                + timedelta(minutes=i * interval_minutes)
            ).isoformat(),
            account=account,
        )
        for i in range(count)
    ]


class DetectionTests(unittest.TestCase):

    def detect(self, events, **kwargs):
        return should_alert(
            events,
            approved_commands=APPROVED_COMMANDS,
            **kwargs,
        )

    def test_baseline_does_not_alert(self):
        self.assertEqual(self.detect(make_failures(4)), [])

    def test_excess_failures_without_command_do_not_alert(self):
        self.assertEqual(self.detect(make_failures(5)), [])

    def test_command_after_fifth_failure_alerts(self):
        events = make_failures(5)
        events.append(
            make_event(
                "2026-09-22T10:10:00",
                outcome="success",
                event_text="COMMAND=unknown-command",
            )
        )

        alerts = self.detect(events)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["account"], "bunny")
        self.assertEqual(alerts[0]["failure_count"], 5)
        self.assertEqual(alerts[0]["command"], "unknown-command")

    def test_command_before_failures_does_not_alert(self):
        events = [
            make_event(
                "2026-09-22T09:59:00",
                outcome="success",
                command="unknown-command",
            )
        ]
        events.extend(make_failures(5))

        self.assertEqual(self.detect(events), [])

    def test_command_between_first_and_fifth_failures_does_not_alert(self):
        events = make_failures(5)
        events.append(
            make_event(
                "2026-09-22T10:02:30",
                outcome="success",
                command="unknown-command",
            )
        )

        self.assertEqual(self.detect(events), [])

    def test_approved_command_after_fifth_failure_does_not_alert(self):
        events = make_failures(5)
        events.append(
            make_event(
                "2026-09-22T10:10:00",
                outcome="success",
                command="systemctl status ssh",
            )
        )

        self.assertEqual(self.detect(events), [])

    def test_blank_structured_command_falls_back_to_event_text(self):
        events = make_failures(5)
        events.append(
            make_event(
                "2026-09-22T10:10:00",
                outcome="success",
                event_text="sudo COMMAND=unknown-command",
                command="   ",
            )
        )

        alerts = self.detect(events)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["command"], "unknown-command")

    def test_accounts_are_not_combined(self):
        events = make_failures(5, account="bunny")
        events.extend(
            make_failures(
                4,
                start="2026-09-22T10:10:00",
                account="analyst",
            )
        )
        events.append(
            make_event(
                "2026-09-22T10:20:00",
                outcome="success",
                account="analyst",
                command="unknown-command",
            )
        )

        self.assertEqual(self.detect(events), [])

    def test_command_outside_window_does_not_alert(self):
        events = make_failures(5)
        events.append(
            make_event(
                "2026-09-22T11:05:00",
                outcome="success",
                command="unknown-command",
            )
        )

        self.assertEqual(self.detect(events), [])

    def test_command_at_window_end_is_included(self):
        events = make_failures(5)
        events.append(
            make_event(
                "2026-09-22T11:00:00",
                outcome="success",
                command="unknown-command",
            )
        )

        self.assertEqual(len(self.detect(events)), 1)

    def test_out_of_order_input_still_alerts(self):
        events = make_failures(5)
        events.append(
            make_event(
                "2026-09-22T10:10:00",
                outcome="success",
                command="unknown-command",
            )
        )
        events.reverse()

        self.assertEqual(len(self.detect(events)), 1)

    def test_duplicate_failure_event_is_counted_once(self):
        events = make_failures(4)
        events.append(events[0].copy())
        events.append(
            make_event(
                "2026-09-22T10:10:00",
                outcome="success",
                command="unknown-command",
            )
        )

        self.assertEqual(self.detect(events), [])

    def test_timezone_offsets_are_normalized(self):
        events = [
            make_event(
                f"2026-09-22T{hour:02d}:{minute:02d}:00+00:00"
            )
            for hour, minute in [
                (10, 0),
                (10, 1),
                (10, 2),
                (10, 3),
                (10, 4),
            ]
        ]
        events.append(
            make_event(
                "2026-09-22T15:40:00+05:30",
                outcome="success",
                command="unknown-command",
            )
        )

        self.assertEqual(len(self.detect(events)), 1)

    def test_missing_allowlist_raises_error(self):
        with self.assertRaises(ValueError):
            should_alert(make_failures(5))

    def test_invalid_timestamp_raises_error(self):
        events = make_failures(5)
        events[0]["timestamp"] = "not-a-timestamp"

        with self.assertRaises(ValueError):
            self.detect(events)


if __name__ == "__main__":
    unittest.main()