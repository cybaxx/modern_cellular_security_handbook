# Appendix H: Change Log

## Overview

This appendix tracks the version history of the Complete Privacy Researcher's Handbook. It documents significant additions, revisions, and corrections across all versions.

The handbook began as a forensic analysis of the two-phone strategy and grew into a comprehensive resource through iterative refinement. Each version reflects new research, community feedback, and evolving threat landscapes.

## Version History

### Version 3.1 — 2026-05-15 (Current)

**Status:** Current release
**Change type:** Content and structural revision

**Summary:** Expanded to 50 chapters across 9 volumes plus 11 appendices. Live dark/light theme toggle added to HTML output. Chapter ordering fixed (Volumes 8 and 9 now precede Appendices). Cross-reference dead links repaired. Volume labels standardized with colons.

**Additions:**
- Volume 8: Case Studies (Chapter 49) — real-world failures and forensic lessons
- Volume 9: ML & Data Science (Chapter 50) — analysis of data pipelines, entity resolution, and ML attack classes
- Appendices I–K: Minimum Viable Privacy, Setup Verification Scripts, International Legal Reference
- Live dark/light theme toggle switch with localStorage persistence in compiled HTML
- Root-level README.md with build instructions

**Revisions:**
- Volume 2 expanded from Ch05–10 to Ch05–13 (added Android OS anatomy, cellular geo-location, legal access)
- Volume 3 expanded from Ch11–17 (now 7 chapters with complete layer model)
- Volume 7 expanded from Ch41–45 to Ch41–48 (added threat tier matrix, empirical testing)
- Chapter anchor IDs prefixed with volume number to resolve V2/V3 chapter number collision
- Ch04 Stock Android privacy baseline corrected from "0%" to "actively collects data"

**Corrections:**
- Ch16: dead reference "mitigated architecture (Chapter 17)" → Chapter 41
- Ch17: dead reference "Part 5" → Chapter 42
- Version string aligned across all chapters (v3.1)
- All "Part N" references from earlier organizational scheme removed or updated to current Volume/Chapter structure

---

### Version 3.0 — 2026-05-14 (Previous)

**Status:** Superseded by Version 3.1
**Change type:** Major revision — complete integration and reorganization

**Summary:** Merged all previous analyses, graphs, guides, and reference materials into a single, cohesive document organized into 48 chapters across 9 volumes plus 8 appendices.

**Additions:**
- Complete reorganization into Volume/Chapter structure with Table of Contents
- Volume 1: Foundations and Strategy (Chapters 1–4) — consolidates original strategy content
- Volume 2: Forensic Deep Dive (Chapters 5–13) — integrates forensic analyses of cellular, Wi-Fi, ISP, application, legal layers, Android OS, and cellular geo-location
- Volume 3: Complete Threat Model (Chapters 11–17) — full layer-by-layer vulnerability catalog with adversary success rates
- Volume 4: Visualizations and Graphs (Chapters 18–27) — 10 forensic graphs with explanations
- Volume 5: Practical Implementation (Chapters 28–31) — citizen's guide, 80/20 rule, one-week plan
- Volume 6: High-Risk Operations (Chapters 32–40) — two-phone playbook, failure scenarios, contract
- Volume 7: Advanced Research (Chapters 41–48) — mitigated architecture, residual risks, cost-benefit methodology, open questions, experiments, threat tier matrix, empirical testing
- Volume 8: Case Studies (Chapter 49) — real-world failures and lessons
- Appendices A–H: Glossary, 3GPP reference, carrier data retention, forensic tools, legal reference, hardware recommendations, quick reference cards, change log
- Updated 5G positioning analysis to reflect 2026 deployment reality
- Expanded carrier data retention comparison (US, EU, China)
- Added chapters on zero-day and baseband exploitation vectors, emerging attack surfaces
- New "Compartmentalized Burner" architecture chapter (Chapter 41)
- Threat Tier matrix and decision framework (Chapter 47)

**Revisions:**
- Citizen's guide rewritten with updated app recommendations and threat model alignment
- OpSec rules consolidated from multiple sections into a single authoritative list (Volume 6, Chapter 38)
- Cost-benefit analysis updated with 2026 pricing
- All tool recommendations updated with latest versions and alternatives
- Legal reference expanded with recent court decisions (Carpenter v. United States implications)

**Corrections:**
- Clarified that Signal metadata retention by Signal's servers (content: none; metadata: minimal but non-zero) is distinct from carrier metadata retention
- Fixed inconsistencies between the "Zero Location" configuration in Chapter 4 (original) and the Compartmentalized Burner mitigations
- Standardized terminology: "Compartmentalized Burner" is now the official name for the mitigated architecture
- Corrected several 3GPP specification references in the protocol analysis sections

---

### Version 2.0 — 2026-05-14 (Earlier)

**Status:** Superseded by Version 3.0
**Change type:** Major revision — first full integration

**Summary:** Merged the original forensic analysis with the citizen's guide and 10 forensic graphs into a single document organized into 7 volumes plus 8 appendices.

**Additions:**
- Volume 4: Visualizations and Graphs (Chapters 18–27) — 10 forensic graphs
- Volume 5: Practical Implementation (Chapters 28–31) — citizen's guide, 80/20 rule, one-week plan
- Volume 6: High-Risk Operations (Chapters 32–40) — two-phone playbook
- Volume 7: Advanced Research (Chapters 41–45) — mitigated architecture, open questions, experiments
- Appendices A–H: Glossary, 3GPP reference, carrier data retention, forensic tools, legal reference, hardware recommendations, quick reference cards, change log

**Revisions:**
- Cost breakdown detailed ($1,800/year estimate)
- US, EU, and China carrier retention policies documented
- Decision matrix for two-phone necessity clarified

---

### Version 1.1 — 2026-05-14 (Earlier)

**Status:** Superseded by Version 2.0
**Change type:** Minor revision — graphs and citizen's guide

**Summary:** Added data visualizations and practical guidance for normal users.

**Additions:**
- 10 forensic graphs with matpotlib code
- Citizen's Guide (80/20 Rule)
- One-week privacy upgrade plan
- Data broker removal guidance

---

### Version 1.0 — 2026-05-14 (Original)

**Status:** Superseded by Version 1.1
**Change type:** Initial release

**Summary:** Forensic security analysis of the two-phone privacy strategy identifying critical gaps, mapping forensic attack surfaces, and proposing mitigations.

**Contents:**
- Original two-phone strategy analysis
- Cellular network data structures (4G/5G NAS, RRC, S1AP/NGAP)
- Identity structs: IMSI, IMEI, SUPI, SUCI, PEI, GUTI, TMSI
- Collection mechanisms: Stingray, CALEA, core network correlation
- Wi-Fi layer tracking, ISP metadata, application geo-location
- 5G NR positioning (Release 16–18+)
- Legal access mechanisms
- Six-layer threat model
- Three-level adversary model

---

## Document Metadata

| Field | Value |
|---|---|
| Current version | 3.1 |
| Publication date | 2026-05-15 |
| Author | Enthusiastic Privacy Researcher (with forensic expertise) |
| Classification | PUBLIC — For educational and threat modeling purposes only |
| License | Creative Commons Attribution-NonCommercial 4.0 International |
| Repository | Available upon request from the author |
| Citation format | "The Complete Privacy Researcher's Handbook, Version 3.1 (2026)" |

## Planned Future Updates

| Topic | Priority | Expected Version |
|---|---|---|
| 5G carrier phase positioning deployment status | High | 3.2 |
| Updated carrier data retention policies (annual review) | High | 3.2 |
| New forensic tool versions and capabilities | Medium | 3.2 |
| Community-contributed experiments and research results | Medium | 3.2–3.5 |
| Legal reference updates (new court decisions) | High | As needed |
| MAC randomization reliability data (vendor testing results) | Medium | 3.2–3.5 |
| Baseband exploit disclosures and mitigations | High | As needed |
| ECH deployment status and impact on SNI visibility | Low | 3.2 |

## How to Contribute

Corrections, additions, and research results can be submitted to the author. Accepted contributions will be credited in future versions. The goal is to maintain this handbook as a living document that evolves with the threat landscape.

## Version Numbering Convention

| Version component | Meaning |
|---|---|
| Major version (X.0) | Structural reorganization, new volumes, significant new content |
| Minor version (1.X) | New chapters, appendices, major additions within existing structure |
| Patch (1.1.X) | Corrections, updates to existing content, minor clarifications |
