# Chapter 44: Open Research Questions

## What We Still Do Not Know

The forensic analysis in this handbook identifies vulnerabilities based on known protocols, published research, and documented carrier practices. But significant knowledge gaps remain. This chapter documents open research questions that the privacy research community should investigate.

These are not minor details. They represent fundamental unknowns about how our devices, networks, and carriers handle data below the layers visible to the operating system and the user.

## 1. Baseband Processor Behavior — The Black Box

The cellular baseband is a proprietary, closed-source system-on-chip that runs real-time firmware. It has direct access to the radio antenna and, on many chipsets, direct memory access (DMA) to the main processor's memory.

### What We Do Not Know

- **What data does the baseband transmit without OS awareness?** The baseband may transmit diagnostic, location, or status information to the carrier independently of what the OS requests. These transmissions would not appear in OS-level logs.

- **Can the baseband be triggered to transmit by silent SMS or network commands?** Silent SMS (Type 0 SMS) is documented but its use for location triggering is not transparent. The baseband may respond to network requests without the OS knowing.

- **How does the baseband handle 5G NAS security?** The transition from SUCI (encrypted IMSI) to SUPI (plain IMSI) in the home network is opaque. We know CALEA mandates carrier-side decryption,[^1] but the baseband's role in this process is not auditable.

- **Can baseband firmware be forensically analyzed after compromise?** Current tools cannot read baseband memory post-mortem. If a baseband exploit is used, there is no way to confirm it after the fact.

### Research Questions

1. Can baseband diagnostic outputs be intercepted via UART or debug interfaces on consumer devices?
2. Do basebands transmit unsolicited measurement reports beyond those required by 3GPP?
3. Can a software-defined radio (USRP, bladeRF) capture and decode baseband responses that the OS does not log?
4. How does the baseband behave when the OS sends a "radio off" command versus physical RF blocking (faraday)?
5. Is there a way to detect baseband-level compromise without dedicated hardware?

## 2. 5G Carrier Phase Positioning (Release 18+)

3GPP Release 18 introduces carrier phase positioning, which promises sub-meter accuracy — comparable to survey-grade RTK GPS. This is not theoretical. The specification is finalized and carriers are beginning deployment.

### What We Do Not Know

- **When will major carriers deploy carrier phase positioning?** Some carriers (Verizon, T-Mobile, NTT Docomo, China Mobile) are testing. Public deployment timelines are unknown.

- **Is carrier phase positioning mandatory or optional for 5G SA networks?** The spec allows it, but whether carriers implement it varies. We do not know which carriers will enable it.

- **Can the user opt out?** Unlikely. Positioning measurements are collected by the network from standard reference signals. The phone cannot refuse to transmit them without losing connectivity.

- **What accuracy is achievable in urban versus rural environments?** Multipath interference may reduce accuracy in dense urban areas. Rural areas with clear line-of-sight may achieve the full sub-meter precision.

- **How is this data retained?** Will carriers log sub-meter location data with the same retention periods as current CDRs? The legal framework for this data is unclear.[^2]

### Research Questions

1. Obtain carrier deployment timelines through freedom of information requests or regulatory filings.
2. Test 5G positioning accuracy using commercial networks with known reference points.
3. Monitor 3GPP meeting minutes for decisions on carrier phase positioning data retention standards.
4. Determine whether existing legal instruments (tower dumps, §2703(d) orders) cover sub-meter positioning data.

## 3. Signal Metadata Retention Policies

Signal is the gold standard for private messaging, but "minimal metadata" is not "zero metadata."

### What We Do Not Know

- **How long does Signal retain account metadata?** Signal's privacy policy says they retain minimal data, but specific retention periods for account creation timestamps, last-seen timestamps, and device registration logs are not publicly specified.[^3]

- **What metadata is visible to Signal's servers for username-based accounts (as opposed to phone-number-based accounts)?** The username system is relatively new. The metadata exposure surface is not fully documented.

- **Can Signal's contact discovery service be compelled to reveal the contact graph?** Signal uses private contact discovery (Intel SGX), but the security of SGX enclaves has been repeatedly challenged. A compromised enclave could reveal who you have in your contacts.

- **What is the forensic value of Signal's "safety number" change logs?** Safety number changes may indicate device registration changes, which could be relevant to active attack detection.

### Research Questions

1. File a GDPR data subject access request with Signal to obtain all stored metadata.
2. Analyze the Signal server protocol to identify exactly what data crosses the wire during registration and message delivery.
3. Investigate the security of Signal's SGX-based contact discovery against current side-channel attacks.
4. Document what a §2703(d) order to Signal returns in practice.

## 4. Wi-Fi Chipset Firmware Behavior When "Disabled"

When a user toggles "Wi-Fi off" in the OS settings, what actually happens inside the Wi-Fi chipset?

### What We Do Not Know

- **Does the Wi-Fi chipset completely power down the radio, or does it enter a low-power listening mode?** Many chipsets continue to scan for networks even when "off" to support location services for the OS.

- **Does the chipset cache BSSIDs from passive scans when "disabled"?** Even in a low-power state, the chipset may record visible access points for later upload to the OS.

- **Does disabling Wi-Fi in GrapheneOS behave differently than in stock Android?** GrapheneOS has fine-grained controls for radio management, but the underlying chipset firmware is the same.

- **Can the Wi-Fi chipset be triggered to scan by a management frame (beacon, probe response) even when "disabled"?** Some chipsets wake on wireless LAN (WoWLAN) features that respond to specific frames even in power-saving states.

- **Does USB-C or Thunderbolt passthrough allow Wi-Fi chipset access when the phone is in "airplane mode"?** If the phone is connected to a computer via USB, can the computer access the Wi-Fi chipset?

### Research Questions

1. Use an external software-defined radio to detect Wi-Fi transmissions when the phone reports Wi-Fi as "disabled."
2. Compare OS-level radio state with physical radio behavior across multiple devices and OS versions.
3. Analyze Wi-Fi chipset firmware binaries for undocumented scanning behaviors.
4. Test whether airplane mode on different phones and OS combinations actually disables all radio transmission.

## 5. MAC Randomization Reliability Across Vendors

MAC randomization is a critical mitigation against Wi-Fi tracking, but its implementation is inconsistent.

### What We Do Not Know

- **Which vendors and driver versions properly implement MAC randomization?** Android's MAC randomization has improved with each release, but device-specific driver bugs are common.

- **Under what conditions does the device fall back to the permanent MAC?** Common triggers include: reboot, connection failure, probe request to a known network, and certain association procedures.

- **Does GrapheneOS's MAC randomization behave differently than stock Android on the same Pixel hardware?** The OS can request randomization, but the driver and chipset ultimately control whether it happens.

- **Can MAC randomization be detected by a passive adversary?** If an adversary knows the OUI range of your device manufacturer, they can infer the likelihood that a given MAC is randomized versus permanent.

- **What is the privacy impact of the OUI (Organizationally Unique Identifier) in MAC addresses?** Even with randomization, the first three bytes (the OUI) reveal the chipset manufacturer, which narrows device identification.

### Research Questions

1. Build a testbed that captures Wi-Fi probe requests and association frames from devices under controlled conditions.
2. Test MAC randomization behavior across Android versions 11 through 14 on Pixel, Samsung, and OnePlus devices.
3. Document the conditions that trigger permanent MAC fallback for each device and driver version.
4. Determine whether applications with location permission can read the permanent MAC despite OS-level randomization.

## 6. Additional Open Questions

### E911 Location Accuracy and Retention

Emergency services location data (E911 Phase II and III) is collected and retained by carriers and PSAPs. How long is this data retained? Can it be accessed without a warrant? What accuracy is logged? These questions have significant implications for anyone who dials 911 from any phone.

### Carrier Data Sharing Between Affiliates

When Phone A uses T-Mobile and Phone B connects to a Wi-Fi network provided by the same carrier as an ISP, is data shared internally? Large telecommunications companies often operate both mobile and fixed-line services. Whether they compartmentalize subscriber data across divisions is not publicly known.

### JavaScript Geolocation Accuracy in Modern Browsers

The HTML5 Geolocation API can use Wi-Fi BSSID databases, IP geolocation, and sensor fusion to locate devices. How accurate is this in 2026? Can a website determine your location within meters without your explicit permission on devices where permission has been granted once and cached?

## A Researcher's Request

If you have the means and the interest, consider investigating one of these questions. Each represents a genuine gap in our collective understanding of mobile privacy. The answers matter for threat modeling, policy advocacy, and the design of future privacy-preserving technologies.

The authors of this handbook can be reached for collaboration, peer review, or data sharing. We maintain a directory of active research projects at the intersection of cellular forensics, privacy, and operational security.

[^1]: CALEA, 47 U.S.C. §§ 1001–1010. Section 1002 requires telecommunications carriers to ensure their systems can deliver call-identifying information (including location) to law enforcement in a usable form; this encompasses carrier-side processing of 5G NAS security context.
[^2]: Under 18 U.S.C. § 2703(d) and Carpenter v. United States, 585 U.S. 296 (2018), CSLI (cell-site location information) requires a warrant. Whether 5G sub-meter carrier phase positioning data falls within the Carpenter holding — or requires a separate analysis — has not been addressed by courts as of the document date.
[^3]: Signal's 2016 response to a federal grand jury subpoena (Eastern District of Virginia) is the most authoritative public record of what Signal's servers actually retain. Signal produced only account creation date and last connection date. See signal.org/bigbrother/. Specific retention periods for other metadata categories are not published.
