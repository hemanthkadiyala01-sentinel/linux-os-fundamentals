# Linux OS Fundamentals & Defensive Security Lab

An evidence-first cybersecurity engineering project built around **Linux system fundamentals, Windows endpoint monitoring, Wazuh telemetry, threat hunting, DFIR-style investigation, and detection engineering**.

The project uses a local **Ubuntu WSL2 + Wazuh deployment + Windows 11 endpoint** environment to investigate system behavior, collect security-relevant evidence, document findings, and validate detection logic through repeatable tests.

---

## Project Overview

This repository documents hands-on security investigations rather than only theoretical exercises.

The work progresses from operating-system fundamentals into practical defensive security:

**Linux fundamentals → system monitoring → authentication triage → Wazuh → Windows telemetry → threat hunting → investigation → detection engineering**

The methodology emphasizes:

- Evidence before conclusions
- Read-only investigation where practical
- Reproducible commands and tests
- Explicit evidence boundaries
- Authorized local-lab activity
- Documented uncertainty rather than unsupported attribution

---

## Environment

| Component | Environment |
|---|---|
| Linux | Ubuntu WSL2 |
| Windows Endpoint | Windows 11 Pro |
| SIEM / XDR Platform | Wazuh |
| Wazuh Agent | 4.14.7 |
| Linux Services | systemd, Filebeat, Wazuh Manager, Indexer, Dashboard |
| Detection Engineering | Python |
| Windows Investigation | PowerShell |
| Version Control | Git / GitHub |

---

## Architecture

```text
┌──────────────────────────────┐
│       Windows 11 Endpoint    │
│                              │
│  Security / Application Logs │
│  Sysmon / Endpoint Activity  │
└──────────────┬───────────────┘
               │
               │ Wazuh Agent 001
               ▼
┌──────────────────────────────┐
│       Ubuntu WSL2            │
│                              │
│  Wazuh Manager               │
│  Filebeat                    │
│  Wazuh Indexer               │
│  Wazuh Dashboard             │
└──────────────┬───────────────┘
               │
               ▼
       Investigation &
       Detection Workflow
<!-- Historical scaffold retained for repository history; superseded by the evidence-first project above.

# 

# \# 🛡️ Linux \& OS Fundamentals

# 

# > A practical cybersecurity engineering learning repository focused on Linux, operating systems, process analysis, memory concepts, and security-relevant system behavior.

# 

# !\[Status](https://img.shields.io/badge/Status-In%20Progress-orange)

# !\[Focus](https://img.shields.io/badge/Focus-Cybersecurity-blue)

# !\[Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows-lightgrey)

# 

# \---

# 

# \## 📌 About This Project

# 

# This repository documents my hands-on learning journey in Linux and operating system fundamentals for cybersecurity engineering.

# 

# The objective is to understand how operating systems manage processes, memory, permissions, system calls, and system resources, and how this knowledge supports security monitoring, digital forensics, incident response, and security research.

# 

# This project is developed incrementally through practical labs, technical documentation, scripts, and verified observations.

# 

# \---

# 

# \## 🎯 Learning Objectives

# 

# \- Build strong Linux command-line fundamentals.

# \- Understand processes and process memory.

# \- Study virtual memory and memory mappings.

# \- Understand Linux file permissions and ownership.

# \- Explore system calls and system tracing.

# \- Develop basic system analysis scripts.

# \- Document technical findings clearly.

# \- Connect operating system concepts to cybersecurity operations.

# 

# \---

# 

# \## 🧪 Learning Modules

# 

# | Module | Description | Status |

# |---|---|---|

# | Linux Command Line | Files, directories, processes, and system commands | Planned |

# | Process Analysis | Process identification and resource inspection | Planned |

# | Memory Analysis | Virtual memory regions and permissions | Planned |

# | File Permissions | Ownership, permissions, and access control | Planned |

# | System Calls | Understanding system interactions | Planned |

# | System Tracing | Observing program behavior in a lab | Planned |

# | Security Documentation | Technical reports and observations | Planned |

# 

# > Module statuses will be updated as each lab is completed and verified.

# 

# \---

# 

# \## 🏗️ Repository Structure

# 

# ```text

# linux-os-fundamentals/

# │

# ├── README.md

# ├── labs/

# │   ├── 01-process-memory/

# │   ├── 02-linux-permissions/

# │   └── 03-system-calls/

# │

# ├── scripts/

# ├── docs/

# ├── reports/

# ├── screenshots/

# └── tests/

# ```

# 

# \---

# 

# \## 🔬 Practical Labs

# 

# Each lab will include:

# 

# 1\. Objective

# 2\. Lab environment

# 3\. Tools and commands

# 4\. Procedure

# 5\. Observations

# 6\. Technical explanation

# 7\. Cybersecurity relevance

# 8\. Limitations

# 9\. References, where applicable

# 

# The labs will be performed only on local systems or authorized environments.

# 

# \---

# 

# \## 🔐 Cybersecurity Relevance

# 

# Understanding operating systems helps cybersecurity practitioners analyze:

# 

# \- Process behavior

# \- Suspicious system activity

# \- File and access permissions

# \- System resource usage

# \- Memory mappings

# \- System calls

# \- Evidence relevant to security investigations

# 

# The repository focuses on defensive learning, responsible security research, and authorized experimentation.

# 

# \---

# 

# \## 🛠️ Tools and Technologies

# 

# The tools and technologies used in each lab will be documented as the project develops.

# 

# Planned areas include:

# 

# \- Linux

# \- Windows PowerShell

# \- Python

# \- Bash

# \- Git and GitHub

# \- Process and system analysis utilities

# 

# \---

# 

# \## 📈 Project Progress

# 

# | Area | Status |

# |---|---|

# | Repository setup | Completed |

# | Initial documentation | In Progress |

# | Linux fundamentals | Planned |

# | Process and memory labs | Planned |

# | Security-focused documentation | Planned |

# | Automated tests | Planned |

# 

# \---

# 

# \## 👨‍💻 About Me

# 

# \*\*Hemanth Kadiyala\*\*

# 

# Cybersecurity Engineering Student building practical skills in security monitoring, threat detection, DFIR, Linux, networking, and security automation.

# 

# I focus on learning through implementation, testing, documentation, and responsible security research.

# 

# \---

# 

# \## ⚠️ Responsible Use

# 

# All activities in this repository are intended for educational, defensive, and authorized security purposes.

# 

# Do not use the techniques or tools documented here against systems without explicit permission.

# 

# \---

# 

# \## 📄 License

# 

# A license will be selected as the project develops.
-->

