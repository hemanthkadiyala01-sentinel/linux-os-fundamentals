# Scope, Authorization, and Limitations

## Authorized scope

Only the project owner's local Windows host and Ubuntu WSL2 installation are in
scope. Commands are read-only unless an explicitly documented controlled test
is approved by the owner. No scanning, credential testing, persistence,
external targets, or remote publication is authorized by this repository.

## Known limitations as of 2026-09-21

- `sudo -n` was unavailable, so manager logs and `agent_control` were not read.
- The current Windows account could query `WazuhSvc` but could not read its
  protected `ossec.log`.
- Therefore agent enrollment, last check-in, and event delivery remain
  unverified—not failed, and not assumed successful.
- Authentication counts are a retained-log baseline, not lifetime totals.

## Controlled-test decision

No telemetry-generating test was run in this sprint. A valid future test needs
owner approval, a defined test file or benign event, a collection window, and
both endpoint and manager-side confirmation. This limitation is deliberate:
creating a signal without being able to validate delivery would produce a
misleading result.
