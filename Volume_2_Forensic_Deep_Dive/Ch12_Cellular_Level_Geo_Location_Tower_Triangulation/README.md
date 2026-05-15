# Chapter 12: Cellular-Level Geo-Location — Tower Triangulation

## Introduction

Cellular-level geo-location is the carrier's permanent record of your movements. Unlike application-level tracking, which depends on software configuration and permission grants, cellular geo-location is mandatory, involuntary, and hardware-enforced. Every phone with an active cellular connection — even a dumb flip phone, even a phone with no apps, even a phone with location services disabled — transmits the data necessary for the network to determine its position.

This data is logged by the carrier, retained for months or years, and available to law enforcement through established legal processes.[^1] It is the single most reliable source of historical location information in mobile forensics.

## Basic Tower Triangulation: The Cell ID Method

Every time an active phone is powered on and connected to the cellular network, it registers with a specific tower sector. The network logs this registration along with measurements that enable location estimation.

### Cell ID (CGI / ECGI)

The Cell Global Identifier (or E-UTRAN Cell Global Identifier in 4G) uniquely identifies each tower sector. Urban towers may have three or more sectors, each covering approximately 120 degrees. The Cell ID alone provides accuracy ranging from 500 meters to 5 kilometers in urban environments and 5 to 35 kilometers in rural environments. Carriers maintain databases that map every Cell ID to the tower's precise GPS coordinates.

### Timing Advance (TA)

Timing Advance is a measurement of signal propagation delay. The tower calculates how long it takes for the phone's signal to arrive, expressed in units of bit periods. In 4G (LTE), each Timing Advance unit equals approximately 78 meters.[^2] In 5G NR, the higher subcarrier spacing means each Timing Advance unit equals approximately 39 meters.[^3] The Timing Advance value reveals the phone's distance from the tower along the signal path — effectively placing the phone within a ring around the tower.

When combined with Cell ID, Timing Advance narrows the phone's location from the entire sector coverage area to a specific distance band. If the network can measure the Angle of Arrival (using directional antennas or phased arrays), the intersection of the angle and the distance band yields a precise location estimate.

### Angle of Arrival (AoA)

Modern base stations use multiple antenna elements arranged in arrays. These arrays can measure the angle from which the phone's signal arrives by analyzing the phase difference between elements. In urban deployments, AoA accuracy ranges from 50 to 200 meters, depending on antenna height, multipath environment, and the number of antenna elements.[^4]

### Time Difference of Arrival (TDOA)

TDOA requires three or more geographically separated towers to measure the arrival time of the phone's signal. By comparing the time differences between towers, the network calculates hyperbolic curves that intersect at the phone's location. TDOA provides accuracy of 20 to 100 meters when sufficient towers participate in the measurement.[^4]

### Forensic Reconstruction

A forensic analyst reconstructs movement by collecting all Call Detail Records for a given IMSI over a period of time. Each CDR contains the Cell ID, Timing Advance, timestamp, and duration. The analyst maps each Cell ID to its GPS coordinates using the carrier's tower database. They apply the Timing Advance value to calculate the distance from each tower. If multiple towers recorded the phone simultaneously, they triangulate. If only a single tower recorded the phone, they assume the coverage area.[^1]

Over a 30-day period, this produces a movement map with per-location accuracy of 50 to 200 meters. The map reveals home location, workplace, regular routes, frequent destinations, and deviations from routine.

A real-world example demonstrates the power of this technique. At 8:00 AM, the phone registers with Cell ID corresponding to the home tower, with a Timing Advance of 5 units, placing it approximately 390 meters from the tower — pinning the phone to a specific home address. At 9:00 AM, the phone registers with the work tower, Timing Advance of 3 units, placing it at a specific office building. At 12:00 PM, the phone registers with a tower near a restaurant, with a Timing Advance of 8 units. At 6:00 PM, the phone is back on the home tower. The analyst concludes, without GPS data and without accessing the phone, that the target works at a specific company, lives at a specific address, and eats lunch at a specific restaurant.

## 5G NR Positioning: Centimeter Accuracy

5G New Radio introduces positioning methods that dramatically exceed 4G capabilities.[^5] These methods are mandatory for carrier compliance with 5G specifications, and by 2026, most major carriers in the US, EU, and Asia have deployed 5G Standalone networks with advanced positioning features.

### NR E-CID (Enhanced Cell ID)

The baseline 5G positioning method combines Cell ID, Timing Advance, and Angle of Arrival. Accuracy ranges from 50 to 200 meters. This is the standard positioning method for most voice calls and routine data sessions.[^5]

### OTDOA (Observed Time Difference of Arrival)

The phone measures the time difference of arrival of Positioning Reference Signals transmitted by multiple towers. OTDOA operates passively — the phone does not need to transmit any additional signals, meaning the user cannot detect that positioning is occurring. Accuracy ranges from 10 to 50 meters.[^5]

### UTDOA (Uplink Time Difference of Arrival)

Network towers measure the arrival time of the phone's uplink signals — the normal transmissions the phone makes for registration, calls, and data. Because the network controls the measurement, UTDOA cannot be disabled or detected by the user. Accuracy ranges from 5 to 30 meters.[^5]

### Multi-RTT (Round Trip Time)

The phone exchanges timing requests with multiple towers simultaneously. Each exchange measures the round-trip time, and the combination of measurements from multiple towers triangulates the phone's position. Multi-RTT requires 5G Standalone (SA) mode — the phone must be connected to a 5G core network, not a 4G core. Accuracy ranges from 1 to 10 meters.[^5]

### Downlink Angle of Departure / Uplink Angle of Arrival

5G's massive MIMO and beamforming capabilities enable extremely precise angular measurement. The network knows which beam the phone is using for transmission and reception, providing angular resolution of a few degrees. Combined with distance estimates, this yields accuracy of 5 to 20 meters as a standard capability of 5G beam management.[^5]

### Carrier Phase Positioning

The most advanced 5G positioning method measures the phase shift of the carrier wave between the phone and multiple towers. This is conceptually similar to RTK (Real-Time Kinematic) GPS. Theoretical accuracy is below 1 meter, with practical accuracy of 0.1 to 0.5 meters. Carrier phase positioning is planned for 5G-Advanced (3GPP Release 18 and beyond).[^6]

### Forensic Implication

Law enforcement can now request "all UTDOA locations for IMSI 310410123456789 for May 14, 2026" and receive a list of GPS-level coordinates (within 5 to 30 meters) for every transmission the phone made — calls, SMS, data sessions, even background registration pings. The flip phone used as a public face in the two-phone strategy is not exempt. 4G and 5G networks use these positioning methods for legacy devices as well. The dumb phone cannot opt out.

## Stingray / DRT Box / Hailstorm

IMSI catchers represent the active surveillance side of cellular geo-location. These devices impersonate legitimate cell towers to force phones to connect and reveal their identity and location.

### The Stingray (Harris Corporation / L3Harris)

The Stingray broadcasts a stronger signal than the legitimate tower within its target area. The phone's baseband firmware automatically connects to the strongest signal, following the LTE and NR cell selection algorithms. Once connected, the Stingray sends an Identity Request message. In 4G, the phone responds with the IMSI in plaintext. In 5G, the phone responds with the SUCI (encrypted IMSI), which the Stingray cannot decrypt — but the Stingray can force the phone to fall back to 4G by broadcasting only 4G-compatible signals.

Even without the IMSI, the Stingray captures the IMEI/PEI and measures the phone's signal strength and Timing Advance to calculate its location with 50 to 200 meter accuracy. The Stingray is detectable through baseband fuzzing applications like SnoopSnitch (Android only), but detection is not prevention.

### DRT Box (Digital Receiver Technology)

The DRT Box is a passive capture device. It does not transmit any signals, making it effectively undetectable. It captures all phone metadata within a range of approximately one mile — IMSI, IMEI, location, and traffic patterns — by listening to the phone's normal transmissions to legitimate towers.

### Hailstorm (KeySight Technologies)

Hailstorm is a 5G-capable IMSI catcher that supports Multi-RTT positioning. It can force 5G phones to connect, capture their identifiers, and measure their location with the precision that 5G positioning methods provide. Detection methods for Hailstorm are still immature.

### Defense Considerations

Against Stingray devices, the two-phone strategy provides partial protection. Phone B (Wi-Fi only, no cellular modem) is not vulnerable to cellular IMSI catchers because it has no cellular radio. Phone A (the flip phone used as a public face) is fully vulnerable. 5G SUCI encryption provides partial protection against passive IMSI capture, but fallback attacks and active probing remain effective.

## Tower Dumps

A tower dump is a court order that compels a carrier to produce a list of every IMSI and IMEI that connected to a specified set of towers during a specified time window. The legal threshold is "reasonable suspicion" — lower than the probable cause required for a search warrant.[^7]

The attack on compartmentalization is devastating. A crime occurs at a specific address and time. The investigator identifies the towers serving that address. They request a tower dump for those Cell IDs covering a time window around the crime. The carrier provides a list of every device that connected. The investigator cross-references the list: IMSI A (Phone A's SIM) appears at 1:45 PM and 2:15 PM. IMEI B (Phone B's device ID) appears at 1:50 PM and 2:10 PM. The investigator concludes, with high probability, that the same person carries both devices.

If Phone B has no cellular modem, it does not appear in the tower dump. But if Phone B ever had a SIM inserted — even briefly — its IMEI is in the carrier's database. And Phone A's presence alone may be sufficient to establish suspicion.

## E911 Backdoor

All phones in the United States (and most countries) are required to transmit enhanced location information during emergency calls.[^8] This requirement overrides all privacy settings.

### E911 Phase I

The carrier provides the tower address and Cell ID. Accuracy is the tower coverage area itself — typically several hundred meters to kilometers.[^8]

### E911 Phase II

The carrier uses Timing Advance and Angle of Arrival to estimate the phone's location. Accuracy ranges from 50 to 300 meters.[^8]

### E911 Phase III (Advanced)

The phone uses a hybrid of GPS, Wi-Fi positioning, and cellular measurements to determine its location. Accuracy ranges from 10 to 50 meters. The phone transmits this location even if GPS is disabled in the user's settings.[^8]

### Continuous E911

Some carriers (T-Mobile, Verizon, and others) have implemented continuous E911 location reporting for "network optimization" purposes. The phone periodically transmits enhanced location even when no emergency call has been placed. This is disclosed in the carrier's terms of service and is legal. The data is retained by the carrier and is accessible through the same legal processes as other location records.[^8]

## Forensic Reconstruction of Movement Patterns

The most powerful application of cellular geo-location data is the reconstruction of movement patterns over time. By combining multiple data sources — Cell ID sequences, Timing Advance values, neighbor cell measurement reports, and handover logs — a forensic analyst can reconstruct a subject's movements with precision that approaches GPS tracking.[^1]

The reconstruction begins with raw CDR data: each record contains a timestamp, Cell ID, and Timing Advance. The analyst plots each point at the tower's GPS coordinate, offset by the distance indicated by the Timing Advance. Over hours, days, and weeks, the points form a trail. Periods of movement appear as sequences of changing Cell IDs and Timing Advances. Periods of stationary activity appear as repeated connections to the same towers with consistent Timing Advance values.

The analyst can identify home and work locations, frequently visited establishments, travel routes, and deviations from routine patterns. They can determine when the subject was home, when they left for work, which route they took, where they stopped along the way, and when they returned.

This reconstruction is possible without any access to the phone itself, without any GPS data, and without any cooperation from the subject. It relies entirely on data that the carrier collects as a normal part of network operation.

---

[^1]: Carpenter v. United States, 585 U.S. 296 (2018). The Supreme Court's majority opinion contains a detailed factual record of how carriers log Cell ID and Timing Advance data in Call Detail Records, how that data reconstructs historical movement, and how law enforcement obtained such records via a court order under the Stored Communications Act.

[^2]: 3GPP TS 36.211 v17, "Evolved Universal Terrestrial Radio Access (E-UTRA); Physical channels and modulation," Release 17. Section 8 defines the Timing Advance command and the TA granularity: one TA unit corresponds to 16·Ts = 16/(30720000) seconds ≈ 520 ns of round-trip propagation, equating to approximately 78 meters of one-way distance from the eNodeB.

[^3]: 3GPP TS 38.305 v17, "NG Radio Access Network (NG-RAN); Stage 2 functional specification of User Equipment (UE) positioning in NG-RAN," Release 17. Specifies NR positioning reference signals and positioning methods including E-CID with TA, noting that the finer NR subcarrier spacing yields approximately 39-meter TA granularity for the standard numerology.

[^4]: 3GPP TS 36.305 v17, "Evolved Universal Terrestrial Radio Access Network (E-UTRAN); Stage 2 functional specification of User Equipment (UE) positioning in E-UTRAN," Release 17. Defines UE positioning methods including E-CID (Cell ID + TA + AoA) and OTDOA/UTDOA, specifying accuracy requirements and performance targets for LTE positioning methods.

[^5]: 3GPP TR 38.855 v16, "Study on NR positioning support," Release 16. The 5G positioning study item technical report; establishes performance requirements and evaluation results for NR positioning methods including Multi-RTT, DL-TDOA, UL-TDOA, DL-AoD, UL-AoA, and E-CID. Multi-RTT is specified to achieve 1–10 m accuracy in indoor and outdoor dense urban scenarios.

[^6]: 3GPP TR 38.857, "Study on NR positioning enhancements," Release 17. Evaluates carrier-phase-based positioning for 5G-Advanced, documenting sub-meter theoretical accuracy and planned inclusion in Release 18 (5G-Advanced).

[^7]: In re Application of the United States for Historical Cell Site Data, 724 F.3d 600 (5th Cir. 2013). The Fifth Circuit addressed the legal standard for obtaining historical cell-site location information, examining the "specific and articulable facts" standard under 18 U.S.C. § 2703(d) for tower dump-type requests. See also United States v. Diggs (5th Cir.), examining tower dump evidence in a criminal prosecution.

[^8]: FCC Report and Order, FCC 15-9 (January 29, 2015), "Wireless E911 Location Accuracy Requirements," 47 CFR § 20.18. Establishes mandatory E911 Phase I and Phase II location accuracy requirements for wireless carriers, including horizontal and vertical accuracy standards, and requires carriers to provide dispatchable location to PSAPs. Documents the progression from Phase I (tower ID) through Phase II (TA/AoA, 50–300 m) to Phase III hybrid (10–50 m).
