
from datetime import datetime, timedelta, timezone
import re


def _parse_timestamp(value):
    """Parse an ISO-8601 timestamp and normalize it to UTC."""
    if not isinstance(value, str):
        raise ValueError("timestamp must be an ISO-8601 string")

    try:
        timestamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"Invalid timestamp: {value!r}") from exc

    # Documented convention: timestamps without a timezone are UTC.
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return timestamp.astimezone(timezone.utc)


def _normalize_command(value):
    """Normalize whitespace and case for exact allowlist comparison."""
    if not isinstance(value, str):
        return None

    value = " ".join(value.strip().split())
    return value.casefold() or None


def _get_command(event):
    """
    Prefer a structured command field.
    Fall back to COMMAND= in event_text, if available.
    Structured fields are more reliable than free-form log parsing.
    """
    if event.get("command") is not None:
        return _normalize_command(event["command"])

    text = event.get("event_text", "")
    if not isinstance(text, str):
        return None

    match = re.search(r"(?:^|\s)COMMAND=(.*)", text)
    return _normalize_command(match.group(1)) if match else None


def should_alert(
    events,
    baseline=4,
    window_minutes=60,
    approved_commands=None,
):
    """
    Alert when an account has more than `baseline` sudo failures
    in a window and an unapproved successful sudo command occurs
    in that same window.

    Returns at most one alert per account: the earliest qualifying
    window. A window includes both its start and end timestamps.

    `approved_commands` must be an explicit collection of complete
    command strings. Matching is case-insensitive and whitespace-
    normalized; it is not a shell-aware command parser.
    """
    if not isinstance(baseline, int) or isinstance(baseline, bool) or baseline < 0:
        raise ValueError("baseline must be a non-negative integer")

    if (
        not isinstance(window_minutes, int)
        or isinstance(window_minutes, bool)
        or window_minutes <= 0
    ):
        raise ValueError("window_minutes must be a positive integer")

    if approved_commands is None:
        raise ValueError("Provide an explicit approved_commands collection")

    approved = {
        normalized
        for command in approved_commands
        if (normalized := _normalize_command(command)) is not None
    }

    # Validate and normalize events once.
    prepared = []

    for event in events:
        if not isinstance(event, dict):
            raise ValueError("Each event must be a dictionary")

        account = event.get("account")
        if not account:
            continue

        timestamp = _parse_timestamp(event.get("timestamp"))

        prepared.append({
            **event,
            "account": account,
            "_time": timestamp,
            "_process": str(event.get("process", "")).casefold(),
            "_outcome": str(event.get("outcome", "")).casefold(),
            "_command": _get_command(event),
        })

    alerts = []
    window = timedelta(minutes=window_minutes)

    accounts = sorted({event["account"] for event in prepared})

    for account in accounts:
        account_events = sorted(
            (
                event for event in prepared
                if event["account"] == account
                and event["_process"] == "sudo"
            ),
            key=lambda event: event["_time"],
        )

        failures = [
            event for event in account_events
            if event["_outcome"] == "failure"
        ]

        successes = [
            event for event in account_events
            if event["_outcome"] == "success"
        ]

        # Find the earliest window with enough failures and
        # at least one unapproved successful command.
        right = 0

        for left, start_event in enumerate(failures):
            start = start_event["_time"]
            end = start + window

            right = max(right, left)

            while (
                right < len(failures)
                and failures[right]["_time"] <= end
            ):
                right += 1

            failure_count = right - left

            if failure_count <= baseline:
                continue

            suspicious = next(
                (
                    event for event in successes
                    if start <= event["_time"] <= end
                    and event["_command"] is not None
                    and event["_command"] not in approved
                ),
                None,
            )

            if suspicious:
                alerts.append({
                    "account": account,
                    "failure_count": failure_count,
                    "window_start": start.isoformat(),
                    "window_end": end.isoformat(),
                    "command": suspicious["_command"],
                    "reason": (
                        "Repeated sudo authentication failures and "
                        "an unapproved successful sudo command "
                        "within the same time window"
                    ),
                })
                break

    return alerts
