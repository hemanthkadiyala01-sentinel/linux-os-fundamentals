import unittest
from labs._07_detection_engineering_loader import should_alert

class DetectionTests(unittest.TestCase):

    def test_baseline_does_not_alert(self):
        events = [
            {"timestamp": f"2026-09-22T10:0{i}:00", "account": "bunny", "process": "sudo", "outcome": "failure", "event_text": "authentication failure"}
            for i in range(4)
        ]
        self.assertEqual(should_alert(events), [])

    def test_excess_failures_without_command_do_not_alert(self):
        events = [
            {"timestamp": f"2026-09-22T10:0{i}:00", "account": "bunny", "process": "sudo", "outcome": "failure", "event_text": "authentication failure"}
            for i in range(5)
        ]
        self.assertEqual(should_alert(events), [])

    def test_excess_failures_followed_by_unknown_command_alert(self):
        events = [
            {"timestamp": f"2026-09-22T10:0{i}:00", "account": "bunny", "process": "sudo", "outcome": "failure", "event_text": "authentication failure"}
            for i in range(5)
        ]
        events.append({
            "timestamp": "2026-09-22T10:10:00",
            "account": "bunny",
            "process": "sudo",
            "outcome": "success",
            "event_text": "COMMAND=unknown-command"
        })

        self.assertEqual(len(should_alert(events)), 1)

    def test_accounts_are_not_combined(self):
        events = [
            {"timestamp": f"2026-09-22T10:0{i}:00", "account": "bunny", "process": "sudo", "outcome": "failure", "event_text": "authentication failure"}
            for i in range(5)
        ]

        events += [
            {"timestamp": f"2026-09-22T10:1{i}:00", "account": "analyst", "process": "sudo", "outcome": "failure", "event_text": "authentication failure"}
            for i in range(4)
        ]

        self.assertEqual(should_alert(events), [])

    def test_outside_window_does_not_alert(self):
        events = [
            {"timestamp": f"2026-09-22T10:0{i}:00", "account": "bunny", "process": "sudo", "outcome": "failure", "event_text": "authentication failure"}
            for i in range(4)
        ]

        events += [
            {"timestamp": f"2026-09-22T11:0{i}:00", "account": "bunny", "process": "sudo", "outcome": "failure", "event_text": "authentication failure"}
            for i in range(4)
        ]

        self.assertEqual(should_alert(events), [])

if __name__ == "__main__":
    unittest.main()
