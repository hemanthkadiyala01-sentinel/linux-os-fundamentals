
# Linux OS Fundamentals & Defensive Security Lab

[![Python Tests](https://github.com/hemanthkadiyala01-sentinel/linux-os-fundamentals/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/hemanthkadiyala01-sentinel/linux-os-fundamentals/actions/workflows/tests.yml)

An evidence-first cybersecurity engineering project focused on Linux and Windows operating-system behavior, endpoint telemetry, authentication investigation, threat hunting, digital forensics and incident response (DFIR), and rule-based detection engineering.

This repository combines practical operating-system labs, documented investigations, Python detection logic, synthetic security-event datasets, repeatable tests, and a local Wazuh environment.

The primary objective is to build a reproducible defensive-security laboratory in which technical conclusions are supported by observable evidence, documented methods, and explicit limitations.

> **Project status:** Active development. The detection demo and automated tests have been verified locally. Production readiness and complete end-to-end SIEM integration are not claimed.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Key Capabilities](#key-capabilities)
- [Architecture](#architecture)
- [Lab Environment](#lab-environment)
- [Quick Start](#quick-start)
- [Detection Engineering Demo](#detection-engineering-demo)
- [Automated Testing](#automated-testing)
- [Detection Methodology](#detection-methodology)
- [Repository Structure](#repository-structure)
- [Investigation Methodology](#investigation-methodology)
- [Security, Privacy and Responsible Use](#security-privacy-and-responsible-use)
- [Known Limitations](#known-limitations)
- [Roadmap](#roadmap)
- [License](#license)

---

## Project Overview

This project explores how operating-system fundamentals and endpoint telemetry can support practical defensive-security investigations.

The work progresses through the following areas:

**Operating-System Fundamentals → System Monitoring → Authentication Triage → Endpoint Telemetry → Threat Hunting → Investigation → Detection Engineering**

The repository emphasizes:

- Evidence before conclusions.
- Reproducible procedures and test cases.
- Read-only investigation where practical.
- Separation of observed facts from analytical conclusions.
- Explicit documentation of uncertainty and limitations.
- Controlled testing with synthetic events where appropriate.
- Authorized experimentation in local lab environments.

The project is intended to demonstrate practical security engineering skills through implementation, validation, documentation, and iterative improvement rather than relying exclusively on theoretical descriptions.

## Key Capabilities

| Area | Implementation |
|---|---|
| Linux fundamentals | System, process, permissions, services, and authentication-related labs |
| Windows endpoint investigation | PowerShell-based collection and endpoint monitoring exercises |
| SIEM lab | Wazuh-based monitoring architecture using Ubuntu WSL2 and a Windows endpoint |
| Threat hunting | Documented threat-hunting exercises and investigation workflows |
| DFIR-style investigations | Case notes, evidence interpretation, and bounded conclusions |
| Detection engineering | Python-based rule logic for suspicious authentication sequences |
| Synthetic event testing | JSONL datasets for benign and suspicious demonstration scenarios |
| Automated testing | Python `unittest` suite |
| Continuous integration | GitHub Actions workflow for automated unit tests |
| Technical documentation | Architecture, investigation methodology, lab scope, and threat model |

The implemented features and their current validation status are documented separately. The presence of a lab or workflow does not automatically imply that every integration or detection has been verified end to end.

---

## Architecture

The lab uses a Windows endpoint and an Ubuntu WSL2 environment for defensive monitoring and investigation. The Python detection demo can also be run independently using synthetic events.

```text
┌─────────────────────────────────────┐
│         Windows 11 Endpoint         │
│                                     │
│  Windows Security / Application Logs│
│  Endpoint Activity                  │
│  PowerShell Investigation Tools     │
└──────────────────┬──────────────────┘
                   │
                   │ Wazuh Agent
                   ▼
┌─────────────────────────────────────┐
│          Ubuntu WSL2                │
│                                     │
│  Wazuh Manager                      │
│  Filebeat                           │
│  Wazuh Indexer                      │
│  Wazuh Dashboard                    │
└──────────────────┬──────────────────┘
                   │
                   ▼
┌─────────────────────────────────────┐
│     Investigation and Analysis      │
│                                     │
│  Evidence Collection                │
│  Event Triage                       │
│  Threat Hunting                     │
│  Detection Engineering              │
│  Documentation and Validation       │
└─────────────────────────────────────┘


Independent Detection Demo
───────────────────────────

Synthetic JSONL Events
          │
          ▼
Python Detection Logic
          │
          ▼
Rule Evaluation
          │
          ▼
Structured JSON Output
```

The independent detection demo does not require the Wazuh services to be running. It evaluates the supplied synthetic event records directly through the repository's Python detection implementation.

The diagram describes the intended lab architecture. It should not be interpreted as proof that every event source, indexer path, dashboard query, or custom detection rule has been validated end to end.

---

## Lab Environment

| Component | Environment |
|---|---|
| Operating system for SIEM lab | Ubuntu under WSL2 |
| Windows endpoint | Windows 11 Pro |
| Monitoring platform | Wazuh |
| Wazuh agent version recorded in the project environment | 4.14.7 |
| Supporting services | Wazuh Manager, Wazuh Indexer, Filebeat, and Dashboard |
| Detection implementation | Python |
| Windows investigation and collection | PowerShell |
| Version control | Git and GitHub |
| Automated testing | Python `unittest` |
| CI workflow | GitHub Actions |

The exact service state and data flow may vary as the lab evolves. Refer to the corresponding investigation records and environment notes for the evidence available for a particular exercise.

---

## Quick Start

### Prerequisites

- Git
- Python 3.12 or newer
- Windows PowerShell, Windows Terminal, or a compatible terminal
- An internet connection to clone the repository

The synthetic detection demo uses Python's standard library and does not require third-party Python packages.

### 1. Clone the repository

```bash
git clone https://github.com/hemanthkadiyala01-sentinel/linux-os-fundamentals.git
cd linux-os-fundamentals
```

### 2. Confirm Python is available

```bash
python --version
```

### 3. Run the automated tests

```bash
python -m unittest discover -s tests -v
```

### 4. Run the synthetic detection demo

```bash
python scripts/demo/run_detection_demo.py
```

The demo prints JSON results for both the benign and suspicious-sequence scenarios.

The commands above are intended to run from the repository root. On Windows, prefix the script path with `.\` if desired:

```powershell
python .\scripts\demo\run_detection_demo.py
```

---

## Detection Engineering Demo

The repository includes a Python detection rule that evaluates synthetic `sudo` authentication events.

It demonstrates a limited but reproducible detection scenario:

1. Read structured events from JSONL sample files.
2. Validate and normalize timestamps.
3. Group relevant events by account.
4. Evaluate authentication failures inside a configured time window.
5. Check whether an unapproved successful command occurs after the failure threshold is crossed.
6. Produce a structured JSON alert when the rule conditions are satisfied.

### Sample datasets

| Dataset | Purpose | Expected alerts |
|---|---|---:|
| `samples/authentication/benign.jsonl` | Demonstrates a sequence that does not exceed the configured failure threshold | 0 |
| `samples/authentication/suspicious-sequence.jsonl` | Demonstrates five failures followed by an unapproved successful command | 1 |

These datasets contain fabricated events. They are intended for repeatable tests and demonstrations, not as evidence of a real attack.

### Run both scenarios

```bash
python scripts/demo/run_detection_demo.py
```

### Run the benign scenario

```bash
python scripts/demo/run_detection_demo.py --scenario benign
```

Expected result:

```json
[
  {
    "scenario": "benign",
    "input_events": 4,
    "alert_count": 0,
    "alerts": []
  }
]
```

### Run the suspicious scenario

```bash
python scripts/demo/run_detection_demo.py --scenario suspicious-sequence
```

Expected result, summarized:

```json
{
  "scenario": "suspicious-sequence",
  "input_events": 6,
  "alert_count": 1,
  "alerts": [
    {
      "account": "analyst1",
      "failure_count": 5,
      "command": "unknown-command"
    }
  ]
}
```

The actual output also includes the configured time window and a human-readable detection reason.

The name `unknown-command` is an illustrative test value. It is not evidence that a real command is malicious.

### Demo implementation

| File | Responsibility |
|---|---|
| `labs/07-detection-engineering/detection_logic.py` | Timestamp normalization, command normalization, event processing, and detection-rule evaluation |
| `labs/_07_detection_engineering_loader.py` | Loads the detection implementation from its lab directory |
| `scripts/demo/run_detection_demo.py` | Loads synthetic JSONL events and prints detection results |
| `samples/authentication/benign.jsonl` | Synthetic non-alerting scenario |
| `samples/authentication/suspicious-sequence.jsonl` | Synthetic alerting scenario |
| `samples/authentication/README.md` | Sample descriptions, expected behavior, and limitations |

---

## Automated Testing

Automated tests are included to validate the detector's behavior and the public demo.

Run the complete suite with:

```bash
python -m unittest discover -s tests -v
```

The suite covers scenarios including:

- Failure thresholds and cases without a qualifying command.
- An unapproved successful command after the failure threshold.
- Commands occurring before or between threshold-crossing failures.
- Approved commands.
- Account separation.
- Commands outside the configured time window.
- Inclusive time-window boundary behavior.
- Out-of-order input events.
- Duplicate failure events.
- Blank structured command fallback.
- Time-zone normalization.
- Invalid timestamps and missing allowlist configuration.
- Demo output and expected alert counts.

### Local verification

During the current local development session, **all 18 tests passed**.

The demo was also run independently for both scenarios, with the expected result of zero alerts for the benign sample and one alert for the suspicious sample.

These results establish the behavior exercised by the tests. They do not establish complete detection accuracy against real-world attacks.

### Continuous integration

The repository includes a GitHub Actions workflow:

`.github/workflows/tests.yml`

It is configured to run the Python unit tests on pushes to `main` and pull requests targeting `main`.

The workflow can be inspected here:

[View GitHub Actions](https://github.com/hemanthkadiyala01-sentinel/linux-os-fundamentals/actions)

A successful workflow verifies the checks configured for that specific commit. After making changes, confirm that the latest run also passed.

---

## Synthetic Detection Evaluation

The repository includes a labeled synthetic corpus to evaluate the
implemented sudo detection rule against predefined scenarios.

### Run the evaluation

```bash
python scripts/evaluation/evaluate_detection.py
```

The evaluator reports scenario-level matches, a confusion matrix,
and the following metrics:

- Accuracy
- Precision
- Recall
- Specificity
- F1 score

### Current synthetic evaluation

The initial corpus contains 11 manually designed scenarios:

| Result | Count |
|---|---:|
| True positives | 4 |
| False positives | 0 |
| True negatives | 7 |
| False negatives | 0 |

All 11 scenarios matched their expected rule outcomes. The calculated
metrics were 1.0 for accuracy, precision, recall, specificity, and
F1 score.

### Interpretation and limitations

These results describe consistency with the predefined labels in a
small, manually constructed synthetic dataset. They are not estimates
of real-world detection accuracy, operational false-positive rates,
or performance against previously unseen attacks.

The scenario labels specify expected behavior of this rule. They do
not independently establish whether activity would be malicious in
a real environment.

Additional evaluation should introduce broader benign and suspicious
scenarios, document labeling criteria, and test against cases that
were not used while designing the detection logic.

## Detection Methodology

The authentication detection example uses an explicit configuration for the failure baseline, time window, and approved commands.

The default demonstration configuration uses:

| Parameter | Value |
|---|---|
| Failure baseline | 4 |
| Minimum failures required to exceed the baseline | 5 |
| Time window | 60 minutes |
| Event process | `sudo` |
| Command allowlist | Explicit collection of approved command strings |
| Output | Structured JSON-compatible alert records |

The rule evaluates events per account. It requires the failure threshold to be crossed before an unapproved successful command qualifies for an alert within the evaluated time window.

### Timestamp handling

- Timestamps are expected to use ISO-8601 format.
- Time-zone-aware timestamps are normalized to UTC.
- Timestamps without explicit time-zone information are interpreted as UTC.
- Invalid timestamps raise a validation error.

### Command handling

- A non-blank structured command field is preferred.
- When that field is absent or blank, the implementation can fall back to a `COMMAND=` value in the event text.
- Command comparisons are case-insensitive and whitespace-normalized.
- Matching uses complete normalized command strings, not shell-aware parsing.

### Interpreting an alert

An alert means that the supplied events matched the implemented rule conditions. It should be treated as an investigative lead, not as conclusive evidence of compromise or malicious intent.

Analysts should validate the original event source, account context, time zone, command semantics, and surrounding activity before reaching a conclusion.

---

## Repository Structure

```text
linux-os-fundamentals/
│
├── .github/
│   └── workflows/
│       └── tests.yml
│
├── docs/
│   ├── architecture.md
│   ├── investigation-methodology.md
│   ├── lab-scope.md
│   └── threat-model.md
│
├── investigations/
│   ├── 2026-09-21-pcasvc-sdbinst-investigation.md
│   └── milestone-02-pcasvc-sdbinst-investigation.md
│
├── labs/
│   ├── [Operating-system and defensive-security labs]
│   ├── 07-detection-engineering/
│   │   ├── detection_logic.py
│   │   └── README.md
│   └── _07_detection_engineering_loader.py
│
├── reports/
│   └── [Documented investigation and validation reports]
│
├── samples/
│   └── authentication/
│       ├── README.md
│       ├── benign.jsonl
│       └── suspicious-sequence.jsonl
│
├── scripts/
│   ├── collection/
│   │   └── collect-wazuh-evidence.ps1
│   ├── demo/
│   │   └── run_detection_demo.py
│   └── validation/
│       └── validate-repository.ps1
│
├── tests/
│   ├── test_detection_demo.py
│   ├── test_detection_engineering.py
│   └── validation-tests/
│
├── .gitignore
└── README.md
```

This is a high-level map of the key project files. Consult the repository tree for the complete list of lab, investigation, and report files.

---

## Investigation Methodology

The project follows an evidence-first workflow intended to make investigative work easier to reproduce and review.

### 1. Define the question

State what behavior is being investigated and identify the scope of the lab.

### 2. Collect relevant evidence

Use documented commands and authorized local systems. Prefer read-only collection where practical.

### 3. Validate observations

Record the source of each observation and distinguish direct evidence from assumptions or inference.

### 4. Evaluate competing explanations

Consider benign administrative activity, expected system behavior, misconfiguration, incomplete telemetry, and suspicious behavior.

### 5. Document findings

Explain what the evidence supports, what remains uncertain, and which additional checks would be needed.

### 6. Preserve the evidence boundary

Do not claim that a service is delivering telemetry simply because it is running. Do not claim an alert is visible in a dashboard unless the relevant event and query result have actually been verified.

The supporting documents are available in `docs/`, `investigations/`, and `reports/`.

---

## Security, Privacy and Responsible Use

This repository is intended for educational, defensive, and authorized security engineering.

- Use only systems you own or are explicitly authorized to investigate.
- Use synthetic events for reproducible demonstrations.
- Avoid committing real authentication logs, personal information, credentials, access tokens, or other sensitive evidence.
- Review files before committing them to a public repository.
- Keep local evidence and sensitive artifacts out of version control.
- Clearly label fabricated data and distinguish demonstration results from real investigations.
- Do not interpret a rule match as definitive proof of compromise.

The repository's `.gitignore` includes exclusions for local evidence and log artifacts. A `.gitignore` entry is a safeguard, not a guarantee: review staged files before every commit.

---

## Known Limitations

This is an actively developed engineering and learning project, not a production-ready security monitoring product.

Current limitations include:

1. **Rule scope:** The primary Python detection example focuses on a narrow sequence of `sudo` failures and an unapproved successful command.
2. **Data quality:** Results depend on the correctness, completeness, and meaning of supplied events.
3. **Command interpretation:** Exact normalized string matching is not a shell parser and does not establish whether a command is malicious.
4. **Detection evaluation:** The synthetic demonstration does not provide a representative benchmark for real-world precision, recall, or false-positive rates.
5. **SIEM integration:** A successful standalone Python demo does not prove that the same scenario has been ingested, indexed, detected, and displayed end to end by Wazuh.
6. **Operational readiness:** The repository does not claim comprehensive production monitoring, alert management, or incident-response automation.

These limitations are part of the engineering work and should be revisited as the project evolves.

---

## Roadmap

The following improvements are potential next milestones; they should be marked complete only when implemented and verified.

### Detection and testing

- Expand edge-case tests for configuration validation and event ordering.
- Validate malformed and incomplete event records.
- Add repeatable tests for additional timestamp and command-field variations.
- Keep detection behavior documented alongside test cases.

### Reproducibility

- Expand sanitized synthetic event datasets.
- Document test inputs, expected outputs, and reproduction steps.
- Maintain a clear distinction between synthetic demonstrations and live telemetry.

### Evaluation

- Build a documented set of labeled benign and suspicious scenarios.
- Measure true positives, false positives, true negatives, and false negatives when the dataset supports those calculations.
- Report the test methodology, scenario count, assumptions, and limitations alongside results.

### SIEM integration

- Validate relevant Wazuh rule parsing and event processing.
- Confirm ingestion and searchability for controlled test events.
- Capture sanitized evidence demonstrating each integration step.
- Document what was verified and what remains untested.

### Project quality

- Improve contributor documentation and configuration examples.
- Add code-quality checks where appropriate.
- Review dependency and workflow security.
- Prepare versioned releases when the behavior and documentation are sufficiently stable.

---

## License

No license file is currently included in this repository.

Until a license is added, do not assume that the code and documentation are licensed for redistribution, modification, or other reuse. A license should be selected and committed explicitly when the repository owner is ready to define those permissions.

---

## Project Philosophy

The goal of this repository is to demonstrate that defensive security engineering is more than writing detection rules or collecting logs.

Good engineering also requires careful scope definition, evidence quality, reproducible validation, honest conclusions, and clear documentation of limitations.

**Build carefully. Test reproducibly. Investigate from evidence. Document what the results actually prove.**
