# Chapter 17: Adversary Models & Success Rates

## Overview

The effectiveness of the two-phone strategy is not absolute — it depends entirely on the capabilities, resources, and legal authority of the adversary you face. A strategy that works perfectly against an advertising network may fail catastrophically against a federal law enforcement investigation. Understanding which adversaries you can defeat, which you can merely delay, and which will inevitably deanonymize you is essential to making informed decisions about OpSec investment.

This chapter defines three adversary levels based on capability and legal authority. For each level, we examine the likely success rate against each device in the two-phone strategy, the conditions under which the strategy succeeds, and the conditions under which it fails completely.

---

## Adversary Level 1: Low-Risk

**Adversaries included: Advertisers, data brokers, casual stalkers, corporate tracking systems, analytics platforms.**

Low-risk adversaries are characterized by limited legal authority, no physical surveillance capability, and reliance on voluntarily disclosed data or publicly available information. They cannot compel carriers, ISPs, or service providers to disclose data. They operate within the bounds of commercial data collection — cookies, advertising IDs, IP logging, device fingerprinting, purchase history correlation.

### Threat Analysis

| Goal | Phone A (Flip) | Phone B (GrapheneOS) | Computer | Overall Success Rate |
|------|---------------|---------------------|----------|---------------------|
| Track browsing habits | N/A (no browser) | Low (GrapheneOS + VPN + Tor Browser) | Medium (browser fingerprint, even with Tor) | 20% |
| Build advertising profile | Medium (SMS metadata from carrier data brokers) | Low (no Google services, no advertising ID)[^1] | Medium (IP geolocation, browser fingerprint) | 30% |
| Correlate devices | Low (requires carrier access which data brokers lack) | Low | Low | 10% |
| Identify real identity | Low | Low | Low (unless residential ISP used) | 15% |

### Success Conditions

The two-phone strategy is highly effective against Level 1 adversaries. The reasons:

- **Phone B has no Google Play Services.** Google's advertising ID system is the backbone of mobile ad tracking. Without it, advertising networks cannot build a persistent profile of Phone B's user.[^2] They fall back to IP geolocation and browser fingerprinting, which are less precise and can be disrupted through VPN and Tor Browser.

- **Phone A is not used for browsing.** The flip phone has no web browser, no apps, no advertising SDKs. The only data available to advertisers is SMS metadata, which is less valuable than browsing history or location data.

- **Compartmentalization works.** Level 1 adversaries lack the legal authority to connect Phone A's carrier data with Phone B's network data. The two phones appear as unrelated devices.

### Failure Conditions

The strategy fails against Level 1 adversaries only if:
- Phone B or Computer is used on a residential ISP, allowing IP-based geolocation to identify the user's home address
- Phone B has any Google services installed, enabling Google's advertising system
- The user logs into any identity-linked service (bank, social media, work email) on Phone B or Computer

### Verdict

**Effective.** For low-risk adversaries, even a simplified version of the two-phone strategy (single de-Googled phone + Signal + VPN) provides 90% of the benefit with 10% of the effort. The full two-phone strategy with all mitigations is overkill for this threat level but provides near-complete protection.

---

## Adversary Level 2: Medium-Risk

**Adversaries included: Local police with court order authority, private investigators with legal process, civil litigation discovery, corporate security teams with subpoena power.**

Medium-risk adversaries have legal authority to compel data disclosure from carriers, ISPs, and service providers. They can obtain court orders for subscriber identity, call detail records, tower data, and ISP logs.[^3] They typically have limited resources for physical surveillance and limited technical capability for zero-day exploitation.

### Threat Analysis

| Goal | Phone A (Flip) | Phone B (GrapheneOS) | Computer | Overall Success Rate |
|------|---------------|---------------------|----------|---------------------|
| Obtain subscriber identity | 100% (carrier subpoena reveals subscriber from billing info) | 0% (no SIM, no carrier account) | 100% (ISP subpoena, if used at home) | 67% (2 of 3 devices) |
| Obtain location history | 100% (tower dump + timing advance records from carrier) | 70% (Wi-Fi geolocation if public networks are used) | 0% (unless IP logged at specific location) | Variable |
| Correlate Phone A to Phone B | 80% (if carried together or both used at same home address) | | | High |
| Extract device contents (seizure) | 100% (flip phone, no encryption) | Variable (GrapheneOS encryption resists Cellebrite with strong passphrase)[^4] | Variable (full-disk encryption quality depends on OS and passphrase) | Depends on seizure timing and encryption quality |

### Success Conditions

The strategy works against Level 2 adversaries only if strict OpSec is followed:

- **Phone B never uses a residential ISP.** If Phone B connects only through public Wi-Fi behind a VPN, the ISP subpoena reveals nothing.[^5] The adversary obtains only the public Wi-Fi's IP address, which does not link to the user's identity.

- **Phone B never enters the home address.** Wi-Fi BSSID geolocation cannot link Phone B to the home if Phone B is never within range of the home's routers.

- **Phones A and B are never carried together.** Tower dumps reveal Phone A's IMSI at various locations, but without Phone B's identifiers in the same dump, correlation is impossible.

- **Phone A uses a burner SIM purchased with cash.** The carrier subpoena reveals the subscriber records for the SIM. If the SIM was activated anonymously, the subpoena returns "subscriber: unknown."

### Failure Conditions

The strategy fails completely against Level 2 adversaries if:

- **Phone B ever touches home Wi-Fi.** A single connection creates a permanent link between Phone B's MAC address and the ISP subscriber identity. The adversary subpoenas the ISP, obtains the subscriber name and address, and Phone B is deanonymized.[^6]

- **Phones A and B are carried together.** A tower dump at a location where both phones are present correlates their data. From there, the adversary can request a §2703(d) order for Phone B's network activity, leading to full deanonymization.

- **Phone A is used to call an identity-linked number.** The CDR shows calls to a known associate, a workplace, or a family member. The adversary identifies the user through the called party.

- **Phone A uses a postpaid or registered prepaid SIM.** The carrier records immediately reveal the subscriber identity, making Phone A useless for anonymity.

### Verdict

**Partially effective.** Against a local police investigation with court order authority, the two-phone strategy provides meaningful protection — but only if every mitigation is followed without exception. A single OpSec failure (home Wi-Fi, carrying phones together, calling an identity-linked number) collapses the entire strategy.

---

## Adversary Level 3: High-Risk

**Adversaries included: Federal law enforcement (FBI, DHS, DOJ), intelligence agencies (NSA, CIA, GCHQ, DGSE, MSS), state-level cyber police units, well-resourced nation-state actors.**

High-risk adversaries combine full legal authority, extensive technical capabilities (including zero-day exploitation), physical surveillance resources, and financial tracking. They operate within legal frameworks that include national security letters, FISA court orders, CALEA intercepts,[^7] and international cooperation agreements. They also operate outside legal frameworks when necessary.

### Threat Analysis

| Goal | Phone A (Flip) | Phone B (GrapheneOS) | Computer | Overall Success Rate |
|------|---------------|---------------------|----------|---------------------|
| Obtain subscriber identity | 100% | 0% (no SIM) | 100% (ISP backdoor or subpoena) | 67% |
| Obtain real-time location | 100% (CALEA intercept, Stingray)[^8] | 100% (Wi-Fi geolocation + physical surveillance) | 100% (ISP NetFlow + IP geolocation) | 100% (all devices) |
| Correlate all devices | 100% (tower dumps, ISP logs, surveillance cameras, financial records, associates' devices) | | | 100% |
| Defeat encryption | 100% (flip phone, no encryption) | Variable (GrapheneOS + strong passphrase resists most forensic tools; "rubber hose cryptanalysis" is the limit)[^9] | Variable (Qubes/Tails resists; Windows/Mac does not) | Device-dependent |
| Zero-day exploitation | 100% (baseband is exposed and unpatched) | 80% (baseband if cellular present; 0% if Wi-Fi only + hardened kernel) | 70% (browser, email client are high-value targets) | High |

### Detailed Analysis

**Identity Discovery (67% success, always two of three devices):**

Phone A is always compromised for identity. The carrier has the SIM's subscriber records. Even with a cash-purchased burner SIM, an intelligence agency can identify the purchaser through store surveillance cameras, license plate readers, and financial transaction tracking (see residual risks in Chapter 42).

Phone B (no SIM) has no carrier link. But this protection is temporary. Once Phone A's identity is known, physical surveillance identifies the user's movements, and Phone B is located through observation.

The Computer is always compromised if it ever uses a residential ISP. Even if the computer uses only public Wi-Fi, a state actor can identify the user through financial tracking (purchases at the coffee shop), surveillance cameras, or correlation with Phone A's movements.

**Real-Time Location (100% success, all devices):**

A state actor with CALEA authority tracks Phone A in real time through carrier-level intercept.[^10] Physical surveillance teams follow the user. Tower dumps provide historical location data. Wi-Fi BSSID geolocation databases provide Phone B's location history. For the Computer, ISP NetFlow data provides IP geolocation.

**Device Correlation (100% success):**

State actors operate at a level of data integration that private investigators cannot match. They combine:
- Carrier tower dumps for Phone A
- ISP logs for the Computer
- Wi-Fi geolocation database queries for Phone B
- Financial records (credit card purchases, ATM usage)
- Physical surveillance (camera feeds, license plate readers)
- Associates' devices (identifying unknown phone numbers through call records)

With these data sources, they can correlate any two devices belonging to the same person, regardless of compartmentalization attempts.

**Encryption Defeat (variable):**

GrapheneOS with a strong passphrase (20+ characters, alphanumeric, uppercase, lowercase, symbols) resists known forensic extraction tools. Cellebrite and GrayKey cannot break AES-256 encryption with adequate key derivation parameters.[^11] However, a state actor has options:
- **Rubber hose cryptanalysis**: Compel the passphrase through legal or coercive means.
- **Evil maid attack**: Install a hardware implant or compromised charger that captures the passphrase on next entry.
- **Side-channel attack**: Exploit electromagnetic emissions, power analysis, or timing variations to recover the encryption key.
- **Zero-day in the bootloader**: Exploit an unpatched vulnerability in the device's boot chain to bypass encryption.

A state actor with unlimited resources and physical access will eventually extract the data. It is a question of time and investment, not feasibility.

### The State Actor Playbook

A state-level adversary does not need to exploit every vulnerability. They follow a proven playbook:

1. **Identify the target.** Through Phone A's carrier, informant, financial tracking, or physical surveillance.

2. **Obtain legal authority.** National security letter, FISA order, or parallel construction through an allied agency.

3. **Collect historical data.** Carrier CDRs, ISP logs, tower dumps, Signal metadata.[^12]

4. **Deploy physical surveillance.** Cameras, trackers, tailing teams. Identify home, work, and patterns.

5. **Correlate devices.** Tower dump + ISP log + Wi-Fi BSSID + physical observation = all devices linked.

6. **Seize devices.** Search warrant for home or work location, or dynamic seizure when target is traveling.[^13]

7. **Forensic extraction.** Cellebrite/GrayKey for non-GrapheneOS devices; parallel construction for GrapheneOS devices or long-term passphrase capture.

8. **Exploit if needed.** Zero-day baseband exploit for phones not physically seized; browser exploit for computer.

### Verdict

**The two-phone strategy does not protect against a state-level adversary.**

This is not a failure of the strategy. No consumer-grade technical strategy protects against a nation-state actor with full legal authority, physical surveillance, and zero-day capabilities. The strategy is effective against the adversaries it was designed for: data brokers, local police, and corporate investigators. Against a state actor, it provides delay and friction, not protection.

For targets of state-level adversaries, the only viable communication strategy involves no electronic devices at all — dead drops, pre-arranged in-person meetings, one-time codes, and face-to-face communication in random public locations without any electronic devices present.

---

## The Compartmentalized Burner Model (Mitigated Architecture)

For users facing Level 2 adversaries with strict OpSec requirements, the original two-phone strategy must be modified. The "Compartmentalized Burner" model adds the following requirements:

### Phone A (Public Face) — Revised

| Original | Revised Requirement | Rationale |
|----------|-------------------|-----------|
| Dumb flip phone | Burner flip phone, purchased with cash | No identity link to carrier |
| Carrier plan (postpaid) | Prepaid SIM, cash purchase, refilled with cash | Anonymous activation |
| Used freely | Faraday bag when not in active use | Prevents tower tracking when idle |
| Kept indefinitely | Destroyed and replaced every 30–90 days | Limits historical exposure |
| Carried with Phone B | Never carried with Phone B | Prevents correlation |

### Phone B (Private Hub) — Revised

| Original | Revised Requirement | Rationale |
|----------|-------------------|-----------|
| Moto G / Pixel (cellular capable) | Pixel + GrapheneOS, cellular radio disabled (Wi-Fi only)[^14] | Eliminates baseband tracking |
| Residential ISP Wi-Fi | Never connected to home or work Wi-Fi | Prevents ISP identity link |
| Public Wi-Fi (coffee shop) | Public Wi-Fi only, with MAC randomization + VPN + Tor | Breaks Wi-Fi geolocation |
| Standard Signal setup | Signal with burner phone number (VoIP or prepaid SIM used once)[^15] | Prevents Signal metadata linking to identity |
| Used anywhere | Never within 1 km of home or work | Prevents physical correlation |
| Carried freely | Faraday bag when traveling to/from use locations | Prevents passive scanning |

### Computer — Revised

| Original | Revised Requirement | Rationale |
|----------|-------------------|-----------|
| Standard OS | Tails OS (USB live boot) or Qubes OS | Amnesiac, no persistent tracking |
| ProtonMail | ProtonMail via Tor (or similar anonymous email) | Prevents IP logging |
| VPN on public Wi-Fi | Tor Browser (or VPN + Tor chain) | Defeats traffic analysis |
| Used at home | Never used at home or work | Prevents ISP identity link |
| Standard browsing | No logging into any identity-linked service | Prevents account correlation |

---

## Success Rate by Adversary Level

| Threat Level | Adversary Example | Strategy Effectiveness | Key Failure Point |
|-------------|-------------------|----------------------|-------------------|
| Low-Risk | Advertisers, data brokers | 90%+ | Residential ISP usage, Google services |
| Medium-Risk | Local police, PI | 80% with full OpSec | Home Wi-Fi, carrying phones together |
| High-Risk | Federal LE, intelligence | <50%, temporary delay | Identity discovery leads to all-device compromise |

---

## Acceptance Criteria

The two-phone strategy, even with all mitigations, reduces but does not eliminate tracking. The decision to use this strategy requires accepting residual risks:

- **Physical surveillance cannot be mitigated.** Cameras, license plate readers, and facial recognition operate independently of device security.
- **A single mistake collapses compartmentalization.** Forgetting the faraday bag, connecting to home Wi-Fi "just once," or carrying both phones together creates a permanent forensic link.
- **Burner SIM purchases leave physical trails.** Store cameras and parking lot license plate readers can link the purchase to the buyer's identity.
- **Zero-day exploits exist.** Baseband, Wi-Fi chipset, and browser vulnerabilities may allow remote compromise of any device.[^16]

For 95% of users concerned about privacy, a single de-Googled phone with Signal, a VPN, and careful OpSec provides 90% of the privacy benefit with 10% of the complexity and risk of the two-phone strategy. The full two-phone strategy with all mitigations is appropriate only for the 5% facing serious adversarial threats.

---

## Conclusion

The two-phone strategy is a threat model, not a guarantee. It is effective against the adversaries it was designed for — data brokers, advertisers, and local law enforcement with limited resources. It provides meaningful but incomplete protection against more capable adversaries with court order authority. It provides only temporary delay against state-level actors.

Understanding your adversary is the first step in OpSec. Do not implement mitigations for a Level 3 adversary if you only face Level 1 threats — the operational burden is too high. Conversely, do not assume that a strategy proven against advertisers will protect you from an FBI investigation.

The choice of strategy must match the threat. For most people, a single de-Googled phone is sufficient. For a few, the full Compartmentalized Burner model is necessary. For the highest-risk targets, no electronic strategy is sufficient.

---

[^1]: Narseo Vallina-Rodriguez et al., "An Analysis of Pre-installed Android Software," IEEE Symposium on Security and Privacy (IEEE S&P 2020). Documents the role of Google Play Services advertising ID in persistent mobile ad tracking and the data collection reduction achieved by removing it. https://ieeexplore.ieee.org/document/9152763

[^2]: GrapheneOS Project, "Features," grapheneos.org/features. Describes removal of Google advertising ID and Play Services tracking components. https://grapheneos.org/features

[^3]: Stored Communications Act, 18 U.S.C. § 2703. Establishes the court order and subpoena standards under which carriers and ISPs must disclose subscriber records, CDRs, and IP logs to law enforcement with appropriate legal authority.

[^4]: Cellebrite, "UFED Ultimate," cellebrite.com. Documents forensic extraction capabilities across encryption states; GrapheneOS full-disk encryption resistance is described in GrapheneOS Project, "Features," grapheneos.org/features.

[^5]: Stored Communications Act, 18 U.S.C. § 2703(d). The "specific and articulable facts" standard requires the government to identify a specific IP address and subscriber; connecting through a public Wi-Fi AP places only that AP's subscriber identity in the responsive records.

[^6]: Stored Communications Act, 18 U.S.C. § 2703. A §2703(d) order compels the ISP to disclose subscriber name and address associated with the IP address assigned at the time of the connection, creating the permanent MAC-to-identity link described.

[^7]: Communications Assistance for Law Enforcement Act (CALEA), 47 U.S.C. §§ 1001–1010 (1994). Grants federal law enforcement the authority to compel real-time interception of communications at the carrier level.

[^8]: EFF, "Surveillance Self-Defense: Street-Level Surveillance — IMSI Catchers/Stingrays," ssd.eff.org. Documents IMSI catcher capabilities and legal use by law enforcement for real-time device location. https://ssd.eff.org/module/street-level-surveillance-imsi-catchers-stingrays

[^9]: Apple Inc., "iOS Security Guide," apple.com/privacy/docs/iOS_Security_Guide.pdf. Describes BFU (Before First Unlock) encryption state where key material is not in memory, which provides the strongest resistance to forensic tools; GrapheneOS implements comparable and in some ways stronger key derivation. https://grapheneos.org/features

[^10]: Communications Assistance for Law Enforcement Act (CALEA), 47 U.S.C. § 1002. Mandates that carriers provide real-time call content and location data to law enforcement under a lawful Title III wiretap order.

[^11]: GrapheneOS Project, "Features," grapheneos.org/features. Documents AES-256 full-disk encryption with hardened key derivation parameters that resist brute-force attacks by known forensic tools including Cellebrite UFED Premium.

[^12]: Signal Foundation, "What Does Signal Know About Me?" signal.org/bigbrother. Documents the account metadata Signal produces under valid legal process: account creation date and last connection date. https://signal.org/bigbrother/

[^13]: Riley v. California, 573 U.S. 373 (2014). Established the warrant requirement for cell phone searches; state actors operating under FISA or national security authority may operate under different standards.

[^14]: GrapheneOS Project, "Features," grapheneos.org/features. Describes the ability to permanently disable the cellular radio at the software level to eliminate baseband attack surface. https://grapheneos.org/features

[^15]: Signal Foundation, "What Does Signal Know About Me?" signal.org/bigbrother. Confirms that the only persistent identifier Signal stores is the registered phone number, making a disposable VoIP or prepaid number the key anonymization measure. https://signal.org/bigbrother/

[^16]: EFF, "Surveillance Self-Defense," ssd.eff.org. Discusses baseband and zero-day vulnerabilities as nation-state-level capabilities beyond the reach of most adversaries. https://ssd.eff.org
