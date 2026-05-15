# Graph 4: Wi-Fi Probe Request & BSSID Geolocation (Passive Tracking)

## Purpose

This graph demonstrates how a smartphone reveals its presence and location even when it is not connected to any network. The mechanism is Wi-Fi probe requests — periodic broadcasts sent by the device to discover available networks — combined with BSSID geolocation databases maintained by Google, Apple, and other commercial services. This is the primary tracking vector for Phone B.

## The Graph

```
SCENARIO: You walk down a city street with Phone B (Wi-Fi on, scanning enabled)

Time  │ Your Phone Action                    │ Data Captured by Adversary
──────┼──────────────────────────────────────┼────────────────────────────────────
00:00 │ Powers on, Wi-Fi enables            │ Nothing yet
00:05 │ Sends PROBE REQUEST: "Any SSID?"    │ MAC: AA:BB:CC:DD:EE:FF (Google Pixel)
      │                                      │ Supported rates: 802.11ax
00:10 │ Receives BEACON from Coffee Shop    │ Coffee Shop BSSID: 11:22:33:44:55:66
      │ Router (BSSID 11:22:33:44:55:66)    │ Signal strength: -45 dBm
00:12 │ Phone caches BSSID + signal strength│ (Phone now remembers this router)
00:15 │ Later, adversary queries Google API │ Google returns: 
      │ with BSSID 11:22:33:44:55:66        │ GPS: 40.7128°N, 74.0060°W
      │                                      │ Address: "Starbucks, 123 Main St"
00:20 │ Adversary now knows:                │ "MAC AA:BB:CC was at 123 Main St"
      │                                      │   at approximately 00:10-00:15
─────────────────────────────────────────────────────────────────────────────
```

## How Probe Requests Enable Tracking

Every Wi-Fi-enabled device periodically sends probe request frames to discover available networks. These frames are broadcast packets — they are not directed at any specific access point and are received by any Wi-Fi radio within range. The probe request contains:

- **The device's MAC address**: The hardware identifier of the Wi-Fi radio. Even with MAC randomization, the address may be the real MAC or a randomized address that is predictable across scans.
- **Supported data rates**: Information about the device's Wi-Fi capabilities (802.11a/b/g/n/ac/ax), which can fingerprint the device model.
- **Probe request SSIDs (directed probes)**: The device may broadcast the names of previously connected networks (e.g., "HomeNetwork", "WorkWiFi", "Starbucks_WiFi"). This is a catastrophic information leak.
- **Sequence numbers**: Each frame includes a sequence number that can be used to correlate probe requests across time and location, even if the MAC address changes.

## Proactive Tracking: The Adversary's Sniffer

Beyond passive observation, an adversary can deploy Wi-Fi sniffers at strategic locations:

```
EVEN WORSE (Proactive Tracking):
─────────────────────────────────────────────────────────────────────────────
Adversary places Wi-Fi sniffer at 123 Main St (coffee shop).
Logs show:
  Timestamp: 2026-05-14 14:23:45
  MAC: AA:BB:CC:DD:EE:FF
  Probe Request containing: "HomeNetwork", "WorkWiFi"
  
Adversary now knows:
  - Your device MAC
  - Your home SSID ("HomeNetwork")
  - Your work SSID ("WorkWiFi")
  - You were at the coffee shop at 2:23 PM
  
Later, adversary drives near your home, captures same "HomeNetwork" probe.
Correlation complete.
```

This scenario demonstrates the most dangerous aspect of probe requests: **SSID history leakage**. When a device sends directed probe requests for previously connected networks (e.g., "HomeNetwork"), it broadcasts the names of those networks to anyone listening. An adversary who captures these probes can:

1. Identify the networks the device typically connects to
2. Drive or walk near locations where those SSIDs are broadcast to find the device's home and workplace
3. Correlate the device across multiple locations using the unique combination of SSIDs in its probe history

## MAC Randomization Effectiveness

```
MAC Randomization Effectiveness (against passive tracking)
─────────────────────────────────────────────────────────────────────────────
100% ┤
 80% ┤    ●●●●●●●●
 60% ┤              ●●●●●●●●
 40% ┤                        ●●●●●●●●
 20% ┤                                  ●●●●●●●●
  0% ┤                                            ●●●●●●●● (old devices)
     └────┬────┬────┬────┬────┬────┬────→
        2018  2020  2022  2024  2026  2028
        
● = Android (varies by vendor)   ● = iOS (strong)
Legend: Early MAC random → Modern MAC random (fails often) → Fully random
```

MAC randomization was introduced by Apple in 2014 (iOS 8) and by Google in 2017 (Android 10) as a privacy feature. The idea: use a different MAC address for each Wi-Fi scan so that probe requests cannot be linked across time and location. In practice, the implementation has been inconsistent and often ineffective.

### Android MAC Randomization

Android's MAC randomization has a troubled history:

- **Android 10 (2019)**: Introduced randomized MACs for probe requests, but many devices continued to use the real MAC for directed probes (probes containing specific SSIDs). This defeated the purpose because directed probes are the most identifying type of probe.
- **Android 11 (2020)**: Improved behavior but still leaked the real MAC in some scenarios, particularly when connecting to a saved network.
- **Android 12+ (2021-2024)**: Further improvements, but vendor fragmentation means that a Pixel behaves differently from a Samsung, which behaves differently from a Xiaomi. Each OEM may disable randomization for "compatibility" reasons.
- **GrapheneOS**: Uses a per-network randomized MAC by default and improves probe request randomization. However, GrapheneOS runs on Pixel hardware, and the underlying Wi-Fi firmware may still leak the real MAC in certain states (e.g., after a reboot, during the initial scan before the OS applies randomization rules).

### iOS MAC Randomization

Apple's implementation has been stronger from the start:

- **iOS 14+**: Uses a randomized MAC for every Wi-Fi scan by default. Directed probes are disabled — iOS does not send probe requests containing specific SSIDs. This eliminates the most identifying type of probe.
- **iOS 16+**: Further hardened with private Wi-Fi addresses per network and improved randomization seed rotation.
- **iOS weakness**: Still leaks the real MAC when the device is in certain states (e.g., during iOS setup, when connecting to carrier Wi-Fi calling, or when using certain enterprise network profiles).

### The Effectiveness Curve

The graph shows that MAC randomization has improved over time but remains imperfect:

- **2018-2020 era devices**: 0-30% effective. Many Android devices effectively had no randomization. Directed probes containing SSID history were the norm. A single capture session could permanently identify a device.
- **2020-2022 era devices**: 30-60% effective. Android improved but remained vulnerable to directed probe leakage and sequence number tracking. iOS became stronger but still had edge cases.
- **2022-2024 era devices**: 60-80% effective. Both platforms improved but sequence number analysis and timing correlation could still defeat randomization.
- **2024-2028 era devices**: 80-95% effective assuming best practices. Fully randomized MACs with frequent rotation and no directed probes. However, the top end remains elusive because the adversary can still correlate based on:
  - Signal strength patterns (each device has a unique RF fingerprint)
  - Supported rate information (device model fingerprinting)
  - Probe timing intervals (unique patterns in scan schedules)
  - Sequence number tracking (even randomized MACs may use sequential sequence numbers)

### The Fundamental Limitation

Even perfect MAC randomization does not prevent all tracking because:

1. **RF fingerprinting**: Each Wi-Fi radio has minute hardware imperfections in its transmission that create a unique signature. An adversary with a software-defined radio can identify a specific device even through randomized MACs.
2. **Behavioral fingerprinting**: The timing of probe requests, the combination of supported rates, and other protocol-level signals create a behavioral fingerprint that persists across MAC changes.
3. **BSSID correlation**: Even without capturing the device's MAC, an adversary who sees which BSSIDs a device responds to can infer location. The device's reactions to beacon frames reveal its location even if the device's MAC is hidden.

## The BSSID Geolocation Database Ecosystem

The tracking scenario shown in Graph 4 relies on BSSID geolocation databases maintained by major technology companies. Understanding how these databases are built and queried is essential for evaluating the tracking risk.

### Google's BSSID Database

Google's location database is the largest in the world, built through:

- **Android device crowdsourcing**: Every Android device with location services enabled periodically reports nearby BSSIDs and their GPS coordinates to Google. This happens silently, in the background, for every device running Google Play Services.
- **Street View vehicles**: Google's Street View cars have been collecting BSSID locations since 2007. Each car carries Wi-Fi scanning equipment that records every visible BSSID and its GPS location. This data was originally collected without explicit consent (the 2010 "Street View Wi-Fi scandal" revealed that Google had also collected payload data, not just BSSIDs).
- **User-contributed data**: Apps that use Google's location API contribute BSSID data as part of their normal operation.

The result is a database of hundreds of millions of BSSIDs with sub-meter GPS accuracy. Querying the Google Maps Geolocation API with a BSSID returns the location within seconds. The API requires an API key (free for limited use) and works over HTTPS.

### Apple's BSSID Database

Apple maintains a similar database, built through:

- **iOS device crowdsourcing**: iOS devices periodically report nearby BSSIDs with GPS coordinates to Apple's location service. This is part of the "Crowd-sourced Wi-Fi" feature.
- **Apple's own war driving**: Apple has been known to deploy Wi-Fi scanning vehicles in urban areas.
- **Limited API access**: Apple's BSSID database is primarily used internally by iOS (for the "Wi-Fi positioning" feature when GPS is unavailable). The API is not publicly documented for arbitrary BSSID lookups, but the database can still be queried through framework-level calls on iOS and macOS devices.

### Commercial Databases

Companies like Skyhook (now part of Google), Unwired Labs, and Combain maintain commercial Wi-Fi positioning databases. These are sold to carriers, advertisers, and law enforcement for location-based services and forensic investigation. Law enforcement agencies have standing contracts with these providers for BSSID geolocation queries.

### Database Query Patterns

The adversary's query pattern against these databases reveals location history:

1. **Single BSSID lookup**: The adversary captures a device's probe request containing a BSSID (from a beacon response), queries the database, and learns the device's approximate location.
2. **Bulk BSSID lookup**: The adversary uploads all BSSIDs captured during a surveillance operation and receives GPS coordinates for each. This creates a map of where the device has been.
3. **Historical lookup**: Some databases retain historical BSSID observations. Google's database, for example, may have multiple observations of the same BSSID over time, revealing changes in access point location or the device's movement patterns.

## The Coffee Shop Tracking Scenario in Detail

The timeline shown in Graph 4 (00:00 to 00:20) is compressed for illustration. In reality, the tracking unfolds as follows:

**Phase 1 (00:00-00:05): Device Power-On and Network Scan** — Phone B's Wi-Fi radio initializes and begins scanning. It transmits probe requests on all supported channels (2.4 GHz and 5 GHz). The probe request frame includes the MAC address and supported rates. Any device within range — including a Raspberry Pi running Kismet placed by the adversary — captures this frame.

**Phase 2 (00:05-00:12): Access Point Discovery** — Phone B receives beacon frames from nearby access points, including the coffee shop's router. The beacon contains the router's BSSID, SSID ("CoffeeShopWiFi"), supported rates, and channel information. Phone B records this information in its internal BSSID cache for later use. The adversary's sniffer also captures this exchange, learning that Phone B detected the coffee shop's router.

**Phase 3 (00:12-00:15): Geolocation Database Query** — The adversary extracts the BSSID 11:22:33:44:55:66 from the captured packets and submits it to a geolocation API. The API returns GPS coordinates (40.7128°N, 74.0060°W) with a confidence radius of approximately 20 meters. The API may also return the street address ("Starbucks, 123 Main St") if the database includes reverse-geocoded information.

**Phase 4 (00:15-00:20): Location-Timestamp Correlation** — The adversary cross-references the geolocation result with the timestamp of the original capture. The result: Phone B (MAC AA:BB:CC:DD:EE:FF) was within 20 meters of 123 Main Street at approximately 00:10-00:15 on the date of capture.

The adversary now has a location-time-device triple. If the same MAC address is observed at other locations, a movement pattern emerges. If the MAC address is linked to an identity (through ISP subpoena or router log correlation), the adversary knows who was at the coffee shop and when.

## Proactive Tracking Deployment Costs

Deploying passive Wi-Fi tracking is inexpensive:

- **Hardware**: A Raspberry Pi 4 with a USB Wi-Fi adapter (~$50-80) running Kismet or similar packet capture software. Battery-powered units can run for 8-12 hours on a portable charger.
- **Software**: Kismet (free, open source), Wireshark (free), or commercial tools like AirMapper. The software captures probe requests, extracts MAC addresses and SSIDs, and logs timestamps.
- **Coverage**: A single sniffer covers approximately 50-100 meters indoors, 200-300 meters outdoors with an external antenna.
- **Deployment**: Multiple sniffers can be deployed in a grid pattern for area coverage. A coffee shop with 2-3 sniffers covers the entire seating area.

For an adversary targeting a specific individual, the cost of deploying sniffers at expected locations (home neighborhood, workplace, regular coffee shops, gym) is under $500 and can be done in an afternoon.

## Preventing SSID History Leakage

The most damaging information in a probe request is the SSID history — the names of previously connected networks. A device that sends directed probe requests for "HomeNetwork" and "WorkWiFi" is broadcasting the names of the adversary's targets.

Prevention strategies, ranked by effectiveness:

1. **Disable "Auto-join" for all saved networks** (or better, never save networks). The device will not send directed probes for networks it has not saved. On GrapheneOS, this is the default behavior.
2. **Use a random MAC address per network** (GrapheneOS and iOS 14+ support this). Each saved network has a different associated MAC, preventing correlation between locations.
3. **Use "Ask to Join Networks" mode** (iOS) or equivalent on Android. The device does not automatically probe for known networks but waits for the user to select a network.
4. **Enable "Private Wi-Fi Address"** (iOS 14+, GrapheneOS). The device uses a different MAC for each network, resetting periodically.
5. **Disable Wi-Fi when not actively in use.** The only absolute prevention.

## Forensic Implication

For the two-phone strategy, Graph 4 demonstrates that **Phone B's Wi-Fi interface is a broadcasting beacon** that cannot be silenced without disabling Wi-Fi entirely. Every time Wi-Fi is enabled, the phone is announcing its presence to any listening device within approximately 100 meters (indoor) to 300 meters (outdoor with directional antenna).

Mitigations include:

- **Disable Wi-Fi when not actively in use**: The only 100% effective countermeasure. If Wi-Fi is off, no probe requests are sent.
- **Enable airplane mode in sensitive locations**: Disables all radios including Wi-Fi and Bluetooth.
- **Never save SSIDs**: Forcing the device to scan for unknown networks prevents directed probe requests containing saved network names. However, this reduces convenience significantly.
- **Use a Faraday bag**: Physical isolation of the device's radios when not in use.
- **Accept the limitation**: Even with all mitigations, a sophisticated adversary with physical proximity and RF analysis equipment can track the device.
