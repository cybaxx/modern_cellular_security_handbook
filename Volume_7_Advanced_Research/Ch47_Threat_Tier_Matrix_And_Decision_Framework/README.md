# Chapter 47: Threat Tier Matrix and Decision Framework

The preceding 46 chapters have established a detailed forensic picture of how phones are tracked, who does the tracking, and what mitigations exist. The problem with detailed analysis is that it can paralyze. Readers who have absorbed the full scope of surveillance capabilities sometimes emerge with the conclusion that privacy is impossible — and stop trying entirely. That conclusion is wrong, and it is dangerous.

This chapter exists to answer one question clearly: **given your specific situation, what should you actually do?**

The answer is structured as a tiered matrix and a decision flowchart. The matrix maps threat actors to recommended strategies. The flowchart guides you through the decision in under five minutes. Together they replace hours of research with a specific, actionable answer.

---

## The Threat Tier System

Not all adversaries are equal. The surveillance capabilities of an advertising network, a stalker ex-partner, a local police department, a federal agency, and a nation-state intelligence service are radically different — in technical capability, legal authority, resource availability, and motivation. Applying the same strategy against all of them produces either over-engineering (for lower threats) or catastrophic under-preparation (for higher threats).

The tier system below is a synthesis of the adversary models documented in Volume 3. Each tier is defined by the capabilities and resources available to that class of adversary, not by their specific identity. A well-resourced private investigator may operate at Tier 2. A poorly-resourced federal agency may not exceed Tier 3 in practice. Use the tier that matches the actual capabilities you are facing, not the institutional label.

---

## The Five-Tier Threat Matrix

### Tier 0 — Passive Commercial Surveillance

**Who this is:** Advertisers, data brokers, analytics companies, social media platforms, retail loyalty programs.

**Capabilities:**
- Device advertising IDs (IDFA, GAID)
- App-level location and behavior tracking
- Third-party cookie tracking and browser fingerprinting
- Cross-app data sharing and identity graph construction
- Purchase history, location history, and content consumption patterns

**What they cannot do:**
- Access carrier records (no legal authority)
- Issue subpoenas or warrants
- Deploy Stingrays or conduct active RF surveillance
- Compel account disclosure from other companies

**Primary data channels:** The apps on your phone, the websites you visit, and the data brokers that aggregate purchased records.

**Recommended Strategy: Citizen Max (Single Phone)**

| Action | Why |
|---|---|
| Install GrapheneOS or use iPhone with Lockdown Mode | Limits ad tracking APIs; restricts background location access |
| Revoke location from all apps except essential navigation | Location is the highest-value commercial data point |
| Switch to Signal for all messaging | Eliminates in-app behavioral tracking from commercial messengers |
| Use Firefox + uBlock Origin or Brave | Blocks ~95% of third-party tracking scripts |
| Use encrypted DNS (1.1.1.1 or Quad9) | Prevents ISP from selling your DNS query log to data brokers |
| Opt out of major data brokers (DeleteMe or manual) | Removes existing profiles; reduces future aggregation |

**Time to implement:** 2–3 hours. **Ongoing effort:** 10 minutes per week. **Cost:** $5–10/month (VPN).

---

### Tier 1 — Targeted Commercial and Semi-Institutional Surveillance

**Who this is:** Abusive ex-partners using commercial stalkerware; employers with MDM-managed devices; schools with device management profiles; landlords or family members with physical access to devices; private investigators using commercial lookup tools.

**Capabilities:**
- Commercial stalkerware (mSpy, FlexiSPY, Hoverwatch) — requires brief physical access to target device
- Employer MDM profiles — full device visibility if profile is installed
- Commercial people-search sites, reverse phone lookup, property records
- Physical access to device without user knowledge
- "Shoulder surfing" and password observation

**What they cannot do:**
- Access carrier CDRs without legal process
- Deploy cellular interception equipment (IMSI catchers) — illegal without authorization
- Issue subpoenas or warrants (private parties)
- Compel platform disclosure from carriers or app providers

**Recommended Strategy: Citizen Max + Device Hygiene**

All Tier 0 actions apply, plus:

| Action | Why |
|---|---|
| Never allow untrusted physical access to your phone | Stalkerware requires approximately 90 seconds of physical access to install |
| Use a strong PIN or passphrase, not biometric | Under duress, biometric unlock can be compelled physically; a PIN cannot |
| Audit installed apps periodically (Settings > Apps) | Stalkerware often runs under a disguised process name |
| If employer-managed device: use a separate personal device for private communications | MDM profiles give employers complete visibility including encrypted messaging apps |
| If stalkerware is suspected: factory reset without backup restore | Backup restores re-install stalkerware; start completely clean |
| Secure your carrier account with a port-out PIN | Prevents SIM swap attacks that redirect your SMS |

**Time to implement:** 3–4 hours. **Ongoing effort:** 20 minutes per week. **Cost:** Same as Tier 0.

---

### Tier 2 — Institutional Surveillance (Local and State Level)

**Who this is:** Local police departments, county sheriffs, state police, civil litigants with subpoena power, insurance investigators, process servers.

**Capabilities:**
- Administrative subpoenas to carriers (CDRs, subscriber identity, tower records)
- Administrative subpoenas to app providers (account records, login history, IP logs)
- Cell tower dump orders (all devices that hit a specific tower in a time window)
- Basic IMSI catcher deployment (available to most law enforcement agencies)
- Geofence warrants (all devices in a geographic area during a time window)
- Device seizure and forensic extraction with warrant
- Standard GPS tracker deployment on vehicles

**What they cannot do (practically):**
- Real-time access to encrypted message content (Signal, iMessage end-to-end)
- Access to data outside their jurisdiction without MLAT process
- Deploy sophisticated zero-day exploits (cost-prohibitive for most local agencies)

**Recommended Strategy: Two-Phone Strategy (Mitigated)**

All Tier 0 and Tier 1 actions apply, plus the full two-phone architecture documented in Volume 6:

| Component | Requirement | Failure Mode |
|---|---|---|
| Phone A | Prepaid flip phone; cash-purchased SIM; no apps, no accounts | If Phone A carries any linked accounts, subpoena to carrier yields identity |
| Phone B | GrapheneOS on Pixel; Wi-Fi only (no SIM); purchased with cash; no Google accounts | If Phone B ever connects to home or work Wi-Fi, ISP record links device to identity |
| Physical separation | Never carry both phones simultaneously | Tower co-location data links devices within 90 days |
| Faraday bags | Required during transport for both devices | Wi-Fi probe requests leak home SSID to passive scanners |
| SIM rotation | Phone A SIM replaced every 30–90 days | Extended SIM history creates trackable pattern |
| Network discipline | Phone B uses only public Wi-Fi at non-predictable locations | Predictable location pattern is itself identifying |

**Expected protection:** 70–85% against Tier 2 adversaries. **Annual cost:** ~$1,800. **Ongoing effort:** Significant — see Chapter 38 (Unbreakable OpSec Rules) and Appendix G.

**Critical warning:** The two-phone strategy fails catastrophically against Tier 2 adversaries if any single rule is broken. One home Wi-Fi connection from Phone B ends the strategy. One instance of carrying both phones together links the devices. Partial implementation provides less protection than a well-configured single phone, because it creates a false sense of security.

---

### Tier 3 — Federal and National-Level Surveillance

**Who this is:** Federal law enforcement (FBI, DEA, Homeland Security), national intelligence agencies (NSA, GCHQ, Five Eyes partners), prosecutors with grand jury subpoena authority, regulatory agencies with broad investigative powers.

**Capabilities (above Tier 2):**
- National Security Letters (NSLs) — compel disclosure without prior court review, with mandatory gag order; NSLs can be challenged post-issuance under 18 U.S.C. § 3511, but challenges are rare and the gag order typically prevents the recipient from disclosing receipt
- Section 702 FISA collection — bulk interception of internet communications
- CALEA-compliant real-time access to call metadata at carriers
- Sophisticated IMSI catchers (Hailstorm, dirtbox aircraft-based systems)
- International MLAT requests for foreign-held data
- Covert device exploitation (Cellebrite UFED, GrayKey, zero-day implants)
- Long-term physical and electronic surveillance operations
- Cross-agency data sharing (DEA's Special Operations Division, etc.)

**What they cannot do (with difficulty):**
- Break strong end-to-end encryption at rest on a locked, modern device without exploit
- Retroactively recover deleted Signal messages (no server-side storage)
- Rapidly correlate anonymized data without legal process to intermediate parties

**Recommended Strategy: Two-Phone Strategy + Legal Counsel + Opsec Training**

The two-phone strategy documented in Volume 6, executed with perfect discipline, provides meaningful protection against some Tier 3 capabilities (CDR subpoenas, standard device seizure). It does not protect against:

- Zero-day exploits targeting GrapheneOS or the underlying Android firmware
- Physical implants or covert device access
- Metadata analysis at national scale using NSA collection infrastructure
- Compelled disclosure from third parties (Signal, ProtonMail) via National Security Letter

At Tier 3, the hard truth is this:

> **No electronic strategy is sufficient as a primary defense. Legal protection, operational security training, and professional counsel are not supplements — they are the primary strategy.**

If you face a Tier 3 adversary, contact the Electronic Frontier Foundation, the ACLU, or a First Amendment attorney before taking any technical action. The legal landscape matters as much as the technical one. Understand your rights before trying to exercise them.

---

### Tier 4 — Nation-State / Intelligence Service Adversaries

**Who this is:** Foreign intelligence services targeting dissidents, journalists, activists, or persons of national security interest; domestic intelligence agencies with no effective judicial oversight; non-state actors with state-level resources (some cartels, terrorist organizations with significant technical infrastructure).

**Capabilities:**
- Persistent, targeted device compromise (Pegasus, Predator, Triangulation-class implants)
- Real-time location tracking via carrier-level access (in home jurisdiction)
- Physical surveillance teams
- Social engineering and human intelligence operations targeting your contacts
- Jurisdiction-immune collection (no legal process required)
- Device exploitation across all platforms including GrapheneOS on patched hardware

**What they cannot do:**
- Break Signal's encryption protocol (no known attack; legal process required)
- Retroactively recover end-to-end encrypted messages that were never on their servers
- Simultaneously maintain full coverage without significant resource commitment

**Recommended Strategy: There is no electronic strategy.**

| Reality | Implication |
|---|---|
| Your phone is compromised the moment it is targeted | All data on the device, including encrypted apps, is visible to the operator |
| Legal process is irrelevant in their jurisdiction | Carrier subpoenas, warrants, and court orders do not protect you |
| Physical surveillance accompanies digital surveillance | Your location is known independent of your phone |
| Your contacts are also targets | Even if your device is clean, someone in your network is not |

Against a Tier 4 adversary, the goal shifts from concealment to limitation of damage:
- **Face-to-face only** for sensitive communications, in locations not associated with your routine
- **No electronic record** of sensitive discussions — paper notes destroyed after use
- **Legal protection in a third country** — residence, legal counsel, and operations in a jurisdiction outside the adversary's reach
- **Source compartmentalization** — the fewer people who know anything, the fewer entry points for infiltration

This is not paranoia. It is the operational baseline that journalists, activists, and dissidents operating in hostile jurisdictions have documented through hard-won experience.

---

## The Decision Flowchart

Use the following flowchart to identify your tier and strategy in under five minutes.


> *See the figure generated below.*


---

## The Consolidated Reference Matrix

The table below summarizes all five tiers in a single reference. Print this page. Keep it with your equipment.

| | **Tier 0** | **Tier 1** | **Tier 2** | **Tier 3** | **Tier 4** |
|---|---|---|---|---|---|
| **Adversary** | Advertisers, data brokers | Stalkers, employers, PIs | Local/state police | Federal LE, intelligence | Nation-state |
| **Primary Tool** | Ad tracking, app data | Stalkerware, MDM | CDRs, tower dumps, IMSI catchers | NSLs, CALEA, zero-days | Pegasus-class implants, physical surveillance |
| **Legal Authority** | None | None (civil only) | Subpoenas, warrants | Grand jury, FISA, NSLs | None required (their jurisdiction) |
| **Strategy** | Citizen Max | Citizen Max + device hygiene | Two-phone (Volume 6) | Two-phone + legal counsel | No electronic strategy |
| **Cost/Month** | $5–10 | $5–10 | ~$150 | ~$150 + legal fees | N/A |
| **Effort/Week** | 10 min | 20 min | 5+ hours | 5+ hours | N/A |
| **Expected Protection** | 90% | 85% | 70–85% | 40–60% | <10% |
| **Key Failure Mode** | Excessive app permissions | Physical device access | One home Wi-Fi connection from Phone B | Zero-day exploit; NSL | Compromise is assumed |
| **Who Should Use This** | Everyone | Specific situation applies | Journalists, activists, DV survivors, frequent border crossers | Federal targets, national security whistleblowers | Dissidents in authoritarian regimes; seek professional help |

---

## Using This Framework Correctly

### Tier selection is not permanent

Your threat model changes. A journalist who becomes a federal target moves from Tier 2 to Tier 3 overnight. A person going through a divorce may temporarily move from Tier 0 to Tier 1 and back. Revisit this framework when your situation changes significantly. The monthly review item in Appendix G Card 4 ("Review threat model — has your situation changed?") exists for exactly this reason.

### Higher tiers include lower tiers

Every action listed in Tier 0 applies at Tier 1, 2, 3, and 4. The tiers are cumulative. A Tier 2 user who does not implement the Tier 0 basics is not running a Tier 2 strategy — they are running a broken strategy that fails at the most basic level. Do not skip the foundation.

### Protection percentages are estimates

The protection percentages in the matrix represent approximate effectiveness against the stated adversary tier under ideal implementation. Real-world effectiveness is lower due to operational errors, unpatched vulnerabilities, and adversary capability growth. Do not treat them as guarantees. Treat them as comparative guidance: a Tier 2 strategy offers meaningfully more protection against a Tier 2 adversary than a Tier 0 strategy does, but it is not impenetrable.

### The most common mistake

Most people who seek out this handbook over-estimate their threat tier. They read about Stingrays and FISA collection and conclude they need a Tier 3 strategy for what is actually a Tier 0 threat model. This mismatch produces burnout, abandonment of all privacy practices, and the worst possible outcome: a person who has convinced themselves that privacy is impossible and has therefore stopped trying.

The second most common mistake is under-estimating threat tier in the opposite direction: a domestic violence survivor who has not recognized that their abuser represents a Tier 1 threat model, and who is therefore running a Tier 0 strategy against a stalkerware installation they do not know exists.

Accurate threat modeling is the most important privacy skill. Use this framework honestly. Use the right tier for your actual situation. Then implement that tier with discipline.

---

## A Note on Expert Alignment: Michael Bazzell

Michael Bazzell — former FBI Special Agent (Cyber Division), author of *Extreme Privacy* (5th ed., 2025), and longtime host of the Privacy, Security & OSINT Show — independently arrives at a tiered framework broadly consistent with this chapter. His key contributions and divergences are worth noting.

**Alignment:** Bazzell recommends GrapheneOS exclusively for privacy-focused mobile use, specifically on Google Pixel hardware (for the Titan M security chip and verified boot support). His two-phone approach in *Extreme Privacy* Section Five mirrors the Tier 2 strategy here. His emphasis on data broker removal as a foundational, high-impact step before device hardening is a critical point that Appendix I addresses directly.

**Divergence — VPN selection:** Bazzell has specifically recommended Private Internet Access (PIA) as a VPN that is affordable, simple, and widely used enough to avoid standing out. This contrasts with the Mullvad and ProtonVPN recommendations in Chapter 28, which prioritize non-US jurisdiction and no-account registration. Both approaches are defensible; they reflect different threat models. Mullvad (Sweden) and ProtonVPN (Switzerland) provide jurisdictional distance from US legal process. PIA (US) provides familiarity, lower cost, and in Bazzell's view sufficient protection for Tier 0 threats where jurisdiction is not the primary concern. High-risk users should prefer non-US jurisdiction. Normal citizens may find PIA sufficient.

**Divergence — minimum viable approach:** Bazzell's "minimum viable" entry point begins with data broker removal rather than device hardening — a position supported by the observation that your phone's cellular metadata and publicly purchased commercial data are often more actionable to adversaries than whether you use Brave or Firefox. See Appendix I for the handbook's minimum viable stack, now updated to reflect this priority.

---

## Legal References

- 18 U.S.C. § 2709 — National Security Letter statutory authority
- 18 U.S.C. § 3511 — NSL judicial review and challenge procedures
- 50 U.S.C. § 1881a — FISA Section 702 collection authority
- Communications Assistance for Law Enforcement Act (CALEA), 47 U.S.C. §§ 1001–1010
- Signal, "Government Requests," signal.org/bigbrother/ — primary-source documentation of Signal's subpoena response (2016 Eastern District of Virginia: only data produced was account creation timestamp and last connection date)
