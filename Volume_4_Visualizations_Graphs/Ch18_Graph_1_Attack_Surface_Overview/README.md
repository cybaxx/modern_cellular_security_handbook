# Graph 1: Attack Surface Overview (All Devices)

## Purpose

This graph compares the relative data exposure of three devices — Phone A (flip phone), Phone B (GrapheneOS), and a Computer — across six vulnerability layers. It is the foundational visualization for understanding that no device is inherently "private"; each merely shifts risk between different attack vectors.

## The Graph

```
DATA EXPOSURE INDEX (0 = none, 10 = complete deanonymization)

Layer                    Phone A (Flip)    Phone B (GrapheneOS)    Computer
─────────────────────────────────────────────────────────────────────────────
Cellular (CDRs/TA/AoA)   ██████████ 10     ██ 2 (if cellular off)  █ 1
Wi-Fi (MAC/BSSID)        █ 1                ████████ 8              ██████ 6
ISP (IP/DNS/NetFlow)     █ 1                ██████████ 10*          ██████████ 10*
Application (metadata)   ███ 3              ████ 4                  ██████ 6
Physical Co-location     ████ 4             ██████ 6                ███ 3
Legal Access (subpoena)  ██████████ 10      ████████ 8              ████████ 8
─────────────────────────────────────────────────────────────────────────────
TOTAL EXPOSURE           HIGH (38/60)       HIGH (38/60)            HIGH (34/60)

* = If ever used on residential ISP
```

## Layer-by-Layer Breakdown

### Cellular Layer

Phone A scores a maximum 10 on the cellular layer. As a flip phone with a cellular radio and a SIM card tied to a real identity (or at least a purchasable prepaid), it generates Call Detail Records (CDRs), Timing Advance (TA) measurements, and Angle of Arrival (AoA) data every time it connects to a tower. Every carrier retains these records. Every tower it pings is logged with a timestamp.

Phone B scores only 2 in this category because it operates in Wi-Fi-only mode with its cellular radio disabled. This is the single biggest privacy advantage of the mitigated two-phone strategy: Phone B generates no carrier-side location data. However, turning off cellular is not a default behavior — it requires deliberate configuration, and any slip (e.g., emergency call routing accidentally re-enabling the radio) resets this protection.

The Computer scores 1 on cellular because most laptops lack a cellular modem entirely. Some cellular-connected tablets and laptops would score higher, but for a standard desktop or laptop using Ethernet or Wi-Fi, the cellular exposure is effectively zero.

### Wi-Fi Layer

Phone A scores 1 on Wi-Fi. A flip phone typically has minimal Wi-Fi capability or is used so infrequently for data that Wi-Fi probe requests are a negligible risk. The flip phone's primary function — voice calls over cellular — does not involve Wi-Fi at all. This is one of the few areas where the flip phone genuinely outperforms a smartphone for privacy.

Phone B scores 8 on Wi-Fi because it is a modern smartphone (Google Pixel running GrapheneOS) that uses Wi-Fi constantly. Even with MAC randomization enabled, Android devices (including Pixels) have a spotty track record: they sometimes leak the real MAC in probe requests, especially after reboot. The Wi-Fi layer is the single greatest attack surface for Phone B.

The Computer scores 6 on Wi-Fi. A laptop's Wi-Fi interface also emits probe requests, stores BSSID databases, and can be geolocated through the same mechanism. Desktop computers connected via Ethernet avoid this entirely, but laptops used on public Wi-Fi generate a trail.

### ISP Layer

Phone A scores 1 on ISP — again, because it rarely uses data. If the flip phone never connects to a home Wi-Fi network and uses only cellular data (if at all), the ISP sees nothing. No IP assignment, no DNS queries, no NetFlow records. This is a significant privacy property of the flip phone design: it is invisible to the residential ISP.

Phone B and the Computer both score 10 on ISP, and the asterisk is critical: *If ever used on residential ISP.* The moment either device connects to a home Comcast, Spectrum, or AT&T router, the ISP logs the IP address assignment, every DNS query, every destination IP, and the exact timestamps. That IP is tied to a subscriber name and address. From an ISP's perspective, there is no anonymity — every connection is logged against a billing account.

This is the single most dangerous attack vector in the entire threat model. A single connection to home Wi-Fi from Phone B collapses the entire two-phone strategy.

### Application Layer

Phone A scores 3 on application metadata. Flip phones run minimal software — typically a proprietary real-time OS with no app store, no browser, no Google Play Services. However, even a flip phone generates some metadata: contact lists stored on the device, SMS headers (sender, recipient, timestamp), and call logs. If the phone runs KaiOS or a similar stripped-down OS, there is additional exposure through the browser or pre-installed apps.

Phone B scores 4 on application metadata despite running GrapheneOS. The operating system itself is hardened, but the applications installed on it (Signal, a VPN client, a burner email app) each generate their own metadata. Signal encrypts message content but not the fact that two parties are communicating, nor the frequency, timing, or message sizes. The metadata channel remains.

The Computer scores 6 on application metadata because desktop operating systems and their applications generate a richer data set: browser history, file metadata, email headers, document editing timestamps, and telemetry from background services. Even on Tails or Qubes, the applications themselves produce metadata that can be correlated.

### Physical Co-location Layer

Phone A scores 4. A flip phone carried in a pocket or bag can be detected by IMSI catchers and passive cellular monitoring. Its physical presence at a location is knowable through tower dumps and signal detection.

Phone B scores 6 because a modern smartphone emits more detectable signals: Wi-Fi probe requests, Bluetooth advertisements, NFC polls, and cellular signaling (even in airplane mode, some phones emit periodic location updates). The physical footprint of a smartphone is larger and more easily detected by passive surveillance equipment.

The Computer scores 3 because laptops are typically stationary or used in fewer locations. A laptop at home or in a coffee shop generates a physical presence signal, but it is less continuous than a phone carried on-body.

### Legal Access Layer

Phone A scores 10. Flip phones are not legally protected devices. No encryption, no warrant-proof design. A subpoena to the carrier yields CDRs, SMS metadata, cell tower logs, and subscriber information immediately. There is no technical barrier to legal access.

Phone B scores 8. GrapheneOS offers full-disk encryption, and the device can be wiped remotely. In a legal confrontation, the device itself may resist forensic extraction. However, the carrier-side data (if the cellular radio was ever on) and the ISP-side data (if ever connected at home) are still available through legal process. The device is resilient; the network is not.

The Computer scores 8 for similar reasons. Full-disk encryption (FileVault, LUKS, BitLocker) protects data at rest, but cloud services, email providers, and ISPs all retain logs accessible by subpoena.

## Key Insight

Phone A and Phone B have an identical total exposure score of 38 out of 60. The Computer scores 34. This is the most critical takeaway of the entire graph: **Phone B is not "more private" than Phone A in aggregate.** It merely shifts the risk from cellular-layer attacks (CDRs, tower triangulation) to Wi-Fi and ISP-layer attacks (probe requests, DNS logs, IP correlation).

A naive observer sees "Phone B runs GrapheneOS" and assumes superior privacy. The graph demonstrates that the total data exposure index is nearly identical. The difference is in the distribution, not the magnitude. A cell-forensic adversary who cannot track Phone A through Wi-Fi will instead track Phone B through ISP logs. A law enforcement agency that cannot tap Phone B's encrypted storage will subpoena the carrier for Phone A's tower data.

The implication is sobering: the two-phone strategy does not reduce total exposure. It diversifies it. The adversary must work across two attack surfaces instead of one, but the amount of exploitable data is roughly the same. The strategy's value lies in compartmentalization — forcing the adversary to correlate two separate identities — not in reducing the absolute quantity of leaked data.

## Limitations of the Exposure Index

The exposure index is a comparative tool, not an absolute measurement. Several limitations must be acknowledged:

**Weighting is uniform across layers.** In reality, not all layers carry equal forensic weight. Cellular and ISP layers are typically more valuable to an adversary because they provide legally admissible evidence with known chain-of-custody procedures. Application metadata is less reliable because it depends on app-specific logging practices that vary across services.

**The index does not account for adversary capability.** A score of 10 on cellular exposure means different things to different adversaries. For a cybercriminal, cellular CDRs are inaccessible (they cannot subpoena carriers). For law enforcement, cellular CDRs are the first and most reliable source of evidence. The exposure index must be interpreted in the context of the specific adversary's capabilities and legal authority.

**The index ignores the cost of exploiting each layer.** Exploiting cellular data requires a subpoena or lawful intercept authorization. Exploiting Wi-Fi data requires physical proximity or access to BSSID databases. Exploiting ISP data requires a subpoena or court order. Some layers are cheap to exploit (Wi-Fi sniffing costs $50 in hardware) while others are expensive (carrier subpoenas require legal process). A high exposure score on a hard-to-exploit layer is less dangerous than a medium score on an easy-to-exploit layer.

**The index is static.** It represents exposure at a single point in time. In reality, exposure changes: new vulnerabilities are discovered, carrier retention policies change, and adversary capabilities evolve. An exposure score from 2024 may look very different in 2026 as 5G positioning improves and carrier data retention expands.

## Practical Application

For a forensic analyst evaluating a target's operational security, the procedure is:

1. Identify all devices the target uses (phones, tablets, laptops, desktops, smartwatches)
2. For each device, score each layer 0-10 based on device characteristics and usage patterns
3. Sum the scores to get a total exposure index
4. Identify the layers with the highest scores — these are the adversary's easiest attack paths
5. Do not treat total exposure as a meaningful metric (identical totals can mask very different risk profiles)

In the two-phone strategy, the key finding is not the total but the asymmetry: Phone A exposes on cellular and legal; Phone B exposes on Wi-Fi and ISP. An adversary who only has access to carrier data will see Phone A but not Phone B. An adversary who only has ISP data will see Phone B but not Phone A. The strategy works only if the adversary lacks access to both data sources simultaneously. Once they obtain both (through a joint investigation, data sharing agreement, or physical surveillance), the compartmentalization collapses.

## Conclusion

The Attack Surface Overview graph establishes the foundational forensic principle of the entire volume: privacy is not a property of a device but of the total system, and every device leaks data somewhere. The choice is not between leaking and not leaking, but between which layer bears the risk. The two-phone strategy succeeds not by eliminating exposure but by distributing it across two separate identity domains — a defense that holds only as long as those domains never intersect.

## Forensic Relevance

For forensic analysts, this graph provides a framework for evaluating any device's privacy profile. When assessing a target's operational security, map each device against these six layers. The total exposure score is less important than the shape of the distribution: a device that concentrates risk in one or two layers (e.g., Phone A's cellular score of 10) creates a single point of failure that an adversary can exploit with a single legal instrument (a carrier subpoena). A device that distributes risk more evenly (Phone B) forces the adversary to use multiple instruments but offers more attack surfaces.

The graph also reveals the counterintuitive truth that a "dumb" flip phone and a "secure" smartphone have the same forensic footprint — just in different domains. Any privacy assessment that ignores ISP-layer exposure is fundamentally incomplete.
