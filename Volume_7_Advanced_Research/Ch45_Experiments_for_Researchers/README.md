# Chapter 45: Experiments for Researchers

## A Call to Practical Investigation

Theory is necessary but not sufficient. The forensic claims in this handbook should be tested, validated, and challenged by independent researchers. This chapter provides practical experiments you can run to investigate your own devices, networks, and operational security.

These experiments are designed to be accessible to a motivated researcher with modest equipment. Some require hardware (software-defined radio, Wi-Fi monitoring adapter). Others require only your phone and a willingness to file legal requests.

## Experiment 1: Capture Your Own Wi-Fi Probe Requests

### Objective

Observe what your phone transmits over Wi-Fi when it is not connected to any network. This reveals your permanent MAC address, probed SSIDs, and device fingerprint.

### Equipment

- Computer with a Wi-Fi adapter that supports monitor mode (Alfa AWUS036ACH, TP-Link TL-WN722N, or internal adapter on Linux with compatible driver)
- Wireshark (free, cross-platform)
- Aircrack-ng suite (free)

### Procedure

1. Put your Wi-Fi adapter into monitor mode:
   ```
   sudo airmon-ng start wlan0
   ```
2. Start capturing on the monitoring interface:
   ```
   sudo wireshark
   ```
3. Select the monitoring interface (usually `wlan0mon`).
4. Apply a display filter for probe requests:
   ```
   wlan.fc.type_subtype == 4
   ```
5. Walk past your phone (or have someone carry it past your capture station) with Wi-Fi enabled.
6. Observe the probe requests. Note:
   - The source MAC address (is it randomized or permanent?)
   - The SSID being probed (does it reveal your home or work network name?)
   - The supported rates and vendor-specific information elements

### What to Look For

- **MAC randomization failure:** Compare the MAC in probe requests to the MAC seen when the device connects. If they match, randomization is broken or not enabled.
- **SSID leakage:** If your phone probes for "HomeNetwork" or "WorkWiFi", you are leaking location-relevant information.
- **Vendor fingerprinting:** The OUI in the MAC address and the supported rates can identify your device manufacturer.

## Experiment 2: Request Your Own Carrier Records

### Objective

File legal requests to obtain your own data from your mobile carrier. This reveals exactly what the carrier logs and retains about your phone.

### Equipment

- Your phone number and account information
- A valid government ID (you are filing as the subscriber)
- Patience (processing can take 30–90 days)

### Procedure

#### Option A: GDPR Data Subject Access Request (EU)

1. Send a GDPR Article 15 request to your carrier's data protection officer.[^1]
2. Request all personal data, including:
   - Call detail records (CDRs)
   - Location data (Cell IDs, Timing Advance, triangulation data)
   - Subscriber information (IMSI, IMEI, billing address)
   - IP assignment logs
   - Any data shared with third parties
3. The carrier must respond within 30 days and cannot charge a fee.
4. Analyze the response. What data is included? What is excluded? What retention period is applied?

#### Option B: CPNI Request (US)

1. Under the Telecommunications Act, you can request your carrier's Customer Proprietary Network Information (CPNI).
2. Contact your carrier's privacy department and request all CPNI data.
3. This data includes call detail records, location data, and service usage patterns.

#### Option C: Subpoena Your Own Records via Third-Party Service

Services exist that help you request your own data from carriers, ISPs, and online platforms. These automate the process and help interpret the response.

### What to Look For

- **Retention period:** How many months of data does the carrier retain? Does it match the claimed 18 months?
- **Location accuracy:** Does the data include Timing Advance values? Cell IDs? GPS coordinates?
- **Data categories:** What columns are in the CDR? Is there data you did not expect?
- **Third-party sharing:** Does the carrier share data with data brokers or analytics companies?

## Experiment 3: Test Faraday Bag Effectiveness

### Objective

Verify that a faraday bag blocks all RF communication. Many cheap "faraday" bags leak significantly.

### Equipment

- The faraday bag to be tested
- A phone with an active cellular connection (test phone, not your personal device)
- A phone with Wi-Fi enabled
- A software-defined radio (optional, for rigorous testing)

### Procedure — Simple Test

1. Place the phone inside the faraday bag and close the seal completely.
2. Call the phone from another device.
3. If the call goes to voicemail (phone unreachable), the bag is blocking cellular frequencies.
4. If the phone rings, the bag is leaking. Return it.
5. Test at least 3 times with different orientations of the phone inside the bag.

### Procedure — Rigorous Test (with SDR)

1. Use a software-defined radio (USRP, HackRF, or RTL-SDR) with a spectrum analyzer tool (GQRX, SDR#).
2. Record the baseline RF environment with the phone outside the bag.
3. Place the phone inside the bag and record again.
4. Compare signal levels at:
   - Cellular frequencies (700 MHz, 800 MHz, 1900 MHz, 2600 MHz)
   - Wi-Fi frequencies (2.4 GHz, 5 GHz)
   - Bluetooth frequencies (2.4 GHz)
5. Any signal above the noise floor indicates a leak.

### What to Look For

- **Zipper gaps:** Most bags leak at the zipper seam. Test with the phone oriented so the antenna points at the zipper.
- **Material fatigue:** Bags degrade with folding. Test new bags and bags that have been folded 100+ times.
- **Low-cost bags:** Many bags under $15 use single-layer shielding that is ineffective against 5 GHz and above.

## Experiment 4: Analyze Your Own Device's Location Leaks

### Objective

Discover which applications and services on your phone transmit location data, and to whom.

### Equipment

- Rooted Android phone or a phone with GrapheneOS (which has better logging)
- Wireshark or tcpdump
- A DNS logging server (Pi-hole, or a custom DNS resolver)
- mitmproxy (optional, for HTTPS inspection)

### Procedure

1. Set up a mobile hotspot (or use a Wi-Fi network you control) and route all traffic through a capture point.
2. Configure the capture point to log:
   - All DNS queries
   - All destination IP addresses
   - Connection timestamps and durations
3. Use your phone normally for 24 hours.
4. After 24 hours, analyze the logs:
   - Which domains are queried most frequently?
   - Are any of them location services (e.g., `location.googleapis.com`, `ls.apple.com`)?
   - Are there unexpected periodic queries (suggesting background location transmission)?
5. Cross-reference with app permissions:
   - Which apps have location permission?
   - Do the periodic queries correspond to apps with location permission?
   - Do any queries come from apps without visible location permission (suggesting OS- or firmware-level transmission)?

### What to Look For

- **Background location queries:** Does your phone contact location services even when you are not using any location-aware app?
- **Third-party location aggregators:** Are any of the queried domains belonging to data brokers or analytics companies?[^2]
- **Unencrypted location data:** Are any of the queries in plain HTTP (not HTTPS)?
- **Carrier-specific queries:** Does your phone contact carrier-specific domains with diagnostic or location data?

## Experiment 5: Signal Metadata Analysis

### Objective

Understand what metadata Signal's servers can observe about your communications.

### Equipment

- Two phones with Signal installed
- A network capture point (see Experiment 4)

### Procedure

1. Capture all traffic between Phone B and Signal's servers.
2. Register Signal on Phone B with a number that is not linked to your identity.
3. Send a message to a contact.
4. Analyze the captured traffic:
   - What data is in the TLS handshake (SNI)?
   - Can you determine that the traffic is Signal (packet sizes, timing patterns, IP range)?
   - Can you identify which contact you are messaging?
5. Repeat with Signal's censorship circumvention mode enabled.
6. Repeat with Signal routed through Tor (Orbot).[^3]

### What to Look For

- **Traffic fingerprinting:** Can you identify Signal traffic by packet size distribution alone?
- **Contact graph inference:** Can you determine who you are talking to based on connection timing patterns?
- **Metadata in the clear:** Is any metadata visible outside the TLS encryption (beyond SNI and IP addresses)?

## Tools Reference

### Wireshark

Wireshark is the standard network protocol analyzer. It supports thousands of protocol dissectors including 3GPP protocols (with the right plugins). Use it for:

- Capturing and analyzing Wi-Fi management frames
- Inspecting DNS queries and responses
- Analyzing TLS handshake metadata
- Examining DHCP traffic for device fingerprinting

### SnoopSnitch

SnoopSnitch is an Android app that analyzes mobile network security. It requires root access and a Qualcomm-based device. It can:

- Detect IMSI catchers (Stingrays)
- Monitor baseband security
- Analyze network encryption downgrade attacks
- Log 3GPP signaling messages

### Cellebrite Alternatives

For forensic device extraction without a commercial license:

- **AFLogical OSE:** Open-source forensic acquisition for Android
- **LiME (Linux Memory Extractor):** Extracts RAM from Android devices
- **Fridump:** Memory dumping tool using Frida
- **ABE (Android Backup Extractor):** Extracts Android backup data
- **Magnet Forensics free tools:** Various free acquisition tools

## Python Graph Generation

The following Python code generates the forensic graphs presented in this handbook. Use these for research presentations, threat modeling workshops, or your own documentation.

```python
import matplotlib.pyplot as plt
import numpy as np

# Graph 1: Attack Surface Overview
layers = ['Cellular', 'Wi-Fi', 'ISP', 'App', 'Physical', 'Legal']
phone_a = [10, 1, 1, 3, 4, 10]
phone_b = [2, 8, 10, 4, 6, 8]
computer = [1, 6, 10, 6, 3, 8]

x = np.arange(len(layers))
width = 0.25

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(x - width, phone_a, width, label='Phone A (Flip)')
ax.bar(x, phone_b, width, label='Phone B (GrapheneOS)')
ax.bar(x + width, computer, width, label='Computer')
ax.set_ylabel('Data Exposure Index (0-10)')
ax.set_title('Attack Surface Overview by Device')
ax.set_xticks(x)
ax.set_xticklabels(layers)
ax.legend()
ax.set_ylim(0, 11)
plt.savefig('graph1_attack_surface.png', dpi=150)

# Graph 2: Cellular Tracking Accuracy Over Time
years = [2015, 2018, 2021, 2024, 2026, 2029]
accuracy_m = [2500, 400, 100, 30, 8, 2]

fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(years, accuracy_m, marker='o', linewidth=2, markersize=8)
ax.set_yscale('log')
ax.set_ylabel('Location Accuracy (meters, log scale)')
ax.set_xlabel('Year')
ax.set_title('Cellular Tracking Accuracy Improvement (4G to 5G)')
ax.grid(True, alpha=0.3)
for i, (y, a) in enumerate(zip(years, accuracy_m)):
    ax.annotate(f'{a}m', (y, a), textcoords="offset points", xytext=(0, 10), ha='center')
plt.savefig('graph2_cellular_accuracy.png', dpi=150)
```

## The Researcher's Reflection

The privacy researcher who compiled this handbook went through the same journey you are on. Starting with the original two-phone strategy, they stress-tested it by roleplaying as a skeptic, identified forensic gaps, mapped attack surfaces, quantified the OpSec burden, and tested their own willingness to follow the rules.

The key insight from this process: the two-phone strategy is not wrong. It is contextual. It is a tool, not a religion. Use it where it fits.

The most dangerous phrase in privacy is "I have nothing to hide." The second most dangerous is "This strategy makes me invisible." Neither is true. Privacy is not about invisibility. It is about control — over who sees what, when, and under what legal process.

The two-phone strategy gives you control. It does not give you immunity.

Use it wisely. Use it where it fits. And always assume the adversary is smarter than you think.

Now go break something else. That is what researchers do.

[^1]: EU GDPR, Regulation (EU) 2016/679, Article 15 (right of access). The data controller (carrier) must respond within one month (extendable to three months for complex requests) and must provide the information free of charge.
[^2]: Norwegian Consumer Council, "Out of Control: How consumers are exploited by the online advertising industry," forbrukerradet.no, 2020. This report documented Grindr and other apps transmitting precise location and behavioral data to advertising and analytics third parties in violation of GDPR, resulting in FTC complaints and enforcement actions.
[^3]: Roger Dingledine, Nick Mathewson, and Paul Syverson, "Tor: The Second-Generation Onion Router," USENIX Security Symposium, 2004. Routing application traffic through Tor adds multiple relays and randomized latency, preventing a network-layer observer from correlating the traffic to the originating IP address, though timing analysis by a global passive adversary remains a theoretical risk.
