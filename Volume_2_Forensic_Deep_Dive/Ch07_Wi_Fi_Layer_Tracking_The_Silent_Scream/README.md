# Chapter 7: Wi-Fi Layer Tracking — The Silent Scream

## Introduction

Removing the cellular modem from a private phone eliminates the entire attack surface of baseband tracking, IMSI collection, and tower triangulation. This is a significant improvement. However, Wi-Fi is not a safe harbor — it simply shifts the tracking vector from cellular protocols to 802.11 management frames and ISP metadata. A device without a cellular modem still screams identifying information into the air every moment it is powered on.

The assumption that "no cellular means no tracking" is false. Wi-Fi has its own equivalent of IMSI and cell tower tracking: MAC addresses, probe requests, and BSSID geolocation databases. These mechanisms are often less understood than their cellular counterparts, but they are equally powerful in forensic contexts.

## Probe Requests: The Shout Before Connection

Before your phone connects to any Wi-Fi network, it broadcasts probe requests to discover available networks. These are management frames in the 802.11 protocol suite,[^1] and they are transmitted even when Wi-Fi scanning appears to be off, unless the radio is fully disabled at the kernel level.

### Source MAC Address

The source MAC address in a probe request is the permanent hardware identifier of your Wi-Fi chipset. It is the Wi-Fi equivalent of an IMEI — globally unique and, under normal operation, unchanging. The first three bytes (the OUI, or Organizationally Unique Identifier) reveal the manufacturer of the chipset: for example, a Google Pixel 6, a Broadcom chip in a Samsung device, or an Intel chip in a laptop. Without MAC randomization, this address is a persistent tracker that follows you across every network you encounter.

### SSID Probe List

Your phone does not just broadcast its own MAC address. It also shouts the names of every Wi-Fi network it remembers. This list of probed SSIDs is a behavioral fingerprint that leaks your routine, your home network name, your workplace, your favorite coffee shop, and your gym. An adversary with a Wi-Fi sniffer in monitor mode can capture these probes from a distance of several hundred feet using a directional antenna.

The forensic attack proceeds as follows: an adversary places a Wi-Fi sniffer (running Wireshark with a monitor-mode adapter) near a location of interest — your home, your workplace, or a protest. They observe probe requests from a specific MAC address that include the SSID "HomeNetwork." Now they know your phone's hardware identifier, its manufacturer, and that its owner lives near the sniffer's location.

### Supported Rates and Capabilities

Probe requests also include the supported data rates and Wi-Fi standards your device supports — for example, 802.11ax (Wi-Fi 6) or 802.11ac (Wi-Fi 5).[^1] This enables device fingerprinting. Combined with the OUI, it narrows the device model.

### MAC Address Randomization and Its Failures

Modern operating systems implement MAC address randomization to prevent this tracking. However, the implementation is inconsistent and often ineffective. Many implementations randomize only the probe request source address but use the real MAC address during association — meaning the randomization is bypassed the moment the device connects to a network.[^2] Some implementations randomize only when the screen is off or only for specific SSID types. Some operating systems include the real MAC address in the randomized probe request as an information element, negating the randomization entirely. And even when randomization works correctly at the OS level, the Wi-Fi chipset firmware may have its own scanning behavior that leaks the real address.[^3]

The forensic takeaway is that MAC randomization is a mitigation, not a solution. It raises the cost of tracking but does not eliminate it, particularly against a determined adversary with multiple observation points.

### Active versus Passive Wi-Fi Tracking

Wi-Fi tracking can be divided into two broad categories: active and passive. Active tracking involves the adversary transmitting signals to solicit responses from target devices. This includes sending probe request frames to specific MAC addresses, deauthentication attacks that force devices to reconnect and reveal themselves, and directed probe requests that elicit responses from devices that know a particular SSID. Active tracking is generally detectable because the adversary must transmit, but it is also more reliable — the adversary controls when and how the interrogation occurs.

Passive tracking involves only listening. The adversary deploys one or more monitoring stations that capture all 802.11 management frames within range.[^1] Because passive tracking does not involve any transmission, it is inherently undetectable. The device being tracked has no indication that its probe requests, association frames, and data packets are being logged. A network of passive monitors across a city can track a device's movement without the device ever knowing it is under observation. This is the same principle as CCTV camera networks, but applied to radio-frequency identifiers rather than visual ones.

The forensic implication is that the detection of Wi-Fi tracking is asymmetrically difficult. Passive tracking leaves no trace on the target device. The target cannot determine whether they are being tracked by Wi-Fi sniffers unless they physically locate the monitoring equipment.

## The 802.11 Protocol Layers in Forensic Detail

### Beacon Frames

Access points periodically broadcast beacon frames announcing their presence. These frames contain the BSSID, SSID, supported rates, capabilities information, and timestamp.[^1] From a forensic perspective, beacon frames are relevant because they populate the device's scanned BSSID list. A forensic examiner who extracts the scanned BSSID list from a device learns which access points the device has been near.

### Deauthentication and Disassociation Frames

Management frames for deauthentication and disassociation are typically unencrypted in 802.11.[^1] An adversary can forge these frames to disconnect a device from its access point. When the device attempts to reconnect, it broadcasts probe requests and transmits association frames — both of which reveal its identity. This is a common active tracking technique used by Wi-Fi forensic tools.

### Power Save Mode Behavior

When a device enters power save mode, it signals this to the access point. The access point buffers incoming data and periodically transmits a Traffic Indication Map (TIM) in the beacon frame. The device wakes up, receives the TIM, and sends a Power Save Poll to retrieve buffered data.[^1] Each wake-and-poll cycle creates observable timing patterns that can fingerprint the device and reveal communication activity.

## Enterprise Wi-Fi Tracking

Enterprise Wi-Fi deployments add additional tracking capabilities. When a device connects to a WPA2-Enterprise or WPA3-Enterprise network using 802.1X authentication, the device presents digital certificates or credentials. The RADIUS server logs the authentication attempt with the device's MAC address, identity, and timestamp. Many enterprise Wi-Fi controllers also maintain location tracking databases that calculate device position based on signal strength measurements from multiple access points.

The forensic extraction of these logs — either through a subpoena to the enterprise or through legal process against the organization — provides a precise record of device location within the enterprise environment, down to room-level accuracy in well-calibrated deployments.

## Bluetooth as a Parallel Tracking Vector

Bluetooth Low Energy beacons follow many of the same principles as Wi-Fi probe requests. BLE devices regularly transmit advertisement packets containing their MAC address and, in many cases, a unique device identifier or service UUID. These advertisements are captured by any BLE-enabled device within range.

Apple's Find My network uses this mechanism: iPhones transmit rotating public keys via BLE, and any nearby Apple device relays the signal. Google's Nearby network works similarly. Even on de-Googled Android devices, the BLE chipset firmware may broadcast advertisements that cannot be disabled through OS-level settings.

## Association Frames: The Handshake to Your Router

When your phone connects to a Wi-Fi network, it exchanges association frames with the access point. These frames are rich with forensic data.

### Association Request

The association request frame includes your MAC address (real, not randomized, in most implementations),[^2] supported data rates, capabilities information, and the BSSID (MAC address) of the router you are connecting to. This ties your device to a specific access point at a specific timestamp.

### The 4-Way Handshake (EAPOL)

In WPA2 and WPA3 personal networks, authentication uses a 4-way handshake transmitted in EAPOL frames.[^1] The handshake exposes the PMKID (Pairwise Master Key Identifier). If the network password is weak, the PMKID can be brute-forced offline. Once the password is recovered, the adversary can decrypt all previously captured traffic from that session retroactively — even if WPA2 encryption was in use.

### Forensic Router Logs

If law enforcement seizes your router (or a neighbor's compromised router), they can extract logs showing your MAC address connected from a specific start time to end time on specific dates. Many consumer routers retain these logs for weeks or months, and forensic imaging tools like Cellebrite UFED can recover them even after deletion.

## DHCP Traffic: The "I Am Here" Announcement

Once connected and authenticated, your phone requests an IP address via DHCP (Dynamic Host Configuration Protocol). The DHCP exchange leaks information that directly ties the device to your identity.

### DHCP Client Identifier and Hostname

The DHCP Client Identifier field often includes or is identical to the device hostname. Default hostnames like `Android-Pixel-6`, `iPhone12-Pro`, or `Samsung-Galaxy` reveal the exact device model. If the user has set a custom hostname, it may include their real name or other identifying information.

### Vendor Class ID

The Vendor Class ID tells the router exactly what operating system and version is requesting the IP. A typical string might be `dhcpcd-6.8.2:Android-13`. This enables precise device fingerprinting and OS version identification.

### Requested IP and MAC Correlation

The DHCP exchange ties your MAC address to a specific IP address on the local network. The ISP's upstream logs then tie that IP address to your residential account — your name, your billing address, your phone number. The correlation path is: MAC address → local IP → public IP (via NAT) → subscriber account. This is the mechanism by which Wi-Fi-only compartmentalization collapses.

## Wi-Fi Scanning Even When "Off"

One of the most persistent forensic vulnerabilities is that Wi-Fi chipsets continue to scan for access points even when the Wi-Fi radio appears to be off in the operating system settings. This occurs through two mechanisms.

First, the OS itself may maintain "Wi-Fi scanning" as a separate background service, distinct from "Wi-Fi connectivity." On stock Android, Google Location Services uses Wi-Fi scanning for location even when Wi-Fi is "off." On de-Googled operating systems like GrapheneOS, this toggle is respected — but not all custom OSes implement this correctly.

Second, the Wi-Fi chipset firmware has its own scanning behavior that operates independently of the operating system. Qualcomm, Broadcom, and MediaTek chipsets have been demonstrated to perform autonomous scans that are invisible to the OS.[^3] These firmware-level scans can be observed by an external sniffer and can leak MAC addresses and probe requests that the OS believes are not being transmitted.

The forensic implication is that physical presence near a Wi-Fi sniffer is detectable even if the user has deliberately disabled Wi-Fi in the OS settings, unless the device is in a Faraday bag.

## Wi-Fi Geolocation Databases

This is one of the most underappreciated tracking vectors in mobile forensics. Companies maintain massive databases that map Wi-Fi BSSIDs (access point MAC addresses) and Bluetooth MAC addresses to precise GPS coordinates.

### Major Database Operators

Google Location Services is populated by every Android device with Google Play Services installed. Each device scans for nearby Wi-Fi networks and Bluetooth beacons, records the BSSIDs, tags them with its own GPS location, and reports the mapping to Google's servers. Apple Location Service does the same with every iPhone. Skyhook Wireless (now part of Loc-Aid) populates its database through OEM agreements with Samsung, LG, and other manufacturers. Mozilla Location Service was crowdsourced via Firefox mobile users. HERE Location Suite (formerly Nokia) aggregates data from automotive and mobile OEMs.

### Forensic Attack Without GPS

An investigator does not need to access your phone's GPS to know where it has been. The attack proceeds in three steps. First, the investigator captures your phone's Wi-Fi scan results — either via a forensic tool that extracts the Wi-Fi scan cache from the device, or by capturing probe requests and association frames from your phone over the air. Second, they extract the BSSIDs of the access points your phone detected. Third, they query a geolocation API (such as Google's Geolocation API, which is publicly accessible with an API key) with those BSSIDs. The API returns the estimated GPS coordinates of those access points, typically with 10 to 20 meter accuracy.

The result is that the investigator knows where your phone was, at what time, without ever accessing your phone's GPS, without a warrant for your phone, and without any cooperation from your carrier.

### The Reverse Attack

Even more troubling is the passive variant. You walk past a coffee shop. Your phone passively scans and detects the coffee shop's Wi-Fi access point. The BSSID of that access point is in Google's database, mapped to a precise GPS coordinate. Later, an adversary with a Wi-Fi sniffer captures your phone's probe requests or association frames. By extracting the BSSIDs your phone remembers or detects, they can reconstruct a timeline of locations you have visited.

### Mitigation

Disabling "Wi-Fi scanning" and "Bluetooth scanning" in location settings is the first step. On custom operating systems, verifying that these toggles actually disable the radio — via `adb shell dumpsys` or similar — is essential. MAC randomization should be enabled and verified. However, even with all mitigations in place, passing within range of any public access point that is in a geolocation database leaves a traceable record of your presence.

## Protocol Deep Dive: Frame Structures and Wire Format

This section details the exact on-wire layout of the frames discussed throughout this chapter. Understanding the binary format is prerequisite to both capture analysis and to evaluating whether any given mitigation actually eliminates the leak at the byte level.

---

### 1. 802.11 Probe Request Frame

The probe request is transmitted by a client into open air before any association occurs. It is a management frame with subtype 0x04.[^1] The Frame Control field encodes this subtype in bits 4–7 of the first octet. Every byte from the source MAC field onward is readable by any adapter in monitor mode — there is no encryption at this stage.

```c
/* 802.11 Probe Request — fixed fields (24 bytes) */
struct ieee80211_probe_req_fixed {
    uint16_t frame_control;     /* 0x0040 = version 0, type Management (00),
                                   subtype Probe Request (0100) */
    uint16_t duration;          /* 0x0000 — no NAV reservation needed */
    uint8_t  da[6];             /* FF:FF:FF:FF:FF:FF — broadcast destination */
    uint8_t  sa[6];             /* Source MAC — device hardware address
                                   (or randomized addr if OS has intervened) */
    uint8_t  bssid[6];         /* FF:FF:FF:FF:FF:FF — wildcard BSSID */
    uint16_t seq_ctrl;          /* Sequence number | fragment number */
} __attribute__((packed));

/* Tagged parameters follow immediately after fixed fields */
struct ieee80211_tagged_param {
    uint8_t  tag_number;
    uint8_t  tag_length;
    uint8_t  value[];           /* variable length */
} __attribute__((packed));

/*
 * Tags present in a typical probe request:
 *   Tag  0  — SSID (empty for wildcard probe, or specific SSID name)
 *   Tag  1  — Supported Rates (e.g. 1, 2, 5.5, 11, 6, 9, 12, 18 Mbps)
 *   Tag 50  — Extended Supported Rates (24, 36, 48, 54 Mbps)
 *   Tag 45  — HT Capabilities (802.11n MIMO, channel width, MCS set)
 *   Tag 127 — Extended Capabilities (BSS Transition, Interworking, etc.)
 *   Tag 107 — Interworking (Hotspot 2.0 access network type)
 */
```

Annotated hexdump — probe request from a Pixel 6 (Broadcom BCM4389) before randomization was confirmed active. Captured on channel 6, 2.4 GHz, via `airmon-ng` on a ALFA AWUS036ACH adapter.

```hexdump
Offset  Hex bytes                                         ASCII / annotation
------  ------------------------------------------------  ------------------
0000    40 00                                             Frame Control: 0x0040
                                                          Type=Management, Subtype=Probe Req
0002    00 00                                             Duration: 0
0004    ff ff ff ff ff ff                                 DA: broadcast
000a    28 cd c1 0a 4f 2e                                 SA: 28:CD:C1:0A:4F:2E
                                                          OUI 28:CD:C1 = Google LLC
                                                          (Broadcom BCM4389, Pixel 6)
0010    ff ff ff ff ff ff                                 BSSID: wildcard
0016    b0 1c                                             Seq Ctrl: seq=0x1cb, frag=0
        -- Tagged Parameters --
0018    00 0b 48 6f 6d 65 4e 65 74 77 6f 72 6b           Tag 0 (SSID), len=11: "HomeNetwork"
0025    01 08 82 84 8b 96 0c 12 18 24                     Tag 1 (Supported Rates), len=8
                                                          Rates: 1,2,5.5,11,6,9,12,18 Mbps
002f    32 04 30 48 60 6c                                 Tag 50 (Ext Rates), len=4
                                                          Rates: 24,36,48,54 Mbps
0035    2d 1a ...                                         Tag 45 (HT Capabilities), len=26
                                                          MIMO streams, short GI, MCS set
004f    7f 08 ...                                         Tag 127 (Ext Capabilities), len=8
                                                          BSS Transition, Interworking
0059    6b 05 ...                                         Tag 107 (Interworking), len=5
                                                          Access Network Type, Hotspot 2.0
```

Forensic significance of each tagged parameter:

- **Tag 0 (SSID):** A non-empty SSID in a directed probe request names a network the device remembers. Each remembered SSID is a historical data point — past home, past employer, past travel accommodation. An empty SSID is a wildcard probe; devices often alternate between directed and wildcard probes, leaking the remembered network list over time.
- **Tag 1 / Tag 50 (Supported Rates):** The specific rate set — particularly the combination of legacy, HT, and VHT rates — narrows the chipset generation to within a few hardware revisions. Combined with the OUI, this is often sufficient to identify the device model without any other metadata.
- **Tag 45 (HT Capabilities):** The MCS (Modulation and Coding Scheme) bitmap, spatial stream count, and short guard interval flag are chipset-specific. Broadcom BCM4389 has a distinct HT capability signature that differs from a Qualcomm WCN6856 even when both use MAC randomization correctly.[^3]
- **Tag 127 (Extended Capabilities):** The BSS Transition Management bit reveals whether the device supports 802.11v roaming. The Interworking bit reveals Hotspot 2.0 (Passpoint) support. These bits are set by firmware and do not change across sessions — they contribute to a stable behavioral fingerprint even when MAC and SSID information is suppressed.
- **Tag 107 (Interworking):** Encodes the access network type the device prefers for Hotspot 2.0 negotiation. Devices that have ever connected to a carrier Wi-Fi offload network (T-Mobile Wi-Fi Calling, AT&T Wi-Fi, eduroam) will advertise specific Interworking parameters that link the device to a carrier relationship.

---

### 2. 802.11 Association Request Frame

The association request is transmitted after the probe-and-response exchange succeeds and the device has decided to join a specific AP. At this stage, in the vast majority of implementations, the device transmits its **real hardware MAC address** in the SA field — the MAC randomization used during probing is discarded.[^2] This is the structural link that collapses probe-phase anonymity: a passive observer who captures both the randomized probe and the de-randomized association frame can correlate them by sequence number continuity and timing.

```c
/* 802.11 Association Request — fixed fields (28 bytes) */
struct ieee80211_assoc_req_fixed {
    uint16_t frame_control;     /* 0x0000 = Management, subtype Assoc Req (0000) */
    uint16_t duration;
    uint8_t  da[6];             /* AP MAC address (BSSID of the target AP) */
    uint8_t  sa[6];             /* REAL device MAC — randomization ends here */
    uint8_t  bssid[6];         /* Same as DA for infrastructure mode */
    uint16_t seq_ctrl;
    uint16_t capability_info;   /* Capability bitmap:
                                     bit 0  — ESS (infrastructure mode)
                                     bit 4  — Privacy (WPA/WPA2 in use)
                                     bit 5  — Short Preamble
                                     bit 10 — Short Slot Time
                                     bit 12 — DSSS-OFDM */
    uint16_t listen_interval;   /* How many beacon intervals to sleep */
} __attribute__((packed));

/*
 * Tagged parameters in Association Request:
 *   Tag  0  — SSID (the specific network being joined — plaintext)
 *   Tag  1  — Supported Rates
 *   Tag 50  — Extended Supported Rates
 *   Tag 48  — RSN Information Element (WPA2/WPA3 cipher suites, AKM)
 *             Contains: RSN version, Group Cipher Suite, Pairwise Cipher
 *             Suite List, AKM Suite List, RSN Capabilities, PMKID List
 */

struct ieee80211_rsn_ie {
    uint8_t  tag;               /* 0x30 = tag 48 */
    uint8_t  length;
    uint16_t rsn_version;       /* 0x0001 */
    uint8_t  group_cipher[4];   /* e.g. 00:0F:AC:04 = CCMP-128 */
    uint16_t pairwise_count;
    uint8_t  pairwise_cipher[4]; /* 00:0F:AC:04 = CCMP-128 */
    uint16_t akm_count;
    uint8_t  akm_suite[4];      /* 00:0F:AC:02 = PSK, 00:0F:AC:08 = SAE */
    uint16_t rsn_capabilities;
    uint16_t pmkid_count;
    uint8_t  pmkid[16];         /* PMKID if performing fast BSS transition */
} __attribute__((packed));
```

```hexdump
Offset  Hex bytes                                         Annotation
------  ------------------------------------------------  ------------------
0000    00 00                                             Frame Control: Assoc Req
0002    3a 01                                             Duration
0004    a4 c3 f0 88 21 09                                 DA: AP MAC a4:c3:f0:88:21:09
000a    28 cd c1 0a 4f 2e                                 SA: 28:CD:C1:0A:4F:2E
                                                          REAL hardware MAC — same OUI
                                                          as the probe, randomization gone
0010    a4 c3 f0 88 21 09                                 BSSID: same as DA
0016    c0 17                                             Seq Ctrl
0018    31 04                                             Capability Info: 0x0431
                                                          ESS=1, Privacy=1, ShortPreamble=1
                                                          ShortSlotTime=1
001a    0a 00                                             Listen Interval: 10 beacons
        -- Tagged Parameters --
001c    00 0b 48 6f 6d 65 4e 65 74 77 6f 72 6b           Tag 0 (SSID): "HomeNetwork"
0029    01 08 82 84 8b 96 0c 12 18 24                     Tag 1 (Supported Rates)
0033    32 04 30 48 60 6c                                 Tag 50 (Ext Supported Rates)
0039    30 14                                             Tag 48 (RSN IE), len=20
003b    01 00                                             RSN Version: 1
003d    00 0f ac 04                                       Group Cipher: CCMP-128
0041    01 00                                             Pairwise Count: 1
0043    00 0f ac 04                                       Pairwise: CCMP-128
0047    01 00                                             AKM Count: 1
0049    00 0f ac 02                                       AKM: PSK (WPA2-Personal)
004d    00 00                                             RSN Capabilities
004f    00 00                                             PMKID Count: 0
```

The Capability Information field is forensically relevant because it is a fixed function of firmware and driver — `0x0431` on a Pixel 6 running Android 13 with the stock Wi-Fi driver. This value is consistent across sessions and does not change with MAC randomization, providing a stable session-linking fingerprint independent of the address fields.

---

### 3. EAPOL 4-Way Handshake

The EAPOL 4-way handshake executes immediately after 802.11 association, before any data traffic is permitted.[^1] It is carried inside Ethernet frames (EtherType 0x888E) and is visible in full to any passive observer on the same broadcast medium. The first two messages are forensically sufficient for offline attack.

```c
/* Ethernet header encapsulating EAPOL */
struct eth_header {
    uint8_t  dst[6];            /* AP MAC for msg1, client MAC for msg2 */
    uint8_t  src[6];            /* Source of this message */
    uint16_t ethertype;         /* 0x888E — EAPOL */
} __attribute__((packed));

/* EAPOL header */
struct eapol_header {
    uint8_t  version;           /* 0x02 = EAPOL-2004 */
    uint8_t  type;              /* 0x03 = Key */
    uint16_t length;            /* Length of body that follows */
} __attribute__((packed));

/* EAPOL Key frame (RSN Key Descriptor, 802.11-2020 Table 12-7) */
struct eapol_key {
    uint8_t  descriptor_type;   /* 0x02 = RSN */
    uint16_t key_info;          /* Bitmap:
                                     bits 0-2:  Key Descriptor Version (2=AES)
                                     bit  3:    Key Type (1=Pairwise, 0=Group)
                                     bit  6:    Install
                                     bit  7:    Key ACK (set by AP in msg 1 & 3)
                                     bit  8:    Key MIC (set when MIC is present)
                                     bit  9:    Secure (set in msg 3 & 4)
                                     bit  10:   Error
                                     bit  11:   Request
                                     bit  12:   Encrypted Key Data */
    uint16_t key_length;        /* Length of temporal key — 16 for CCMP */
    uint64_t replay_counter;    /* Monotonic counter, matches msg1 to msg2 */
    uint8_t  nonce[32];         /* ANonce (AP random, msg1) / SNonce (STA, msg2) */
    uint8_t  key_iv[16];        /* Unused in WPA2 PSK — all zeros */
    uint8_t  key_rsc[8];        /* Receive Sequence Counter */
    uint8_t  reserved[8];
    uint8_t  mic[16];           /* HMAC-SHA1 or AES-CMAC over entire EAPOL frame;
                                   zero in msg1, computed in msg2 */
    uint16_t key_data_length;
    uint8_t  key_data[];        /* msg1: PMKID (16 bytes) wrapped in RSN IE
                                   msg2: SNonce + client RSN IE
                                   msg3: GTK encrypted with KEK
                                   msg4: empty */
} __attribute__((packed));
```

**PMKID location:** In message 1, the Key Data field contains an RSN IE (tag 48) with a PMKID List of exactly one entry. The PMKID is computed as:

```
PMKID = HMAC-SHA1-128(PMK, "PMK Name" || AP_MAC || Client_MAC)
```

Because the PMK is derived from the passphrase via PBKDF2-SHA1, and because all inputs (PMKID, AP MAC, client MAC) are captured in message 1, an attacker can test candidate passphrases entirely offline without completing the handshake — this is the `hcxdumptool`/`hashcat` -m 22000 attack that made traditional 4-way handshake capture optional.

Annotated hex — EAPOL Message 1 (AP to client):

```hexdump
Offset  Hex bytes                                         Annotation
------  ------------------------------------------------  ------------------
        [ Ethernet header ]
0000    28 cd c1 0a 4f 2e                                 DST: client real MAC
0006    a4 c3 f0 88 21 09                                 SRC: AP MAC
000c    88 8e                                             EtherType: EAPOL
        [ EAPOL header ]
000e    02                                                Version: EAPOL-2004
000f    03                                                Type: Key
0010    00 5f                                             Length: 95 bytes
        [ EAPOL Key descriptor ]
0012    02                                                Descriptor Type: RSN
0013    00 8a                                             Key Info: 0x008A
                                                          KeyDescVer=2 (AES-MIC)
                                                          KeyType=1 (Pairwise)
                                                          KeyACK=1 (AP sending)
                                                          KeyMIC=0 (no MIC yet)
0015    00 10                                             Key Length: 16 (AES-128)
0017    00 00 00 00 00 00 00 01                           Replay Counter: 1
001f    a3 7f 2c 91 e4 08 b1 d0                           ANonce (32 bytes):
        5c f3 44 a9 12 77 3b e8                           random per-session value
        20 1d 88 c4 f9 0a 63 11                           generated by AP
        9e 45 d2 87 b3 0f 1a c6
003f    00 00 00 00 00 00 00 00                           Key IV: all zeros
        00 00 00 00 00 00 00 00
004f    00 00 00 00 00 00 00 00                           RSC: all zeros
0057    00 00 00 00 00 00 00 00                           Reserved
005f    00 00 00 00 00 00 00 00                           MIC: all zeros (msg 1)
        00 00 00 00 00 00 00 00
006f    00 16                                             Key Data Length: 22
0071    30 14 01 00 00 0f ac 04                           RSN IE (tag 48)
        01 00 00 0f ac 04 01 00
        00 0f ac 02 00 00
        -- PMKID embedded in RSN IE --
007f    dd 16 00 0f ac 00                                 Vendor IE wrapping PMKID
0085    4a f3 91 c2 88 b1 07 3d                           PMKID (16 bytes)
        e4 55 12 9a 30 f7 aa c1                           HMAC-SHA1-128(PMK,"PMK Name"||APs||STAs)
                                                          Sufficient for hashcat -m 22000
```

---

### 4. DHCP Discover / Request

DHCP runs over UDP with the client sourcing from port 68 and the DHCP server listening on port 67. The entire exchange is broadcast in plaintext and is visible to any host on the local segment — including a rogue AP or a compromised device on the same network. The BOOTP fields and DHCP options together constitute a device identity card transmitted in the clear on every new network join.

```c
/* UDP header */
struct udp_header {
    uint16_t src_port;          /* 68 — DHCP client */
    uint16_t dst_port;          /* 67 — DHCP server */
    uint16_t length;
    uint16_t checksum;
} __attribute__((packed));

/* BOOTP / DHCP fixed fields */
struct bootp_header {
    uint8_t  op;                /* 1 = BOOTREQUEST (client to server) */
    uint8_t  htype;             /* 1 = Ethernet */
    uint8_t  hlen;              /* 6 = MAC address length */
    uint8_t  hops;              /* 0 for client */
    uint32_t xid;               /* Transaction ID — random per-session */
    uint16_t secs;              /* Seconds since lease started */
    uint16_t flags;             /* 0x8000 = broadcast flag */
    uint32_t ciaddr;            /* Client IP (0.0.0.0 in Discover) */
    uint32_t yiaddr;            /* Your IP (filled by server in Offer) */
    uint32_t siaddr;            /* Server IP */
    uint32_t giaddr;            /* Gateway/relay IP */
    uint8_t  chaddr[16];        /* Client hardware address — real MAC in bytes 0-5,
                                   zero-padded to 16 bytes; MAC randomization
                                   in Wi-Fi does NOT affect this field on
                                   most Android versions below 13 QPR2 */
    uint8_t  sname[64];         /* Server host name — usually empty */
    uint8_t  file[128];         /* Boot file — usually empty */
    uint32_t magic_cookie;      /* 0x63825363 — DHCP magic */
} __attribute__((packed));

/*
 * DHCP Options (variable length TLV, terminated by option 255)
 *   Option 53  — DHCP Message Type (1=Discover, 3=Request)
 *   Option 55  — Parameter Request List (list of option codes the client wants)
 *   Option 60  — Vendor Class Identifier (plaintext OS/version string)
 *   Option 12  — Host Name (device name — set by user or OS default)
 *   Option 61  — Client Identifier (type byte + hardware address)
 *   Option 255 — End
 */
struct dhcp_option {
    uint8_t  code;
    uint8_t  length;
    uint8_t  value[];
} __attribute__((packed));
```

Annotated hexdump — DHCP Discover from Android 13 device:

```hexdump
Offset  Hex bytes                                         Annotation
------  ------------------------------------------------  ------------------
        [ UDP header ]
0000    00 44 00 43 01 4c d3 8a                           src=68, dst=67, len=332
        [ BOOTP fixed fields ]
0008    01 01 06 00                                       op=REQUEST, htype=ETH, hlen=6
000c    3f a1 c8 12                                       xid: random transaction ID
0010    00 00 80 00                                       secs=0, flags=broadcast
0014    00 00 00 00                                       ciaddr: 0.0.0.0 (no IP yet)
0018    00 00 00 00                                       yiaddr
001c    00 00 00 00                                       siaddr
0020    00 00 00 00                                       giaddr
0024    28 cd c1 0a 4f 2e                                 chaddr[0-5]: client MAC
        00 00 00 00 00 00 00 00 00 00                     chaddr[6-15]: zero pad
        ...                                               sname[64], file[128]: empty
00f0    63 82 53 63                                       DHCP magic cookie
        [ DHCP Options ]
00f4    35 01 01                                          Opt 53: DHCP Discover
00f7    39 02 05 dc                                       Opt 57: Max DHCP Msg Size=1500
00fb    37 0e 01 03 06 0f 1a 1c                           Opt 55: Parameter Request List
        33 3a 3b 2b 77 5f 2c               codes: subnet, router, DNS, domain,
                                                          ARP proxy, interface MTU,
                                                          lease time, renewal, rebind,
                                                          NTP, domain search, WPAD
010b    3c 0e 41 6e 64 72 6f 69           Opt 60 (Vendor Class ID), len=14:
        64 2d 31 33 00 00 00 00            "Android-13\x00\x00\x00\x00"
                                                          Leaks OS and major version.
                                                          "Android-14" on API 34+.
                                                          Unaffected by MAC randomization.
011b    0c 0e 70 69 78 65 6c 36           Opt 12 (Host Name), len=14:
        2d 75 73 65 72 6e 61 6d            "pixel6-username"
        65                                 Default on GrapheneOS if user has not
                                           changed device name: "pixel6".
                                           Stock Android default: "android-<hex>".
012b    3d 07 01 28 cd c1 0a 4f           Opt 61 (Client ID), len=7:
        2e                                 type=0x01 (Ethernet), then MAC address.
                                           If Opt 61 uses the real MAC while
                                           the Wi-Fi frame SA is randomized,
                                           the randomization is fully defeated here.
0134    ff                                Opt 255: End
```

Option 60 is the key forensic element: `Android-13` is transmitted verbatim and cannot be suppressed without modifying the DHCP client library (`dhcpcd` or `netd`). When cross-referenced against the BSSID logs from a managed Wi-Fi controller, this option allows precise device typing at the moment of association — no app telemetry required.

---

### 5. BLE Advertisement Packet

BLE advertising packets are transmitted on three fixed advertising channels (37, 38, 39 — mapped to 2402, 2426, 2480 MHz). They use a fixed access address of `0x8E89BED6` for advertising state, making them trivially identifiable in raw RF captures. The PDU type determines whether the advertiser is connectable, non-connectable, or directed.

```c
/* BLE Link Layer Advertising PDU */

/* PDU Header — 2 bytes */
struct ble_adv_pdu_header {
    uint8_t  pdu_type   : 4;    /* ADV_IND=0x00, ADV_NONCONN_IND=0x02,
                                   ADV_DIRECT_IND=0x01 */
    uint8_t  rfu        : 2;
    uint8_t  tx_add     : 1;    /* TxAdd: 0=Public address, 1=Random address.
                                   A value of 1 does NOT mean the address
                                   rotates — it means it is random-typed.
                                   Static random addresses have TxAdd=1 and
                                   never change. Only Resolvable Private
                                   Addresses (RPA) actually rotate. */
    uint8_t  rx_add     : 1;
    uint8_t  length;            /* Total length of AdvA + AdvData */
} __attribute__((packed));

/* Advertising PDU payload */
struct ble_adv_payload {
    uint8_t  adv_a[6];          /* AdvA: advertiser address.
                                   If TxAdd=1 and bits 47-46 = 11,
                                   this is a Static Random Address (SRA) —
                                   it is set at device boot and does not
                                   rotate until the Bluetooth stack restarts.
                                   If bits 47-46 = 01, it is an RPA and
                                   rotates every ~15 minutes per spec. */
    uint8_t  adv_data[];        /* AD structures follow */
} __attribute__((packed));

/* AD Structure (repeated) */
struct ble_ad_structure {
    uint8_t  length;            /* Length of type + value */
    uint8_t  type;              /* AD Type:
                                     0x01 — Flags
                                     0x09 — Complete Local Name
                                     0x0A — TX Power Level
                                     0xFF — Manufacturer Specific Data */
    uint8_t  value[];
} __attribute__((packed));

/* Manufacturer Specific Data payload (AD Type 0xFF) */
struct ble_manufacturer_specific {
    uint16_t company_id;        /* Little-endian. 0x004C=Apple, 0x0006=Microsoft,
                                   0x05F1=Linux Foundation */
    uint8_t  data[];            /* Vendor-defined. For iBeacon:
                                     type=0x02, len=0x15,
                                     uuid[16], major[2], minor[2], tx_power[1]
                                   The 16-byte UUID is static across address
                                   rotations — it is the persistent identifier. */
} __attribute__((packed));
```

Annotated hexdump — BLE ADV_NONCONN_IND from an iOS device advertising iBeacon. The AdvA here is a Resolvable Private Address (bits 47-46 = 01), which rotates. The iBeacon UUID in the Manufacturer Specific Data does not rotate and is the cross-session tracking token.

```hexdump
Offset  Hex bytes                                         Annotation
------  ------------------------------------------------  ------------------
        [ Link Layer header ]
0000    d6 be 89 8e                                       Access Address: 0x8E89BED6
                                                          Fixed value for all advertising —
                                                          distinguishes adv from data pkts
0004    02                                                PDU Header byte 0:
                                                          pdu_type=0x02 (ADV_NONCONN_IND)
                                                          TxAdd=0 (this example: public)
0005    1e                                                PDU Length: 30 bytes
        [ AdvA ]
0006    09 21 33 f4 c1 3a                                 AdvA: 3A:C1:F4:33:21:09
                                                          Bits 47-46 = 00 11 => Static Random
                                                          TxAdd=1 (random type, but static)
                                                          This address does NOT rotate.
        [ AdvData — AD structures ]
000c    02 01 06                                          AD: len=2, type=0x01 (Flags)
                                                          value=0x06: LE General Discoverable
                                                          BR/EDR Not Supported
000f    1a ff 4c 00                                       AD: len=26, type=0xFF (Mfr Specific)
                                                          Company ID: 0x004C = Apple Inc.
0013    02 15                                             iBeacon indicator (type=0x02, len=0x15)
0015    e2 c5 6d b5 df fb 48 d2                           UUID (16 bytes):
        b0 60 d0 f5 a7 10 96 e0                           e2c56db5-dffb-48d2-b060-d0f5a71096e0
                                                          This is a FIXED, PERSISTENT UUID.
                                                          It is identical across every
                                                          advertising rotation. Any BLE
                                                          scanner that logs this UUID can
                                                          track the beacon owner regardless
                                                          of whether the AdvA rotates.
0025    00 01                                             iBeacon Major: 1
0027    00 02                                             iBeacon Minor: 2
0029    c5                                                TX Power: -59 dBm (calibrated)
002a    d8 4c                                             CRC (3 bytes, LL computed)
```

The TxAdd bit and the top two bits of AdvA together determine address type: `00` = Public (static, OUI-rooted), `11` in bits 47-46 with TxAdd=1 = Static Random (stable per boot cycle), `01` in bits 47-46 with TxAdd=1 = Resolvable Private Address (rotates, but resolvable by bonded devices and trackable via payload contents). A MySudo or similar privacy-app BLE advertisement that includes a persistent manufacturer UUID in the payload is trackable across RPA rotations because the UUID survives the address change — the address field is irrelevant when the payload contains a stable identifier. Any BLE scanner in passive mode captures both without transmitting.

---

[^1]: IEEE 802.11-2020, "IEEE Standard for Information Technology — Telecommunications and Information Exchange Between Systems — Local and Metropolitan Area Networks — Specific Requirements — Part 11: Wireless LAN Medium Access Control (MAC) and Physical Layer (PHY) Specifications," IEEE, 2020. Defines all 802.11 management frame types including probe request/response, beacon, association request, deauthentication, EAPOL key descriptor, and power save mode behavior. Available at https://standards.ieee.org/ieee/802.11/7028/.

[^2]: Mathy Vanhoef, Célestin Matte, Mathieu Cunche, Leonardo S. Cardoso, and Frank Piessens, "Why MAC Address Randomization is Not Enough: An Analysis of Wi-Fi Network Discovery Mechanisms," *Proceedings of the 11th ACM on Asia Conference on Computer and Communications Security (AsiaCCS)*, 2016, pp. 413–424. Demonstrates that association frames reveal the real hardware MAC even when probe randomization is active, enabling cross-phase correlation.

[^3]: Jeremy Martin, Travis Mayberry, Collin Donahue, Lucas Foppe, Lamont Brown, Chadwick Henning, Elizabeth Rye, and Dane Brown, "A Study of MAC Address Randomization in Mobile Devices and When it Fails," *Proceedings on Privacy Enhancing Technologies* (PoPETs), 2017(4):365–383. Identifies chipset-level scanning behavior that leaks real MAC addresses despite OS-level randomization, including firmware autonomous scan modes in Qualcomm and Broadcom chipsets.
