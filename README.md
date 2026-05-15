# Modern Cellular Security Handbook

A comprehensive, evidence-based resource on cellular security, privacy threat modeling, and the Two-Phone Strategy. 9 volumes, 50 chapters, 11 appendices, 13 forensic graphs.

## Structure

| Volume | Focus |
|--------|-------|
| V1 | Foundations & Strategy (executive summary, threat modeling, two-phone strategy) |
| V2 | Forensic Deep Dive (cellular topology, Wi-Fi tracking, ISP metadata, VPN/Tor, Android OS) |
| V3 | Complete Threat Model (6-layer model: cellular, Wi-Fi, ISP, app/OS, physical, legal) |
| V4 | Visualizations & Graphs (10 forensic graphs of attack surfaces and data flows) |
| V5 | Practical Implementation (citizen's guide, 80/20 rule, 1-week privacy upgrade) |
| V6 | High-Risk Operations (burner phones, faraday discipline, OpSec rules, failure recovery) |
| V7 | Advanced Research (mitigated architecture, residual risks, open questions, threat tier matrix) |
| V8 | Case Studies (real-world failures and lessons) |
| V9 | ML & Data Science (data analysis and machine learning surveillance) |

## Build

```bash
pip install -r requirements.txt
make              # or: python3 compile_handbook.py
make html         # HTML only (no PDF)
make light        # print-ready light theme
make epub         # also generate EPUB
```

Output: `docs/handbook.html`, `docs/Privacy_Researchers_Handbook.pdf`, `docs/graphs/*.png`

## Theme

Dark theme by default (screen-optimized). Use `make light` for a print-ready light theme.

## Dependencies

- Python 3.10+ with matplotlib, markdown, networkx, numpy, weasyprint
- WeasyPrint on macOS: `brew install pango glib`
- EPUB: pandoc (`brew install pandoc`)
