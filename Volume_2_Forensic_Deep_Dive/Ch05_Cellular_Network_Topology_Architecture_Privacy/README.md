# Chapter 5: Cellular Network Topology, Architecture, and Privacy

## Introduction

The cellular network is not a single system. It is a collection of interconnected subsystems — radio access networks, backhaul transport, core network functions, subscriber databases, charging systems, and interconnect gateways — each with its own data collection capabilities, retention policies, and legal access procedures. Understanding the topology of these systems, how data flows between them, and where collection points exist, is essential to understanding what cellular privacy actually means.

Most privacy analyses focus on the phone-to-tower radio interface. This is the visible layer, but it is only the first of many data collection points. The core network, the roaming exchanges, the billing systems, and the lawful intercept gateways all collect, process, and retain data that is at least as revealing as anything transmitted over the air.

This chapter provides a forensic-level map of the cellular network architecture. It traces the path of a single packet or message from the phone through each network element, identifies what data is collected and processed at each point, and analyzes the privacy implications for the two-phone strategy.

---

## Part 1: Cellular Network Architecture Overview

### 1.1 The Four Major Domains

A cellular network is divided into four functional domains:

**User Equipment (UE):** The mobile device — phone, tablet, hotspot, IoT module. The UE contains the SIM/USIM (the subscriber identity module), the baseband processor (the modem), and the application processor. From the network's perspective, the UE is identified by the IMSI (subscriber identity stored on the SIM) and the IMEI (device identity burned into the modem).[^1]

**Radio Access Network (RAN):** The towers and base stations that provide radio connectivity. In 4G, the RAN consists of eNodeBs (evolved Node Bs). In 5G, the RAN consists of gNBs (next-generation Node Bs).[^2] The RAN handles radio resource management, scheduling, encryption over the air, and measurement reporting. The RAN is the first point at which the network observes the device's approximate location.

**Core Network (CN):** The central switching and routing infrastructure. The core network handles authentication, mobility management, session establishment, subscriber policy enforcement, and interconnection with other networks. The core network is where subscriber data is permanently stored, where billing records are generated, and where lawful intercept is implemented.[^3]

**Transport Network:** The backhaul infrastructure that connects the RAN to the core network, and the core network to external networks (the public internet, the PSTN, other carriers' core networks). The transport network is typically built on IP/MPLS and is where bulk metadata collection often occurs.

### 1.2 Network Generations: Architectural Evolution

The architecture of cellular networks has evolved significantly across generations. Each generation introduced new network elements, new protocols, and new data collection capabilities.

**2G (GSM):** Circuit-switched voice and SMS with limited data (GPRS/EDGE). The architecture was flat: the Base Station Controller (BSC) connected directly to the Mobile Switching Center (MSC). Location tracking was limited to Cell ID. Data collection occurred primarily at the MSC and the Home Location Register (HLR). SMS messages passed through the Short Message Service Center (SMSC) in plaintext and were stored indefinitely on many carriers.

**3G (UMTS):** Introduced a parallel packet-switched core (SGSN, GGSN) alongside the circuit-switched voice core. The RNC (Radio Network Controller) aggregated traffic from multiple NodeBs. The packet core introduced IP-level metadata collection: GGSN logs contained the device's IP address, all destination IPs, and session timing. The MSC continued to handle voice and SMS.

**4G (LTE):** Eliminated the circuit-switched core entirely. All traffic — voice, SMS, data — runs over IP. The evolved packet core (EPC) introduced several new data collection points: the Mobility Management Entity (MME) handles signaling and mobility tracking; the Serving Gateway (SGW) handles user-plane traffic; the PDN Gateway (PGW) handles IP allocation and external connectivity.[^4] The PGW is the 4G equivalent of the GGSN and collects per-session IP metadata. Voice calls run as VoIP over IMS (IP Multimedia Subsystem), which generates SIP signaling logs containing calling party, called party, call duration, and timestamps.

**5G (NR):** Introduced a service-based architecture (SBA) where core network functions are virtualized and communicate via APIs. The Access and Mobility Management Function (AMF) replaces the MME. The Session Management Function (SMF) replaces the SGW control plane. The User Plane Function (UPF) replaces the SGW/PGW user plane.[^5] 5G introduces subscription concealed identifiers (SUCI) to protect the IMSI over the air, but all other data collection points remain.[^6] 5G also introduces significantly more precise location capabilities (Multi-RTT positioning accurate to 1-10 meters).

### 1.3 The 4G/5G Network Map

The following diagram shows the major network elements and data collection points in a modern 4G/5G network. Each numbered point represents a location where subscriber data is collected, processed, or stored.


> *See the figure generated below.*


---

## Part 2: Network Elements and Data Collection

### 2.1 Radio Access Network (RAN) — Cell Sites and Base Stations

The RAN is the first point at which the network observes the device. Every transmission between the phone and the tower creates records at the base station.

**What the RAN collects:**

| Data Element | Protocol | Granularity | Retention (typical) |
|-------------|----------|-------------|-------------------|
| Cell ID (ECGI/NCGI) | RRC / S1AP | Per connection | 30-90 days |
| Timing Advance (TA) | MAC / RRC | Per transmission | 30-90 days |
| Angle of Arrival (AoA) | RRC (5G beam mgmt) | Per transmission | 30-90 days |
| Neighbor cell measurements | RRC Measurement Report | Every ~200ms | Not retained (volatile) |
| Signal strength (RSRP/RSRQ) | RRC | Per measurement | 7-30 days |
| Bearer establishment/teardown | S1AP / NGAP | Per session | 30-90 days |
| Attach/detach events | NAS (via S1AP/NGAP) | Per event | 30-90 days |
| Handover events | S1AP / NGAP | Per handover | 30-90 days |

The protocols listed above — RRC, S1AP, and NGAP — are defined in 3GPP TS 36.331, TS 36.413, and TS 38.413 respectively.[^7]

**Forensic processing:** The RAN does not process data for content — it processes data for mobility management. However, the logs it generates (especially handover sequences and measurement reports) are invaluable for location reconstruction. By collecting timing advance values and neighbor cell measurements across multiple towers, a forensic analyst can reconstruct a device's path with accuracy approaching GPS.

**Privacy relevance:** The RAN operator (the tower owner, which may be the MNO or a tower company like Crown Castle or American Tower) has access to real-time device location for every connected phone. This data is not subject to the same legal protections as core network data in many jurisdictions.

### 2.2 Mobility Management Entity (MME) / Access and Mobility Management Function (AMF)

The MME (4G) and AMF (5G) are the control plane anchors. They handle all signaling between the UE and the core network. Every NAS (Non-Access Stratum) message passes through the MME/AMF.[^8]

**What the MME/AMF collects:**

- Every attach and detach request (IMSI, IMEI, timestamp, cell ID)
- Every tracking area update (TAU) — sent periodically and at cell boundary crossings
- Every service request (when the phone transitions from idle to active)
- Every bearer establishment (for each data session, voice call, or SMS)
- Every paging attempt (when the network tries to reach an idle device)
- Every handover signaling message
- Subscriber authentication vectors and ciphering keys

The MME/AMF maintains a mobility context for each subscriber that includes the current tracking area list, the last known cell ID, and the device's reachability state. This context is updated on every network interaction.

**Forensic value:** The MME/AMF logs are the single most complete record of a device's network activity. They capture every interaction, not just billable events. A subpoena to the MME/AMF logs provides a complete timeline of when the device was active, which towers it used, and how it moved between them.

**Privacy relevance:** The MME/AMF is operated by the MNO and is typically located in a central data center. Access to MME/AMF logs is controlled by the MNO and is accessible to law enforcement through standard legal processes (Section 2703(d) in the US, PACE in the UK, etc.). The Supreme Court held in *Carpenter v. United States* that law enforcement generally requires a warrant to obtain historical cell-site location information from carriers.[^9]

### 2.3 Home Subscriber Server (HSS) / Unified Data Management (UDM)

The HSS (4G) and UDM (5G) are the master subscriber databases. They store the permanent subscriber profile for every customer.[^10]

**What the HSS/UDM stores:**

| Data Element | Description | Persistent? |
|-------------|-------------|-------------|
| IMSI | Permanent subscriber identity | Yes (SIM lifetime) |
| MSISDN | Phone number(s) | Yes (account lifetime) |
| IMEI (last used) | Last device used with this SIM | Yes (updated on attach) |
| Authentication key (Ki) | Secret key for network authentication | Yes (SIM lifetime) |
| Subscribed services | Voice, SMS, data, roaming, etc. | Yes (account lifetime) |
| QoS profiles | Allowed data speeds, priority levels | Yes (account lifetime) |
| Roaming agreements | Allowed roaming partners | Yes (account lifetime) |
| Location (last known) | Last VLR/MME/AMF address | Yes (updated on movement) |
| Call forwarding settings | Supplementary services | Yes (user-configurable) |
| Lawful intercept flag | Whether LI is active on this line | Yes (court order duration) |

**Forensic value:** The HSS/UDM is the permanent link between the subscriber's identity (name, address, billing info) and the device's network activity. Every attach request queries the HSS/UDM, creating a record that can be correlated with other logs. The HSS/UDM also maintains the LI flag, which indicates that a device is under active surveillance.

**Privacy relevance:** The HSS/UDM is the subscriber database. It is the single point in the network where identity is permanently linked to activity. Law enforcement routinely obtains HSS/UDM subscriber data through administrative subpoenas (which do not require judicial approval in many US jurisdictions).

### 2.4 Serving Gateway (SGW) / User Plane Function (UPF) — Control

The SGW (4G) and the control portion of the UPF (5G) manage user-plane bearers. They route traffic between the RAN and the PGW/UPF.

**What the SGW/UPF-C collects:**

- Bearer establishment and teardown timestamps
- Data volume per bearer (bytes transferred)
- QoS class identifier (QCI/5QI) per bearer
- Tunnel endpoint identifiers (TEIDs) for GTP tunnels
- Handover-related bearer context

**Forensic value:** SGW/UPF-C logs provide session-level metadata — when a data session started, when it ended, how much data was transferred, and what quality of service was used. This data is used for charging and is retained for billing purposes (typically 6-12 months).

### 2.5 Packet Data Network Gateway (PGW) / User Plane Function (UPF) — User

The PGW (4G) and the user-plane UPF (5G) are the gateways to external networks. They allocate IP addresses to devices, enforce policy, and generate charging records.

**What the PGW/UPF collects:**

- IP address assignment (internal and public IP, start/end time)
- All destination IP addresses and ports (via NetFlow/IPFIX)
- Data volume per destination (bytes sent/received)
- Session timing (start, end, duration)
- APN (Access Point Name — identifies the type of connection, e.g., "internet" vs. "ims" vs. "enterprise.vpn")
- Protocol type (TCP, UDP, ICMP)
- Deep packet inspection metadata (if DPI is deployed)

**NetFlow/IPFIX records from the PGW/UPF provide the carrier's equivalent of ISP metadata.** Every IP connection the device makes — to Signal's servers, to a VPN endpoint, to a website, to an email server — is logged with the destination IP, port, protocol, and data volume.

**Forensic value:** PGW/UPF logs are the most revealing data source in the core network for communications intelligence. They show every server the device contacts, the timing of each connection, and the volume of data exchanged. Machine learning analysis of this data can identify the applications in use (Signal, WhatsApp, Telegram, Tor, VPN protocols) with high accuracy.

**Privacy relevance:** The PGW/UPF is the core network element that sees all internet-bound traffic. Its logs are routinely produced in response to law enforcement requests. Carriers retain PGW/UPF logs for varying periods (30 days to 12 months depending on jurisdiction and carrier policy).

### 2.6 IP Multimedia Subsystem (IMS) Core

The IMS core handles voice calls and SMS over IP in 4G/5G networks (VoLTE, VoNR, SMS over IP). It replaces the circuit-switched MSC of 2G/3G.

**What the IMS core collects:**

- SIP signaling messages (INVITE, BYE, REGISTER, MESSAGE)
- Calling party number, called party number
- Call start time, end time, duration
- SIP trunk identifier (which carrier interconnect)
- RTP session metadata (codec, packetization, jitter)
- SMS content (if not using SMS over IP with encryption)
- Conference call participants
- Call forwarding and diversion records

**Forensic value:** SIP logs are the IMS equivalent of CDRs. They contain the dialed number, the calling number, and the exact call duration. Unlike legacy CDRs, SIP logs also include the device's IP address and the IMSI (embedded in the SIP Private User Identity). IMS logs are the primary source for call metadata in 4G/5G networks and are subject to the same legal access procedures as traditional CDRs.

**Privacy relevance:** Even though voice content is encrypted over the air (and potentially end-to-end if using VoLTE with SRVCP), the SIP signaling is visible to the carrier. The dialed number, the duration, and the parties involved are all logged. SMS sent over IMS (SMS over IP / SMSoIP) passes through the IMS core in plaintext on the carrier's internal network.

### 2.7 Billing and Charging Systems

The billing system is often overlooked in privacy analyses, but it is one of the most data-rich systems in the carrier's infrastructure.

**What billing systems collect:**

- Call Detail Records (CDRs) for every billable event
- SMS Detail Records (SDRs) for every SMS
- Data session records (volume, duration, APN, timestamp)
- Roaming records (visited network, charges)
- Top-up and payment records (amount, method, timestamp, location)
- Customer service interactions (calls, chats, account changes)
- Device upgrade and purchase history
- Payment method (credit card, bank account, prepaid card)

**Forensic value:** Billing records are retained longer than any other carrier data — typically 3-7 years for regulatory compliance (tax, fraud prevention). They provide a complete history of when the device was used, for what purpose, and how it was paid for. Billing records are routinely produced in response to court orders and are often the first data source investigators request.

**Privacy relevance:** Billing data directly links network activity to a name and payment method. For prepaid customers (who pay in cash), the link may be weaker, but carriers still require registration information in many countries. Billing records are the most persistent data link between the subscriber's identity and their phone usage.

### 2.8 Lawful Intercept Systems

Lawful Intercept (LI) is a mandated capability in virtually every country with a telecommunications regulatory framework. In the United States, carriers are required by law under CALEA (the Communications Assistance for Law Enforcement Act, 47 U.S.C. §§ 1001–1010) to install equipment that enables law enforcement to intercept communications in real time.[^11]

**How LI works:**

The LI system sits between the core network elements and the external networks. When a lawful intercept order is active for a subscriber, the LI system:

1. Copies all signaling messages (NAS, SIP, SS7) to the law enforcement monitoring facility
2. Copies all user-plane traffic (voice, data, SMS) to the monitoring facility
3. Provides real-time location information (cell ID, TA, and in 5G, precise coordinates)
4. Maintains interception records for the duration of the court order

The LI system is implemented as a mediation function — it does not interfere with the subscriber's service and is transparent to both the subscriber and the network. The subscriber has no indication that LI is active.

**Types of intercept:**

| Type | What Is Provided | Legal Standard (US) |
|------|-----------------|-------------------|
| Pen register / Trap and trace | Dialed numbers, source/dest IP, timestamps (metadata only) | Court order (Reasonable suspicion) |
| Wiretap (Title III) | Full content of communications + metadata | Warrant (Probable cause) |
| Call content intercept | Real-time voice content | Warrant |
| SMS intercept | Real-time SMS content | Warrant |
| Data intercept | Real-time IP traffic content | Warrant |
| Historical records retrieval | Stored CDRs, location history, subscriber info | §2703(d) order (Specific facts) |

**Privacy relevance:** LI is the single most complete surveillance capability available to law enforcement. No OS modification, no encryption, no VPN, no privacy tool on the device can prevent LI from intercepting communications at the carrier level. LI intercepts communications before they reach the device's encryption layer (for voice and SMS) or at the network edge (for IP traffic). End-to-end encrypted services like Signal are protected against content interception, but the metadata (who, when, how long) is still visible to LI systems.

### 2.9 Deep Packet Inspection (DPI) Systems

Many carriers deploy DPI systems in the core network, typically at the PGW/UPF or at the Gi/SGi interface (between the carrier network and the internet).

**What DPI systems detect:**

- Application identification (Signal, WhatsApp, Telegram, Tor, Skype, Netflix)
- Protocol identification (OpenVPN, WireGuard, IPSec, SSH, HTTP/2)
- Website categorization (social media, adult, streaming, news)
- Malware and botnet traffic
- Encrypted traffic fingerprinting (packet size distributions, timing patterns)

DPI systems do not decrypt traffic, but they identify applications by their network fingerprints — the pattern of packet sizes, timing, and connection establishment that is unique to each application.

**Privacy relevance:** DPI allows the carrier to know which applications you use, even with end-to-end encryption and VPN usage. If you use Signal over a VPN, the DPI system sees the VPN protocol (by fingerprint) and may not identify Signal specifically — but it knows you are using a VPN, which itself is a signal for "attempting to hide activity." In some jurisdictions, VPN/Tor detection triggers additional monitoring or bandwidth throttling.

---

## Part 3: Data Processing and Correlation

### 3.1 The Data Flow Path

The following trace shows the flow of a single Signal message from Phone B and the data collected at each point:


> *See the figure generated below.*


### 3.2 Data Correlation Across Systems

The carrier does not maintain these data sources in isolation. They are correlated through the subscriber's IMSI and the device's IMEI:[^1]

- The MME knows the IMSI, the current cell ID, and the current SGW.
- The PGW knows the IMSI, the assigned IP address, and all destination IPs.
- The billing system knows the IMSI, the MSISDN, and the subscriber's name.
- The HSS knows the IMSI and the permanent subscriber profile.
- The LI system correlates all of the above.

An investigator who obtains records from multiple systems can construct a complete picture:

| Query | Data Source | Result |
|-------|-------------|--------|
| Who owns this phone number? | HSS / Billing | Name, address, payment method |
| Where was this phone on May 14? | MME / RAN logs | Cell ID + TA for every interaction |
| Who did this phone call? | IMS / SIP logs | Dialed numbers, durations |
| What servers did this phone contact? | PGW / NetFlow | All destination IPs, volumes, timing |
| What apps does this phone use? | DPI system | Application identification |
| Is this phone under intercept? | HSS (LI flag) | Yes/No |

### 3.3 Data Processing vs. Data Collection

It is important to distinguish between what is collected and what is processed:

**Collection:** All network elements log data by default. The MME logs every NAS message. The PGW generates NetFlow for every session. The RAN logs every connection. Collection is automatic, continuous, and unavoidable for network operation.

**Processing:** Most collected data is stored without immediate processing. It is written to logs and retained for a retention period. Processing occurs when:

- The data is queried by law enforcement (retrospective analysis)
- The data is analyzed for network optimization (capacity planning, troubleshooting)
- The data is processed for billing (CDR generation)
- The data is analyzed for fraud detection (anomalous usage patterns)
- The data is processed through DPI for traffic management

The forensic implication: the data exists whether or not anyone is actively analyzing it. The retention period determines how far back the data is available. The legal standard determines who can access it and under what conditions.

---

## Part 4: Roaming, MVNOs, and Network Slicing

### 4.1 Roaming Architecture

When a device roams on a visited network (a carrier different from the subscriber's home carrier), the data collection points multiply:

**Home network (HPMN):** Retains the subscriber profile (HSS) and receives charging records from the visited network. The home network knows the device is roaming and which network it is using, but does not have real-time access to the visited network's RAN logs or MME logs.

**Visited network (VPMN):** Operates the RAN and the local MME. The visited network collects all the same data as the home network — cell ID, TA, IMSI, IMEI, IP addresses, destination traffic.

**Roaming exchange (GRX/IPX):** The data exchange between home and visited networks. The GRX/IPX provider sees the signaling traffic (MAP, SS7, Diameter) and the user-plane traffic (GTP). The GRX/IPX provider is a third party that both carriers trust with their subscriber data.

**Forensic implication:** Roaming creates additional data holders. An investigator may obtain records from the visited network (which has the precise location data) and the home network (which has the subscriber identity). The roaming exchange is an additional third party with signaling and user-plane metadata that neither carrier controls.

### 4.2 MVNO Architecture

Mobile Virtual Network Operators (MVNOs) do not operate their own RAN or core network. They lease access from a Mobile Network Operator (MNO). The data collection implications depend on the MVNO's degree of independence:

**Thin MVNO (no core network):** The MVNO uses the MNO's core network entirely. The MNO collects all subscriber data and provides the MVNO with billing records and subscriber management interfaces. The MNO has full visibility into all MVNO subscriber activity.

**Thick MVNO (own core network):** The MVNO operates its own HSS, MME, PGW, and IMS core but uses the MNO's RAN. The MNO sees the device on the radio layer (cell ID, TA, IMSI) but does not have access to the MVNO's subscriber data or traffic metadata. The MVNO's core network is the data collector for higher-layer information.

**Privacy relevance:** The two-phone strategy sometimes recommends MVNOs as a way to "avoid the major carriers." In practice, MVNOs (especially thin MVNOs) provide no additional privacy protection. The underlying MNO has the same access to cell-level location data and signaling metadata regardless of the MVNO brand.

### 4.3 5G Network Slicing

5G introduces network slicing — the ability to create multiple virtual networks on a shared physical infrastructure.[^5] Each slice can have different data collection and processing policies.

**Privacy implications of network slicing:**

- A device may be connected to multiple slices simultaneously (e.g., a public internet slice and an enterprise private slice)
- Each slice has its own UPF and its own data collection policies
- The slice identifier (S-NSSAI) is visible in NAS signaling and is logged by the AMF
- Slice-specific DPI and lawful intercept can be configured independently

Network slicing does not currently provide privacy benefits for consumer devices. Consumer devices typically use a single "default" slice with standard data collection. However, for enterprise users on private slices, the data collection may be reduced (or increased, depending on the enterprise's policies).

---

## Part 5: Privacy Implications for the Two-Phone Strategy

### 5.1 What the Carrier Sees for Each Phone

**Phone A (Flip phone, active cellular connection):**

The carrier sees everything the network architecture allows:
- The IMSI (identifying the subscriber)[^1]
- The IMEI (identifying the device hardware)[^1]
- Every cell ID the device connects to (continuous location tracking)
- Timing advance values (sub-cell location precision)
- Every call (dialed number, duration, timestamp)
- Every SMS (content in 2G/3G, metadata in 4G/5G)
- Every data session (if data is enabled)
- The subscriber's name, address, and payment method (from billing)

**Phone B (De-Googled smartphone, Wi-Fi only, no cellular):**

If Phone B has no cellular connection and no SIM:
- The carrier sees nothing directly
- However, if Phone B ever connects to a known Wi-Fi network that the carrier also provides (e.g., carrier Wi-Fi hotspots), the carrier may correlate through MAC address or captive portal login

**Phone B (De-Googled smartphone, with cellular + data):**

The carrier sees:
- The IMSI (subscriber identity, if a SIM is present)
- The IMEI (device identity — permanent, cannot be changed)
- Cell ID and TA for every connection
- If data is used through the carrier: all destination IPs via PGW NetFlow
- If VPN is used over cellular: VPN server IP, protocol fingerprint, encrypted traffic metadata
- DPI application identification (VPN usage, Signal patterns, Tor patterns)

### 5.2 The Carrier Correlation Attack

The single most powerful investigative capability against the two-phone strategy is carrier-side correlation. If both Phone A and Phone B have active cellular connections, the carrier (or law enforcement with access to carrier records) can:

1. Query the MME/AMF logs for both IMSIs
2. Compare the cell ID and TA records across both devices
3. Identify timestamps where both devices were at the same cell location simultaneously
4. Conclude that the same person carries both phones

This correlation does not require any technical sophistication. It is a simple database query across two subscriber records. The cell ID logs from normal network operation provide sufficient granularity to establish co-location within a city block.

### 5.3 Mitigation at the Network Architecture Level

The only way to prevent carrier-side correlation is to ensure Phone B is never visible to a cellular network:

- **No SIM in Phone B:** Without a SIM, Phone B has no IMSI and cannot authenticate to the cellular network. The carrier has no record of the device.
- **Wi-Fi only operation:** Phone B connects only through Wi-Fi networks that are not associated with the carrier.
- **IMEI exposure:** Even without a SIM, if Phone B is powered on with cellular radios enabled, it may still transmit the IMEI during emergency calls (E911). The carrier logs this transmission. Phone B's cellular radio should be disabled at the hardware level or the device kept in a faraday bag when not in use.

For users who must have cellular connectivity on Phone B, the mitigations are:
- Use a prepaid SIM purchased with cash (no identity link)
- Rotate SIMs regularly (prevent long-term IMSI correlation)
- Accept that the carrier has the metadata described in this chapter

---

## Chapter Summary

| Topic | Key Finding |
|-------|-------------|
| Network architecture | Four domains: UE, RAN, Core, Transport — each with independent data collection capabilities |
| RAN collection | Cell ID, Timing Advance, Angle of Arrival, measurement reports — sufficient for sub-block location tracking |
| MME/AMF logs | Complete timeline of every network interaction (attach, TAU, service request, handover) |
| PGW/UPF logs | Carrier-side NetFlow: every destination IP, port, protocol, data volume |
| IMS/SIP logs | Call metadata (dialed number, duration) for all VoLTE/VoNR calls; SMS metadata |
| HSS/UDM | Permanent subscriber identity database; links IMSI to name, address, payment method |
| Billing records | Retained 3-7 years; provides financial link between subscriber identity and network activity |
| Lawful Intercept | Real-time content + metadata; OS/app-level encryption does not protect carrier-side metadata |
| DPI systems | Application identification (Signal, Tor, VPN) through traffic fingerprinting |
| Roaming/MVNO | Additional data holders (visited network, GRX/IPX operator); MVNOs do not provide privacy benefit |
| Two-phone correlation | Carrier can correlate Phone A and Phone B by comparing MME logs (same cell ID at same time = same person) |
| Mitigation | No SIM in Phone B, Wi-Fi only, cellular radio disabled, faraday bag discipline |

---

[^1]: 3GPP TS 23.003, "Numbering, addressing and identification," defines IMSI, SUPI, SUCI, GUTI, and IMEI/PEI structures. European Telecommunications Standards Institute (ETSI) / 3GPP, current version available at https://www.3gpp.org/dynareport/23003.htm.

[^2]: 3GPP TS 38.331, "NR; Radio Resource Control (RRC); Protocol specification," defines gNB RRC procedures and measurement reporting for 5G NR. Available at https://www.3gpp.org/dynareport/38331.htm.

[^3]: NIST SP 800-187, "Guide to LTE Security," National Institute of Standards and Technology, December 2017. Describes the LTE/EPC architecture, security procedures, and data collection points. Available at https://doi.org/10.6028/NIST.SP.800-187.

[^4]: 3GPP TS 24.301, "Non-Access-Stratum (NAS) protocol for Evolved Packet System (EPS)," defines NAS messaging between UE and MME/AMF, including Attach Request and Tracking Area Update procedures. Available at https://www.3gpp.org/dynareport/24301.htm.

[^5]: 3GPP TS 38.413, "NG-RAN; NG Application Protocol (NGAP)," defines the interface between gNB and AMF in 5G, including network slicing support via S-NSSAI. Available at https://www.3gpp.org/dynareport/38413.htm.

[^6]: 3GPP TS 33.501, "Security architecture and procedures for 5G System," defines the SUCI mechanism, SUPI concealment using ECIES (Profiles A and B), and null-scheme fallback behavior. Available at https://www.3gpp.org/dynareport/33501.htm.

[^7]: 3GPP TS 36.413, "Evolved Universal Terrestrial Radio Access Network (E-UTRAN); S1 Application Protocol (S1AP)," defines S1AP messages including Initial UE Message carrying EUTRAN-CGI and TAI. Available at https://www.3gpp.org/dynareport/36413.htm.

[^8]: 3GPP TS 36.331, "Evolved Universal Terrestrial Radio Access (E-UTRA); Radio Resource Control (RRC); Protocol specification," defines RRC measurement report structures and RRC connection procedures. Available at https://www.3gpp.org/dynareport/36331.htm.

[^9]: *Carpenter v. United States*, 585 U.S. 296 (2018). The Supreme Court held that the government's acquisition of seven days of historical cell-site location information constitutes a Fourth Amendment search requiring a warrant supported by probable cause.

[^10]: Ravishankar Borgaonkar, Lucca Hirschi, Shinjo Park, and Altaf Shaik, "New Privacy Threat on 3G, 4G, and Upcoming 5G AKA Protocols," *Proceedings on Privacy Enhancing Technologies* (PoPETs), 2019(3):108–127. Demonstrates how HSS-side data can be correlated to track device identity across sessions.

[^11]: Communications Assistance for Law Enforcement Act (CALEA), 47 U.S.C. §§ 1001–1010 (1994). Mandates that telecommunications carriers design their networks to support lawful interception of communications and call-identifying information upon lawful authorization.
