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

## Limitation

The agent log was protected from the account used for this assessment. Do not
claim enrollment or manager delivery until an authorized administrator confirms
both the endpoint log and manager registration.
