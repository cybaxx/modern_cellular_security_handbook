# Chapter 46: Emerging Attack Surfaces

The forensic landscape documented in Volumes 2 and 3 reflects the state of surveillance technology as of 2024–2026. That landscape is not static. New attack surfaces are emerging from three directions simultaneously: new connectivity infrastructure (satellite internet, eSIM), new positioning technologies (5G Multi-RTT, UWB), and new analytical capabilities (AI-assisted behavioral correlation). Each of these deserves careful attention because they alter the risk calculus of strategies that were sound under older assumptions.

This chapter does not provide final verdicts. The technologies described here are in active development, deployment, and research. Where firm conclusions can be drawn, they are stated plainly. Where uncertainty remains, it is acknowledged rather than papered over. Researchers and high-risk users should treat this chapter as a living threat assessment, not a settled reference.

---

## Starlink and Low-Earth Orbit Satellite Internet

### The Technology

SpaceX Starlink, Amazon Kuiper, and OneWeb are deploying low-earth orbit (LEO) satellite internet constellations that deliver broadband speeds to areas previously underserved or completely unserved by terrestrial ISPs. As of 2026, Starlink operates over 6,000 satellites and serves millions of subscribers globally. Ground-based terminals communicate with satellites at altitudes of 340–570 km, with latency of 20–40 ms — low enough for real-time communications.

### The Attack Surface

The conventional ISP privacy problem assumes your home ISP can be subpoenaed to reveal your connection logs. Satellite internet does not eliminate this problem — it relocates it. Starlink's service is tied to a specific terminal hardware unit (a registered device with a serial number) and a billing account. SpaceX is a U.S.-based company subject to U.S. legal process. A subpoena to SpaceX yields the same data a subpoena to Comcast yields: IP address assignments, connection timestamps, and billing identity.

The mobility problem is more subtle. A user who moves their Starlink terminal — or who uses Starlink's in-motion service on a vehicle — creates a different metadata profile than a fixed ISP. Terminal location is tracked by Starlink for beam management — this is technically inherent to phased-array beam steering. This location telemetry is retained and, in principle, subject to legal process. Starlink's published privacy policy acknowledges collection of device and usage data; a January 2026 policy update expanded SpaceX's right to use customer data including usage metadata.[^5] Independent researchers at the University of Maryland (2024) also demonstrated that Starlink terminal BSSIDs were being used to geolocate devices via Wi-Fi positioning databases — SpaceX subsequently deployed BSSID randomization in response.[^6] No specific retention period for beam management telemetry has been publicly disclosed, and no court-published subpoena response equivalent to Signal's 2016 disclosure exists for Starlink. The retention claim should be treated as technically certain but legally unquantified.

The practical implication for the two-phone strategy: if Phone B connects to a Starlink terminal at a fixed location (a cabin, a friend's property, a rented space), that terminal's billing identity and physical location create a record linking Phone B's activity to a place. If that place can be linked to your identity — even indirectly, through property records or cell tower data from Phone A — the compartmentalization fails exactly as it would with a home ISP connection.

| Threat Level | Starlink Privacy Assessment |
|---|---|
| **Advertisers / Data Brokers** | No meaningful difference from terrestrial ISP |
| **Local Police** | Subpoena to SpaceX possible; same risk as domestic ISP |
| **Federal LE / Intelligence** | Starlink terminal location data available via legal process; satellite constellation beam logs retained |
| **State-Level (non-US)** | U.S. law governs; SpaceX has resisted some foreign government requests, but outcomes vary |

### Mitigation

Using Starlink as a "neutral" connection point only works if the terminal itself is not linked to you. A public Starlink terminal in a library, hotel, or campground — where the terminal registration belongs to the establishment — provides roughly the same anonymity as public Wi-Fi, with similar caveats (MAC address logging, connection timestamps shared with service provider). A privately-registered terminal, or a terminal physically located at a place that correlates to your movements, provides no anonymity advantage over a home ISP.

---

## eSIM Forensics

### The Technology

Embedded SIMs (eSIMs) replace the physical removable SIM card with a programmable chip soldered to the device's mainboard. The eSIM can be provisioned and re-provisioned remotely: you download a carrier profile, and the device behaves as though a new SIM has been inserted. Most flagship smartphones sold after 2020 support eSIM. Some devices are eSIM-only.

### The Attack Surface

The privacy implications of eSIM are underappreciated in most security guidance. Physical SIM swapping has a clean property: the old SIM stops being used and the new one starts. If the new SIM is purchased with cash and not registered, the transition leaves a gap in carrier records. The old SIM goes dark; the new SIM appears with no prior history.

eSIM provisioning is different. Every eSIM profile change is logged by the carrier's provisioning server. The log contains the ICCID (integrated circuit card identifier) of the previous profile, the ICCID of the new profile, the device's EID (embedded identity document — a permanent hardware identifier), and the timestamp of the change. The EID is immutable. It cannot be changed, randomized, or spoofed. It is the hardware fingerprint of the device itself.

This creates a chain of custody problem. If you provision a new eSIM profile on an existing device, the carrier's provisioning logs link the new profile to the device's permanent EID. If any previous profile on that device was linked to your identity, the chain is established. The new "anonymous" profile is retroactively attributed to the same device, and by extension, to you.

The EID is defined and governed under GSMA SGP.29 ("EID Definition and Assignment Process," v1.1, March 2024) — the dedicated standard for EID assignment and persistence.[^7] Consumer eSIM remote provisioning is governed by GSMA SGP.22 (RSP Technical Specification, v3.1, December 2023).[^8] Security researchers at Security Exploration (Poland) have demonstrated successful cloning of eSIM profiles at the provisioning protocol layer — exploiting weak test keys in GSMA TS.48 — but these attacks clone the operator *profile*, not the EID chip itself. The EID hardware binding remained intact in the demonstrated attacks; the vulnerability is at the remote provisioning layer.[^9] The practical takeaway is unchanged: you cannot create a new device identity by changing an eSIM profile. The EID persists regardless.

> **The EID is not a SIM identifier. It is a device identifier. A new eSIM profile does not create a new phone.**

| Operation | Physical SIM | eSIM |
|---|---|---|
| Replace SIM with cash-purchased replacement | Old SIM history ends; new SIM has no prior history | Impossible to replicate — EID persists across profile changes |
| Buy a pre-provisioned SIM from a store | No device linkage at point of purchase | N/A |
| Provision anonymously over the air | N/A | Provisioning server logs EID + previous profile ICCID |
| Carry device with SIM removed | No cellular broadcast | No cellular broadcast, but EID persists in provisioning logs |

### Mitigation

For high-risk users, the mitigation is simple and non-negotiable: **eSIM devices cannot serve as the anonymous phone in a two-phone strategy.** Phone A must be a physical-SIM device. Phone B, if it uses cellular at all, must use a physical SIM. If you purchase a new device that is eSIM-only, that device cannot be used in any role where cellular anonymity is required.

If you are currently using an eSIM-only device as Phone B, assume the strategy is compromised and replace the device with a physical-SIM capable handset.

---

## AI-Assisted Behavioral Correlation

### The Technology

Traditional cell phone forensics relies on discrete events: tower connections, call records, IP address assignments. The adversary asks "was this device at this tower at this time?" AI-assisted correlation asks a different question: "which of these 10,000 devices has the behavioral fingerprint that matches this person?"

The distinction matters because behavioral correlation does not require identifying a specific device. It requires only that a pattern of behavior — location dwell times, app usage cadence, typing rhythm, content preferences, sleep schedule, movement speed — be distinctive enough to match across devices. If your two phones share any behavioral overlap (you use both at the same times of day, both in the same geographic range, both with similar communication patterns), machine learning models trained on population data can identify the pairing with statistical confidence even without a direct hardware or network link.

### The Specific Risks

**Location dwell time correlation.** If Phone A and Phone B both show extended dwell times at a location that is not a common transit hub — a specific shopping center, a relative's neighborhood, a recurring medical appointment — the overlap is statistically significant. At scale, this correlation is reliable enough for investigative leads even if not courtroom-admissible evidence.

**Communication timing correlation.** If the person using Phone A goes quiet on messaging every time Phone B becomes active, the temporal anti-correlation is itself evidence of a two-phone strategy. Investigators call this "device shadowing" — one device falls silent as another activates on the same schedule.

**Typing cadence fingerprinting.** Research published between 2020 and 2025 has demonstrated that individuals have distinctive typing rhythms. Latency between keystrokes, error patterns, and deletion habits create a fingerprint that can match an anonymous device to a known identity with accuracy exceeding 95% in controlled, single-device conditions.[^1] The "across devices" scenario is more limited: cross-device identification degrades significantly when users switch between hardware keyboards and touchscreens, and remains an active research challenge rather than a deployed capability.[^2] The practical threat today is single-device: if your anonymous phone runs any application that collects input timing telemetry — input method editors (IME keyboards), social media apps, browser autofill — that telemetry can be correlated to typing patterns from a known identity device. This technique requires either active key logging or an application that sends timing telemetry — it is not passive network surveillance. Applications with broad permissions routinely collect this data.

**Wi-Fi probe request behavioral patterns.** Even with MAC randomization, the timing and frequency of probe requests, the specific channel scanning behavior, and the probe packet content can be used to fingerprint a specific device chipset. This is not theoretical: multiple peer-reviewed papers have demonstrated that MAC randomization is largely defeatable through probe request behavioral analysis. Timing-based attacks achieve re-identification accuracies of 92–99% in real-world datasets.[^10][^11][^12] Information Elements embedded in probe requests — supported rate sets, channel lists, vendor-specific tags — create a device profile that is distinct from and independent of the rotating MAC address.[^13] Two phones from the same manufacturer, purchased around the same time, may share behavioral signatures that distinguish them from the background population.

| Correlation Method | Data Source | Adversary Required | Countermeasure |
|---|---|---|---|
| Location dwell time | Carrier CDRs, app location permissions | Subpoena + ML analysis | Never use phones in same geographic area |
| Communication timing | Carrier message logs, app server logs | Subpoena + temporal analysis | Randomize communication windows; enforce strict schedules |
| Typing cadence | Apps with input telemetry, IME keyboards | App-level data access | Use GrapheneOS with restricted permissions; no third-party keyboards |
| Wi-Fi probe fingerprinting | Passive Wi-Fi capture | Physical proximity or deployed sensors | Faraday bag discipline; disable Wi-Fi when not in use |
| Social graph overlap | Signal metadata, app contact lists | Legal process to app providers | Strict contact separation; different contact networks on each phone |

### What This Means for the Two-Phone Strategy

The behavioral correlation threat does not break the two-phone strategy — it raises the operational discipline required to maintain it. A two-phone strategy executed with rigorous schedule discipline, geographic separation, and strict permission controls on Phone B is still highly effective against behavioral correlation. A two-phone strategy executed casually — same daily schedule, same geographic range, apps with broad telemetry permissions — is vulnerable to correlation even without a hardware or network link.

The practical takeaway: **technical mitigations alone are insufficient.** Behavioral discipline is not optional for a strategy designed to defeat adversaries with analytical capabilities.

---

## UWB, Bluetooth 5.x, and Crowd-Sourced Tracking Networks

### The Technology

Ultra-wideband (UWB) is a short-range radio technology capable of centimeter-level positioning accuracy. Introduced commercially in Apple iPhone 11 (2019) and Samsung Galaxy devices, UWB enables precise device-to-device ranging and location. It is used in AirDrop, AirTag precision finding, Samsung SmartThings, and automotive keyless entry.

Bluetooth 5.x, particularly the BLE (Bluetooth Low Energy) advertising protocol, enables passive broadcast of device identifiers to nearby receivers. Apple's Find My network and Google's Find My Device network use BLE broadcasts from hundreds of millions of enrolled devices to passively track any Bluetooth-capable device — including devices that are not enrolled in the network.

### The Tracking Mechanism

Apple's Find My network works as follows: AirTags (and AirTag-like accessories) broadcast a rotating Bluetooth identifier. Any Apple device within Bluetooth range reports the identifier, the device's location, and the timestamp to Apple's servers — silently, without user intervention. The reporting device's owner receives no notification. Apple aggregates these reports to provide location of the tracked device to the AirTag's owner.

Two rotation mechanisms operate on different timescales. The cryptographic public key embedded in the BLE advertisement payload rotates approximately every 15 minutes.[^3] Only the owner's paired device, holding the corresponding private key, can correlate successive identifiers across rotation boundaries — meaning a passive BLE scanner cannot link two advertisements from the same AirTag if they straddle a rotation event. The BLE device address (the lower-layer hardware address) rotates approximately once per day when the AirTag is separated from its owner's device. The 15-minute cryptographic rotation is the operationally meaningful anti-tracking protection. A 2026 relay attack demonstrated that AirTag location can be spoofed by replaying captured BLE signals to different geographic areas, but this is an attack on the location data quality, not on the rotation mechanism itself.[^4]

The critical privacy concern is the inverse case: if a small BLE device is placed inside your bag, wallet, phone case, or vehicle, every Apple device you pass reports your location to the person who placed it. The attack does not require your phone to be an Apple device or enrolled in Find My. It requires only that you are within BLE range of any Apple device (which, in most urban environments, is constant).

Google's Find My Device network, fully deployed in 2024, operates on the same principle for Android devices. The combined reach of Apple Find My and Google Find My Device covers virtually every location where mobile phones are in use.

| Tracking Technology | Range | Accuracy | Stealth |
|---|---|---|---|
| BLE passive advertising (AirTag-style) | 10–30m per hop; unlimited via network relay | 5–15m (urban); 50–200m (rural) | Complete — no indication on tracked device |
| UWB precision ranging | <10m | 10–30 cm | Requires UWB-capable device on both ends |
| BLE RSSI triangulation | 30–50m | 2–5m with 3+ reference points | Low — standard BLE broadcast |
| Bluetooth 5.x directional finding (AoA/AoD) | 50m | 1m | Requires specialized receiver hardware |

### Implications for the Two-Phone Strategy

Physical tracking via planted BLE devices is not a cellular forensics problem — it is a physical security problem. No amount of SIM rotation, MAC randomization, or Faraday bag discipline protects against a BLE tracker placed inside your bag without your knowledge.

The mitigation is physical inspection. High-risk users should periodically scan for unexpected BLE devices using a Bluetooth scanner application or dedicated hardware. Apple devices running iOS 14.5+ alert users if an unknown AirTag appears to be traveling with them for an extended period. Android devices running Google Play Services 23.x+ provide similar alerts through the Find My Device application. These alerts are imperfect — they can be delayed, spoofed, or absent — but they represent a baseline detection capability.

The deeper implication: the crowd-sourced tracking networks operated by Apple and Google have fundamentally changed the cost of physical tracking. A physical tail that once required dedicated personnel now requires a $30 device and a smartphone application. Any analysis of a threat model that involves physical surveillance must account for this shift.

---

## Meshtastic, goTenna, and Mesh Network Communications

### The Technology

Mesh communication networks — including Meshtastic (LoRa radio), goTenna Mesh, and Reticulum — provide peer-to-peer radio communication that does not rely on cellular infrastructure. Messages hop between nodes carried by users in the network. The sender does not need a cellular connection. There is no carrier. There is no SIM. There is no CDR.

### The Privacy Properties

Mesh networks eliminate the carrier metadata problem entirely. A message transmitted via Meshtastic leaves no carrier record because there is no carrier. There is no tower, no CDR, no IMSI, and no billing identity. For the specific threat of carrier subpoenas and lawful intercept, mesh networks represent a genuine gap in the adversary's toolkit.

The privacy properties are not universal, however:

**Physical layer forensics.** LoRa radio transmissions are directional and locatable. A receiver with a directional antenna can triangulate a transmission source to within meters. This requires physical proximity and active monitoring — it is not passive mass surveillance — but it is technically feasible for a motivated adversary.

**Traffic analysis.** Even encrypted mesh traffic has metadata: transmission timing, message size, frequency, and relay paths. A network-level observer who can monitor multiple nodes can reconstruct the topology of communications even without decrypting content.

**Device registration.** Some mesh networks (goTenna's commercial products) have registered hardware. The device serial number is tied to a purchase identity. Open-source hardware (Meshtastic on generic LoRa modules) avoids this problem entirely.

**Limited range.** LoRa mesh range is approximately 2–10 km in line-of-sight conditions, significantly less in dense urban areas. This limits practical use to situations where communicating parties are geographically proximate or where a relay network has been pre-deployed.

### Role in the Privacy Architecture

Mesh communications are not a replacement for the two-phone strategy. They are a supplement for specific operational scenarios: communications within a protest area, communications in a jurisdiction where cellular infrastructure has been shut down or is unreliable, or communications where the goal is specifically to avoid carrier metadata.

For most users, the complexity and range limitations of mesh communications make them impractical for everyday use. For researchers and high-risk users who understand the tradeoffs, they represent a genuine supplement to existing strategies — not a panacea, but a tool that eliminates a specific class of surveillance that cellular and internet-based communications cannot.

---

## Summary: Updating the Threat Model

The emerging attack surfaces described in this chapter do not invalidate the analysis in Volumes 2 and 3. They extend it. The six vulnerability layers — cellular, Wi-Fi, ISP, application, physical, and legal — remain the core framework. What changes is the specific capabilities within each layer:

| Layer | 2024 State | 2026 Emerging Risk |
|---|---|---|
| **Cellular** | CDRs, tower location, 5G Multi-RTT | eSIM EID persistence creates immutable device fingerprint |
| **Wi-Fi** | MAC randomization broadly deployed but demonstrably defeatable via behavioral analysis | Timing + Information Element fingerprinting achieves 92–99% re-identification in published research |
| **ISP** | Terrestrial ISP subpoena | Satellite ISP (Starlink) subpoena; terminal location data |
| **Application** | App metadata, account linkage | Typing cadence fingerprinting via input telemetry |
| **Physical** | Manual surveillance, co-location | $30 BLE tracker + crowd-sourced tracking networks |
| **Legal** | Carrier subpoenas, device seizure | Provisioning server records for eSIM EID chains |

The pattern is consistent: the cost of targeted surveillance is falling, the precision is increasing, and the data sources are multiplying. Strategies that were adequate in 2022 require review. The two-phone strategy, executed with the discipline described in Volume 6, remains effective against most non-state threats. Against state-level adversaries with access to multiple data layers simultaneously, no electronic strategy is sufficient — a conclusion that has not changed and is unlikely to change.

---

## References and Source Notes

[^1]: Martins et al., "Keystroke dynamics for intelligent biometric authentication with machine learning," *Discover Applied Sciences*, Springer, 2025. Single-device CNN with boosting achieved 99.95% accuracy on CMU Benchmark Dataset. "The Improved Biometric Identification of Keystroke Dynamics Based on Deep Learning Approaches," *Sensors* 24(12):3763, 2024 (PMC11207587). Earlier ANN-based work: 95.05% across 51 users on constrained password typing task.

[^2]: Yang et al., "Cross-device free-text keystroke dynamics authentication using federated learning," *Personal and Ubiquitous Computing* 28:491–505, 2024. Explicitly identifies device-specific model degradation when switching between desktop keyboards and touchscreen input as an active research challenge. See also: "Continuous User Identification Across Devices Using Keystroke Dynamics," Springer — acknowledges the cross-device degradation problem. ACM Computing Surveys, "Keystroke Dynamics: Concepts, Techniques, and Applications," dl.acm.org/doi/10.1145/3733103.

[^3]: Adam Catley, "AirTag Reverse Engineering," adamcatley.com/AirTag.html. Primary technical reverse-engineering source; documents 15-minute cryptographic key rotation and daily BLE device address rotation cycle.

[^4]: "Apple AirTag tracking can be misled by replayed Bluetooth signals," *Help Net Security*, April 2026. Documents relay attack spoofing AirTag geolocation via replayed BLE signals.

[^5]: Starlink Global Privacy Policy, starlink.com/legal/documents/DOC-1000-41799-67. January 2026 update expanded SpaceX rights to use customer metadata for AI training.

[^6]: "Researchers Expose Privacy Risks in Apple and Starlink Geo-Location Data," CircleID, 2024, citing University of Maryland research. Starlink terminal BSSID geolocatability via crowdsourced Wi-Fi positioning databases; subsequently mitigated by Starlink BSSID randomization deployment.

[^7]: GSMA SGP.29 v1.1, "EID Definition and Assignment Process," March 2024. gsma.com/solutions-and-impact/technologies/esim/wp-content/uploads/2024/03/SGP.29-v1.1.pdf. Governing standard for EID permanence and assignment.

[^8]: GSMA SGP.22 v3.1, "RSP Technical Specification for Consumer Devices," December 2023. Governing standard for consumer eSIM remote SIM provisioning protocol.

[^9]: Security Exploration (Poland), "Billions of eSIMs vulnerable: Researchers manage to clone and spoof phone numbers," *CyberNews*, 2024. Demonstrated profile cloning via exploitation of weak test keys in GSMA TS.48 Generic Test Profile v6.0 and earlier; ARM Kigen eUICC. EID hardware binding remained intact; attack operated at provisioning protocol layer. IEEE Xplore: "Mobile Forensic Investigation: Extractions and Connectivity Isolation in Phones Utilizing eSIM, iSIM Technology," 2024 (doi:10.1109/10527246).

[^10]: "StateFi: Effectively Identifying Wi-Fi Devices through State Transitions," arXiv:2507.02478. Achieves 92–97% re-identification accuracy using finite state machine models of probe request behavior on large public datasets.

[^11]: "MAC address de-randomization for WiFi device counting: Combining temporal- and content-based fingerprints," *Computer Networks*, ScienceDirect, 2022. >98% of successive probe bursts from one device arrive within 65 ms window; exploitable for re-identification.

[^12]: Vanhoef et al., "Why MAC Address Randomization is not Enough: An Analysis of Wi-Fi Network Discovery Mechanisms," ACM CCS 2016. Foundational paper establishing that Information Elements in probe requests fingerprint devices independent of MAC address.

[^13]: "Defeating MAC Address Randomization Through Timing Attacks," ResearchGate. "Exploration of User Privacy in 802.11 Probe Requests with MAC Address Randomization," arXiv:2206.10927, 2022. "MAC Address De-Randomization using Multi-Channel Analysis," arXiv:2408.01578, 2024.
