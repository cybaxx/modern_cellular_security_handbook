# Graph 3: Data Flow & Correlation Attack (The "Collapse" Diagram)

## Purpose

This is the most important graph in the entire volume. It demonstrates how an adversary links Phone A to Phone B to the user's real identity through a single point of failure: the home residential ISP connection. The diagram is called the "Collapse" because the entire two-phone compartmentalization unravels into a single identifiable node the moment any device touches the home network.

## The Graph


> *See the figure generated below.*


## The Five-Step Correlation Attack

### Step 1: Subpoena the ISP

The adversary begins with the simplest legal action: a subpoena to the residential ISP (Comcast, Spectrum, AT&T, or any other provider). The ISP maintains subscriber records linking IP addresses to names, billing addresses, and payment methods. Given an IP address observed in a relevant context, the ISP returns your real identity within days.

This step is trivial because ISPs are legally required to maintain subscriber records under data retention laws (18 U.S.C. § 2703 in the US, the Investigatory Powers Act in the UK, the Telecommunications Act in Australia). There is no probable cause requirement for basic subscriber information — a subpoena (not a warrant) is sufficient.

### Step 2: Subpoena the Carrier for Phone A

With your name and address in hand, the adversary subpoenas the cellular carrier for Phone A. The carrier cross-references the billing address, payment method, or account name associated with your identity to identify the IMSI (International Mobile Subscriber Identity) of Phone A.

Once the IMSI is known, the adversary requests:

- Call Detail Records: every call and SMS, with timestamps and tower IDs
- Timing Advance data: distance from tower at each interaction
- Tower dumps: all phones connected to specific towers at specific times
- Historical location: reconstructed movement patterns over the retention period

### Step 3: Router Logs Expose Phone B's MAC

The critical step. If Phone B (or the Computer) has ever connected to the home Wi-Fi network, the home router's logs contain:

- MAC address of Phone B
- DHCP lease records (hostname, IP assignment, lease duration)
- Connection and disconnection timestamps
- Potentially DNS queries and destination IPs (if the router logs this data)

Consumer routers from Netgear, Asus, TP-Link, and ISP-provided gateways all maintain connection logs. Many ISP-provided routers report this data back to the ISP automatically through TR-069 remote management. The ISP may already have Phone B's MAC address without a separate router subpoena.

### Step 4: Wi-Fi Geolocation Confirms the Link

With Phone B's MAC address known, the adversary queries public Wi-Fi geolocation databases (Google's BSSID location API, Apple's crowd-sourced Wi-Fi database, or commercial services like Skyhook or Unwired Labs). These databases map BSSIDs to GPS coordinates.

If Phone B's MAC was observed by any war-driving vehicle or crowd-sourced scanner near the home address, the geolocation database confirms: "This MAC address is associated with this physical location." The adversary now has independent corroboration that Phone B's device is present at the user's home.

### Step 5: Tower Dump Ties Phone A to the Same Location

Finally, the adversary requests tower dumps from carriers that cover the home address. Tower dumps reveal all IMSIs that connected to specific towers during specific time windows.

If Phone A's IMSI appears in tower dumps from the cell sector covering the home address at timestamps matching Phone B's router connection logs, the correlation is complete: the same person carries both phones.

## Critical Takeaway

**The entire two-phone strategy collapses if Phone B or the Computer ever connects to any network linked to the user's identity.** This includes:

- Home Wi-Fi (the most obvious and most common mistake)
- Work Wi-Fi (the employer's ISP knows the employee's identity)
- School or university Wi-Fi (student records are linked to identity)
- A friend's home Wi-Fi that is linked to their identity (adversary subpoenas the friend)
- A public Wi-Fi that requires any form of registration or payment (hotel, airport, conference)

Once any device associates with an identity-linked network, the graph compresses from multiple nodes to a single node labeled with the user's real name. The compartmentalization that makes the two-phone strategy work is destroyed in a single connection.

## Why This Is Called the "Collapse" Diagram

The diagram's structure mirrors the mathematical concept of graph collapse in network theory. The ideal two-phone strategy maintains two disconnected graphs:

- Graph A: Phone A ↔ Carrier ↔ Public Identity
- Graph B: Phone B ↔ Public Wi-Fi ↔ Anonymous Identity

These two graphs share no common nodes. When Phone B connects to home Wi-Fi, the two graphs merge at the home router node, and from there the ISP node links both graphs to the real identity. The collapse is instantaneous and irreversible.

## Why ISP Disclosure Is the Single Point of Failure

The collapse diagram reveals that the residential ISP is the single node connecting the real identity to both devices. This is not accidental — it is structural. The ISP is the only entity in the average person's digital life that simultaneously knows:

- Your real name and physical address (from the billing relationship)
- The IP addresses assigned to every device in your home
- The timestamps, durations, and destination IPs of every connection
- The MAC addresses of every device (through DHCP logs, if the ISP provides the router)
- The DNS queries made by every device (if the ISP operates the DNS resolver)

No other entity has this complete picture. The cellular carrier knows the real name and Phone A's location, but not Phone B's activity. Google knows Phone B's location (through Android) but not necessarily the real name. The home router knows the MAC addresses but not the real name (unless it phones home to the ISP through TR-069).

The ISP is the universal correlator. Once the adversary obtains ISP records, all compartmentalization fails.

## Advanced Correlation Techniques

The five-step attack is the simplest path. Adversaries with greater resources can use additional correlation techniques:

### Traffic Correlation (Timing Analysis)

Even if Phone B uses a VPN, an adversary who can monitor both the ISP link and the VPN exit node can correlate traffic by timing patterns. If Phone B sends a burst of data at exactly the same time as an encrypted stream leaves the VPN exit, the adversary can infer that Phone B and the VPN stream are the same session — even without decrypting the traffic. This technique, known as traffic correlation or timing analysis, is used by NSA and GCHQ.

### SS7 Location Queries

A state actor with access to the SS7 signaling network can query Phone A's home network for its current location at any time. This works globally, requires no warrant, and cannot be detected by the phone user. The SS7 query returns the cell tower currently serving Phone A, which narrows the location to a few kilometers — sufficient to identify the home neighborhood or workplace.

### BSSID Correlation

If Phone B's Wi-Fi interface broadcasts probe requests containing saved SSID names (a common Android flaw), an adversary who captures these probes learns the names of the user's home network and work network. They can then search BSSID geolocation databases for these SSID names to identify the physical locations of the user's home and workplace. This is a no-subpoena correlation technique that works entirely through passive collection.

### Physical Surveillance

For a subject under active investigation, physical surveillance is the most direct correlation technique. A surveillance team observes the subject leaving home, carrying both phones, and using them at different times. The correlation is visual and immediate. No technical hacking or legal process is needed.

## Why the "Just Once" Mistake Is Fatal

The most common failure mode of the two-phone strategy is the user connecting Phone B to home Wi-Fi "just once" — for a software update, a large file download, or because the public Wi-Fi was unavailable and "it's just this one time."

The graph shows why this is fatal: the connection is logged permanently. The ISP's DHCP server records the MAC address. The router's connection log records the timestamp. A neighbor's Wi-Fi sniffer may capture the probe request. Even if the user immediately forgets the network, the logs persist.

There is no "undo" for a Wi-Fi connection. The MAC address has been logged. The IP address has been assigned. The ISP knows which device connected, when, and for how long. Years later, when an adversary subpoenas those logs, the connection is still there.

## Practical Defense

The only effective defense against the collapse is to ensure Phone B's MAC address never appears in any router log or Wi-Fi geolocation database that can be linked to the user's identity. This means:

- **Phone B must never connect to home Wi-Fi.** This is non-negotiable. If the user needs to download a large file, they do so at a public library or a coffee shop that does not require registration.

- **Phone B must never connect to work Wi-Fi.** Work networks are linked to the employer, which is linked to the employee's identity. If the adversary can subpoena the employer's IT logs, the correlation is as complete as with home Wi-Fi.

- **Phone B must never connect to any network associated with an identifiable person.** This includes a friend's home Wi-Fi, a relative's home Wi-Fi, a hotel Wi-Fi (linked to the user's booking), or an event Wi-Fi (linked to the user's registration).

- **Phone B should use a VPN at all times when on public Wi-Fi.** The VPN prevents the coffee shop or library from logging the user's traffic. However, the VPN does not prevent the Wi-Fi network from logging the MAC address and connection timestamps — only encryption of the probe requests (through MAC randomization) can partially mitigate this.

- **Phone B's MAC randomization must be verified.** Not all Android implementations randomize the MAC effectively. The user should verify that their device's MAC address changes between Wi-Fi scans by using a packet sniffer or network monitoring app.

## Forensic Implication

For an adversary investigating a subject suspected of using two phones, the investigation strategy follows the same five steps. The presence of two devices is irrelevant — the adversary does not need to crack Phone B's encryption, intercept Phone A's calls, or deploy physical surveillance. A single subpoena to the ISP, followed by router logs and tower dumps, deanonymizes both phones.

The only effective defense is to ensure Phone B's MAC address never appears in any router log or Wi-Fi geolocation database that can be linked to the user's identity. This means Phone B must never associate with any saved Wi-Fi network in any location that is traceable to the user. Every connection must be through a network that the adversary cannot link to the user — ideally, public Wi-Fi accessed through a VPN, paid for with cash, at a location the user does not regularly visit.
