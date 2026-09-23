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

| Component | Environment |
|---|---|
| Host OS | Windows 11 Pro |
| Linux environment | Ubuntu WSL2 |
| Security platform | Wazuh |
| Windows endpoint | Windows 11 Pro |
| Wazuh Agent | 001 - Windows-SOC-Lab |
| Wazuh version | 4.14.7 on Windows agent |
| Manager | Ubuntu WSL2 |
| Indexer | Wazuh/OpenSearch |
| Dashboard | Wazuh Dashboard |
| Filebeat | Wazuh Filebeat |
| Detection logic | Python |
| Test framework | Python unittest |
| Version control | Git / GitHub |

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
```
