# Appendix G: Quick Reference Cards

## Introduction

This appendix contains printable quick-reference cards for daily, weekly, and emergency use. Each card is designed to fit on a single page. Print them, laminate them, and keep them with your equipment.

The cards are organized by function:
1. **Threat Level Reference Card** — Helps you assess your current threat level and choose the appropriate response
2. **Operational Security Rules Card** — The non-negotiable rules of the two-phone strategy
3. **Failure Recovery Card** — What to do when you make a mistake
4. **Weekly Privacy Checklist Card** — A weekly maintenance routine
5. **Decision Tree Summary** — Should you use two phones?

---

## Card 1: Threat Level Reference

<div class="ref-card"><pre>
┌─────────────────────────────────────────────────────────────────────────────┐
│                        THREAT LEVEL REFERENCE CARD                          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  LEVEL 1: LOW (Advertisers, Data Brokers, Casual Stalker)                   │
│  ───────────────────────────────────────────────────────────────────────    │
│  Strategy: Single de-Googled phone + Signal + VPN                          │
│  Effort:    2-3 hours setup, 10 min/week                                   │
│  Cost:      $5-10/month                                                    │
│  Protection: 90% of benefit with 10% of effort                             │
│  Key actions:                                                              │
│    □ Install GrapheneOS or de-Google your phone                            │
│    □ Use Signal for all messaging                                          │
│    □ Install uBlock Origin on browser                                      │
│    □ Turn off location for all apps except maps                            │
│    □ Use password manager and 2FA                                           │
│    □ Opt out of data brokers (DeleteMe or manual)                          │
│                                                                             │
│  LEVEL 2: MEDIUM (Local Police, Corporate Surveillance, Employer)           │
│  ───────────────────────────────────────────────────────────────────────    │
│  Strategy: Two-phone strategy with all mitigations                         │
│  Effort:    5+ hours/week                                                  │
│  Cost:      ~$1,800/year                                                   │
│  Protection: 80% against Level 2 adversaries                               │
│  Additional actions:                                                        │
│    □ Phone A: Burner flip phone, cash SIM, faraday bag                     │
│    □ Phone B: GrapheneOS, Wi-Fi only, faraday bag                          │
│    □ Never carry both phones together                                       │
│    □ Never use Phone B at home or work                                      │
│    □ Replace Phone A every 90 days                                          │
│    □ Replace Phone B every 6-12 months                                      │
│                                                                             │
│  LEVEL 3: HIGH (Federal LE, Intelligence Agencies)                          │
│  ───────────────────────────────────────────────────────────────────────    │
│  Strategy: No electronic strategy is sufficient                             │
│  Effort:    Maximum                                                         │
│  Protection: &lt;25%                                                           │
│  Actions:                                                                   │
│    □ Assume all devices are compromised                                     │
│    □ Use offline communication (dead drops, pre-arranged codes)             │
│    □ Face-to-face meetings in random public locations                       │
│    □ No electronic devices for sensitive communications                     │
│    □ Consult a lawyer and security professional                             │
│    □ Accept that even these methods have risks                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
</pre></div>

---

## Card 2: Operational Security Rules (The Ten Commandments)

<div class="ref-card"><pre>
┌─────────────────────────────────────────────────────────────────────────────┐
│              OPERATIONAL SECURITY RULES - THE TEN COMMANDMENTS              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  # │ RULE                                    │ CONSEQUENCE OF BREAKING     │
│ ───┼─────────────────────────────────────────┼───────────────────────────── │
│  1 │ NEVER carry both phones at the          │ Both phones linked forever   │
│    │ same time                                │                             │
│  2 │ NEVER connect Phone B to home Wi-Fi     │ Identity linked to Phone B   │
│  3 │ NEVER power on Phone B at home          │ Home SSID leaked via probe   │
│  4 │ Phone A has NO apps, NO accounts        │ App metadata leaks identity  │
│  5 │ Phone A SIM purchased with CASH         │ Carrier subpoena reveals you │
│  6 │ Phone A replaced every 30-90 DAYS       │ Historical exposure builds   │
│  7 │ Phone B Signal uses BURNER NUMBER       │ Contact graph exposed        │
│  8 │ Phone B NEVER takes photos              │ EXIF GPS + device ID leaked  │
│  9 │ FARADAY BAGS for transport              │ MAC captured at transit      │
│ 10 │ DESTROY Phone A before replacing        │ Forensic recovery possible   │
│                                                                             │
│  REMEMBER: There is no "just this once."                                    │
│  One mistake collapses the entire strategy.                                 │
│                                                                             │
│  Sign: ______________________________  Date: ________________              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
</pre></div>

---

## Card 3: Failure Recovery Procedures

<div class="ref-card"><pre>
┌─────────────────────────────────────────────────────────────────────────────┐
│                      FAILURE RECOVERY PROCEDURES                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  IF YOU CARRIED BOTH PHONES TOGETHER:                                       │
│  ──────────────────────────────────────────────────────────                 │
│  Situation: Tower logs now show co-location.                                │
│  Action:    Both phones are compromised. Destroy both immediately.          │
│  Recovery:  Purchase new Phone A and new Phone B. Start fresh.              │
│  Prevention: Never leave home with both phones. Leave one in a locked       │
│              location.                                                      │
│                                                                             │
│  IF YOU CONNECTED PHONE B TO HOME WI-FI:                                    │
│  ──────────────────────────────────────────────────────────                 │
│  Situation: ISP logs now link Phone B's MAC to your name and address.       │
│  Action:    Phone B is permanently burned. Destroy it immediately.          │
│  Recovery:  Purchase new Phone B. Replace faraday bags (bags may have       │
│             been contaminated). Do NOT use old devices.                      │
│  Prevention: Never turn on Phone B within 1 km of home or work.             │
│                                                                             │
│  IF YOU TOOK A PHOTO WITH PHONE B:                                          │
│  ──────────────────────────────────────────────────────────                 │
│  Situation: EXIF metadata (GPS, device ID, timestamp) is embedded in the    │
│             photo. If shared, the device is identified.                      │
│  Action:    Delete the photo immediately. If shared, request deletion.      │
│             Assume the device is burned if the photo cannot be recalled.     │
│  Recovery:  If photo was shared outside direct Signal (uploaded, MMS, etc.) │
│             replace Phone B. If photo was deleted unshared, continue        │
│             with heightened caution.                                         │
│  Prevention: Disable camera physically (tape) and in OS settings.           │
│                                                                             │
│  IF YOU FORGOT THE FARADAY BAG:                                              │
│  ──────────────────────────────────────────────────────────                 │
│  Situation: Phone B's Wi-Fi chipset scanned and recorded nearby BSSIDs.     │
│  Action:    If Phone B was near home, work, or other identity-linked        │
│             locations, the chipset cache now contains geolocatable BSSIDs.  │
│  Recovery:  No recovery — chipset memory cannot be wiped. Replace Phone B.  │
│  Prevention: Attach faraday bag to phone case so you cannot leave without   │
│              it. Keep a spare bag in car/bag.                               │
│                                                                             │
│  IF YOU USED THE SAME SIGNAL ACCOUNT ON BOTH PHONES:                        │
│  ──────────────────────────────────────────────────────────                 │
│  Situation: Signal servers now link both devices to the same account.       │
│  Action:    You cannot unlink accounts. Create a new burner account for     │
│             Phone B. Do not re-register the old number on Phone B.          │
│  Recovery:  If you only used the same account briefly, delete the account   │
│             and create a new one. The old account's metadata is still on     │
│             Signal's servers.                                                │
│  Prevention: Use a unique burner number for each phone's Signal account.    │
│                                                                             │
│  GENERAL RULE: When in doubt, destroy and replace.                          │
│  A compromised device cannot be un-compromised.                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
</pre></div>

---

## Card 4: Weekly Privacy Checklist

<div class="ref-card"><pre>
┌─────────────────────────────────────────────────────────────────────────────┐
│                       WEEKLY PRIVACY CHECKLIST                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DAILY (2 minutes):                                                         │
│  □ Verify Phone B is in faraday bag when not in active use                  │
│  □ Check that Phone A is not in the same bag as Phone B                     │
│  □ Verify Phone A is powered off or in faraday bag when at home             │
│  □ Confirm you did not carry both phones together                           │
│                                                                             │
│  WEEKLY (15 minutes):                                                       │
│  □ Check OS updates for Phone B (GrapheneOS updates)                        │
│  □ Check VPN client is connected and working                                │
│  □ Verify Wi-Fi/BT scanning is still disabled on Phone B                    │
│  □ Check that MAC randomization is enabled on Phone B                       │
│  □ Review app permissions on Phone B (deny any new requests)                │
│  □ Test faraday bag (call Phone B while bagged)                             │
│  □ Check for any photos taken on Phone B (delete immediately)               │
│  □ Verify Signal number is still the burner number                          │
│                                                                             │
│  MONTHLY (30 minutes):                                                      │
│  □ Review threat model — has your situation changed?                        │
│  □ Check Phone A replacement schedule (is it time?)                         │
│  □ Check burner SIM expiration dates                                        │
│  □ Review public Wi-Fi locations for consistency (too many same places?)    │
│  □ Rotate public Wi-Fi locations if pattern emerged                         │
│  □ Check for firmware updates for both phones                               │
│  □ Test both faraday bags (not just Phone B's)                              │
│  □ Review any OpSec incidents — did anything go wrong?                      │
│                                                                             │
│  QUARTERLY (2 hours):                                                        │
│  □ Replace Phone A and SIM                                                  │
│  □ Replace Phone B if on 6-month cycle                                      │
│  □ Replace or retest faraday bags                                           │
│  □ Review all accounts linked to Phone B (are any identity-linked?)         │
│  □ Review Signal contact list — any contacts who could identify you?        │
│  □ Update threat model worksheet                                            │
│  □ Review carrier data retention policies (any changes?)                    │
│  □ Review recent legal developments (any new surveillance laws?)            │
│                                                                             │
│  CONTACT INFO:                                                              │
│  Emergency contact (trusted person): ________________________               │
│  Lawyer: _____________________________________________                      │
│  Backup location for devices: ________________________                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
</pre></div>

---

## Card 5: Decision Tree Summary

<div class="ref-card"><pre>
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SHOULD YOU USE TWO PHONES? DECISION TREE                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│                          ┌─────────────┐                                    │
│                          │   START     │                                    │
│                          └──────┬──────┘                                    │
│                                 │                                           │
│                                 ▼                                           │
│          Do you face targeted surveillance from                             │
│          police, employer, or a stalker?                                     │
│                                 │                                           │
│                 ┌───────────────┴───────────────┐                           │
│                 │ YES                           │ NO                        │
│                 ▼                               ▼                           │
│     Will you ever need to          ┌─────────────────────┐                  │
│     hand over your primary         │ USE SINGLE PHONE    │                  │
│     phone at a border or           │ (de-Googled + Signal│                  │
│     to law enforcement?            │ + VPN)              │                  │
│                 │                  │                     │                  │
│        ┌────────┴────────┐        │ 80% of benefit       │                  │
│        │ YES             │ NO     │ 10% of effort       │                  │
│        ▼                 ▼        └─────────────────────┘                  │
│ ┌──────────────┐  Will you accept                                          │
│ │ TWO PHONES   │  extreme OpSec?                                            │
│ │ REQUIRED     │  (no home Wi-Fi,                                          │
│ └──────────────┘  faraday bags,                                             │
│        │          burner SIMs)?                                             │
│        │              │                                                     │
│        └──────┬───────┘                                                     │
│               │                                                             │
│      ┌────────┴────────┐                                                    │
│      │ YES             │ NO                                                 │
│      ▼                 ▼                                                     │
│ ┌──────────────────┐  ┌──────────────────────┐                              │
│ │ IMPLEMENT        │  │ SINGLE PHONE + MAX   │                              │
│ │ MITIGATED        │  │ OpSec                │                              │
│ │ TWO-PHONE STRAT  │  │ (Signal, VPN, no     │                              │
│ └──────────────────┘  │ Google, strict perms) │                              │
│ Expected privacy:      └──────────────────────┘                              │
│ 70-85% against         Expected privacy:                                    │
│ Level 2 adversaries    60-70% against                                       │
│ (local police)         Level 2 adversaries                                  │
│                                                                             │
│ Expect failure          Adequate for most                                   │
│ against state actors    non-state threats                                   │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────────┐ │
│ │ KEY TAKEAWAY:                                                           │ │
│ │ Two phones are essential for border crossing and active threats.        │ │
│ │ For normal citizens, a single de-Googled phone is sufficient.           │ │
│ │ Two phones increase OpSec failure risk without corresponding benefit    │ │
│ │ for users without a specific threat.                                    │ │
│ └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
</pre></div>
