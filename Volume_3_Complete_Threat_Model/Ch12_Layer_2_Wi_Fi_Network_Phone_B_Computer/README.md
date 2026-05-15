# Chapter 12: Layer 2 — Wi-Fi Network (Phone B & Computer)

## Overview

Layer 2 addresses the Wi-Fi-based tracking vulnerabilities affecting Phone B (the private communication hub running GrapheneOS) and the Computer. Unlike Layer 1's cellular vulnerabilities, which are largely carrier-mediated and require legal process to exploit, Wi-Fi layer vulnerabilities can be exploited by anyone within wireless range using passive sniffing equipment that costs less than $50. The floor of Wi-Fi exposure is the coffee shop, the airport, the sidewalk outside your home. The ceiling is global-scale geolocation via BSSID databases.

The two-phone strategy assigns Phone B to Wi-Fi-only operation specifically to avoid cellular tracking. But Wi-Fi introduces its own set of persistent identifiers that, if not properly managed, can deanonymize the user just as thoroughly as cellular tracking — and often more quickly, because Wi-Fi identifiers are visible to everyone in range, not just the carrier.

---

## Vulnerability 1: MAC Address (Permanent Hardware ID)

**Severity: Critical**

Every Wi-Fi interface has a Media Access Control (MAC) address — a 48-bit hardware identifier assigned by the manufacturer. The first 24 bits (the Organizational Unique Identifier, or OUI) identify the manufacturer. For example, an OUI beginning with `00:1A:11` belongs to Samsung, while `F4:5E:AB` belongs to Google.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Permanent hardware identifier; OUI reveals device manufacturer |
| Collection Method | Router logs, passive Wi-Fi sniffing, ISP DHCP lease logs |
| Mitigation | MAC randomization enabled, faraday bag when not in use |

When Phone B scans for Wi-Fi networks, it transmits its MAC address in probe requests. When it connects to a network, the router logs the MAC address in its association table and DHCP lease database. The ISP may also log the MAC address alongside the assigned IP address.

The danger of the permanent MAC address is that it is globally unique and never changes unless explicitly randomized. A single network administrator, coffee shop owner, or passive sniffer can record the MAC address and track the device's presence over time. Unlike a cellular IMSI, which requires carrier access, a MAC address is visible to anyone within Wi-Fi range.

Modern operating systems (iOS 14+, Android 10+, Windows 10, macOS) implement MAC randomization for probe requests, generating a random MAC address for each new network scan. However, this randomization is not always enabled by default, and some implementations have been shown to leak the real MAC address through various side channels. GrapheneOS does implement robust MAC randomization, but the feature must be confirmed active.

**Critical Failure Mode**: If Phone B ever connects to a network that logs MAC addresses — especially a home router — the permanent MAC address becomes linked to that location and, through the ISP subscriber records, to your identity.

---

## Vulnerability 2: Probe Requests — SSID Leakage

**Severity: High**

Wi-Fi probe requests serve a legitimate function: the phone asks "Are you any of these networks I remember?" by broadcasting the SSIDs (network names) of previously connected networks. This is how a phone auto-connects to known networks like "HomeWiFi" or "Starbucks_Guest."

| Attribute | Detail |
|-----------|--------|
| Data Exposed | SSIDs of remembered networks (home, work, frequent locations) |
| Collection Method | Passive sniffing in public areas (coffee shops, airports, transit) |
| Mitigation | Disable Wi-Fi scanning when not in use, faraday bag, never connect to home Wi-Fi |

The privacy disaster of probe requests is that they enumerate everywhere you have been. A passive sniffer at an airport can capture probe requests from hundreds of devices, each broadcasting a list of remembered SSIDs. An SSID like "SmithFamilyHome5G" or "Acme-Corp-WiFi" immediately reveals personal information. Even generic SSIDs like "Home-Network" or "ATT-1234" can be cross-referenced with geolocation databases to identify locations.

Researchers have demonstrated that probe request SSID lists can be used to:
- Identify a device's home SSID (and thus home location via BSSID geolocation)
- Identify workplace SSIDs
- Identify frequented businesses (Starbucks, McDonald's, hotels)
- Track movement patterns over time
- Correlate devices owned by the same person

The defense is straightforward: disable Wi-Fi scanning when not actively using Wi-Fi. Phone B should only enable Wi-Fi when in a designated safe location (public Wi-Fi with VPN). When traveling between locations, Wi-Fi should be off and the phone in a Faraday bag.

---

## Vulnerability 3: Association Frames and Connection Timestamps

**Severity: High**

When a phone connects to a Wi-Fi network, it sends an association frame containing its MAC address, supported data rates, and capability information. The access point logs the association event with a timestamp. These logs are retained by the router and, in the case of ISP-provided routers, may be accessible to the ISP.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Connection timestamps, router BSSID |
| Collection Method | Router logs, ISP access logs |
| Mitigation | Never connect Phone B or Computer to home or work Wi-Fi |

Association logs create a timeline of device activity. An adversary with access to router logs can determine:
- When a device arrived and left
- How long it stayed
- What days and times it was present
- How frequently it returns

For a home router, association logs link the device's MAC address to the physical address of the home. For a coffee shop router, association logs can be correlated with CCTV footage (Layer 5) to match a face to a MAC address.

The association frame itself also leaks information about the device's capabilities. The supported rates element can distinguish between device types (phone, laptop, IoT device), and certain implementation-specific fields can fingerprint the exact device model and driver version.

---

## Vulnerability 4: DHCP Client ID and Hostname Leakage

**Severity: Medium**

When a device connects to a Wi-Fi network and requests an IP address via DHCP, it sends a DHCP Discover packet containing a hostname (DHCP Option 12) and often a client identifier (Option 61). The hostname is typically set by the user or the operating system during setup.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Device name (e.g., "Pixel-6", "Johns-MacBook", "grapheneos-device") |
| Collection Method | ISP DHCP logs, router logs |
| Mitigation | Change hostname to a generic identifier (e.g., "android-device") |

The hostname is often overlooked as a privacy leak. A device name like "Johns-Private-Phone" or "Pixel-7-Pro-Graphene" immediately tells an adversary that this device belongs to a specific individual and runs a privacy-oriented operating system. Even without a full name, the hostname becomes an anchor point for correlation across different logs.

ISP DHCP lease logs associate the hostname with the IP address, MAC address, and lease timestamp. An adversary with a subpoena can obtain all DHCP log entries for a given subscriber, revealing every device that has connected to the home network — including the device name.

The mitigation is simple: change the hostname to something generic. "android-device" or "phone" provides no identifying information. On GrapheneOS, this setting is available in the developer options.

---

## Vulnerability 5: Wi-Fi BSSID Geolocation

**Severity: Critical**

Wi-Fi BSSID geolocation is arguably the most dangerous Wi-Fi vulnerability because it operates at global scale and can be exploited by any adversary with access to geolocation APIs — including data brokers and advertisers.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | GPS coordinates of nearby routers, enabling precise device location |
| Collection Method | Geolocation API queries (Google, Apple, Mozilla databases) |
| Mitigation | Never use Phone B at home, faraday bag when not in use |

Google Street View cars and Android devices have been mapping Wi-Fi BSSIDs to GPS coordinates since 2008. Apple's iOS devices do the same. The result is a global database of hundreds of millions of BSSIDs, each with a known GPS location. When a device scans for Wi-Fi networks, the visible BSSIDs can be used to query the database and determine the device's location with street-level accuracy — even without GPS.

This means that even if Phone B never connects to any network, the act of scanning reveals location. Any app with location permissions can query the visible BSSIDs against Google's geolocation API and determine the phone's position. Similarly, an adversary with passive sniffing equipment can collect the BSSIDs visible near a target and query the geolocation database.

The forensic implication for the two-phone strategy is severe. If Phone B is ever used at home, the BSSIDs of nearby routers (including the home router itself and neighbors' routers) are visible. An adversary who identifies one of those BSSIDs — through a database query, passive scan at the home location, or ISP records — immediately knows that Phone B was present at that home address.

**The One-Incontrovertible Rule**: Phone B must never be at your home address. Not for five minutes. Not for a single network scan. The BSSID geolocation databases are too comprehensive, and the correlation is too easy for an adversary to make.

---

## Vulnerability 6: Bluetooth Beacons

**Severity: Medium**

Bluetooth Low Energy (BLE) devices broadcast advertising packets to announce their presence. Phones, smartwatches, headphones, and other BLE devices transmit identifiable patterns that can be used for tracking.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Proximity to other devices, location fingerprinting |
| Collection Method | Passive Bluetooth sniffing |
| Mitigation | Disable Bluetooth when not actively using it |

While Bluetooth tracking is less precise than Wi-Fi BSSID geolocation, it adds another dimension to device correlation. A passive Bluetooth sniffer can detect Phone B's presence in a location and identify it by the combination of Bluetooth MAC address and advertising packet characteristics.

Bluetooth beacons are also used by retail stores, airports, and public venues for proximity marketing and foot-traffic analysis. These systems record the Bluetooth MAC addresses of passing devices, building a movement profile over time.

The mitigation is straightforward: disable Bluetooth on Phone B and the Computer. Enable it only when actively using a Bluetooth peripheral, and disable it immediately afterward. On GrapheneOS, Bluetooth can be toggled in quick settings.

---

## Vulnerability Summary Table

| Vulnerability | Data Exposed | Collection Method | Severity | Mitigation |
|--------------|-------------|-------------------|----------|------------|
| MAC address (permanent) | Hardware ID, manufacturer OUI | Router logs, sniffers, ISP DHCP | Critical | MAC randomization, faraday bag |
| Probe requests | SSIDs of remembered networks | Passive sniffing | High | Disable Wi-Fi scanning, faraday |
| Association frames | Connection timestamps, BSSID | Router logs | High | Never connect to home Wi-Fi |
| DHCP hostname | Device name | ISP logs, router logs | Medium | Change to generic name |
| BSSID geolocation | GPS of nearby routers | Geolocation API query | Critical | Never use at home, faraday |
| Bluetooth beacons | Proximity, fingerprint | Passive sniffing | Medium | Disable Bluetooth |

---

## Mitigations Summary

The Layer 2 mitigations center on three operational rules:

1. **Never at home.** Phone B must never be at your home address. If it is, the combination of BSSID geolocation, router logs, and ISP records provides a complete forensic link to your identity.

2. **Faraday bag when traveling.** Between use locations, Phone B should be in a Faraday bag. This prevents passive scanning from capturing probe requests, MAC addresses, and Bluetooth beacons.

3. **Virtualize the identity.** MAC randomization, generic hostnames, and disabled Bluetooth prevent the device from leaking persistent identifiers into the environment.

---

## Severity Ratings

| Vulnerability | Severity | Rationale |
|--------------|----------|-----------|
| MAC address | Critical | Globally unique hardware ID, visible to all nearby |
| BSSID geolocation | Critical | Street-level location from passive scan, works globally |
| Probe requests | High | Reveals personal locations (home, work) |
| Association frames | High | Connection timestamps link identity to location |
| DHCP hostname | Medium | Identifies device type and sometimes user |
| Bluetooth beacons | Medium | Low range, less precise than Wi-Fi |

---

## Conclusion

Layer 2 vulnerabilities are in some ways more dangerous than Layer 1 because they can be exploited without legal process. MAC addresses and probe requests are visible to any nearby device. BSSID geolocation databases are accessible through public APIs. An adversary does not need a carrier relationship, a subpoena, or a court order to track Phone B — they only need to be within wireless range.

The two-phone strategy's original design made Phone B Wi-Fi-only specifically to avoid cellular tracking. But Wi-Fi introduces its own comprehensive tracking infrastructure. The mitigations exist, but they require absolute discipline: Phone B cannot be at home, cannot be on home Wi-Fi, and must be shielded when not in use.

The single most important rule of Layer 2 is the simplest: **Phone B never goes home.** Any violation of this rule creates a forensic link that cannot be undone. BSSID geolocation databases are permanent. Router logs are retained by ISPs. Once Phone B is linked to your home address, the compartmentalization is permanently compromised.
