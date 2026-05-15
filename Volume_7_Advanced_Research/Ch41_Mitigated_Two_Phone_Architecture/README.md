# Chapter 41: Mitigated Two-Phone Architecture — The "Compartmentalized Burner" Model

## Overview

The original two-phone strategy, while conceptually sound, contains critical forensic gaps that undermine its effectiveness. This chapter presents the fully mitigated architecture — the "Compartmentalized Burner" model — which addresses every identified vulnerability. This is not a minor revision. It is a fundamental re-architecture that transforms the strategy from security theater into a genuinely robust defense for high-risk users.

## The Six Forensic Gaps and Their Mitigations

### Gap 1: Cellular Network Tracking (Phone A)

**Problem:** Phone A transmits IMSI, IMEI, Cell ID, Timing Advance, and Angle of Arrival to the carrier. These are logged and retained for months or years.[^1] Law enforcement can reconstruct your movement history without a warrant for your device.[^2]

**Mitigation:** Phone A must be a burner device. Purchase with cash. Use a prepaid SIM also purchased with cash. Never register any personal information. Keep the phone inside a verified faraday bag except during active calls. Destroy and replace both phone and SIM every 30–90 days. This limits historical exposure and prevents correlation across long time windows.

### Gap 2: Wi-Fi Layer Tracking (Phone B)

**Problem:** Even without a cellular modem, Phone B broadcasts probe requests containing its MAC address and remembered SSIDs. Wi-Fi geolocation databases map nearby BSSIDs to GPS coordinates with 10–20 meter accuracy.

**Mitigation:** Phone B must never be used at home or work. Enable permanent MAC randomization. Disable Wi-Fi and Bluetooth scanning in the OS. Verify radio status via `adb shell dumpsys`. Transport Phone B in a faraday bag at all times when not in active use. Use public Wi-Fi only — never a residential ISP.

### Gap 3: ISP Identity Linking (Phone B and Computer)

**Problem:** The moment Phone B or the Computer connects to a residential ISP, the IP address is tied to your name and billing address via subscriber records.[^3] A single subpoena to the ISP collapses compartmentalization.

**Mitigation:** Never connect Phone B or the Computer to any network linked to your identity. No home Wi-Fi. No work Wi-Fi. No school Wi-Fi. Use public Wi-Fi (coffee shops, libraries) exclusively, with always-on VPN (cash-paid, no-log provider) and Tor via Orbot for high-risk activities.

### Gap 4: Physical Co-Location

**Problem:** Carrying Phone A and Phone B together — even once — allows correlation via tower dumps, Wi-Fi geolocation, surveillance cameras, and temporal pattern analysis. Once linked, the devices are permanently associated.

**Mitigation:** Never carry both phones simultaneously. Never power on Phone B within one kilometer of home or work. Store both phones in separate faraday bags. Never open the bags within 100 meters of each other. Use Phone B only in random public locations that cannot be tied to your identity.

### Gap 5: Signal Metadata Exposure

**Problem:** Signal encrypts message content but not metadata. Signal's servers record who you talk to, when, and how often.[^4] A court order to Signal reveals your entire contact graph.

**Mitigation:** Register Signal with a burner phone number — either a VoIP number purchased anonymously or a prepaid SIM used once and discarded. Never sync contacts. Never use Signal with any number linked to your identity. Accept that metadata protection is incomplete even with these measures.

### Gap 6: Application and OS Leakage

**Problem:** Camera EXIF data embeds GPS coordinates, timestamps, and device identifiers. Browser fingerprinting leaks configuration details. Apps with unnecessary permissions transmit location and contacts.

**Mitigation:** Disable camera location permissions entirely. Use Scrambled EXIF or MAT2 before sharing any photo. Never take photos with Phone B unless absolutely necessary. Deny all app permissions by default. Use Tor Browser or Tails OS for sensitive browsing. Strip all metadata from shared files.

## Revised Requirements

### Phone A — Revised

| Original | Revised Requirement | Rationale |
|---|---|---|
| Dumb flip phone | Burner flip phone, purchased with cash | No identity link to carrier |
| Carrier plan (postpaid) | Prepaid SIM, cash purchase, refilled with cash | Anonymous activation |
| Used freely | Faraday bag when not in active use | Prevents tower tracking when idle |
| Kept indefinitely | Destroyed and replaced every 30–90 days | Limits historical exposure |
| Carried with Phone B | Never carried with Phone B | Prevents correlation |

### Phone B — Revised

| Original | Revised Requirement | Rationale |
|---|---|---|
| Moto G / Pixel (cellular capable) | Pixel + GrapheneOS, cellular radio disabled (Wi-Fi only) | Eliminates baseband tracking |
| Residential ISP Wi-Fi | Never connected to home or work Wi-Fi | Prevents ISP identity link |
| Public Wi-Fi (coffee shop) | Public Wi-Fi only, with MAC randomization + VPN + Tor | Breaks Wi-Fi geolocation |
| Standard Signal setup | Signal with burner number | Prevents Signal metadata linking |
| Used anywhere | Never within 1 km of home or work | Prevents physical correlation |
| Carried freely | Faraday bag when traveling | Prevents passive scanning |

### Computer — Revised

| Original | Revised Requirement | Rationale |
|---|---|---|
| Standard OS (Windows/Mac/Linux) | Tails OS (USB live boot) or Qubes OS | Amnesiac, no persistent tracking |
| ProtonMail | ProtonMail via Tor | Prevents IP logging |
| VPN on public Wi-Fi | Tor Browser or VPN + Tor chain | Defeats traffic analysis |
| Used at home | Never used at home or work | Prevents ISP identity link |
| Standard browsing | No identity-linked logins (bank, social media, work) | Prevents account correlation |

## The "Zero Location" Configuration

For high-risk users who need absolute location privacy, we define the "Zero Location" configuration — the gold standard for preventing geolocation tracking at every layer.

### Phone A Specification

- Dumb flip phone (4G only — no 5G, no Wi-Fi, no Bluetooth)
- SIM purchased with cash, never registered to a name
- Powered on only inside a faraday bag except for specific calls
- Destroyed and replaced every 30 days
- Never carried near home or work

### Phone B Specification

- No cellular modem (Wi-Fi only)
- GrapheneOS on Pixel (Wi-Fi radio only)
- Never enabled Wi-Fi scanning
- Never connected to any network within one kilometer of home or work
- Used only in public spaces with MAC randomization, VPN, and Tor
- Never takes photos
- Never uses any app requesting location
- Destroyed if ever exposed to law enforcement attention

### Physical OpSec

- Both phones stored in separate faraday bags
- Never opened within 100 meters of each other
- No Bluetooth, NFC, or Wi-Fi Direct enabled
- Batteries removed when not in use (if possible)

## How Each Forensic Gap Is Addressed

| Tracking Vector | Phone A Mitigation | Phone B Mitigation |
|---|---|---|
| Google Location Services | N/A (no Android) | None (GrapheneOS removes GLS) |
| Apple Find My | N/A | N/A (no Apple devices) |
| In-app GPS | N/A | Permissions denied to all apps |
| Wi-Fi BSSID Geolocation | N/A (no Wi-Fi) | Scanning disabled, faraday bag used |
| Bluetooth Beacons | N/A | Bluetooth disabled |
| Cellular Tower CDRs | Burner SIM, faraday bag, rotation | N/A (no cellular) |
| Cellular Triangulation | Burner SIM, faraday bag | N/A (no cellular) |
| 5G Multi-RTT | 4G only, faraday bag | N/A (no cellular) |
| Stingray/IMSI Catcher | Faraday bag when cellular on | N/A (no cellular) |
| Tower Dump Correlation | Never carried together, rotation | Never carried together, faraday |
| E911 | Never dial 911 from Phone A | N/A (no cellular) |
| ISP Logs (Home Wi-Fi) | N/A | Never used at home |
| Camera EXIF | N/A | Disabled location, stripped metadata |
| ISP Subpoena | N/A (no identity linked) | N/A (no residential ISP used) |

## The Gold Standard for High-Risk Users

The "Zero Location" configuration plus the "Compartmentalized Burner" model represents the highest practical privacy level achievable with consumer hardware. It is appropriate for:

- Journalists covering sensitive stories in hostile environments
- Activists facing surveillance from state or corporate actors
- Individuals crossing borders where device searches are routine
- Domestic violence survivors hiding from abusers
- Whistleblowers preparing to leak sensitive information

Even this gold standard has limits. It cannot protect against:

- Physical surveillance (cameras, license plate readers, facial recognition)
- Traffic analysis (packet timing and sizes revealing communication patterns)
- Zero-day exploits targeting the Wi-Fi chipset or OS kernel
- Financial tracking (credit card purchases of equipment)
- Human intelligence (informants, social engineering)

The gold standard reduces an adversary's available attack surface from a hundred entry points to perhaps five. That is significant. It is not perfect. Accept this before committing to the architecture.

[^1]: US carriers including Verizon, T-Mobile, and AT&T retain call detail records (IMSI, IMEI, tower ID, timing advance) for up to 18 months. See Appendix C of this handbook; CALEA, 47 U.S.C. §§ 1001–1010 (requiring carrier infrastructure to support lawful interception and delivery of call-identifying information).
[^2]: Carpenter v. United States, 585 U.S. 296 (2018). The Supreme Court held that seven days of cell-site location information (CSLI) reveals a detailed picture of a person's life and that historical CSLI requires a warrant under the Fourth Amendment; prior to this ruling, CDRs and tower location data were obtainable without a warrant under the third-party doctrine.
[^3]: Under 18 U.S.C. § 2703(c)–(d), the government may obtain subscriber records—including the name and address linked to an IP address or phone account—with a court order based on "specific and articulable facts," a standard lower than probable cause.
[^4]: Signal's minimal server-side data retention was confirmed in practice when Signal (Open Whisper Systems) responded to a 2016 federal grand jury subpoena from the Eastern District of Virginia by producing only two data points: account creation date and the date of last connection. See signal.org/bigbrother/.
