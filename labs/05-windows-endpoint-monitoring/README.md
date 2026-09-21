# Lab 05: Windows Endpoint Monitoring Verification

## Objective

Confirm the local Wazuh endpoint service without changing it.

## Verified observation

On 2026-09-21, `Get-Service Wazuh*` reported `WazuhSvc` as **Running** with an
**Automatic** start type. The local agent installation directory and state files
were present.

## Reproduce

```powershell
Get-Service -Name 'Wazuh*' | Select-Object Name, DisplayName, Status, StartType
Get-Item 'C:\Program Files (x86)\ossec-agent\wazuh-agent.state'
```

## Manager-side verification

An authorized manager query on 2026-09-21 confirmed agent `001` as **Active**. It identified the endpoint as Windows 11 Pro running Wazuh 4.14.7 and showed a recent completed file-integrity-monitoring scan. IP addresses, hashes, and raw log lines are intentionally not committed.

## Limitation

The regular Windows account could not read the protected agent log. Manager connectivity is verified, but a new controlled event has not yet been confirmed in the Wazuh dashboard.
