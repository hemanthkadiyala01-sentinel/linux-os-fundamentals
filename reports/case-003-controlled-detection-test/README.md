# Case 003: Controlled Detection Test - Documented Telemetry Verification

No adversarial or simulated security event was executed. A naturally occurring benign Windows Application event was used to verify endpoint telemetry ingestion into Wazuh.

## Telemetry Verification

On 2026-09-22, Windows Application Event ID 16384 from Microsoft-Windows-Security-SPP was observed on the Windows endpoint and subsequently confirmed in the Wazuh alert log.

Observed event:

- Provider: Microsoft-Windows-Security-SPP
- Event ID: 16384
- Channel: Application
- Event time: 2026-09-22T13:44:23.9620851Z
- Event record ID: 86357
- Computer: bunnydevice
- Severity: Information
- Event description: Software Protection scheduled a service restart.
- Wazuh evidence: /var/ossec/logs/alerts/alerts.log

The event was confirmed in the Wazuh alert log with the Windows provider, event ID, timestamp, channel, computer name, and event data preserved. This verifies that Windows Application telemetry from the endpoint is being collected and recorded by Wazuh.

## Evidence Boundary

The available evidence verifies:

1. The Windows Application event existed on the endpoint.
2. The event was received and recorded by Wazuh.
3. The event data was present in /var/ossec/logs/alerts/alerts.log.

The following was not independently verified:

- Wazuh indexer visibility for this specific event.
- Wazuh dashboard visibility for this specific event.
- A dedicated detection rule or security alert triggered by this event.

Therefore, this case does not claim complete endpoint-to-dashboard detection. It documents verified endpoint-to-Wazuh telemetry ingestion and the remaining validation boundary.

## Test Safety

No adversarial payload, malicious activity, or external system was used. The evidence came from a naturally occurring benign Windows Application event.

For any future controlled detection test, document the owner approval, benign test action, target file or event, expected telemetry, collection window, endpoint evidence, manager-side evidence, dashboard or indexer evidence, result, and cleanup procedure before execution.
