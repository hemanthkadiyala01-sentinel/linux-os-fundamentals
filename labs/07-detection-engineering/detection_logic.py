from datetime import datetime, timedelta

def should_alert(events, baseline=4, window_minutes=60):
    alerts = []

    accounts = sorted({e.get("account") for e in events if e.get("account")})

    for account in accounts:
        account_events = [
            e for e in events
            if e.get("account") == account
            and e.get("process") == "sudo"
        ]

        failures = [
            e for e in account_events
            if e.get("outcome") == "failure"
        ]

        if not failures:
            continue

        failures.sort(key=lambda e: e["timestamp"])

        for start_event in failures:
            start = datetime.fromisoformat(start_event["timestamp"])
            end = start + timedelta(minutes=window_minutes)

            window_failures = [
                e for e in failures
                if start <= datetime.fromisoformat(e["timestamp"]) <= end
            ]

            suspicious_commands = [
                e for e in account_events
                if e.get("outcome") == "success"
                and "COMMAND=" in e.get("event_text", "")
                and "COMMAND=approved-" not in e.get("event_text", "")
                and start <= datetime.fromisoformat(e["timestamp"]) <= end
            ]

            if len(window_failures) > baseline and suspicious_commands:
                alerts.append({
                    "account": account,
                    "failure_count": len(window_failures),
                    "window_start": start_event["timestamp"],
                    "reason": "Repeated sudo authentication failures followed by an unrecognized sudo command"
                })
                break

    return alerts
