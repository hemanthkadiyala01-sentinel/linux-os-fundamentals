# Synthetic Authentication Samples

These JSONL files contain fabricated events for testing the
repository's sudo authentication detection logic.

## Files

- `benign.jsonl`: Three failures followed by an unapproved command.
  The failure threshold is not exceeded, so no alert is expected.
- `suspicious-sequence.jsonl`: Five failures followed by an
  unapproved successful command within the configured time window.
  One alert is expected.

## Safety and limitations

These records are synthetic and do not represent real users or
production telemetry. The detector demonstrates a rule-based
scenario; an alert is not proof of compromise.

The approved-command list is configured in the demo script.
Command matching is normalized string matching, not shell parsing.
