# Lab 07: Detection Engineering Proposal

## Proposed rule: unusual sudo authentication failures

Trigger an investigation when local `sudo:auth` failures exceed the established
baseline for a user over a defined time window, particularly when followed by
an unrecognized privileged command. Required fields: timestamp, account,
host, process, event text, and outcome.

## Status: design proposal, not tested detection logic

The available account could count local authentication records but could not
read Wazuh manager logs or query registered agents. No dashboard rule or alert
was created, changed, or tested. Validate only in an owner-authorized lab with
known benign events and a documented rollback/no-change plan.
