
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


def make_failures(count, start="2026-09-22T10:00:00", account="bunny"):
    start_time = datetime.fromisoformat(start)
    return [
        make_event(
            (start_time + timedelta(minutes=i)).isoformat(),
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

    def test_excess_failures_followed_by_unknown_command_alert(self):
        events = make_failures(5)
        events.append(make_event(
            "2026-09-22T10:10:00",
            outcome="success",
            event_text="COMMAND=unknown-command",
        ))

        alerts = self.detect(events)

        self.assertEqual(len(alerts), 1)
        self.assertEqual(alerts[0]["account"], "bunny")
        self.assertEqual(alerts[0]["failure_count"], 5)
        self.assertEqual(alerts[0]["command"], "unknown-command")

    def test_approved_command_does_not_alert(self):
        events = make_failures(5)
        events.append(make_event(
            "2026-09-22T10:10:00",
            outcome="success",
            command="systemctl status ssh",
        ))

        self.assertEqual(self.detect(events), [])

    def test_accounts_are_not_combined(self):
        events = make_failures(5, account="bunny")
        events += make_failures(
            4,
            start="2026-09-22T10:10:00",
            account="analyst",
        )
        events.append(make_event(
            "2026-09-22T10:20:00",
            outcome="success",
            account="analyst",
            command="unknown-command",
        ))

        self.assertEqual(self.detect(events), [])

    def test_command_outside_window_does_not_alert(self):
        events = make_failures(5)
        events.append(make_event(
            "2026-09-22T11:05:00",
            outcome="success",
            command="unknown-command",
        ))

        self.assertEqual(self.detect(events), [])

    def test_event_exactly_at_window_end_is_included(self):
        events = make_failures(5)
        events.append(make_event(
            "2026-09-22T11:00:00",
            outcome="success",
            command="unknown-command",
        ))

        self.assertEqual(len(self.detect(events)), 1)

    def test_out_of_order_events_still_alert(self):
        events = make_failures(5)
        events.append(make_event(
            "2026-09-22T10:10:00",
            outcome="success",
            command="unknown-command",
        ))
        events.reverse()

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
