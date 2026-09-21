# Lab 04: Local Authentication Log Triage

## Objective

Perform a read-only SOC-style review of local Ubuntu authentication telemetry.
This lab does not depend on Wazuh agent connectivity, network reachability, or
Security Guardian. It analyzes evidence already recorded by the operating
system.

## Safety Boundaries

- Do not start, stop, restart, or reconfigure any service.
- Do not create failed login attempts or change user passwords.
- Run only the read-only commands shown below.
- Treat a count as a lead for investigation, not proof of malicious activity.

## Verified Environment

The following were verified on 2026-09-21:

- Ubuntu WSL2 is available and uses `systemd`.
- `/var/log/auth.log`, `/var/log/syslog`, `/var/log/wtmp`, and `/var/log/btmp` exist.
- The `bunny` account can read `/var/log/auth.log`.
- The current baseline has local login-session and `sudo` records. It has no
  `Failed password` or `Accepted password` records, but it does retain four
  historical `sudo` PAM `authentication failure` records. Those are local
  privilege-authentication events, not evidence of a remote password attack.

## Step 1: Confirm the evidence source

Run in **PowerShell**:

```powershell
wsl -d Ubuntu -- bash -lc 'ls -lh /var/log/auth.log /var/log/wtmp /var/log/btmp; tail -n 5 /var/log/auth.log'
```

Reason: confirms that the authentication log and login databases exist and
shows a small, recent sample without modifying them.

Verification: the command must list all three files and print five or fewer
recent log lines. If it reports `Permission denied` or a missing file, stop and
record that result; do not use `sudo` or change permissions for this lab.

## Step 2: Build a baseline from existing events

Run in **PowerShell**:

```powershell
wsl -d Ubuntu -- bash -lc 'printf "failed_password="; grep -Eic "failed password" /var/log/auth.log; printf "pam_authentication_failures="; grep -Eic "authentication failure" /var/log/auth.log; printf "accepted_password="; grep -Eic "accepted password" /var/log/auth.log; printf "sudo_events="; grep -Eic "sudo:" /var/log/auth.log; printf "recent_sessions:\n"; grep -Ei "session (opened|closed)" /var/log/auth.log | tail -n 10'
```

Reason: separates `Failed password`, generic PAM authentication failures,
accepted-password, privilege-use, and session-lifecycle telemetry into simple,
reproducible categories. A generic PAM failure must be interpreted with its
full log line; it may be a local `sudo` prompt rather than a remote login.

Verification: retain the exact counts and the ten-or-fewer session lines in
your investigation notes. A zero count is a valid baseline and is not an error.

## Step 3: Review privileged commands as an analyst

Run in **PowerShell**:

```powershell
wsl -d Ubuntu -- bash -lc 'grep -E "sudo:.*COMMAND=" /var/log/auth.log | tail -n 20'
```

Reason: `sudo` command records answer who requested privilege, from which
working directory, and which command was run. This is useful for attribution
and change review.

Verification: each returned entry should identify a user and include
`COMMAND=`. If the output is empty, record that no privileged command entries
were found in the retained log window.

## Step 4: Review failed-login evidence without creating it

Run in **PowerShell**:

```powershell
wsl -d Ubuntu -- bash -lc 'printf "auth.log failures:\n"; grep -Ei "failed password|authentication failure|invalid user" /var/log/auth.log | tail -n 20; printf "\nbtmp records:\n"; lastb -a 2>/dev/null | head -n 20'
```

Reason: checks two local evidence sources for unsuccessful authentication. It
does not attempt a login and does not alter the host.

Verification: preserve the complete lines returned from `auth.log` and their
event context. If both sections are empty, record **no retained failed-login
evidence observed**. Do not conclude that failures never occurred; logs may be
rotated or outside the current retention window.

## Detection Notes

Investigate when the baseline changes, for example:

- repeated `Failed password` records for one account or source;
- repeated `sudo:auth` failures without an expected explanation;
- an unexpected account in a session-opened record;
- a `sudo` `COMMAND=` entry that was not authorized; or
- a burst of failed attempts followed by a successful authentication event.

For every observation, record the timestamp, account, source (when present),
event text, and why it is unusual relative to the baseline. Do not label an
event malicious solely because it is uncommon.

## Current Outcome

This lab is ready for execution because its evidence sources and baseline were
verified locally. It intentionally has no pass/fail attack simulation: success
means accurately collecting and interpreting the telemetry that actually
exists.
