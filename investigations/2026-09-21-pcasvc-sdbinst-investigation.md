# PcaSvc → sdbinst.exe Investigation

**Project:** Linux OS Fundamentals & Defensive Security Lab  
**Investigation Date:** September 21, 2026  
**Status:** COMPLETE  
**Environment:** Windows 11 endpoint monitored by Wazuh  
**Investigation Type:** Endpoint telemetry correlation

---

## 1. Objective

Investigate an observed execution of `sdbinst.exe` associated with the Windows `PcaSvc` service and determine whether the available endpoint telemetry supports a correlation with Windows Update activity.

The investigation was performed against the local authorized SOC lab environment.

---

## 2. Environment

The investigation environment consisted of:

- Windows 11 endpoint
- Wazuh Windows Agent
- Wazuh Manager
- Wazuh Indexer
- Wazuh Dashboard
- Windows Event Logs
- PowerShell
- Windows Update Operational logging

The Wazuh endpoint telemetry pipeline had previously been validated as operational.

---

## 3. Initial Observation

Previous investigation activity established an observed relationship between:

    PcaSvc
       |
       +----> sdbinst.exe

`PcaSvc` is the Windows Program Compatibility Assistant Service.

`sdbinst.exe` is the Microsoft System Compatibility Assistant command-line utility.

The presence of the execution was treated as an observation requiring contextual investigation rather than automatically classified as malicious.

---

## 4. Windows Update Correlation

The investigation initially targeted Windows Update activity around:

    2026-09-21 01:43–01:45

The Windows Update Operational log was verified to exist and remain enabled.

Observed configuration:

    Log:
    Microsoft-Windows-WindowsUpdateClient/Operational

    Enabled:
    True

    Record count:
    2137

A targeted query covering approximately 01:40–01:48 returned no events.

The investigation was subsequently expanded to the entire September 21, 2026 period.

Windows Update activity was present elsewhere during the day, including:

- 10:28:52 — Windows Update found 1 update
- 10:36:10 — update search/download activity
- 14:33:51–14:33:58 — update download activity
- 14:50–14:57 — multiple update searches/downloads

However, **no Windows Update Operational events were recorded around the previously investigated 01:43–01:45 period.**

---

## 5. Security Event 4688 Investigation

Security Event ID 4688 was queried for process creation involving:

    sdbinst.exe

No matching Event ID 4688 records were found for the relevant period or for the September 21 investigation window.

The Windows audit policy was then checked.

Result:

    Category/Subcategory
    Detailed Tracking
        Process Creation    No Auditing

Therefore, the absence of Event ID 4688 cannot be interpreted as proof that the process did not execute.

Process Creation auditing was disabled, meaning Windows was not configured to generate the expected Security 4688 process-creation records during this investigation period.

---

## 6. Evidence Assessment

| Evidence source | Result |
|---|---|
| Wazuh Windows agent | Confirmed operational |
| Windows endpoint telemetry | Available |
| PcaSvc → sdbinst.exe observation | Confirmed through previously collected telemetry |
| Windows Update Operational log | Enabled and populated |
| Windows Update events at 01:43–01:45 | Not observed |
| Windows Update activity elsewhere on Sept. 21 | Observed |
| Security Event 4688 for sdbinst.exe | Not available |
| Process Creation auditing | Disabled |
| Direct Windows Update → sdbinst.exe correlation | Not established |

---

## 7. Investigation Conclusion

The investigation confirmed that the endpoint telemetry contained an observed `PcaSvc → sdbinst.exe` execution.

The available Windows Update Operational logs did not contain Windows Update events during the previously investigated 01:43–01:45 window. Therefore, the available evidence does **not** establish that Windows Update caused or directly triggered the observed `sdbinst.exe` execution.

Security Event ID 4688 could not provide additional historical process-creation evidence because Windows Process Creation auditing was disabled.

The correct evidence-based conclusion is therefore:

> **A direct Windows Update correlation could not be established from the available telemetry.**

No unsupported attribution of malicious activity was made.

---

## 8. Evidence Limitations

The investigation had the following limitations:

1. Security Event ID 4688 was unavailable because Process Creation auditing was disabled.
2. Windows Update Operational events were not present in the targeted 01:43–01:45 window.
3. Historical telemetry cannot be reconstructed after the fact when the relevant logging was not enabled or retained.
4. The absence of a Windows Update event does not prove that no underlying system activity occurred.
5. The investigation therefore remains bounded by the telemetry that was actually available.

---

## 9. Lessons Learned

This investigation demonstrated several practical SOC principles:

- Telemetry availability is critical to incident reconstruction.
- Absence of an event is not necessarily evidence that an action did not occur.
- Process creation auditing should be enabled when process-level investigations are required.
- Correlation should be based on timestamps and independent evidence sources.
- Suspicious-looking process activity should not automatically be classified as malicious.
- Investigation conclusions must distinguish confirmed observations from unconfirmed hypotheses.
- Evidence limitations should be documented explicitly.

---

## 10. Recommended Future Lab Configuration

For future investigations, enable appropriate process-creation auditing before testing or generating new telemetry.

Where appropriate, future lab exercises should also correlate:

    Process Creation
           +
    Parent/Child Process Relationship
           +
    Windows Services
           +
    Windows Update
           +
    Sysmon
           +
    Wazuh

This will provide a stronger basis for future detection engineering and threat-hunting exercises.

---

## 11. Final Project Status

### LAB SETUP: COMPLETE

The defensive security lab infrastructure was successfully established and validated.

The investigation milestone was completed with an evidence-bounded conclusion.

The inability to establish a Windows Update correlation is itself a valid investigation result and is documented as such.

**Final status: COMPLETE**
