# Lab 04: Services and systemd Investigation

## Objective

Investigate Linux services and systemd units from a SOC analyst perspective using safe, read-only commands.

## Scope

- Identify currently running services.
- Identify failed services.
- Review enabled service units.
- Review recent service startup and failure activity.
- Inspect Wazuh service health.
- Document operational warnings separately from security findings.

## Safety Boundaries

- Do not start, stop, restart, enable, or disable any service.
- Do not modify service configuration files.
- Do not change systemd settings.
- Use read-only commands only.
- Treat warnings and failed services as investigation leads, not proof of malicious activity.

## Environment

- Operating System: Ubuntu under WSL2
- Investigation Type: Local service and systemd analysis
- Approach: Read-only SOC investigation

## Investigation Questions

1. Which services are currently running?
2. Are any services currently failed?
3. Which service units are enabled?
4. What services started recently?
5. Are there service errors or warnings requiring investigation?
6. Are the core Wazuh services healthy?

## Evidence Collection

Evidence was collected using read-only systemd and journalctl commands.

## Findings

The detailed findings are documented below.

## Conclusion

The lab demonstrates an evidence-first approach to Linux service and systemd investigation without modifying the monitored environment.

## Evidence Collected

### Running Services

Command:

`systemctl --no-pager --type=service --state=running`

Result: 17 loaded service units were running.

Relevant services included:

- `filebeat.service`
- `rsyslog.service`
- `systemd-journald.service`
- `systemd-logind.service`
- `systemd-resolved.service`
- `systemd-timesyncd.service`
- `unattended-upgrades.service`
- `wazuh-dashboard.service`
- `wazuh-indexer.service`
- `wazuh-manager.service`
- `wsl-pro.service`

### Failed Services

Command:

`systemctl --no-pager --failed`

Result:

`0 loaded units listed.`

No failed systemd service units were reported during the investigation.

### Enabled Services

Command:

`systemctl --no-pager list-unit-files --type=service --state=enabled`

The enabled service inventory included the Wazuh stack:

- `filebeat.service`
- `wazuh-dashboard.service`
- `wazuh-indexer.service`
- `wazuh-manager.service`

Other enabled units included standard Ubuntu services such as AppArmor, cron, rsyslog, systemd-resolved, systemd-timesyncd, and unattended-upgrades.

An enabled service is not, by itself, evidence of suspicious activity.

### Recent Service Activity

Recent journal activity showed coordinated service startup around:

`2026-09-22 13:16 UTC`

Services and components starting during this period included Filebeat, Wazuh Dashboard, Wazuh Manager components, Wazuh Indexer, rsyslog, systemd-logind, getty, unattended-upgrades, wsl-pro, and snapd.

The timing and grouping were consistent with Ubuntu/WSL startup and Wazuh initialization.

A systemd-journald warning was also observed indicating that a user journal file could not immediately be read for rotation because the resource was busy.

This was documented as an operational warning, not as evidence of malicious activity.

### Wazuh Service Error Check

Command:

`journalctl --no-pager --since "24 hours ago" -p err..alert -u filebeat.service -u wazuh-manager.service -u wazuh-indexer.service -u wazuh-dashboard.service`

Result:

`-- No entries --`

No error-to-alert priority journal entries were returned for the four queried Wazuh services during the selected period.

### Wazuh Service Health

The following services were verified as active and running:

| Service | Active State | Sub-State | Enabled |
| --- | --- | --- | --- |
| Filebeat | active | running | yes |
| Wazuh Manager | active | running | yes |
| Wazuh Indexer | active | running | yes |
| Wazuh Dashboard | active | running | yes |

The Wazuh Manager completed startup successfully.

The Wazuh Indexer produced Java/OpenSearch deprecation warnings during startup. These warnings did not result in a failed service state.

The Wazuh Dashboard completed its initialization and was listening on port 443.

## Findings

### Finding 1 — No Failed Services

No failed systemd service units were reported.

**Assessment:** Normal service state at the time of collection.

### Finding 2 — Wazuh Stack Operational

Filebeat, Wazuh Manager, Wazuh Indexer, and Wazuh Dashboard were all active and running.

**Assessment:** The local Wazuh monitoring stack was operational at the time of collection.

### Finding 3 — Coordinated Startup Activity

Multiple Ubuntu, WSL, and Wazuh services started within a short period around `2026-09-22 13:16 UTC`.

**Assessment:** Consistent with system/WSL startup and Wazuh initialization. No suspicious service behavior was established from this evidence.

### Finding 4 — Journal Rotation Warning

systemd-journald reported that a user journal file could not immediately be read for rotation because the resource was busy.

**Assessment:** Operational warning. Additional investigation would be required before assigning security significance.

### Finding 5 — Indexer Startup Warnings

The Wazuh Indexer produced Java/OpenSearch deprecation warnings during startup.

**Assessment:** Compatibility/deprecation warnings rather than evidence of a failed or malicious service.

## SOC Interpretation

This investigation demonstrates the distinction between service health and security detection.

A service being active, enabled, or recently started does not automatically make it suspicious. Likewise, a warning should be investigated in context rather than treated as proof of compromise.

Useful correlation sources for deeper investigations include:

- systemd journal entries
- process creation telemetry
- authentication logs
- package installation history
- service unit configuration
- Wazuh alerts
- endpoint telemetry

## Limitations

- This investigation represents the local WSL environment at the time of collection.
- Service state can change after collection.
- Journal history is limited by available log retention.
- Service startup timing alone cannot establish malicious behavior.
- No malicious service attribution was established from this lab.

## Conclusion

The investigation confirmed that the Ubuntu WSL2 environment had no currently failed systemd services and that the core Wazuh monitoring stack was active and running.

Recent service activity was consistent with system/WSL startup and Wazuh initialization. Operational warnings were documented separately from security findings.

This lab demonstrates a repeatable, evidence-first method for investigating Linux service health without modifying the monitored environment.
