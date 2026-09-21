# Lab 06: Three Evidence-First Threat Hunts

## Hunt 1 — Authentication anomalies

Question: Is retained Ubuntu authentication telemetry inconsistent with the
baseline? Source: `/var/log/auth.log`, `wtmp`, and `btmp`. The 2026-09-21
baseline had 0 `Failed password`, 4 PAM authentication failures, 0 `Accepted
password`, and 240 `sudo` events. Review the full line before interpreting a
PAM failure.

## Hunt 2 — Wazuh service integrity

Question: Are the expected Wazuh components present and running? Source:
`systemctl`, process inventory, and service journal. The manager, indexer,
dashboard, and Filebeat processes were observed. Investigate unexpected
component absence, repeated restarts, or a previously unseen unit; do not infer
compromise from a single failure.

## Hunt 3 — Windows endpoint visibility

Question: Is the endpoint agent able to provide monitoring coverage? Source:
Windows service state, agent-state timestamp, agent log, and manager agent
status. An authorized manager query confirmed agent `001` as Active and showed a recent completed FIM scan. Treat this as manager-connectivity evidence; a new controlled event must still be confirmed in the dashboard before claiming full end-to-end detection coverage.
