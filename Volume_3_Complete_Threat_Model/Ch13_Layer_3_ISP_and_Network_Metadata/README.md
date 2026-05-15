# Chapter 13: Layer 3 — ISP & Network Metadata (Phone B & Computer)

## Overview

Layer 3 addresses vulnerabilities arising from Internet Service Provider (ISP) network metadata. When Phone B or the Computer connects to the internet through a residential ISP, every packet traverses infrastructure that the ISP controls, monitors, and logs. The IP address assigned to the connection is the single most powerful identity anchor in the digital world: it ties the connection to a specific subscriber account, which ties to a name, billing address, and payment method.

The critical failure mode for Layer 3 is simple: if Phone B or the Computer ever connects via a residential ISP (home internet), the IP address immediately links to the subscriber's real identity. The two-phone compartmentalization collapses in a single connection.

This chapter examines each network-layer vulnerability, the forensic data it exposes, how an adversary collects it, and the mitigations available. The common thread is that the residential ISP connection is the single point of failure for the entire strategy.

---

## Vulnerability 1: IP Address Assignment

**Severity: Critical**

Every device connected to the internet has an IP address. When connected through a residential ISP (cable, DSL, fiber), the IP address is assigned to a specific subscriber account. The ISP maintains subscriber records that map IP addresses to names, physical addresses, phone numbers, and billing information.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Home address, subscriber name, billing info |
| Collection Method | ISP subscriber records (subpoena, §2703(d) order) |
| Mitigation | Never connect via residential ISP |

The IP address is the foundational identity anchor for internet-based communications. When an adversary obtains a target's IP address from server logs, email headers, or real-time monitoring, they can serve a subpoena on the ISP to obtain the subscriber's identity. In the United States, this process is governed by 18 U.S.C. §2703(d), which requires a court order based on "specific and articulable facts" — a lower standard than probable cause.

The residential ISP link is particularly dangerous for the two-phone strategy because it creates a direct, legally enforceable path from an IP address to a person's identity. If Phone B connects via home Wi-Fi, the ISP can identify Phone B's IP address as belonging to the subscriber (you). If the Computer connects via home internet, the same applies.

**The Critical Failure**: Phone B and the Computer must never, under any circumstances, connect to the internet through a residential ISP. This means:
- No home Wi-Fi for Phone B
- No home Ethernet for the Computer
- No tethering through a cellular plan linked to your identity

The only safe network connection for Phone B and the Computer is public Wi-Fi (coffee shop, library) behind a VPN, with strict MAC randomization and no personal account logins.

---

## Vulnerability 2: DNS Queries (Unencrypted)

**Severity: Critical**

The Domain Name System (DNS) translates human-readable domain names (signal.org, protonmail.com) into IP addresses. When a device makes a DNS query, the query itself — containing the full domain name — is transmitted to the DNS resolver. With traditional (unencrypted) DNS, this query is visible to the ISP at the network level.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Every domain visited (signal.org, protonmail.com, torproject.org) |
| Collection Method | ISP logs, passive network monitoring |
| Mitigation | Encrypted DNS (DNS-over-HTTPS or DNS-over-TLS) |

Unencrypted DNS queries reveal the complete browsing profile of a user. Every website visited, every API endpoint called, every service contacted is exposed in the DNS query log. An ISP can see that a user visits signal.org, protonmail.com, and torproject.org — all strong indicators of privacy-seeking behavior.

An adversary with ISP logs can reconstruct:
- The list of all services used (Signal, ProtonMail, Tor)
- The frequency and timing of usage
- Changes in behavior over time
- Patterns correlating to real-world events

Encrypted DNS (DNS-over-HTTPS/DoH or DNS-over-TLS/DoT) encrypts the DNS query itself, preventing the ISP from seeing which domains are being resolved. However, the encrypted DNS traffic is distinguishable from regular traffic, so the ISP knows that DNS encryption is being used — a metadata point in itself.

---

## Vulnerability 3: SNI (Server Name Indication) Exposure

**Severity: High**

Server Name Indication (SNI) is a TLS extension that allows a client to tell a server which hostname it wants to connect to during the TLS handshake. This field is transmitted in plaintext before encryption is established, meaning it is visible to anyone monitoring the network.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Domain names of HTTPS sites being visited |
| Collection Method | ISP deep packet inspection (DPI), passive monitoring |
| Mitigation | Encrypted Client Hello (ECH), VPN, Tor |

Even though the content of HTTPS traffic is encrypted, the SNI field reveals the destination domain. An ISP using DPI equipment can log every domain a user visits, even over HTTPS. This provides the same information as DNS logging but at the connection level rather than the query level.

Encrypted Client Hello (ECH, formerly known as ESNI) is a proposed standard that encrypts the SNI field within the TLS handshake. However, ECH deployment is currently limited. Cloudflare and a handful of other providers support it, but adoption is far from universal.

The practical mitigation is to route traffic through a VPN or Tor. The ISP sees only a single encrypted connection to the VPN server or Tor bridge, not the individual destination domains of each connection.

---

## Vulnerability 4: NetFlow/IPFIX Logging

**Severity: High**

NetFlow (Cisco) and IPFIX (IETF standard) are network protocols used to collect IP traffic metadata. Routers and switches generate flow records that summarize communication between IP addresses, including source and destination IPs, ports, protocol, packet count, byte count, and timestamps.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Source/destination IPs, ports, bytes transferred, timestamps |
| Collection Method | ISP NetFlow/IPFIX logs |
| Mitigation | VPN (shifts trust from ISP to VPN provider) |

NetFlow logs do not contain packet contents, but they provide a rich metadata picture of communication patterns. An ISP can analyze NetFlow logs to:
- Identify services being used by destination IP and port
- Measure the volume of traffic to each service
- Determine communication patterns (times of day, frequency, duration)
- Correlate activity across multiple devices on the same connection

NetFlow analysis can identify Signal usage even through a VPN if timing patterns and packet sizes are analyzed. While the VPN encrypts the destination IP, the tunnel itself generates flow records showing connection to the VPN server, enabling metadata analysis of when and how much the VPN is used.

---

## Vulnerability 5: VPN Detection and Timing Analysis

**Severity: Medium**

Virtual Private Networks (VPNs) are the primary defense against ISP metadata collection. However, VPNs are not invisible. ISPs can detect VPN usage through protocol fingerprinting (OpenVPN, WireGuard, IPsec have distinctive handshake patterns), and can degrade or block VPN connections.

| Attribute | Detail |
|-----------|--------|
| Data Exposed | Use of VPN protocols, conversation patterns (via timing) |
| Collection Method | ISP deep packet inspection, NetFlow analysis |
| Mitigation | Obfuscated VPN, Tor bridge, traffic padding |

VPN detection is itself a metadata point. If an ISP detects that a subscriber is using a VPN, it signals that the subscriber has something to hide — a potentially incriminating inference in itself. In jurisdictions where VPN use is restricted or surveilled, this detection can trigger further investigation.

Timing analysis goes beyond VPN detection. Even with a VPN, the timing and size of encrypted packets can reveal information about the underlying communication. Machine learning models can identify encrypted messaging patterns (Signal, WhatsApp, Telegram) based on:
- Packet inter-arrival times
- Packet size distributions
- Session duration and frequency
- Burst patterns

Tor provides stronger protection against timing analysis through its fixed cell size (512 bytes) and multi-hop routing. However, Tor is noticeably slower and may not be practical for all use cases.

---

## Vulnerability Summary Table

| Vulnerability | Data Exposed | Collection Method | Severity | Mitigation |
|--------------|-------------|-------------------|----------|------------|
| IP address assignment | Home address, name, billing info | ISP subscriber records | Critical | Never use residential ISP |
| DNS queries (unencrypted) | Every domain visited | ISP logs, passive monitoring | Critical | Encrypted DNS (DoH/DoT) |
| SNI exposure | Domain names of HTTPS sites | ISP DPI, passive monitoring | High | ECH, VPN |
| NetFlow/IPFIX | Source/destination IPs, ports, bytes | ISP logs | High | VPN (shifts trust) |
| VPN detection | Use of VPN protocols | ISP DPI | Medium | Obfuscated VPN, Tor bridge |
| Timing analysis | Conversation patterns, message lengths | ISP NetFlow | Medium | Traffic padding, Tor |

---

## The Residential ISP Problem

Layer 3 has a single root cause for all its critical-severity vulnerabilities: the residential ISP connection. The IP address is the identity anchor. DNS, SNI, and NetFlow are supplemental data streams that enrich the picture, but the IP address is sufficient by itself to link online activity to a person.

The two-phone strategy requires that Phone B and the Computer have no identity-linked IP addresses. This means:
- No connections through a residential ISP
- No connections through a cellular data plan linked to identity
- No connections through workplace or educational networks (which are also identity-linked)

The only acceptable connection model is public Wi-Fi (coffee shop, library, public space) behind a VPN, with strict operational security around travel to and from the connection point. The public Wi-Fi's IP address provides no identity link. The VPN prevents the public Wi-Fi operator from seeing the connection destinations.

---

## Severity Ratings

| Vulnerability | Severity | Rationale |
|--------------|----------|-----------|
| IP address assignment | Critical | Direct link to subscriber identity via ISP records |
| DNS queries (unencrypted) | Critical | Reveals every service and site visited |
| SNI exposure | High | Reveals HTTPS destination domains |
| NetFlow/IPFIX | High | Comprehensive metadata of all communications |
| VPN detection | Medium | Reveals privacy-seeking behavior, not content |
| Timing analysis | Medium | Requires ML analysis, lower precision |

---

## Conclusion

Layer 3 is where the two-phone strategy most often fails in practice. The original strategy's critical oversight was assuming that any internet connection — including residential ISP — was safe for Phone B and the Computer. It is not. A single connection through a residential ISP creates a permanent, legally obtainable link between the IP address and the subscriber identity.

The mitigations for Layer 3 are straightforward in concept but demanding in practice. Phone B and the Computer must be used exclusively on public Wi-Fi behind a VPN. Encrypted DNS must be configured. Applications that reveal the user's real IP address (email clients, messengers) must be configured to use the VPN or Tor.

The operational burden is significant: public Wi-Fi requires travel, imposes time constraints, and introduces physical surveillance risks (Layer 5). The user must travel to a coffee shop, connect via VPN, conduct their communications, disconnect, and leave — potentially multiple times per day. This is not a casual strategy. It is a lifestyle.

For the user who cannot maintain this operational discipline, the two-phone strategy provides no meaningful protection against ISP-based deanonymization. The IP address is the link. Control the IP address, or the strategy fails.
