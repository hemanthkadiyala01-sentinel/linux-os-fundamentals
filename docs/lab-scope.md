# Scope, Authorization, and Limitations

## Authorized scope

Only the project owner's local Windows host and Ubuntu WSL2 installation are in
scope. Commands are read-only unless an explicitly documented controlled test
is approved by the owner. No scanning, credential testing, persistence,
external targets, or remote publication is authorized by this repository.

## Known limitations as of 2026-09-21

- Non-interactive sudo was unavailable; an owner-authorized interactive sudo session was used for the manager query.
- The protected Windows agent log remains unavailable to the regular Windows account, but manager-side `agent_control` confirmed agent `001` as Active.
- A recent Windows file-integrity scan was reported by the manager. A new controlled event has not yet been verified in the dashboard.
- Authentication counts are a retained-log baseline, not lifetime totals.

## Controlled-test decision

No telemetry-generating test was run in this sprint. A valid future test needs
owner approval, a defined test file or benign event, a collection window, and
both endpoint and manager-side confirmation. This limitation is deliberate:
the endpoint, manager, and dashboard before it is reported as successful.
