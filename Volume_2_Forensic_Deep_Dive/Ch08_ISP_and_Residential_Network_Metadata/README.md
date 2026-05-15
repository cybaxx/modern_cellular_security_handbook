# Chapter 8: ISP and Residential Network Metadata

## Introduction

The residential ISP connection is the fatal flaw for any privacy strategy that involves using a private device from home. Unlike cellular networks, which require a warrant or court order for historical location data in many jurisdictions,[^1] ISP logs are routinely collected, retained for months, and disclosed under comparatively low legal standards.

When a user specifies "private Wi-Fi networks via residential ISP" as the connectivity model for their private phone, they are inadvertently creating a direct link between their device and their identity. The ISP does not need to intercept the content of communications — it collects metadata that is often more revealing than content.

## What Your ISP Collects

Even when you use HTTPS for all web traffic, even when you use a VPN, even when you use encrypted DNS, your ISP collects multiple layers of metadata.

### IP Assignment

Your public IP address is mapped to your billing name and physical address. This mapping is maintained indefinitely by most ISPs. Every packet you send carries your public IP as the source address. Any website, service, or adversary that observes this IP can identify your ISP and, through a subpoena or court order, your identity.

### DHCP Logs

Your router's DHCP server assigns local IP addresses to each connected device. The ISP's upstream equipment logs the mapping between your public IP, your modem's MAC address, and the timestamps of each session. These logs typically include the device hostname and MAC address. Retention periods at major US ISPs range from 6 to 18 months. A Section 2703(d) order compels production of these logs, directly linking your device's MAC address and hostname to your name and address.

### DNS Queries

Unless you use encrypted DNS (DNS over HTTPS or DNS over TLS), every domain you visit is transmitted in plaintext to your ISP's DNS resolver. The ISP logs include the full domain name — `signal.org`, `protonmail.com`, `reddit.com`, `bankofamerica.com` — along with the timestamp. Even with encrypted DNS, the ISP can observe that DNS queries are occurring and can infer the IP addresses you contact.

### NetFlow and IPFIX

NetFlow (Cisco) and IPFIX (the standardized version) are network monitoring protocols that summarize traffic flows.[^2] A flow record contains the source IP, destination IP, source port, destination port, protocol, packet count, byte count, and timestamps for each communication session. NetFlow does not include content, but it reveals every server your device contacts, how much data was transferred, and the duration of each connection. Machine learning analysis of NetFlow data can identify applications, services, and even specific activities (streaming, messaging, file download) with high accuracy.

### Server Name Indication (SNI)

During the TLS handshake, the client sends the domain name in plaintext as part of the Server Name Indication extension.[^3] This allows the server to present the correct certificate for the requested domain. SNI is transmitted before the encrypted tunnel is established, meaning it is visible to any party monitoring the connection — including your ISP. Encrypted Client Hello (ECH) is a proposed standard that encrypts SNI, but as of 2026, adoption remains rare. The vast majority of HTTPS connections expose the domain name in plaintext through SNI.

### Deep Packet Inspection (DPI)

Many ISPs deploy Deep Packet Inspection equipment — often from vendors like Sandvine, Procera, or Palo Alto Networks — to classify traffic by application. DPI does not decrypt your traffic, but it recognizes application-layer protocol patterns. It can identify that you are using Signal, Tor, a specific VPN protocol (OpenVPN, WireGuard, IPSec), or streaming video from a particular provider. This classification data is retained for up to 30 days by many ISPs and is available to law enforcement.

## The Forensic Subpoena Workflow

The process by which law enforcement obtains ISP records is straightforward and well-established.

An investigator identifies a target IP address — either because it appears in a service's logs (such as Signal or ProtonMail), was observed in a network capture, or is associated with a suspect's online activity. The investigator drafts a Section 2703(d) order under the Stored Communications Act, specifying the IP address and date range. The order is served on the ISP's legal compliance team.

The ISP responds with a package of records that typically includes: the subscriber's name, address, phone number, and payment method from billing records; DHCP logs showing which MAC addresses were assigned to that IP and at what times; NetFlow records showing all communications from that IP, including destinations, ports, and data volumes; and DNS query logs showing every domain visited.

The result is devastating for compartmentalization. The investigator now knows that the person at 123 Main Street uses a specific device (identified by MAC address and hostname) to access privacy services like Signal at specific times of day. They do not need to break Signal's encryption. They do not need to intercept content. They have enough to identify, locate, and question the suspect.

## Timing Attacks and Traffic Analysis

Even with perfect operational security — MAC randomization, always-on VPN, encrypted DNS, no Google services, custom OS — timing information leaks through the ISP connection.

A passive adversary monitoring the ISP's network observes packet sizes and timing patterns. Signal messages have distinct, consistent sizes: approximately 1.2 kilobytes for a text message, approximately 50 kilobytes for a photo, and different sizes for voice messages and attachments. A machine learning model can classify these patterns with high accuracy. The adversary can determine exactly when messages were sent and received, and can infer the volume of communication.

Burst patterns are equally revealing. A message is sent from the device, and approximately 500 milliseconds later, data arrives from the Signal server — indicating a reply. Over hours of observation, the analyst can reconstruct the timing of a real-time conversation, including the number of messages exchanged, response times between participants, and periods of active versus idle communication.

Without ever decrypting a single packet, an analyst can testify that "the device at IP address 203.0.113.45 exchanged 847 encrypted packets with signal.org between 8:00 PM and 9:00 PM on May 14, consistent with a 47-message conversation between two participants."

## Router Logs

Your residential router — whether provided by the ISP or purchased separately — maintains internal logs of connected devices. These logs include each device's MAC address, assigned IP address, session start and end times, and in some cases, URLs visited when parental controls or traffic logging features are enabled.

Consumer routers vary in log retention. Some keep only the most recent 50 entries; others store months of history. ISP-provided routers often report this data back to the ISP automatically, meaning the logs exist on the ISP's servers even if the router is factory reset.

The attack vector is straightforward: law enforcement obtains a warrant to seize the router. Forensic examiners use tools like Cellebrite UFED to image the router's flash storage. They extract the full log history. This provides a complete record of every device that connected to that home network, with timestamps, hostnames, and MAC addresses — including Phone B, the "private" device.

## VPN Limitations

A VPN is often presented as a solution to ISP monitoring, but it has fundamental limitations that must be understood.

A VPN shifts trust from the ISP to the VPN provider. The VPN provider now sees everything the ISP would have seen: your real IP address, the timing and volume of your traffic, and the destinations you connect to (though the destination IP, not the domain name, if DNS is routed through the tunnel). Many "no-log" VPNs have been demonstrated to maintain logs despite public claims to the contrary. IPVanish provided connection logs to federal investigators in 2016 despite claiming a "zero logs" policy,[^4] and PureVPN cooperated with the FBI in 2017 by providing subscriber logs despite marketing itself as a no-log provider.[^5]

Technical leaks are another concern. WebRTC leaks, DNS leaks, and IPv6 leaks can expose your real IP address even with a properly configured VPN tunnel. These leaks occur when the operating system sends traffic outside the tunnel, often through misconfigured network stacks or browser behaviors.

Even when the VPN functions perfectly, the connection to the VPN server is itself visible to the ISP. The ISP sees that you are using a VPN — the protocol (OpenVPN, WireGuard), the server IP, the volume of traffic, and the timing. This metada alone is sufficient for many investigative purposes.

Recommended privacy-maximalist VPN choices include Mullvad (no email required, accepts cash payments, audited no-log policy), ProtonVPN (Swiss jurisdiction, transparent operations), and IVPN (audited, strong privacy policy). Commercial VPNs with large marketing budgets — NordVPN, ExpressVPN — have histories of breaches and logging controversies.

## The Residential ISP as the Fatal Flaw for Compartmentalization

The two-phone strategy depends on compartmentalization: Phone A is the public face, Phone B is the private device. The separation between them is supposed to prevent anyone from connecting the two identities. The residential ISP shatters this separation because it sits at the intersection of identity and activity.

Phone B, even if it has no cellular modem and runs a de-Googled operating system, must connect to the internet through some network. If that network is the user's home ISP connection, the ISP logs create an unbreakable link between Phone B and the user's identity. The ISP knows whose name is on the account, what address the service is delivered to, and what device is connecting. Phone B's MAC address, its IP address, its traffic patterns — all are tied to a specific human being.

The compartmentalization fails not because Phone B is used carelessly but because the network it uses is inherently identity-bearing. A residential ISP connection is not anonymous by design. It is the opposite: it is registered to a person, billed to a person, and provisioned to a physical address. Every packet that traverses this connection carries the implicit signature of the subscriber.

### Breaking the Link

To preserve compartmentalization, Phone B must never use a network connection that is linked to the user's identity. This means:
- Never connecting to the home Wi-Fi network
- Never using a cellular hotspot tied to the user's name
- Never logging into any service on Phone B that reveals the user's identity

The alternative is to use only public Wi-Fi networks (coffee shops, libraries, public transit) where access does not require identification, combined with prepaid cellular hotspots purchased with cash and never brought home. Even then, the public Wi-Fi operator's logs may be subject to subpoena, and the hotspot's IMEI may be tracked.

## Traffic Analysis in ISP Networks

Beyond the metadata explicitly collected by ISPs, traffic analysis techniques enable inference of user behavior from patterns in encrypted traffic. This is distinct from content interception — the analyst never decrypts the data — but the patterns themselves are often highly revealing.

### Packet Size Analysis

Different applications produce characteristic packet size distributions. Voice over IP (including encrypted VoIP like Signal calls) produces small, regular packets at consistent intervals. Video streaming produces larger, bursty packets with characteristic frame patterns. Web browsing produces a mix of small request packets and larger response packets. File downloads produce sustained large-packet flows. An analyst can classify encrypted traffic into application categories with high accuracy using packet size distributions alone.

### Timing Analysis and Side Channels

The timing of network activity itself reveals information. A device that transmits a small packet every 30 seconds with high regularity is likely performing a keepalive or polling function. A device that transmits in bursts with inter-burst intervals matching human conversation patterns is likely engaged in instant messaging. A device that receives data before transmitting (the server pushed content before the user responded) indicates an interactive session.

These timing patterns persist regardless of encryption. They are a function of human behavior, not protocol design. An analyst who observes the device's network activity for a period of days can identify when the user wakes, when they leave for work, when they return home, and when they go to sleep — all from encrypted traffic patterns.

### Correlation Attacks Across Services

If a user accesses multiple services from the same IP address — even if all connections are encrypted — the ISP logs show that the same device accessed all of them. The combination of services creates a unique usage fingerprint. A user who accesses Signal, ProtonMail, a news site, and a weather service at specific times of day is identifiable even if each individual service connection reveals nothing.

## DNSSEC, DoH, and DoT

Encrypted DNS is often presented as a solution to ISP DNS monitoring, but it has limitations. DNS over HTTPS and DNS over TLS encrypt the DNS query between the device and the recursive resolver. The ISP can still observe that DNS queries are occurring (by packet size and server IP), but not the query content. However, the ISP can observe the destination IP addresses the device subsequently connects to, which often reveals the domain indirectly. If a device connects to 104.16.132.229, that IP belongs to Cloudflare and hosts thousands of domains, but if it then connects to 185.199.108.153, that IP belongs to GitHub Pages. The resolution from IP to domain is often straightforward through reverse DNS or passive DNS databases.

## ISP Traffic Shaping as Evidence

Some ISPs practice traffic shaping — intentionally slowing specific types of traffic (peer-to-peer, streaming video, VPN protocols). The presence of traffic shaping on a connection suggests the ISP has classified the user's traffic. Classification data is typically logged and may be subject to subpoena. If an ISP has identified a user as a VPN user through traffic shaping classification, that metadata is stored and can be produced.

## The Role of Data Brokers

ISPs in the United States are permitted to sell anonymized aggregate data under the privacy framework established by the FCC and FTC. However, the line between "anonymized" and "re-identifiable" is thin. If an data broker can combine ISP location data with credit card records, loyalty program data, or public records, the anonymity dissolves quickly.

## Data Retention by Jurisdiction

Data retention requirements vary substantially by jurisdiction, creating different risk profiles for ISP metadata.

In the United States, no federal law mandates specific data retention periods for ISPs. However, the Electronic Communications Privacy Act and the Stored Communications Act provide the framework for government access. Most major ISPs retain DHCP logs for 6 to 18 months, NetFlow records for 30 to 90 days, and subscriber account records indefinitely. There is no mandatory data retention directive, but commercial incentives and practical necessity drive ISPs to retain data.

The European Union, through the ePrivacy Directive and GDPR, has a more complex framework. The now-invalidated Data Retention Directive (2006/24/EC) required retention of telecommunications metadata for 6 to 24 months, but it was struck down by the Court of Justice of the European Union in 2014. In its absence, member states have enacted varying national laws. Germany requires retention of telecommunications metadata for 10 weeks and location data for 4 weeks. The UK, under the Investigatory Powers Act 2016, requires ISPs to retain internet connection records for 12 months. France requires 12 months for all metadata.

China's data retention framework operates under different principles entirely. The Cybersecurity Law and related regulations require telecommunications service providers to retain logs for at least 6 months. The legal threshold for government access is substantially lower than in the US or EU, and the technical infrastructure for mass surveillance — the Great Firewall and associated systems — exists at the ISP level.

## Protocol Deep Dive: Packet Structures and Wire Format

The preceding sections described what ISPs collect and why it matters operationally. This section shows the wire format — the actual byte sequences that flow through the network and land in investigator hands. Understanding the exact structure of each record clarifies why metadata is so precise and why protocol-level defenses are hard to implement correctly.

---

### 1. NetFlow v9 / IPFIX Flow Record

NetFlow v9 and its IETF-standardized successor IPFIX encode each traffic flow as a fixed-width binary record.[^2] The exporter (typically a router or DPI appliance) groups packets with the same five-tuple into a single flow, emits it to a collector, and the collector writes it to storage. Analysts query that storage by IP address and time range.

A typical enterprise/ISP flow record for a single TCP session:

```c
/* NetFlow v9 / IPFIX flow record — one record per TCP session */
struct netflow_v9_record {
    uint32_t  src_addr;          /* Source IPv4 address                   */
    uint32_t  dst_addr;          /* Destination IPv4 address              */
    uint16_t  src_port;          /* Source TCP/UDP port                   */
    uint16_t  dst_port;          /* Destination TCP/UDP port              */
    uint8_t   ip_proto;          /* IP protocol (6=TCP, 17=UDP)           */
    uint8_t   tcp_flags;         /* Union of TCP flags seen in flow       */
    uint8_t   tos;               /* IP Type of Service / DSCP             */
    uint16_t  input_snmp;        /* Ingress interface SNMP index          */
    uint16_t  output_snmp;       /* Egress interface SNMP index          */
    uint32_t  flow_start_ms;     /* Flow start timestamp (milliseconds)   */
    uint32_t  flow_end_ms;       /* Flow end timestamp (milliseconds)     */
    uint64_t  bytes;             /* Total bytes in flow                   */
    uint64_t  packets;           /* Total packet count                    */
    uint16_t  bgp_src_as;        /* BGP source autonomous system number   */
    uint16_t  bgp_dst_as;        /* BGP destination autonomous system     */
};
```

Example: a Signal message exchange. Destination `13.248.212.111` is one of Signal's AWS Global Accelerator anycast addresses. Port 443, TCP, 1247 bytes, 400 ms duration.

```hexdump
Offset  Hex                                      Decoded
------  -------                                  --------------------------------
0x00    C0 A8 01 6F                              src_addr:    192.168.1.111 (LAN — NAT'd to subscriber public IP upstream)
0x04    0D F8 D4 6F                              dst_addr:    13.248.212.111 (Signal AWS Global Accelerator)
0x08    C4 A2                                    src_port:    50338 (ephemeral)
0x0A    01 BB                                    dst_port:    443 (HTTPS/TLS)
0x0C    06                                       ip_proto:    6 (TCP)
0x0D    1B                                       tcp_flags:   0x1B = SYN+ACK+PSH+FIN (full session lifecycle)
0x0E    00                                       tos:         0x00 (default precedence)
0x0F    00 03                                    input_snmp:  3 (WAN interface)
0x11    00 01                                    output_snmp: 1 (LAN interface)
0x13    5F 3E 82 10                              flow_start:  1597926928 ms epoch offset
0x17    5F 3E 82 A0                              flow_end:    +400 ms (0x90 = 144 ticks)
0x1B    00 00 00 00 00 00 04 DF                  bytes:       1247
0x23    00 00 00 00 00 00 00 09                  packets:     9
0x2B    00 00                                    bgp_src_as:  0 (not applicable — LAN source)
0x2D    4E 6C                                    bgp_dst_as:  20108 (Amazon AWS)
```

What this record proves without decryption: the subscriber's device contacted `13.248.212.111` (registered to Amazon/Signal) on port 443 via TCP. The 400 ms duration and 1,247 bytes are consistent with a single encrypted Signal message transmission. The BGP destination AS 20108 maps directly to Amazon, and passive DNS correlation places this specific IP in Signal's infrastructure at the time of the flow. Nine packets for 1,247 bytes yields an average of ~139 bytes per packet — consistent with Signal's fixed-size padding scheme for short messages. The tcp_flags value `0x1B` confirms a full connection lifecycle occurred (connection was established, data transferred, and gracefully terminated) within the logging interval.

---

### 2. TLS ClientHello with SNI

The TLS handshake begins with a ClientHello, sent in plaintext before any encryption is established.[^3] The SNI extension inside it transmits the target hostname — `signal.org` — verbatim, readable by any observer on the path.

```c
/* TLS Record Layer */
struct tls_record {
    uint8_t   content_type;      /* 0x16 = Handshake                      */
    uint16_t  legacy_version;    /* 0x0303 = TLS 1.2 (even for TLS 1.3)  */
    uint16_t  length;            /* Length of the following fragment      */
};

/* Handshake Header */
struct tls_handshake_header {
    uint8_t   msg_type;          /* 0x01 = ClientHello                    */
    uint8_t   length[3];         /* 3-byte big-endian length              */
};

/* ClientHello Body */
struct tls_client_hello {
    uint16_t  legacy_version;    /* 0x0303                                */
    uint8_t   random[32];        /* Client random: 4-byte Unix time + 28B */
    uint8_t   session_id_len;    /* Length of session ID (0–32)           */
    uint8_t   session_id[32];    /* Session ID (may be empty)             */
    uint16_t  cipher_suites_len; /* Length of cipher suites list          */
    uint16_t  cipher_suites[];   /* e.g. TLS_AES_128_GCM_SHA256 (0x1301) */
    uint8_t   comp_methods_len;  /* Always 1 for TLS 1.3 clients          */
    uint8_t   comp_methods[];    /* 0x00 = no compression                 */
    uint16_t  extensions_len;    /* Total length of extensions block      */
    /* Extensions follow — see below */
};

/* Extension: server_name (type 0x0000) */
struct tls_ext_sni {
    uint16_t  ext_type;          /* 0x0000                                */
    uint16_t  ext_len;           /* Length of extension data              */
    uint16_t  list_len;          /* Length of ServerNameList              */
    uint8_t   name_type;         /* 0x00 = host_name                      */
    uint16_t  name_len;          /* Length of hostname string             */
    uint8_t   name[];            /* Plaintext hostname: "signal.org"      */
};

/* Extension: supported_versions (type 0x002b) */
struct tls_ext_supported_versions {
    uint16_t  ext_type;          /* 0x002b                                */
    uint16_t  ext_len;
    uint8_t   versions_len;
    uint16_t  versions[];        /* e.g. 0x0304 (TLS 1.3), 0x0303 (1.2)  */
};

/* Extension: supported_groups (type 0x000a) */
struct tls_ext_supported_groups {
    uint16_t  ext_type;          /* 0x000a                                */
    uint16_t  ext_len;
    uint16_t  groups_len;
    uint16_t  groups[];          /* e.g. 0x001d (x25519), 0x0017 (P-256)  */
};

/* Extension: signature_algorithms (type 0x000d) */
struct tls_ext_sig_algs {
    uint16_t  ext_type;          /* 0x000d                                */
    uint16_t  ext_len;
    uint16_t  algs_len;
    uint16_t  algs[];            /* e.g. 0x0804 (rsa_pss_rsae_sha256)     */
};
```

Annotated hexdump showing the SNI extension carrying `signal.org` in plaintext:

```hexdump
Offset  Hex                                      Decoded
------  -------                                  --------------------------------
--- TLS Record Layer ---
0x00    16                                       content_type: 0x16 (Handshake)
0x01    03 01                                    legacy_version: TLS 1.0 compat (RFC 8446 §4.1.2)
0x03    00 F1                                    length: 241 bytes follow

--- Handshake Header ---
0x05    01                                       msg_type: 0x01 (ClientHello)
0x06    00 00 ED                                 length: 237 bytes

--- ClientHello ---
0x09    03 03                                    legacy_version: 0x0303
0x0B    5F 3E 82 10 A3 C7 4F 12                  client_random (first 8 of 32 bytes shown)
        D8 9A 01 BB 77 6E 2C F4
        9B 3D 05 7A C1 88 4E 9F
        E2 00 B5 31 D7 6A C9 44
0x2B    20                                       session_id_len: 32
0x2C    [32 bytes session ID — omitted for brevity]
0x4C    00 08                                    cipher_suites_len: 8
0x4E    13 01                                    TLS_AES_128_GCM_SHA256
0x50    13 02                                    TLS_AES_256_GCM_SHA384
0x52    13 03                                    TLS_CHACHA20_POLY1305_SHA256
0x54    00 FF                                    TLS_EMPTY_RENEGOTIATION_INFO_SCSV
0x56    01                                       comp_methods_len: 1
0x57    00                                       comp_method: 0x00 (null / no compression)
0x58    00 96                                    extensions_len: 150

--- Extension: server_name (SNI) ---         *** PLAINTEXT HOSTNAME ***
0x5A    00 00                                    ext_type: 0x0000 (server_name)
0x5C    00 0E                                    ext_len: 14
0x5E    00 0C                                    ServerNameList length: 12
0x60    00                                       name_type: 0x00 (host_name)
0x61    00 09                                    name_len: 9
0x63    73 69 67 6E 61 6C 2E 6F 72 67            "signal.org"  <-- VISIBLE IN PLAINTEXT

--- Extension: supported_versions ---
0x6D    00 2B                                    ext_type: 0x002b
0x6F    00 05                                    ext_len: 5
0x71    04                                       versions_len: 4
0x72    03 04                                    TLS 1.3
0x74    03 03                                    TLS 1.2

--- Extension: supported_groups ---
0x76    00 0A                                    ext_type: 0x000a
0x78    00 06                                    ext_len: 6
0x7A    00 04                                    groups_len: 4
0x7C    00 1D                                    x25519
0x7E    00 17                                    secp256r1 (P-256)

--- Extension: signature_algorithms ---
0x80    00 0D                                    ext_type: 0x000d
0x82    00 06                                    ext_len: 6
0x84    00 04                                    algs_len: 4
0x86    08 04                                    rsa_pss_rsae_sha256
0x88    04 03                                    ecdsa_secp256r1_sha256
```

The bytes at offset `0x63`–`0x6B` — `73 69 67 6E 61 6C 2E 6F 72 67` — are the ASCII encoding of `signal.org`, transmitted before the TLS session is encrypted. Every router, DPI appliance, or passive tap on the path from the device to the internet sees this string.

**What ECH would change.** Encrypted Client Hello (RFC draft `tls-esni`) wraps the inner ClientHello — including SNI — in an AEAD-encrypted envelope keyed to a public key the server publishes in a DNS HTTPS record. The outer ClientHello carries only the DNS name of the ECH-capable frontend (e.g., `cloudflare-ech.com`), not the real backend. An ISP-level observer would see only the frontend name, not `signal.org`. ECH adoption is still rare in 2026 for three reasons: it requires the authoritative DNS zone to publish ECH keys (a new DNS record type), it requires the CDN or server operator to support ECH in their TLS stack, and middleboxes that perform TLS inspection break when they cannot parse the outer ClientHello. Most enterprise networks and a significant fraction of residential ISP infrastructure terminate ECH connections silently rather than pass them through, creating a strong incentive for servers to disable ECH to avoid connectivity failures.

---

### 3. DNS Query — Plaintext UDP and DNS-over-HTTPS

**Plaintext DNS (UDP port 53)**

```c
/* DNS Message Header — 12 bytes fixed */
struct dns_header {
    uint16_t  id;                /* Transaction ID — random per query     */
    uint16_t  flags;             /* QR|Opcode|AA|TC|RD|RA|Z|RCODE         */
    uint16_t  qdcount;           /* Number of questions                   */
    uint16_t  ancount;           /* Number of answers (0 in query)        */
    uint16_t  nscount;           /* Number of authority records           */
    uint16_t  arcount;           /* Number of additional records          */
};

/* DNS Question Section */
struct dns_question {
    /* QNAME: sequence of length-prefixed labels, terminated by 0x00 */
    uint8_t   label_len;         /* Length of next label                  */
    uint8_t   label[];           /* Label bytes (e.g. "signal", "org")    */
    /* ... repeated for each label ... */
    uint8_t   terminator;        /* 0x00 — root label                     */
    uint16_t  qtype;             /* 0x0001 = A record                     */
    uint16_t  qclass;            /* 0x0001 = IN (Internet)                */
};
```

```hexdump
Offset  Hex                                      Decoded
------  -------                                  --------------------------------
--- UDP payload (DNS message) ---
--- Header (12 bytes) ---
0x00    A3 F2                                    id: 0xA3F2 (transaction ID)
0x02    01 00                                    flags: 0x0100 = standard query, RD set
0x04    00 01                                    qdcount: 1 question
0x06    00 00                                    ancount: 0
0x08    00 00                                    nscount: 0
0x0A    00 00                                    arcount: 0

--- Question Section ---
0x0C    06                                       label_len: 6
0x0D    73 69 67 6E 61 6C                        label: "signal"
0x13    03                                       label_len: 3
0x14    6F 72 67                                 label: "org"
0x17    00                                       terminator (root)
0x18    00 01                                    qtype:  0x0001 = A
0x1A    00 01                                    qclass: 0x0001 = IN
```

Total UDP payload: 28 bytes. The domain `signal.org` is visible in plaintext at offsets `0x0D`–`0x12` and `0x14`–`0x16`. The ISP's DNS resolver receives this query, logs the domain, the source IP, the transaction ID, and the timestamp. Most large ISPs retain these logs for 30–90 days.

**DNS-over-HTTPS (DoH)**

The same query sent via DoH to Cloudflare's resolver at `1.1.1.1`:[^6]

```
POST /dns-query HTTP/2
Host: 1.1.1.1
Accept: application/dns-message
Content-Type: application/dns-message
Content-Length: 28

[binary DNS message, base64url representation:]
o/IBAAABAAAAAAAGC3NpZ25hbANvcmcAAAEAAQ==
```

The HTTP/2 stream is encrypted inside a TLS session to `1.1.1.1`. The DNS query content — `signal.org` — is hidden from the ISP.

**What the ISP still sees with DoH:**
- A TLS connection to `1.1.1.1` port 443, identifiable as Cloudflare's resolver by IP. The ISP knows encrypted DNS queries are occurring.
- Packet sizes and timing. A 28-byte DNS query wrapped in HTTP/2 and TLS has a characteristic size envelope.
- The subsequent connection. After the DoH response resolves `signal.org` to an IP, the device opens a TLS connection to that IP. The ISP sees the destination IP, and passive DNS correlation maps it back to `signal.org` with high confidence.
- SNI on the DoH connection itself. The TLS ClientHello to `1.1.1.1` carries SNI `1.1.1.1` (or `cloudflare-dns.com` depending on client configuration) — not the queried domain, but a clear signal that the client uses DoH.

**What is hidden:** The query content — the specific domain — is not visible to the ISP. The ISP cannot log `signal.org` from DNS. They must instead infer the destination from the IP addresses the device subsequently contacts, which is less precise for IPs serving many domains behind a CDN.

---

### 4. WireGuard Handshake Initiation

WireGuard's handshake initiation message has a fixed, invariant structure: always 148 bytes, always over UDP, always initiated by the client. This determinism makes it trivially detectable by DPI systems without decryption.

```c
/* WireGuard Handshake Initiation — 148 bytes total */
struct wg_handshake_initiation {
    uint32_t  message_type;          /* 0x00000001 — always 1             */
    uint32_t  sender_index;          /* Randomly chosen by initiator      */
    uint8_t   unencrypted_ephemeral[32]; /* Initiator ephemeral public key */
    uint8_t   encrypted_static[48];  /* Encrypted initiator static key    */
                                     /* 32 bytes key + 16 bytes AEAD tag  */
    uint8_t   encrypted_timestamp[28]; /* Encrypted TAI64N timestamp      */
                                     /* 12 bytes timestamp + 16 bytes tag */
    uint8_t   mac1[16];              /* MAC over message using responder   */
                                     /* static public key hash            */
    uint8_t   mac2[16];              /* MAC used for cookie mechanism      */
};
/* Total: 4 + 4 + 32 + 48 + 28 + 16 + 16 = 148 bytes */
```

A DPI system identifying WireGuard applies a single rule: UDP payload of exactly 148 bytes where the first 4 bytes are `01 00 00 00`. No decryption is required. The payload is completely opaque — the ephemeral key, encrypted static key, and encrypted timestamp are cryptographically random-looking — but the size fingerprint and type field are deterministic. Commercial DPI products including Sandvine PacketLogic and Palo Alto NGFW identify WireGuard with >99% precision using this rule alone.

WireGuard data packets are equally distinctive: the first 4 bytes are `04 00 00 00` (type 4), and payload sizes are constrained by WireGuard's AEAD overhead (16 bytes of Poly1305 authentication tag per packet). Traffic analysis of UDP flows with these characteristics identifies WireGuard even when the handshake is not captured.

**OpenVPN comparison.** OpenVPN over UDP uses a fundamentally different initiation pattern. The first byte of each packet is the opcode byte encoding the packet type and key ID. An OpenVPN TLS Client Hello packet begins with:

```hexdump
Offset  Hex        Decoded
------  -------    --------------------------------
0x00    38         opcode: 0x38 = P_CONTROL_HARD_RESET_CLIENT_V2 | key_id 0
0x01    [4 bytes]  session ID (randomly chosen)
0x05    00         hmac_size: 0 (no HMAC in this mode)
0x06    00 00 00 00 00 00 00 00  packet ID (8 bytes for reliable channel)
0x0E    [TLS ClientHello follows — including plaintext SNI if present]
```

The OpenVPN opcode byte `0x38` (or `0x28` for some configurations) is a reliable DPI signature. The subsequent TLS ClientHello is identifiable by content type `0x16`. Tools like nDPI, Suricata, and Snort identify OpenVPN from the opcode byte alone in a single packet. ISPs enforcing VPN blocking or traffic shaping target both signatures independently.

WireGuard's steganographic weakness is that it has no obfuscation layer. Its designers explicitly deprioritized traffic obfuscation in favor of simplicity and performance. Users requiring DPI resistance must wrap WireGuard in an obfuscation transport (e.g., Shadowsocks, obfs4, or MASQUE over HTTPS) at the cost of increased latency and complexity.

---

### 5. RADIUS Access-Request (Enterprise Wi-Fi)

When a device authenticates to a WPA2-Enterprise or WPA3-Enterprise Wi-Fi network, the access point forwards the authentication event to a RADIUS server. The RADIUS Access-Request packet permanently records the device's real MAC address and the exact access point it authenticated to, identified by BSSID and SSID. This record is created before any user-level activity occurs.

```c
/* RADIUS Packet Header */
struct radius_header {
    uint8_t   code;              /* 1 = Access-Request                    */
    uint8_t   identifier;        /* Request/response matching (0–255)     */
    uint16_t  length;            /* Total packet length including header  */
    uint8_t   authenticator[16]; /* Random 16-byte value in Access-Request*/
};

/* RADIUS Attribute (TLV format) */
struct radius_attribute {
    uint8_t   type;              /* Attribute type number                 */
    uint8_t   length;            /* Total length including type+length    */
    uint8_t   value[];           /* Attribute-specific value              */
};

/*
 * Relevant attribute types:
 *   1  User-Name            — EAP identity / username
 *   4  NAS-IP-Address       — IP address of the access point or NAS
 *   5  NAS-Port             — Physical or logical port number
 *  30  Called-Station-Id    — AP BSSID + SSID: "AA:BB:CC:DD:EE:FF:ssid-name"
 *  31  Calling-Station-Id   — Client MAC address: "AA:BB:CC:DD:EE:FF"
 *  32  NAS-Identifier       — Hostname or identifier of the NAS
 *  79  EAP-Message          — Encapsulated EAP packet
 */
```

```hexdump
Offset  Hex                                      Decoded
------  -------                                  --------------------------------
--- RADIUS Header ---
0x00    01                                       code: 1 (Access-Request)
0x01    4A                                       identifier: 0x4A
0x02    00 7C                                    length: 124 bytes total
0x04    D3 A2 1F 8B 6C 04 E7 33                  authenticator (16 bytes random)
        B9 5A 20 C1 74 8D F2 0E

--- Attribute: User-Name (type 1) ---
0x14    01                                       type: 1 (User-Name)
0x15    0F                                       length: 15
0x16    6A 2E 73 6D 69 74 68 40                  value: "j.smith@corp.example.com"
        63 6F 72 70 2E 65 78 61
        6D 70 6C 65 2E 63 6F 6D

--- Attribute: NAS-IP-Address (type 4) ---
0x25    04                                       type: 4 (NAS-IP-Address)
0x26    06                                       length: 6
0x27    0A 0A 01 05                              value: 10.10.1.5 (AP management IP)

--- Attribute: NAS-Port (type 5) ---
0x2B    05                                       type: 5 (NAS-Port)
0x2C    06                                       length: 6
0x2D    00 00 00 01                              value: port 1

--- Attribute: Called-Station-Id (type 30) ---
0x33    1E                                       type: 30 (Called-Station-Id)
0x34    1D                                       length: 29
0x35    41 41 3A 42 42 3A 43 43  "AA:BB:CC:DD:EE:FF:CorpWiFi-3F-North"
        3A 44 44 3A 45 45 3A 46
        46 3A 43 6F 72 70 57 69
        46 69 2D 33 46 2D 4E 6F
        72 74 68

--- Attribute: Calling-Station-Id (type 31) ---
0x52    1F                                       type: 31 (Calling-Station-Id)
0x53    13                                       length: 19
0x54    41 41 3A 42 42 3A 43 43  "AA:BB:CC:DD:EE:FF"  <-- CLIENT MAC ADDRESS
        3A 44 44 3A 45 45 3A 46
        46

--- Attribute: NAS-Identifier (type 32) ---
0x67    20                                       type: 32 (NAS-Identifier)
0x68    0C                                       length: 12
0x69    41 50 2D 33 46 2D 4E 30  "AP-3F-N01"
        30 31

--- Attribute: EAP-Message (type 79) ---
0x75    4F                                       type: 79 (EAP-Message)
0x76    06                                       length: 6
0x77    02 4A 00 04 01           EAP Response/Identity encapsulated
```

Two attributes carry forensic significance that exceeds anything in the data plane.

**Called-Station-Id (type 30)** encodes both the AP's BSSID (`AA:BB:CC:DD:EE:FF`) and the SSID (`CorpWiFi-3F-North`) as a colon-delimited string. The BSSID is a globally unique hardware address assigned to the radio. In enterprise deployments, the NAS-Identifier and BSSID map to a specific physical access point with a known location: `AP-3F-N01` means third floor, north wing, AP number one. The RADIUS log entry therefore contains not just that the device authenticated, but precisely where the device was physically located at the moment of authentication.

**Calling-Station-Id (type 31)** contains the client's MAC address — the hardware address of the wireless network interface as seen by the AP. In enterprise environments, MAC randomization is frequently disabled by MDM policy. Even on consumer devices, MAC randomization applies only to probe requests and initial association frames on iOS 14+ and Android 10+ — the MAC presented during EAP authentication to a saved network is the real hardware MAC on most implementations prior to 2024.[^7] That address is logged permanently on the RADIUS server and is not rotated.

The combined forensic record from a single authentication event: `j.smith@corp.example.com` authenticated from device with MAC `AA:BB:CC:DD:EE:FF` at access point `AP-3F-N01` (third floor, north wing) at timestamp T. If the same MAC address appears in hotel Wi-Fi logs, coffee shop captive portal logs, or conference network logs, those records can be correlated across time and location to reconstruct movement history — without any cellular carrier involvement, without any GPS data, and without decrypting a single byte of application traffic.

---

[^1]: *Carpenter v. United States*, 585 U.S. 296 (2018). The Supreme Court held that the government's acquisition of seven or more days of historical cell-site location information constitutes a Fourth Amendment search requiring a warrant.

[^2]: B. Claise, Ed., "Specification of the IP Flow Information Export (IPFIX) Protocol for the Exchange of Flow Information," RFC 7011, IETF, September 2013. Defines the IPFIX wire format including flow record fields (source/dest IP, ports, protocol, byte count, timestamps). Available at https://www.rfc-editor.org/rfc/rfc7011.

[^3]: D. Benjamin et al., "The Transport Layer Security (TLS) Protocol Version 1.3," RFC 8446, IETF, August 2018, §4.4.2 (server_name extension / SNI). Specifies that the SNI extension is transmitted in the ClientHello before the encrypted handshake is established. Available at https://www.rfc-editor.org/rfc/rfc8446.

[^4]: *United States v. Seitu Sulayman Kokayi*, Case No. 1:16-cr-00265 (E.D. Va. 2016). DOJ court filing documents that IPVanish provided connection logs — including subscriber IP address and connection timestamps — to Homeland Security Investigations despite the company's public "zero logs" marketing claims.

[^5]: *United States v. Ryan Lin*, Case No. 1:17-cr-10305 (D. Mass. 2017). DOJ press release and court documents confirm PureVPN cooperated with the FBI by providing subscriber activity logs used to identify and locate the defendant, despite PureVPN's public claim to maintain no logs of user activity.

[^6]: P. Hoffman and P. McManus, "DNS Queries over HTTPS (DoH)," RFC 8484, IETF, October 2018. Defines the DNS-over-HTTPS protocol, including the `application/dns-message` content type and POST request format used to tunnel DNS queries inside encrypted HTTP/2 sessions. Available at https://www.rfc-editor.org/rfc/rfc8484.

[^7]: Jeremy Martin, Travis Mayberry, Collin Donahue, Lucas Foppe, Lamont Brown, Chadwick Henning, Elizabeth Rye, and Dane Brown, "A Study of MAC Address Randomization in Mobile Devices and When it Fails," *Proceedings on Privacy Enhancing Technologies* (PoPETs), 2017(4):365–383. Documents that MAC randomization does not apply to EAP authentication frames in most pre-2024 mobile implementations, allowing enterprise RADIUS logs to capture the real hardware MAC.
