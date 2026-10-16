
from datetime import datetime, timedelta, timezone
import re


def _parse_timestamp(value):
    """Parse an ISO-8601 timestamp and normalize it to UTC."""
    if not isinstance(value, str):
        raise ValueError("timestamp must be an ISO-8601 string")

    try:
        timestamp = datetime.fromisoformat(
            value.replace("Z", "+00:00")
        )
    except ValueError as exc:
        raise ValueError(f"Invalid timestamp: {value!r}") from exc

    # Convention: timestamps without a timezone are interpreted as UTC.
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    return timestamp.astimezone(timezone.utc)


def _normalize_command(value):
    """Normalize whitespace and case for exact allowlist comparison."""
    if not isinstance(value, str):
        return None

    normalized = " ".join(value.strip().split())
    return normalized.casefold() or None


def _get_command(event):
    """
    Prefer a non-blank structured command.
    Fall back to COMMAND= in event_text when needed.

    This extracts text from logs; it does not perform shell parsing.
    """
    structured = _normalize_command(event.get("command"))

    if structured is not None:
        return structured

    text = event.get("event_text", "")

    if not isinstance(text, str):
        return None

    match = re.search(r"(?:^|\s)COMMAND=(.*)", text)

    if not match:
        return None

    return _normalize_command(match.group(1))


def should_alert(
    events,
    baseline=4,
    window_minutes=60,
    approved_commands=None,
):
    """
    Detect repeated sudo authentication failures followed by an
    unapproved successful sudo command.

    Detection rules:
    - Events are evaluated separately for each account.
    - More than `baseline` distinct failure events must occur within
      a window of `window_minutes`.
    - The suspicious successful command must occur strictly after
      the (baseline + 1)th failure in that window.
    - The suspicious command must occur no later than the window end.
    - Window start and end timestamps are inclusive for failures.
    - At most one alert is returned per account.

    Timestamp convention:
    - ISO-8601 timestamps are required.
    - Timestamps without timezone information are interpreted as UTC.
    - Invalid or missing timestamps raise ValueError.

    Command matching:
    - An explicit approved_commands collection is required.
    - Commands are compared as complete normalized strings.
    - Matching is case-insensitive and whitespace-normalized.
    - This is not shell-aware command parsing.

    Duplicate events:
    - Identical event dictionaries are counted only once.
    - Events that differ in any field are treated as distinct events.
    """
    if (
        not isinstance(baseline, int)
        or isinstance(baseline, bool)
        or baseline < 0
    ):
        raise ValueError("baseline must be a non-negative integer")

    if (
        not isinstance(window_minutes, int)
        or isinstance(window_minutes, bool)
        or window_minutes <= 0
    ):
        raise ValueError("window_minutes must be a positive integer")

    if approved_commands is None:
        raise ValueError(
            "Provide an explicit approved_commands collection"
        )

    if isinstance(approved_commands, (str, bytes)):
        raise ValueError(
            "approved_commands must be a collection of command strings"
        )

    try:
        approved = {
            normalized
            for command in approved_commands
            if (normalized := _normalize_command(command)) is not None
        }
    except TypeError as exc:
        raise ValueError(
            "approved_commands must be an iterable of command strings"
        ) from exc

    # Validate, normalize and deduplicate events.
    prepared = []
    seen = set()

    for event in events:
        if not isinstance(event, dict):
            raise ValueError("Each event must be a dictionary")

        account = event.get("account")

        if not isinstance(account, str) or not account.strip():
            continue

        timestamp = _parse_timestamp(event.get("timestamp"))

        # Use a stable representation to avoid counting exact duplicate
        # event dictionaries more than once.
        try:
            fingerprint = (
                tuple(sorted(event.items())),
                timestamp,
            )
            hash(fingerprint)
        except (TypeError, ValueError):
            # Events with nested or unhashable values still need a
            # safe deduplication strategy.
            fingerprint = None

        if fingerprint is not None:
            if fingerprint in seen:
                continue
            seen.add(fingerprint)

        prepared.append(
            {
                **event,
                "account": account,
                "_time": timestamp,
                "_process": str(event.get("process", "")).casefold(),
                "_outcome": str(event.get("outcome", "")).casefold(),
                "_command": _get_command(event),
            }
        )

    alerts = []
    window = timedelta(minutes=window_minutes)

    accounts = sorted(
        {event["account"] for event in prepared}
    )

    for account in accounts:
        account_events = sorted(
            (
                event
                for event in prepared
                if event["account"] == account
                and event["_process"] == "sudo"
            ),
            key=lambda event: event["_time"],
        )

        failures = [
            event
            for event in account_events
            if event["_outcome"] == "failure"
        ]

        successes = [
            event
            for event in account_events
            if event["_outcome"] == "success"
        ]

        # Check candidate windows in chronological order.
        for left, start_event in enumerate(failures):
            start = start_event["_time"]
            end = start + window

            window_failures = [
                event
                for event in failures[left:]
                if event["_time"] <= end
            ]

            failure_count = len(window_failures)

            if failure_count <= baseline:
                continue

            # The command must follow the failure that crosses the
            # threshold, not merely occur somewhere in the window.
            threshold_failure = window_failures[baseline]
            threshold_time = threshold_failure["_time"]

            suspicious = next(
                (
                    event
                    for event in successes
                    if threshold_time < event["_time"] <= end
                    and event["_command"] is not None
                    and event["_command"] not in approved
                ),
                None,
            )

            if suspicious is None:
                continue

            # Count only failures that occurred before the suspicious success.
            failure_count = sum(
                event["_time"] < suspicious["_time"]
                for event in window_failures
            )
            if failure_count <= baseline:
                continue

            alerts.append(
                {
                    "account": account,
                    "failure_count": failure_count,
                    "window_start": start.isoformat(),
                    "window_end": end.isoformat(),
                    "command": suspicious["_command"],
                    "reason": (
                        "Repeated sudo authentication failures "
                        "followed by an unapproved successful sudo "
                        "command within the same time window"
                    ),
                }
            )

            # Return only the earliest qualifying alert per account.
            break

    return alerts
