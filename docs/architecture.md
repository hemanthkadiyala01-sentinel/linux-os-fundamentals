# Architecture and Data Boundaries

## Components

```text
Windows endpoint (WazuhSvc) --[agent telemetry]--> Wazuh manager (Ubuntu WSL2)
Ubuntu local logs -------------------------------> analyst read-only review
Wazuh manager --> indexer --> dashboard
Filebeat ----------------------------------------> indexer
```

On 2026-09-21, the Windows Wazuh service was Running/Automatic and the Ubuntu
host had live Wazuh manager, indexer, dashboard, and Filebeat processes. This
is component-health evidence only. End-to-end Windows event ingestion was not
verified because protected manager and agent logs were unavailable to the
current account.

## Data minimization

- Collect only the fields needed for a stated hunt: time, host, account,
  process/service, event type, and outcome.
- Do not commit raw logs, IP addresses, host credentials, enrollment keys, or
  personally identifying command history.
- Store collection output in ignored `evidence/` and redact before sharing.
- Keep each conclusion tied to a source and an observation window.
