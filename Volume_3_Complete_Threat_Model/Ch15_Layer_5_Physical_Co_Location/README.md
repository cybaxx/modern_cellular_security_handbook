# Chapter 15: Layer 5 — Physical Co-Location (The Compartmentalization Killer)

## Overview

Layer 5 addresses the most devastating vulnerability in the two-phone strategy: physical co-location. Every other vulnerability layer assumes that the adversary must actively collect data — subpoena carriers, sniff Wi-Fi, extract EXIF metadata, or query geolocation APIs. Layer 5 exploits the simplest fact of human behavior: the user carries both phones in the same bag, uses them at the same home, or follows predictable temporal patterns that link the two devices to the same person.

Physical co-location is called "the compartmentalization killer" because it defeats every other mitigation simultaneously. You can use burner SIMs, faraday bags, encrypted DNS, GrapheneOS, Tor Browser, and never-use-at-home rules, but if you carry Phone A and Phone B together in the same backpack for a single hour, you have created a forensic link that an adversary can exploit to correlate every data source across both devices.

This chapter examines the vulnerabilities that arise from physical proximity of the two phones, using the home address as a base of operations, and following predictable behavioral patterns.

---

## Vulnerability 1: Carrying Both Phones Together

**Severity: Critical**

The most direct physical co-location vulnerability is simply carrying both phones at the same time. When Phone A connects to a cellular tower, its IMSI and IMEI are logged by the carrier. Simultaneously, Phone B's Wi-Fi chipset (even if not connected to a network) is scanning for visible BSSIDs and potentially transmitting probe requests.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Correlation of Phone A tower logs with Phone B Wi-Fi/BT scans at the same location and time |
| Collection Method | Tower dump + Wi-Fi geolocation database query |
| Mitigation | Never carry Phone A and Phone B together |

The forensic mechanism works as follows:
1. An adversary obtains a tower dump for a specific area and time window (Layer 6 legal process).[^1]
2. Phone A's IMSI-IMEI pair appears in the tower dump at a specific timestamp.
3. Separately, an adversary queries the Wi-Fi BSSID geolocation database for that area.
4. Phone B's Wi-Fi scan (which happens automatically whenever Wi-Fi is enabled) reveals visible BSSIDs.
5. If the BSSIDs visible to Phone B match the geolocation of the tower where Phone A was seen, the two devices are correlated to the same person.

Even without a tower dump, passive Wi-Fi sniffing captures Phone B's MAC address or probe requests. If an adversary has one device identified (Phone A, through carrier records), they can place Wi-Fi sniffers in locations where Phone A is known to be, and capture Phone B's identifiers when the user passes through.

This vulnerability is exacerbated by the physical constraints of Wi-Fi range. If Phone B is within approximately 50–100 meters of Phone A, their network footprints overlap. This means that keeping the phones in the same bag, the same car, or the same room creates the forensic link.

**Operational Rule**: When Phone A is active (out of the faraday bag, connected to the cellular network), Phone B must be at least 1 kilometer away, inside a faraday bag, and powered off or in airplane mode. The two devices must never occupy the same physical space.

---

## Vulnerability 2: Home Address Overlap

**Severity: Critical**

The home address is the single most identity-anchored location in any person's life. It is linked to utility bills, voter registration, driver's licenses, tax records, package deliveries, and ISP accounts. If both phones are ever present at the same home address, the adversary has a direct link.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Both phones present at same residence |
| Collection Method | Carrier logs (Phone A cell ID near home) + ISP logs (Phone B IP from home) or Wi-Fi geolocation |
| Mitigation | Phone B never enters home address; Phone A minimized at home |

The home address overlap vulnerability is unique because it can be exploited in two ways:
1. **Phone A at home + Phone B at home**: Both phones generate location data that places them at the same address.
2. **Phone A at home + Phone B connecting to home Wi-Fi**: Phone B's IP address is linked to the home ISP account, providing the identity link.[^2]

For the two-phone strategy, Phone B must never enter the home address under any circumstances. This means:
- Phone B is never used at home
- Phone B is never charged at home
- Phone B is never stored at home
- Phone B is not brought home even inside a faraday bag (the bag can be X-rayed or detected by RF scanners at checkpoints)

The operational model requires Phone B to be stored at a separate location, used only in public spaces, and never associated with the residential address. This is the most demanding operational requirement of the entire strategy.

For Phone A, usage at home should also be minimized. Every connection at home adds to the log of times the phone was at the residence. If an adversary later identifies Phone A's subscriber identity, the home location records confirm the user's primary address.

---

## Vulnerability 3: Temporal Pattern Correlation

**Severity: High**

Temporal pattern correlation exploits the timing of device usage rather than direct location overlap. Even if the two phones are never in the same place at the same time, patterns in when they are active can link them to the same person.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Phone A active → Phone B active (same person, different devices) |
| Collection Method | Metadata analysis, traffic pattern correlation |
| Mitigation | Use at different times, from different locations, with variable patterns |

The forensic logic is based on behavioral inference:
- Phone A is active (making calls) during certain hours
- Phone B becomes active (Signal messages) shortly after Phone A goes silent
- The pattern repeats daily

An adversary with access to both Phone A's carrier records and Phone B's network logs (or Signal metadata) can build a behavioral model that matches the two devices to the same individual. Machine learning techniques can detect these patterns even with significant noise.[^3]

The defense is to disrupt temporal patterns:
- Vary the times of day when each phone is used
- Do not use Phone B immediately after Phone A
- Create false patterns (leave Phone A active at a location while using Phone B elsewhere)
- Use both phones at different locations to prevent geographic correlation

---

## Vulnerability 4: Surveillance Camera Correlation

**Severity: High**

Physical surveillance has not been replaced by digital surveillance — it has been augmented by it. CCTV cameras, traffic cameras, license plate readers, private security cameras, and body-worn cameras create a dense network of visual surveillance in urban and suburban environments.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Your face, clothing, vehicle matched to both devices |
| Collection Method | CCTV, traffic cameras, private security cameras |
| Mitigation | Avoid cameras, change appearance, use indirect routes |

The surveillance camera vulnerability is simple in mechanism but devastating in effect:
1. A camera captures your image at a specific time and location.
2. Phone A's carrier log places Phone A at that same time and location.
3. Phone B's network logs (or physical presence) place Phone B nearby.
4. The visual image links both devices to your physical identity (face, body, vehicle).

Surveillance cameras are everywhere. London has an estimated 500,000+ public cameras.[^4] Major US cities have extensive traffic camera and red-light camera networks. License plate readers (ALPR) are mounted on police cars, bridges, and toll roads nationwide. Private cameras (Ring, Nest, Arlo) add millions more.

Mitigations include:
- Learning camera locations in your usage area
- Using routes that avoid cameras
- Wearing clothing that does not stand out (but does not match across Phone A and Phone B trips)
- Using different vehicles or public transit
- Changing appearance between Phone A and Phone B usage sessions

---

## Vulnerability 5: Home Router Logs

**Severity: Critical**

The home router logs represent a confluence of multiple vulnerability layers. If Phone B ever connects to the home Wi-Fi network, the router logs record the connection and the ISP subscriber records identify the subscriber.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Phone B MAC address linked to home IP address (your identity) |
| Collection Method | ISP subpoena + router log seizure |
| Mitigation | Phone B never at home, never on home Wi-Fi |

The home router log is the single most damning piece of evidence in a deanonymization investigation:
1. Phone B connects to home Wi-Fi (even once).
2. Router logs record MAC address, assigned IP address, DHCP hostname, connection timestamp.
3. ISP logs record which subscriber account was assigned that IP address at that time.[^5]
4. An adversary with a subpoena obtains both sets of records.
5. The MAC address of Phone B is now linked to the subscriber name and address.

This is a permanent link. MAC addresses are globally unique and assigned permanently to the device hardware. Once the link is made, Phone B is deanonymized forever. No amount of future OpSec can undo it.

The critical operational rule: Phone B must never be at home. Never connected to home Wi-Fi. Never powered on within range of the home router. This is not negotiable.

---

## Vulnerability Summary Table

| Vulnerability | Data Exposed | Collection Method | Severity | Mitigation |
|--------------|-------------|-------------------|----------|------------|
| Carrying both phones together | Correlation of tower logs + Wi-Fi/BT | Tower dump + Wi-Fi geolocation | Critical | Never carry together |
| Home address overlap | Both phones at same residence | Carrier logs + ISP logs | Critical | Phone B never at home |
| Temporal pattern correlation | Activity patterns across devices | Metadata analysis | High | Vary usage patterns |
| Surveillance cameras | Face, clothing, vehicle | CCTV, traffic cameras | High | Avoid cameras, change appearance |
| Home router logs | Phone B MAC linked to home IP | ISP subpoena + router seizure | Critical | Phone B never at home |

---

## Severity Ratings

| Vulnerability | Severity | Rationale |
|--------------|----------|-----------|
| Carrying both phones together | Critical | Creates direct forensic correlation link |
| Home address overlap | Critical | Links both phones to identity-anchored location |
| Home router logs | Critical | Permanent MAC-to-identity link |
| Temporal pattern correlation | High | Requires behavioral analysis, strong but not definitive |
| Surveillance cameras | High | Depends on camera coverage, can be evaded |

---

## Conclusion

Layer 5 is the most dangerous vulnerability layer because it cannot be fully mitigated by technology alone. Technical controls — encryption, MAC randomization, VPNs, burner SIMs — are irrelevant if the user carries both phones together or uses Phone B at home. The physical layer is controlled by behavior, not by configuration.

The original two-phone strategy's fatal flaw was assuming that digital compartmentalization was sufficient. It assumed that Phone B's lack of a cellular connection and use of encryption would protect its identity, regardless of its physical relationship to Phone A. This assumption was wrong. Physical co-location provides a forensic link that bypasses every digital protection.

The rules for Layer 5 are absolute:

1. **Phones A and B must never be in the same physical location.** Not in the same bag, not in the same car, not in the same building. Keep at least 1 kilometer of distance between them.

2. **Phone B must never be at home.** Not in the house, not in the garage, not in the driveway. The home address is the identity anchor, and any proximity to it links Phone B to that identity.

3. **Vary patterns.** Do not be predictable in when or where each phone is used. If an adversary identifies a temporal pattern, they can correlate the devices.

4. **Assume cameras see everything.** Every trip outside involves passing surveillance cameras. Assume your face is recorded and the time/location is logged.

5. **Once is enough.** A single violation of any of these rules — one hour of carrying both phones together, one connection to home Wi-Fi — creates a permanent forensic link that cannot be undone. The two-phone strategy does not survive a single physical co-location mistake.

---

[^1]: Carpenter v. United States, 585 U.S. 296 (2018). The Supreme Court addressed the legal framework for obtaining historical cell-site location records from carriers, requiring a warrant; tower dump orders are a related instrument used in criminal investigations for identifying devices present at a location.

[^2]: Stored Communications Act, 18 U.S.C. § 2703. Establishes the legal standard (§2703(d) "specific and articulable facts" order) under which ISPs must disclose subscriber identity and IP address logs, enabling the home-ISP identity link.

[^3]: Signal Foundation, "What Does Signal Know About Me?" signal.org/bigbrother. Documents the metadata (timestamps and connection data) that Signal servers retain, which combined with carrier CDRs enables temporal pattern correlation analysis. https://signal.org/bigbrother/

[^4]: EFF, "Surveillance Self-Defense," ssd.eff.org. Discusses the density of surveillance camera infrastructure in urban environments and its role in physical surveillance correlated to device tracking. https://ssd.eff.org

[^5]: Stored Communications Act, 18 U.S.C. § 2703. A §2703(d) court order compels ISPs to disclose subscriber name, address, and IP address assignment logs, linking a device's MAC address to the account holder.
