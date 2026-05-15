# Chapter 11: Layer 1 — Cellular Network (Phone A)

## Overview

Layer 1 is the most fundamental and inescapable vulnerability of any phone that connects to a cellular network. Phone A, the "public face" flip phone in the two-phone strategy, is deliberately designed to absorb superficial interactions. But every time it connects to a tower, it generates a permanent, legally obtainable record of its presence, identity, and location. This chapter analyzes each cellular-layer vulnerability, its forensic exposure, collection method, severity, and available mitigations.

The core truth of cellular tracking is simple: a phone cannot communicate with a tower without identifying itself. The SIM card authenticates the subscriber; the baseband chipset broadcasts the device hardware ID. Both are logged, retained for months or years, and accessible to law enforcement with varying levels of legal process.[^1] For an adversary, the cellular network is the single richest source of identity data.

---

## Vulnerability 1: IMSI/IMEI Transmission

**Severity: Critical**

Every GSM, UMTS, LTE, and 5G NR cellular connection begins with the phone transmitting its International Mobile Subscriber Identity (IMSI) and International Mobile Equipment Identity (IMEI). The IMSI is stored on the SIM card and identifies the subscriber account. The IMEI is burned into the phone's hardware and identifies the specific device.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Permanent subscriber ID, permanent device hardware ID |
| Collection Method | Carrier call detail records (CDRs), tower dumps, IMSI catchers (Stingray) |
| Retention Period | 6–18 months (US), 12–24 months (EU under data retention directives), longer in parts of Asia |
| Mitigation | Burner SIM purchased with cash, phone purchased with cash, regular SIM/phone rotation |

The IMSI is transmitted when the phone attaches to a network, when it makes or receives a call, when it sends an SMS, and periodically for location updates. Every tower the phone touches logs the IMSI-IMEI pair.[^1] This means that from the moment Phone A is turned on, it leaves a trail of timestamped location records directly linking the device and subscriber to specific places at specific times.

The IMEI is particularly dangerous because it is tied to the hardware. Unlike a SIM card, which can be swapped, the IMEI cannot be changed without specialized equipment that is illegal to possess in many jurisdictions. Even if you swap the SIM, the same IMEI continues to appear in tower logs, allowing an adversary to identify that the same device is in use over time.

**Forensic Graph**: If an adversary obtains a tower dump for a specific location and time window, every IMSI-IMEI pair within range is captured. Phone A will appear in every dump at every tower it connected through.

---

## Vulnerability 2: Cell ID Logging

**Severity: High**

Each time a phone communicates with a tower, the carrier logs the Cell ID — a unique identifier for the specific tower sector. Combined with carrier tower location databases, this provides the approximate location of the phone at the time of communication.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Tower location (500 m to 35 km accuracy depending on cell density) |
| Collection Method | Carrier logs, CDR records |
| Mitigation | Faraday bag when not actively in use |

Cell ID accuracy varies dramatically by environment. In dense urban areas with small cells, accuracy can be as good as 500 meters — enough to identify a specific neighborhood or city block. In suburban and rural areas with macro cells, accuracy drops to several kilometers. An adversary analyzing Cell ID logs can reconstruct a phone's movement patterns over weeks or months, identifying home location, work location, frequent routes, and relationships between locations.[^1]

A single Cell ID log entry provides one data point. A sequence of entries over time reveals travel patterns, commute routes, and regular schedules. When correlated with other devices (Layer 5 vulnerability), Cell ID logs become a powerful tool for deanonymization.

---

## Vulnerability 3: Timing Advance (TA)

**Severity: High**

Timing Advance is a value used by GSM and LTE networks to compensate for signal propagation delay. In simple terms, the network measures how long it takes for the signal to travel between the tower and the phone, and uses this to calculate the distance from the tower.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Distance from tower, accurate to 78 meters per TA unit in 4G (548 meters in 2G) |
| Collection Method | Carrier logs retained with CDR data |
| Mitigation | Faraday bag when not in use |

TA granularity varies by generation. In 2G (GSM), one TA unit represents approximately 548 meters. In 4G (LTE), one unit represents approximately 78 meters.[^2] With multiple TA readings from different towers, triangulation becomes possible, narrowing the phone's position to a much smaller area than Cell ID alone.

For law enforcement, TA data is frequently used alongside Cell ID and Angle of Arrival data to obtain location information precise enough for search warrants.[^3] The combination of Cell ID + TA provides a radial band around the tower within which the phone must be located.

---

## Vulnerability 4: Angle of Arrival (AoA)

**Severity: Medium**

Modern cellular towers use multiple antennas arranged in arrays. By measuring the phase difference of a signal arriving at different antenna elements, the network can calculate the direction from which the signal originated.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Directional angle from tower, typically 50–200 meter accuracy at the cell edge |
| Collection Method | Carrier logs from multi-antenna tower configurations |
| Mitigation | Faraday bag when not in use |

AoA is most effective when combined with Timing Advance. TA provides distance from tower; AoA provides direction. Together, they can locate a phone to within approximately 50–200 meters in urban environments with multi-antenna tower configurations.[^4] This is generally sufficient to identify a specific building or intersection.

Not all towers support AoA logging. It requires sectorized antenna arrays and carrier-side logging infrastructure. However, deployments supporting AoA are increasingly common as carriers upgrade equipment for 5G.

---

## Vulnerability 5: 5G Multi-RTT

**Severity: Critical (by 2026)**

5G Standalone (SA) networks introduce Multi-Round Trip Time (Multi-RTT) positioning, a native network-based geolocation capability built into the 5G NR specification. Multi-RTT measures the signal propagation time between the phone and multiple transmission points (gNBs), achieving submeter accuracy in theory and 5–30 meter accuracy in practice.[^4]

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Precise location (5–30 meter accuracy) |
| Collection Method | Carrier logs from 5G SA networks |
| Mitigation | Configure Phone A for 4G only (disable 5G), faraday bag when not in use |

Multi-RTT does not require GPS. It operates entirely at the network layer, using standardized positioning reference signals (PRS) defined in 3GPP Release 16 and enhanced in Release 17.[^4] The phone passively measures PRS from multiple transmission points, and the network computes the location.

By 2026, 5G SA networks with Multi-RTT capability are expected to be widely deployed in urban areas across North America, Europe, and East Asia. This means Phone A's location can be determined to building-level accuracy on every single connection, without any warrant for GPS data or special intercept equipment. Standard carrier logs will contain precise location data for every network interaction.

This is arguably the single most dangerous cellular vulnerability for anyone relying on a two-phone strategy. The location precision of Multi-RTT means that even a brief connection — a five-second call, a single SMS transmission — fixes the phone's position to within a few meters. If Phone A is ever at the same location as Phone B (Chapter 15), Multi-RTT provides the forensic link.

---

## Vulnerability 6: E911 Location Data

**Severity: Critical**

Enhanced 911 (E911) is a regulatory requirement in the United States and many other countries requiring carriers to provide precise caller location to emergency services (Public Safety Answering Points, or PSAPs). Modern E911 systems aggregate GPS, Wi-Fi positioning, and cellular tower data to provide location accurate to 10–50 meters.[^5]

| Attribute | Detail |
|-----------|--------|
| Data Exposed | GPS + Wi-Fi + cellular hybrid location (10–50 meter accuracy) |
| Collection Method | PSAP logs, carrier retention |
| Mitigation | Never dial 911 from Phone A |

The danger of E911 is that the data is retained. While the primary purpose is emergency response, PSAPs and carriers retain E911 location logs for compliance and liability purposes. An adversary with legal process can obtain the precise GPS coordinates of every 911 call made from a phone number.[^5]

Dialing 911 from Phone A, even in a genuine emergency, creates a record of your precise location at a specific moment. If that location is your home, your work, or near Phone B's known location (Chapter 15), the forensic link is established. This is a critical vulnerability because the instinct to call 911 in an emergency is strong, and the consequences for compartmentalization are catastrophic.

---

## Vulnerability 7: Stingray (IMSI Catcher) Capture

**Severity: High**

A Stingray (also known as an IMSI catcher or cell-site simulator) is a device that impersonates a legitimate cellular tower, forcing all nearby phones to connect to it. Once connected, the Stingray captures the phone's IMSI, IMEI, and real-time location.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | IMSI, IMEI, real-time location |
| Collection Method | Active law enforcement impersonation of cellular tower |
| Mitigation | Faraday bag when phone is not in active use |

Stingray devices operate by broadcasting a signal stronger than legitimate towers, causing phones in the area to prefer the fake tower. The device then captures identifying information and can track the phone in real time as it moves through the coverage area. Modern Stingrays can also intercept call content and SMS messages on older protocols (2G/GSM).

The Federal Bureau of Investigation and local law enforcement agencies have used Stingray devices since at least the mid-2000s, and the technology is now available to a wide range of international law enforcement and intelligence agencies. The use of Stingrays has been controversial due to the lack of warrant requirements in many jurisdictions.

Phone A is vulnerable to Stingray capture whenever it is powered on and not inside a Faraday bag. The only reliable defense is to keep the phone in a Faraday bag when it is not actively being used, preventing any signal from reaching or leaving the device.

---

## Mitigations Summary

| Vulnerability | Primary Mitigation | Secondary Mitigation |
|--------------|-------------------|---------------------|
| IMSI/IMEI | Burner SIM, cash purchase | Regular rotation (30–90 days) |
| Cell ID logging | Faraday bag when idle | Minimize call/SMS frequency |
| Timing Advance | Faraday bag | Use in dense urban areas for ambiguity |
| Angle of Arrival | Faraday bag | — |
| 5G Multi-RTT | Disable 5G, use 4G only | Faraday bag |
| E911 location | Never dial 911 from Phone A | Use public phone or Phone B for emergencies |
| Stingray capture | Faraday bag | — |

The common thread across all seven vulnerabilities is the Faraday bag. When Phone A is inside a properly tested Faraday bag, it emits no RF signal, connects to no towers, and generates no logs. Every vulnerability listed in this chapter is defeated by the same simple countermeasure: keep the phone shielded when it is not actively in use.

However, the Faraday bag is a behavior, not a technology. It must be used consistently. A single failure to bag the phone — forgetting after a call, leaving it on the nightstand overnight — creates a window of exposure that an adversary can exploit.

---

## Severity Ratings Summary

| Vulnerability | Severity | Rationale |
|--------------|----------|-----------|
| IMSI/IMEI transmission | Critical | Direct link to subscriber identity and device |
| 5G Multi-RTT | Critical | 5–30 meter accuracy from standard carrier logs |
| E911 location | Critical | GPS-precision data retained by PSAP and carrier |
| Cell ID logging | High | Identifies general location area |
| Timing Advance | High | Provides distance-from-tower measurement |
| Stingray capture | High | Real-time tracking and data interception |
| Angle of Arrival | Medium | Requires multi-antenna towers, limited accuracy |

---

## Conclusion

Layer 1 represents the most complete set of identity-anchoring vulnerabilities in the threat model. Every connection from Phone A generates a permanent, legally obtainable record. The IMSI links to the subscriber; the IMEI links to the hardware; the Cell ID, TA, AoA, and Multi-RTT data link to the physical location.

The mitigations exist, but all of them depend on behavioral discipline. A burner SIM and cash-purchased phone prevent the initial identity link. A Faraday bag prevents ongoing tracking. Rotation limits the temporal window of exposure. But any of these mitigations can be defeated by a single mistake — and for an adversary with legal process, the mistake does not need to be repeated. One instance of Phone A being on, out of the Faraday bag, at the same location as Phone B is enough to collapse the entire two-phone compartmentalization.

The key operational rule for Layer 1: Phone A is a limited-use tool, not a daily driver. Every interaction creates a record. Minimize interactions. Bag the phone. Rotate frequently. And never, ever dial 911.

---

[^1]: Carpenter v. United States, 585 U.S. 296 (2018). The Supreme Court's factual record documents how carrier Call Detail Records log IMSI-IMEI pairs, Cell IDs, and timestamps for every tower contact; and how seven days of records reconstructed the defendant's historical movements. The Court held such records are subject to Fourth Amendment warrant protection. See also In re Application of the United States for Historical Cell Site Data, 724 F.3d 600 (5th Cir. 2013), discussing the legal standards applicable to CDR tower dump requests.

[^2]: 3GPP TS 36.211 v17, "Evolved Universal Terrestrial Radio Access (E-UTRA); Physical channels and modulation," Release 17. Section 8 defines LTE Timing Advance granularity: one TA unit = 16·Ts ≈ 78 meters of one-way propagation distance from the eNodeB. In 2G GSM, one TA unit = 553.5 ns ≈ 548 meters (3GPP TS 45.010).

[^3]: Stored Communications Act, 18 U.S.C. §§ 2701–2712; Pen Register Act, 18 U.S.C. §§ 3121–3127. These statutes define the graduated legal standards — from pen register certification through § 2703(d) court orders to probable-cause warrants — under which law enforcement obtains TA and AoA-enhanced CDR records from carriers.

[^4]: 3GPP TR 38.855 v16, "Study on NR positioning support," Release 16. Establishes performance requirements for 5G NR positioning methods including Multi-RTT (1–10 m accuracy in dense urban scenarios), DL-AoD, UL-AoA, and NR E-CID. Multi-RTT is defined in 3GPP TS 38.305 v17, "Stage 2 functional specification of User Equipment (UE) positioning in NG-RAN."

[^5]: FCC Report and Order, FCC 15-9 (January 29, 2015), "Wireless E911 Location Accuracy Requirements," 47 CFR § 20.18. Mandates Phase I (tower ID), Phase II (TA/AoA, 50–300 m), and advanced Phase III hybrid location (10–50 m) accuracy requirements for wireless carriers, and requires carriers to retain location data associated with emergency calls.
