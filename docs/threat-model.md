# Threat Model

## Defensive questions

| Scenario | Useful telemetry | Analyst caution |
| --- | --- | --- |
| Account misuse | Authentication outcomes, session records, sudo records | A PAM failure may be a mistyped local sudo password, not an attack. |
| Service disruption or tampering | Unit state, process tree, service journal | A failed unit is a lead; confirm expected maintenance first. |
| Endpoint visibility loss | Agent service state, agent log, manager registration | Service-running status alone does not prove delivery. |

The project intentionally avoids offensive execution. It is designed to improve
the quality and restraint of defensive decisions.
