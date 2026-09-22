# Lab 04: Services and systemd Investigation

## Objective

Learn how to investigate Linux services and systemd units from a SOC analyst perspective using safe, read-only commands.

## Scope

- Identify active and inactive services.
- Inspect systemd service states.
- Review service configuration and recent logs.
- Identify failed services and suspicious behavior.
- Document observations without modifying system services.

## Safety Boundaries

- Do not start, stop, restart, enable, or disable any service.
- Do not modify service configuration files.
- Do not change systemd settings.
- Use read-only commands only.
- Treat failed services as investigation leads, not proof of malicious activity.

## Environment

- Operating System: Ubuntu running under WSL2
- Investigation Type: Local service and systemd analysis
- Approach: Read-only SOC investigation

## Investigation Questions

1. Which services are currently active?
2. Which services have failed?
3. Which services started recently?
4. Are there unusual service names or descriptions?
5. Do service logs show errors or unexpected activity?

## Evidence Collection

Results and observations will be recorded during the practical investigation.

## Findings

To be completed after command execution.

## Conclusion

This lab develops foundational skills for investigating Linux service health and systemd activity in a defensive cybersecurity environment.
