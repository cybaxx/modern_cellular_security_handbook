# Appendix H: Change Log

## Overview

This appendix tracks the version history of the Complete Privacy Researcher's Handbook. It documents significant additions, revisions, and corrections across all versions.

The handbook began as a forensic analysis of the two-phone strategy and grew into a comprehensive resource through iterative refinement. Each version reflects new research, community feedback, and evolving threat landscapes.

## Version History

### Version 2.0 — 2026-05-14 (Current)

**Status:** Current release
**Change type:** Major revision — complete integration and reorganization

**Summary:** This version merges all previous analyses, graphs, guides, and reference materials into a single, cohesive document organized into 45 chapters across 7 volumes plus 8 appendices.

**Additions:**
- Complete reorganization into Volume/Chapter structure with Table of Contents
- Volume 1: Foundations and Strategy (Chapters 1–4) — consolidates original strategy content
- Volume 2: Forensic Deep Dive (Chapters 5–10) — integrates all forensic analyses of cellular, Wi-Fi, ISP, application, and legal layers
- Volume 3: Complete Threat Model (Chapters 11–17) — full layer-by-layer vulnerability catalog with adversary success rates
- Volume 4: Visualizations and Graphs (Chapters 18–27) — 10 forensic graphs with explanations
- Volume 5: Practical Implementation (Chapters 28–31) — citizen's guide, 80/20 rule, one-week plan
- Volume 6: High-Risk Operations (Chapters 32–40) — two-phone playbook, failure scenarios, contract
- Volume 7: Advanced Research (Chapters 41–45) — mitigated architecture, residual risks, cost-benefit methodology, open questions, experiments
- Appendices A–H: Glossary, 3GPP reference, carrier data retention, forensic tools, legal reference, hardware recommendations, quick reference cards, change log
- Updated 5G positioning analysis to reflect 2026 deployment reality
- Expanded carrier data retention comparison (US, EU, China)
- Added chapter on zero-day and baseband exploitation vectors
- New "Compartmentalized Burner" architecture chapter

**Revisions:**
- Citizen's guide rewritten with updated app recommendations and threat model alignment
- OpSec rules consolidated from multiple sections into a single authoritative list (Part 6, Chapter 38)
- Cost-benefit analysis updated with 2026 pricing
- All tool recommendations updated with latest versions and alternatives
- Legal reference expanded with recent court decisions (Carpenter v. United States implications)

**Corrections:**
- Clarified that Signal metadata retention by Signal's servers (content: none; metadata: minimal but non-zero) is distinct from carrier metadata retention
- Fixed inconsistencies between the "Zero Location" configuration in Chapter 4 (original) and the revised Part 4 mitigations
- Standardized terminology: "Compartmentalized Burner" is now the official name for the mitigated architecture
- Corrected several 3GPP specification references in the protocol analysis sections

---

### Version 1.1 — 2026-05-14 (Earlier)

**Status:** Superseded by Version 2.0
**Change type:** Minor revision — graphs and citizen's guide

**Summary:** Added data visualizations and practical guidance for normal users, while maintaining the original threat model structure.

**Additions:**
- Ten forensic graphs added as Chapter 7 within the original document structure:
  - Attack Surface Overview
  - Cellular Tracking Accuracy Over Time
  - Data Flow & Correlation Attack Diagram
  - Wi-Fi Probe Request & BSSID Geolocation
  - Threat Model Effectiveness by Adversary
  - OpSec Failure Cascade
  - Privacy vs. Convenience Trade-Off
  - Forensic Data Retention by Carrier (US vs. EU vs. China)
  - Cost-Benefit Analysis
  - Decision Tree: Should You Use Two Phones?
- Python code for generating graphs (matplotlib/seaborn) included for researchers
- Citizen's Guide (80/20 Rule) added as Part 8 — addresses normal users who do not need two phones
- One-week privacy upgrade plan (day-by-day actions)
- "Good Citizen vs. Privacy Maximalist" comparison table
- Threat-specific escalation criteria (when to move from citizen to high-risk strategy)
- Data broker removal guidance (DeleteMe, OneRep, manual opt-out)
- Social media app-specific recommendations

**Revisions:**
- Cost breakdown detailed in Graph 9 ($1,800/year estimate)
- US, EU, and China carrier retention policies documented in Graph 8
- Decision matrix for two-phone necessity clarified

**Corrections:**
- None (first version with graphs)

---

### Version 1.0 — 2026-05-14 (Original)

**Status:** Superseded by Version 1.1 and 2.0
**Change type:** Initial release

**Summary:** The original document was a forensic security analysis of the two-phone privacy strategy. It identified critical gaps, mapped forensic attack surfaces, and proposed mitigations.

**Contents of Version 1.0:**
- Original two-phone strategy as proposed (Phone A: flip phone, Phone B: custom OS, Computer: controlled)
- Forensic analysis of cellular network data structures (4G/5G NAS, RRC, S1AP/NGAP)
- Identity structs: IMSI, IMEI, SUPI, SUCI, PEI, GUTI, TMSI
- Location and mobility structs: Cell ID (ECGI/NCGI), Timing Advance, Angle of Arrival, Measurement Reports
- Session and usage structs: QoS Class, APN, SIP Headers
- Collection mechanisms: Stingray/IMSI catcher, CALEA/Lawful Intercept, Core Network Correlation (S1AP)
- Wi-Fi layer tracking: Probe requests, association frames, DHCP traffic, residential ISP problem
- ISP metadata collection: DNS, SNI, NetFlow, DPI, timing analysis
- Application-level geo-location: Google Location Services, Apple Find My, in-app tracking, Wi-Fi geolocation databases, EXIF metadata
- Cellular-level geo-location: Cell ID method, Timing Advance, Angle of Arrival, TDOA
- 5G NR positioning: NR E-CID, OTDOA, UTDOA, Multi-RTT, DL-AoD/UL-AoA, Carrier Phase Positioning (Release 18+)
- Legal access mechanisms: Tower dumps, Pen Register, §2703(d) orders, Title III wiretaps, CALEA intercepts
- Six-layer threat model: Cellular, Wi-Fi, ISP, Application, Physical Co-Location, Legal Access
- Three-level adversary model: Low (advertisers), Medium (local police), High (federal/state)
- Part 4: "Compartmentalized Burner" mitigated architecture (original version)
- Part 5: "No Safe Harbor" residual risks
- Part 6: Decision matrix and "Do Not" list
- Part 7: Quick reference summary table

**Key findings documented in Version 1.0:**
1. Phone A (flip) is fully tracked by the carrier via CDRs, TA, and AoA (50-200m accuracy)
2. Phone B (Wi-Fi only) is vulnerable to Wi-Fi BSSID geolocation and ISP metadata
3. Physical co-location (carrying both phones) collapses compartmentalization
4. Five specific failure scenarios documented
5. The "Zero Location" gold standard configuration defined
6. E911 backdoor identified as a critical vulnerability

**Known limitations at Version 1.0:**
- Graphs not yet included
- Citizen's guide not yet included
- Cost-benefit analysis was qualitative, not quantitative
- No appendix materials (glossary, legal reference, hardware recommendations)
- Document focused on two-phone analysis with less emphasis on single-phone alternatives

---

## Document Metadata

| Field | Value |
|---|---|
| Current version | 2.0 |
| Publication date | 2026-05-14 |
| Author | Enthusiastic Privacy Researcher (with forensic expertise) |
| Classification | PUBLIC — For educational and threat modeling purposes only |
| License | Creative Commons Attribution-NonCommercial 4.0 International |
| Repository | Available upon request from the author |
| Citation format | "The Complete Privacy Researcher's Handbook, Version 2.0 (2026)" |

## Planned Future Updates

The following updates are planned for future versions:

| Topic | Priority | Expected Version |
|---|---|---|
| 5G carrier phase positioning deployment status | High | 2.1 |
| Updated carrier data retention policies (annual review) | High | 2.1 |
| New forensic tool versions and capabilities | Medium | 2.1 |
| Community-contributed experiments and research results | Medium | 2.1–2.5 |
| Legal reference updates (new court decisions) | High | As needed |
| MAC randomization reliability data (vendor testing results) | Medium | 2.1–2.5 |
| Baseband exploit disclosures and mitigations | High | As needed |
| ECH deployment status and impact on SNI visibility | Low | 2.1 |

## How to Contribute

Corrections, additions, and research results can be submitted to the author. Accepted contributions will be credited in future versions. The goal is to maintain this handbook as a living document that evolves with the threat landscape.

## Version Numbering Convention

| Version component | Meaning |
|---|---|
| Major version (X.0) | Structural reorganization, new volumes, significant new content |
| Minor version (1.X) | New chapters, appendices, major additions within existing structure |
| Patch (1.1.X) | Corrections, updates to existing content, minor clarifications |
