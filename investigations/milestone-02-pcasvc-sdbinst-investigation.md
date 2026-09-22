# Milestone 02 — PcaSvc / sdbinst.exe Investigation

## 1. Investigation Objective

Investigate observed `sdbinst.exe` executions on the Windows-SOC-Lab endpoint and determine whether the activity can be attributed to the Program Compatibility Assistant Service (PcaSvc), Windows Update, or potentially malicious activity.

The investigation focuses on identifying the execution context, parent process, related Windows events, and available Wazuh/Sysmon telemetry.

## 2. Environment

- Endpoint: Windows-SOC-Lab
- Operating System: Windows 11 Pro
- Wazuh Agent ID: 001
- Wazuh Agent Version: 4.14.7
- Monitoring Platform: Wazuh
- Process Telemetry: Sysmon
- Investigation Type: Host-based process and event correlation

## 3. Investigation Scope

Primary investigation window:

`2026-09-21 01:35:00 – 01:50:00`

Additional Sysmon and Wazuh telemetry from September 22 was examined to determine whether the observed `sdbinst.exe` behavior was repeated and consistent.

## 4. Confirmed sdbinst.exe Activity

Wazuh Sysmon telemetry recorded multiple executions of:

`C:\Windows\System32\sdbinst.exe`

The observed command line was:

`sdbinst.exe -m -bg`

The process executed under:

- User: `NT AUTHORITY\SYSTEM`
- Logon ID: `0x3E7`
- Integrity Level: `System`
- Terminal Session ID: `0`

The executable metadata identified it as:

- Description: Application Compatibility Database Installer
- Product: Microsoft Windows Operating System
- Company: Microsoft Corporation
- Original Filename: `sdbinst.exe`
- File Version: `10.0.26100.9278`

Observed SHA-256:

`8F67CBBDB8250CEDA1E5DB21DF87AD870576229B8FD729E80F9092EB578B6915`

The executable was located in the expected Windows System32 directory.

## 5. Repeated Executions

Three Sysmon Event ID 1 process creation records were identified on September 22:

| UTC Time | Process ID |
|---|---:|
| 2026-09-22 05:21:51.836 | 13124 |
| 2026-09-22 06:30:21.834 | 23308 |
| 2026-09-22 07:34:33.092 | 6660 |

All three executions used the same executable path, command line, SYSTEM context, and SHA-256 hash.

This establishes that the activity was repeated and consistent rather than being a single isolated execution.

## 6. Parent-Process Investigation

The Sysmon records contained:

- Parent Process ID: `10256`
- Parent Image: unavailable
- Parent Command Line: unavailable
- Parent User: unavailable
- Parent Process GUID: all zeros

A search of available Wazuh alerts for process ID `10256` and related process identifiers did not identify a corresponding parent process creation event.

Therefore, the available telemetry does not establish which process directly launched the observed `sdbinst.exe` instances.

Although PcaSvc was previously observed in connection with the investigation, the available Sysmon records do not provide sufficient parent-process evidence to attribute these specific executions directly to PcaSvc.

## 7. Wazuh Archive Investigation

Wazuh archive telemetry was searched for:

- `PcaSvc`
- `Program Compatibility Assistant`
- `sdbinst.exe`

No matching records were found in the available Wazuh archive log.

This limits retrospective reconstruction of the complete process chain.

## 8. Windows System Log Investigation

The Windows System log was queried for the original investigation window:

`2026-09-21 01:35:00 – 01:50:00`

The search targeted:

- PcaSvc
- Program Compatibility Assistant
- Service Control Manager

No matching events were returned.

Therefore, the System log does not provide supporting evidence connecting PcaSvc to the activity during the specified window.

## 9. Windows Update Correlation

Windows Update Operational events were examined for the same investigation period.

No Windows Update events were found between:

`2026-09-21 01:40:00 – 01:48:00`

Therefore, the available telemetry does not establish a causal relationship between Windows Update activity and the `sdbinst.exe` execution observed during the investigation.

Later Windows Update activity observed after the investigation window was not treated as evidence of causation.

## 10. Security Event 4688 Investigation

Windows Security Event ID 4688 process-creation telemetry was searched for `sdbinst.exe` between:

`2026-09-21 00:00:00 – 03:00:00`

No matching Event ID 4688 record was found.

This indicates that a corresponding Security process-creation event was not available for the examined period.

## 11. Program Compatibility Assistant Log

The following Windows logs were examined for available PCA-related telemetry:

- `Microsoft-Windows-Application-Experience/Program-Compatibility-Assistant`
- `Microsoft-Windows-Application-Experience/Program-Compatibility-Troubleshooter`
- `Microsoft-Windows-Program-Compatibility-Assistant/CompatAfterUpgrade`
- `Microsoft-Windows-Program-Compatibility-Assistant/Analytic`
- `Microsoft-Windows-Kernel-ApphelpCache/Operational`

The Program Compatibility Assistant log was enabled and contained historical records, but no events matching the original investigation window were returned.

The PCA Analytic log was disabled, limiting the amount of detailed diagnostic telemetry available.

## 12. Evidence Assessment

### Confirmed

- `sdbinst.exe` executed multiple times.
- The executable was located at `C:\Windows\System32\sdbinst.exe`.
- The executable identified itself as Microsoft's Application Compatibility Database Installer.
- All observed executions used the same SHA-256 hash.
- All observed executions ran under `NT AUTHORITY\SYSTEM`.
- The command line was consistently `sdbinst.exe -m -bg`.
- Wazuh successfully collected Sysmon process-creation telemetry.

### Not Confirmed

- The specific observed executions were directly launched by PcaSvc.
- Windows Update caused the observed executions.
- The activity was malicious.
- The parent process associated with PID `10256`.

## 13. SOC Analyst Conclusion

The investigation confirms repeated execution of the legitimate Windows `sdbinst.exe` binary in a SYSTEM context with a consistent command line and hash.

However, the available telemetry does not provide sufficient evidence to establish the parent process for the observed executions. The parent PID recorded by Sysmon (`10256`) could not be correlated with a corresponding process-creation event in the available Wazuh telemetry.

No supporting PcaSvc, Windows Update, Security 4688, or Windows System log evidence was found for the original investigation window.

Accordingly, the activity should be documented as:

**Observed and investigated, but not attributed to PcaSvc, Windows Update, or malicious activity based on the available telemetry.**

The investigation demonstrates the importance of preserving complete process ancestry and correlating multiple telemetry sources before assigning attribution.

## 14. Detection and Monitoring Recommendations

1. Continue collecting Sysmon Event ID 1 process-creation events.
2. Ensure parent process fields and process GUIDs are retained by the monitoring pipeline.
3. Enable and retain Windows Security Event ID 4688 where appropriate.
4. Increase retention for Wazuh archives so historical process chains can be reconstructed.
5. Monitor unusual executions of `sdbinst.exe`, especially from unexpected paths or with unusual command-line arguments.
6. Correlate process creation with Windows Update, Application Experience, and PCA telemetry.
7. Preserve SHA-256 hashes for process investigations.
8. Build baseline behavior for legitimate Windows compatibility processes.
9. Investigate deviations from the known `System32\sdbinst.exe -m -bg` execution pattern.

## 15. Investigation Limitations

The investigation was limited by the telemetry available on the endpoint and in Wazuh.

The primary limitation was the absence of usable parent-process metadata for the observed `sdbinst.exe` events. The parent PID was recorded, but a corresponding process creation event could not be located.

Additionally, the Windows Security Event 4688 search did not return a matching record, and the relevant PCA logs contained no events for the original time window.

These limitations prevent definitive reconstruction of the original process chain.

## 16. Key SOC Lesson

A security investigation should distinguish between:

1. What the telemetry proves.
2. What the telemetry suggests.
3. What cannot be established from the available evidence.

In this case, the telemetry proves repeated execution of `sdbinst.exe`, but it does not prove that PcaSvc or Windows Update initiated those executions.

Documenting that uncertainty is preferable to forcing an attribution that the evidence cannot support.
