# Linux Process Investigation Lab

## Objective
Investigate Linux processes, process relationships, and process metadata.

## Tools Used
- ps
- pstree
- /proc filesystem
- grep

## Investigation Findings

### 1. Wazuh Monitoring Processes
Identified running security-monitoring processes:
- filebeat
- wazuh-analysisd
- wazuh-syscheckd
- wazuh-remoted
- wazuh-logcollector
- wazuh-modulesd
- rsyslogd

### 2. Wazuh API Process
- PID: 722
- Process: python3
- Parent PID: 1
- State: Sleeping
- Threads: 14
- TracerPid: 0

### 3. Process Tree
The Wazuh Python process had child processes:
- PID 723
- PID 724
- PID 727
- PID 733

Additional Python threads were visible in the process tree.

### 4. Process Command Line
Executable:
`/var/ossec/framework/python/bin/python3`

Script:
`/var/ossec/api/scripts/wazuh_apid.py`

## Security Relevance
Process investigation helps analysts identify running services, understand parent-child relationships, inspect process metadata, and investigate unexpected activity.

## Conclusion
The investigation demonstrated Linux process enumeration, process hierarchy analysis, status inspection, thread identification, and command-line inspection using the `/proc` filesystem.
