# Linux & Windows Security Monitoring Lab

An evidence-first cybersecurity engineering lab focused on Linux administration, Windows endpoint monitoring, Wazuh-based telemetry collection, threat hunting, incident investigation, and tested detection logic.

This project documents hands-on security investigations performed in an authorized local lab using Ubuntu WSL2, Windows 11, and Wazuh.

---

## Project Overview

This repository is a practical security engineering and investigation environment built to develop and demonstrate skills in:

- Linux process and system investigation
- Linux file permissions and access control
- Users, groups, UID/GID, and privilege boundaries
- Authentication and log analysis
- systemd service investigation
- Windows endpoint monitoring
- Wazuh agent and manager validation
- Security telemetry verification
- Threat hunting
- Endpoint investigation
- Detection engineering
- Evidence-driven incident analysis
- Security documentation and investigation reporting

The project follows an evidence-first principle:

> Collect evidence → validate observations → document findings → state limitations → avoid unsupported conclusions.

The goal is not to manufacture malicious activity or overstate findings. The goal is to demonstrate how a security analyst investigates what the available telemetry actually supports.

---

## What I Demonstrated

This project demonstrates an evidence-first security monitoring and investigation workflow across Linux and Windows environments.

### Endpoint Visibility

- Linux system and process investigation
- Windows endpoint monitoring
- Wazuh agent and manager validation
- Security telemetry collection and verification
- Operating-system logs and endpoint data analysis

### Security Investigation

- Authentication and log analysis
- Process and service investigation
- Windows endpoint investigation
- Evidence collection and preservation
- Correlation of related security observations
- Threat-hunting methodology
- Documentation of investigation findings and limitations

### Detection Engineering

- Translation of a documented detection concept into Python logic
- Separation of detection logic from production-deployment claims
- Testing of expected detection conditions
- Testing of conditions that should not trigger detection
- Repository and detection validation

The project connects these activities into a single workflow:

> Collect telemetry → preserve evidence → investigate → document findings → create detection logic → test the detection.

---

## Project Objectives

The project was designed to build practical capability across three connected areas:

### 1. Endpoint Visibility

Establish visibility into Linux and Windows systems through operating-system telemetry and Wazuh.

### 2. Security Investigation

Use logs, process information, service state, authentication records, and endpoint telemetry to investigate suspicious or security-relevant activity.

### 3. Detection Engineering

Translate a documented detection concept into tested Python logic while keeping the implementation separate from claims about a production Wazuh deployment.

---

## Lab Environment

| Component         | Environment             |
| ----------------- | ----------------------- |
| Host OS           | Windows 11 Pro          |
| Linux environment | Ubuntu WSL2             |
| Security platform | Wazuh                   |
| Windows endpoint  | Windows 11 Pro          |
| Wazuh Agent       | 001 - Windows-SOC-Lab   |
| Wazuh version     | 4.14.7 on Windows agent |
| Manager           | Ubuntu WSL2             |
| Indexer           | Wazuh/OpenSearch        |
| Dashboard         | Wazuh Dashboard         |
| Filebeat          | Wazuh Filebeat          |
| Detection logic   | Python                  |
| Test framework    | Python unittest         |
| Version control   | Git / GitHub            |

This is a local authorized laboratory environment and is not presented as a production SOC deployment.

---

## Architecture

```text
                    Windows 11 Endpoint
                    -------------------
                    Wazuh Agent 001
                           |
                           | Security telemetry
                           v
                    Ubuntu WSL2
                    ------------
                    Wazuh Manager
                           |
             +-------------+-------------+
             |                           |
             v                           v
       Wazuh Indexer              Wazuh Dashboard
             |
             v
          Filebeat

Additional investigation sources:

Linux
  |
  +-- ps / pstree
  +-- /proc
  +-- systemd
  +-- auth.log
  +-- journald
  +-- users / groups / permissions

Windows
  |
  +-- Event Logs
  +-- Sysmon
  +-- Wazuh Agent
  +-- File Integrity Monitoring
---

## Final Project Status

**Status: COMPLETE**

The Linux OS Fundamentals & Defensive Security Lab has completed its initial implementation and investigation phase.

The project established a working Wazuh-based endpoint monitoring environment and validated Windows endpoint telemetry through an authorized local SOC lab.

The final investigation examined an observed PcaSvc -> sdbinst.exe execution and attempted to correlate the activity with Windows Update telemetry. No Windows Update Operational events were present during the investigated 01:43-01:45 window on September 21, 2026. Security Event ID 4688 was also unavailable because Windows Process Creation auditing was disabled.

Therefore, a direct Windows Update correlation could not be established. The project records this as an evidence-bounded finding rather than making an unsupported attribution.

### Final Milestones

- [x] Linux / WSL2 environment established
- [x] Wazuh Manager deployed
- [x] Wazuh Indexer deployed
- [x] Wazuh Dashboard deployed
- [x] Windows 11 endpoint connected
- [x] Wazuh Windows Agent validated
- [x] Endpoint telemetry pipeline validated
- [x] SOC investigation performed
- [x] PcaSvc -> sdbinst.exe activity investigated
- [x] Windows Update correlation attempted
- [x] Evidence limitations identified
- [x] Final investigation conclusion documented
- [x] Project phase completed

### Final Investigation

See:

investigations/2026-09-21-pcasvc-sdbinst-investigation.md

**Final status: COMPLETE**

