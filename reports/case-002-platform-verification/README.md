# Case 002: Wazuh Platform and Endpoint Verification

## Scope

Read-only health verification of the owner's local Ubuntu WSL2 Wazuh platform
and Windows endpoint on 2026-09-21.

## Observations

- Ubuntu WSL2 was running with systemd.
- Wazuh manager, indexer, dashboard, and Filebeat unit files were present.
- Expected Wazuh and Filebeat processes were observed.
- The Wazuh manager journal showed successful component startup on 2026-09-21.
- Windows `WazuhSvc` was Running and configured for Automatic startup.

## Conclusion

The local platform components and endpoint service were healthy enough to
justify further authorized telemetry validation. This case does not establish
agent enrollment or end-to-end event ingestion because protected logs and
registered-agent status could not be read by the assessment account.
