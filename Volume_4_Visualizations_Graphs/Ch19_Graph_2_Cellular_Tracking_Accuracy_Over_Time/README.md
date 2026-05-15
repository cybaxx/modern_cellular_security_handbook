# Graph 2: Cellular Tracking Accuracy Over Time (4G vs. 5G)

## Purpose

This logarithmic chart shows how cellular location accuracy has evolved from 2015 through 2029, demonstrating that the "anonymity" of even a basic flip phone is rapidly eroding. The graph is essential for understanding why cellular-layer privacy assumptions from the 2010s no longer hold.

## The Graph

```
Location Accuracy (meters, logarithmic scale)
─────────────────────────────────────────────────────────────────────────────
10,000m ┤
 5,000m ┤
 1,000m ┤                                    ● 4G Cell ID only (1000-5000m)
   500m ┤                         ●─────────● 4G + TA (300-800m)
   100m ┤              ●──────────●─────────● 4G + AoA (50-200m)
    50m ┤         ●────●
    30m ┤    ●────●                         ● 5G OTDOA (10-50m)
    10m ┤ ●──●
     5m ┤●                                  ● 5G Multi-RTT (1-10m)
     1m ┤
     0 └────┬────┬────┬────┬────┬────┬────→ Year
           2015  2018  2021  2024  2026  2029
           (4G)  (4G+) (5G)  (5G+) (5G Adv)

Key:
● = Typical accuracy for consumer phones
Legend: Cell ID → +TA → +AoA → OTDOA → Multi-RTT
```

## The Accuracy Timeline

### 2015: 4G Cell ID (1000–5000 meters)

In 2015, cellular location accuracy was measured in kilometers. The network knew which cell tower your phone was connected to, but that was the limit of their knowledge. In dense urban areas with small cells, accuracy might approach 500 meters. In suburban or rural areas with macro cells covering several kilometers, accuracy was worse than 5 km. This era is fondly remembered by privacy advocates as a time when "turning off location services" genuinely prevented precise tracking — but only because the cellular network itself was imprecise.

### 2018: 4G + Timing Advance (300–800 meters)

The introduction of Timing Advance (TA) data marked the first significant improvement. TA measures the signal propagation delay between the phone and the tower. Since radio waves travel at the speed of light, the round-trip time reveals the phone's distance from the tower within a sector. With TA available from standard 4G signaling messages (part of the MAC layer), carriers could locate phones to within 300-800 meters.

This was the first indication that cellular networks were becoming a tracking infrastructure independent of GPS. The phone does not need to consent to TA measurement — it is an inherent part of the 4G protocol.

### 2021: 4G + Angle of Arrival (50–200 meters)

Angle of Arrival (AoA) techniques use multiple antenna elements at the base station to estimate the direction from which the phone's signal arrives. Combined with TA for distance, this reduced uncertainty to 50-200 meters. AoA is available through standardized 4G features like PRS (Positioning Reference Signals) and OTDOA (Observed Time Difference of Arrival) precursors.

At this accuracy, cellular tracking became useful for law enforcement investigations. A 50-200 meter radius is small enough to identify a specific building or street segment.

### 2024: 5G OTDOA (10–50 meters)

With the rollout of 5G's positioning features, Observed Time Difference of Arrival (OTDOA) became practical. OTDOA measures the time difference between signals arriving from multiple base stations, triangulating the phone's position with far greater precision than 4G allowed. The denser 5G network (more small cells, closer spacing) contributed additional accuracy.

At 10-50 meters, cellular tracking now rivals Wi-Fi-based positioning. A flip phone with no GPS, no Wi-Fi, and no apps can be located to the precision of a city block. This is the threshold where flip phone "anonymity" begins to crack.

### 2026: 5G Multi-RTT (1–10 meters)

Multi-Round Trip Time (Multi-RTT) is a 5G-Advanced feature that measures the time of flight between the phone and multiple transmission points, using multiple frequency layers for higher resolution. At 1-10 meters, the cellular network itself can locate a phone with GPS-like precision.

The forensic implication is profound: **by 2026, 5G networks can locate your flip phone to within 5–30 meters without GPS, without apps, without Wi-Fi.** The phone's cellular radio alone is sufficient. There is no user-facing setting to disable this — positioning reference signals are an integral part of the 5G air interface.

### 2029: 5G Advanced Carrier Phase (sub-1 meter)

The 5G-Advanced roadmap includes carrier phase positioning, which uses the phase of the carrier signal itself (millimeter wave frequencies) to achieve centimeter-level accuracy. At this resolution, cellular tracking exceeds the accuracy of consumer GPS. The phone can be located to a specific room in a building.

## Forensic Implication for Flip Phones

The flip phone (Phone A in our model) was historically chosen as the "dumb" privacy device precisely because it had no GPS, no apps, and no Wi-Fi. The assumption was that without those features, the phone could not be tracked with precision. Graph 2 demonstrates that this assumption is obsolete.

The cellular network itself has become a tracking infrastructure. Every flip phone with a 4G or 5G radio participates in positioning measurements automatically. There is no opt-out. The phone cannot refuse to transmit PRS. It cannot refuse to respond to TA requests. These are mandatory protocol-level interactions.

For the two-phone strategy, this means:

- **Phone A's location is knowable to within 5-30 meters by 2026.** If an adversary has access to carrier logs — through subpoena, lawful intercept, or insider access — they can reconstruct Phone A's movements to block-level precision.

- **The flip phone's reputed anonymity is a myth** that was accidentally true in 2015 but has been systematically dismantled by 3GPP standardization.

- **The only defense is to never carry Phone A at sensitive times or locations.** If Phone A is carried to a protest, a meeting, or a sensitive location, its presence is logged and locatable.

## Logarithmic Scale Explanation

The graph uses a logarithmic scale on the vertical axis because cellular accuracy has improved by more than three orders of magnitude over the 14-year period. A linear scale would compress the early years (5000 meters) and late years (1 meter) into unreadable proportions. The logarithmic scale reveals that each technology generation has produced roughly a 5-10x improvement in accuracy — a consistent and accelerating trend.

## Technical Mechanisms Behind Each Accuracy Level

### Cell ID (4G, 2015 era)

The coarsest granularity. The network records which eNodeB (base station) the phone is registered with. In rural areas with macro cells, a single Cell ID covers several kilometers. Accuracy is simply the geographic coverage radius of that cell sector. No special signaling is required — this information is part of routine mobility management.

### Timing Advance (4G+, 2018 era)

Timing Advance is a MAC-layer parameter used by the network to synchronize uplink transmissions. The eNodeB measures the propagation delay of the phone's signal and sends a TA command (0-63 in 4G, with each step representing approximately 78 meters of distance). The TA value reveals the phone's distance from the tower within its sector. Combined with the sector's azimuth angle, this narrows the location to an arc rather than a full circle.

TA data is available in standard 4G signaling messages (RRC Connection Setup Complete, Measurement Reports). Carriers routinely log this for network optimization. It requires no special equipment to capture — the network records it automatically.

### Angle of Arrival (4G+/5G, 2021 era)

AoA uses multiple antenna elements at the base station to estimate the direction of the incoming signal. Modern base stations use phased-array antennas with 8, 16, or 64 elements. By comparing the phase difference of the signal arriving at each element, the network computes the angle of arrival with precision of a few degrees.

Combined with TA (distance), AoA provides 2D positioning. The precision depends on the number of antenna elements and the signal bandwidth. Wider bandwidth (e.g., carrier aggregation in 4G+) provides better resolution.

### OTDOA (5G, 2024 era)

Observed Time Difference of Arrival is a downlink-based positioning method. The network transmits Positioning Reference Signals (PRS) from multiple base stations. The phone measures the time difference between arrivals of these signals and reports the measurements to the network. With three or more base stations, the network can triangulate the phone's position.

OTDOA accuracy depends on PRS bandwidth and the geometry of the base stations. 5G's wider channel bandwidths (up to 100 MHz in sub-6 GHz, 400 MHz in mmWave) provide significantly better resolution than 4G's narrowband PRS. The dense deployment of 5G small cells (every 200-500 meters in urban areas) further improves geometry and accuracy.

### Multi-RTT (5G-Advanced, 2026 era)

Multi-RTT is an uplink-based method where multiple transmission points measure the round-trip time of signals from the phone. Unlike OTDOA (which relies on the phone's measurements), Multi-RTT uses network-side measurements, making it more reliable and harder for the phone to manipulate.

Multi-RTT uses multiple frequency layers (carrier aggregation) to measure time of flight at different frequencies, resolving multipath propagation ambiguities. The network computes the phone's position by trilateration from three or more transmission points.

### Carrier Phase Positioning (5G-Advanced, 2029 era)

The most precise method, still in standardization. Carrier phase positioning measures the phase of the carrier signal itself (the number of carrier wave cycles between the phone and the base station). At millimeter-wave frequencies (28 GHz, 39 GHz), a single cycle is approximately 1 cm. By measuring the phase difference between multiple base stations, the network can achieve centimeter-level positioning accuracy.

This technique is already used in GPS (carrier phase differential GPS achieves centimeter accuracy). Applying it to 5G terrestrial signals in a dense small-cell deployment promises indoor positioning accuracy comparable to outdoor GPS.

## The Flip Phone Paradox

The flip phone (Phone A) was selected for the two-phone strategy precisely because it was assumed to be "dumb" — no GPS, no apps, no Wi-Fi, no location services. The paradox revealed by Graph 2 is that the flip phone is the most trackable device of all, because:

1. It has a cellular radio that must connect to the network to function
2. It has no privacy features (no OS-level location permission controls, no ability to disable positioning reference signals)
3. It generates a permanent trail at the carrier (CDRs, TA, paging events)
4. It is typically registered to a real identity or purchased with identifiable currency (credit card at a retail store)

The flip phone is, from a cellular network perspective, a perfect tracking beacon. The only way to prevent this is to not carry it — which defeats its purpose as a communication device.

## Practical Countermeasures

Given the accuracy trend, users of the two-phone strategy should:

1. **Minimize Phone A usage at sensitive locations.** If Phone A is present at a protest, confidential meeting, or other sensitive location, the network knows. The only defense is physical separation — leave Phone A at home or in a Faraday bag.

2. **Assume carrier logs contain near-GPS precision location data.** By 2026, Timing Advance combined with 5G OTDOA provides 10-30 meter accuracy. By 2029, Multi-RTT provides sub-10 meter accuracy. Historical logs from these periods will be available for subpoena.

3. **Rotate Phone A frequently.** Replace the flip phone and SIM every 1-3 months to limit the historical window in carrier logs. This is imperfect (older devices' logs still exist) but shortens the available record.

4. **Accept the limitation.** Cellular location tracking is an inherent property of the network, not a user-configurable setting. There is no "disable tracking" switch for cellular. The two-phone strategy cannot protect against this at the network level — it can only ensure that tracking Phone A does not reveal Phone B.

## Strategic Takeaway

The trend line points in one direction: cellular location accuracy will approach GPS quality within the current decade. Any operational security model that relies on "my phone can't be tracked because it's a dumb phone" is relying on a technical limitation that no longer exists. The two-phone strategy must account for the tracking capability of the network itself, not just the tracking capability of the device.
