# Case 001: Ubuntu Authentication Baseline Review

## Question

Do retained local authentication records show evidence that requires escalation?

## Evidence

Collected read-only on 2026-09-21 from `/var/log/auth.log`:

| Metric | Count |
| --- | ---: |
| `Failed password` | 0 |
| PAM `authentication failure` | 4 |
| `Accepted password` | 0 |
| `sudo:` events | 240 |

`auth.log`, `wtmp`, and `btmp` existed. `btmp` was zero bytes at collection.

## Assessment

There was no retained SSH-style failed- or accepted-password evidence in the
measured log window. The four generic PAM failures require line-level context;
they may represent local sudo authentication activity and are not evidence of a
remote password attack by themselves. The result is a baseline, not an all-time
security conclusion.

## Next action

Use the collection script after a material change, compare like-for-like time
windows, and escalate only when the contextual evidence supports it.
