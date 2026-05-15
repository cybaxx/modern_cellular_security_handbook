# Chapter 6: Cellular Network Forensics — What Your Phone Transmits

## The Protocol Stack: Your Phone's Language with the Tower

Your phone does not simply "send location" to the network. It speaks a complex set of protocols defined by the 3GPP standards body. These protocols are layered, and each layer exposes different kinds of forensic data. Understanding them is essential to understanding what law enforcement and intelligence agencies can collect without ever touching your device.

### NAS (Non-Access Stratum)

The NAS layer handles the high-level conversation between your phone and the core network — specifically the MME (Mobility Management Entity) in 4G or the AMF (Access and Mobility Management Function) in 5G. This layer is responsible for authentication, mobility tracking, and session management. When your phone attaches to the network, performs a location update, or establishes a data session, the NAS layer carries the messages.[^1] Forensically, NAS is critical because it contains your permanent and temporary identity structures, including the IMSI and location update requests.

### RRC (Radio Resource Control)

The RRC layer governs the low-level conversation between your phone and the specific tower (eNB in 4G, gNB in 5G). It handles connection setup and release, measurement reports, and handovers. When you move from one cell to another, RRC messages coordinate the transition.[^2] The forensic value of RRC is enormous: it contains the Cell ID you are connected to, Timing Advance values that measure your distance from the tower, and neighbor cell measurement reports that reveal the signal strength of every tower in your vicinity.

### S1AP / NGAP (Application Protocols)

S1AP (in 4G) and NGAP (in 5G) are the back-end protocols that connect the radio access network (the tower) to the core network.[^3] They run over SCTP (Stream Control Transmission Protocol) on the backhaul link. Forensic analysts focus on S1AP/NGAP because these protocols contain the "handshake" that links your radio session to your subscriber identity. Every connection creates a unique identifier — the eNodeB UE S1AP ID and MME UE S1AP ID — that ties your device to your session at the network level.

### Expert Observation

The NAS and RRC layers are either unencrypted or only lightly protected. They function as the "return address" on a letter. Law enforcement does not need to break Signal, WhatsApp, or any other encrypted application to obtain this data. The metadata transmitted at these protocol layers is often sufficient to build a complete picture of your communications behavior and movements.

## Identity Structures: The Who

These are the unique identifiers hardcoded into your SIM card and device hardware. They are the foundation of cellular forensic investigation.

### IMSI and SUPI

The IMSI (International Mobile Subscriber Identity) is the permanent identifier stored on your SIM card.[^4] In 4G networks, the IMSI is transmitted in plaintext during the initial attach procedure.[^1] It links directly to your billing identity — your name, address, and account details. The 5G equivalent is the SUPI (Subscription Permanent Identifier). The IMSI/SUPI is the single most valuable piece of forensic data a carrier log can contain because it provides an unbreakable link between a device and a person.

### TMSI / GUTI and 5G-GUTI

To protect the IMSI from over-the-air interception, the network assigns a temporary identifier: the TMSI (Temporary Mobile Subscriber Identity) in 4G or the GUTI (Globally Unique Temporary Identifier).[^4] In 5G, this is the 5G-GUTI. These temporary IDs change as you move through the network, but a forensic analyst can correlate them to the permanent IMSI via core network logs. Capturing a TMSI over the air does not directly reveal your identity, but combined with network-side logs, the linkage is trivial.

### IMEI and PEI

The IMEI (International Mobile Equipment Identity) identifies the physical device hardware — the specific phone itself, not the SIM card.[^4] In 5G, this is called the PEI (Permanent Equipment Identifier). Even if you swap SIM cards, the IMEI remains constant. This allows investigators to link a SIM to a physical device and to track that device across different SIM cards. The IMEI is logged by the core network every time your phone attaches, and it is one of the few identifiers that cannot be changed without specialized (and often illegal) tools.

### The 5G SUCI Fix and Its Limitations

5G introduced the SUCI (Subscription Concealed Identifier) as a privacy improvement.[^5] Instead of transmitting the IMSI (SUPI) in plaintext, the phone encrypts it using the home network's public key. This prevents passive IMSI catchers from capturing your permanent identity over the air.

However, the forensic reality is more nuanced. First, CALEA (the Communications Assistance for Law Enforcement Act, 47 U.S.C. §§ 1001–1010)[^6] and similar lawful intercept frameworks in other countries mandate that carriers must decrypt the SUCI upon receiving a valid court order. The encryption protects against passive surveillance by non-authorized parties, but not against compelled carrier cooperation. Second, if your phone falls back to 4G — due to poor signal, network configuration, or active downgrade attacks — it transmits the IMSI in plaintext immediately.[^7] The security of SUCI is only as strong as the network's refusal to fall back to 4G, and in practice, fallback is common and often invisible to the user.

## Location and Mobility Structures: The Where

The cellular network tracks your movement through a hierarchy of location structures. These operate independently of any GPS chip in your device.

### Cell ID (ECGI / NCGI)

Every tower sector has a unique identifier: the E-UTRAN Cell Global Identifier (ECGI) in 4G and the NR Cell Global Identifier (NCGI) in 5G.[^3] Your phone reports the Cell ID of the tower it is connected to as part of normal operation. The forensic accuracy of Cell ID alone ranges from a city block (500 meters) in dense urban areas to several kilometers in rural environments. Carriers maintain databases that map every Cell ID to precise GPS coordinates of the tower location.

### Tracking Area (TA)

A Tracking Area is a group of cells used by the network to efficiently page your phone when an incoming call or message arrives.[^1] Your phone performs a Tracking Area Update (TAU) whenever it crosses into a new area. These updates are logged and reveal your general region of movement.

### Timing Advance (TA)

Timing Advance is a measurement of how long it takes your phone's signal to reach the tower. The tower calculates this value based on signal round-trip time. Each Timing Advance unit corresponds to approximately 78 meters in 4G and 39 meters in 5G.[^2] By combining Cell ID with Timing Advance, an investigator can narrow your location from a broad cell sector to a specific distance band around the tower. Over multiple measurements, this produces a movement track with meaningful precision.

### Angle of Arrival (AoA)

Modern base stations use directional antennas or antenna arrays that can measure the angle from which your phone's signal arrives. Combined with Timing Advance and Cell ID, AoA enables triangulation within a single tower sector. Typical forensic accuracy is 50 to 200 meters.

### Measurement Reports

Your phone constantly scans for neighboring towers to prepare for handovers. It reports the signal strength of every tower it can hear — typically 6 to 16 neighboring cells — back to the serving tower.[^2] These measurement reports are a forensic goldmine. They reveal not just which tower you are connected to, but which towers you could hear, which tells an analyst exactly where you must have been geographically. Over time, measurement reports allow reconstruction of your precise path of movement through a city, including which side of a street you walked on, without ever accessing your phone's GPS.

### Forensic Reconstruction

By collecting Timing Advance values, Cell IDs, and neighbor cell measurement reports over time, a forensic analyst can plot your path of movement with accuracy approaching that of GPS. This is not theoretical — it is standard practice in criminal investigations and intelligence analysis.

## Session and Usage Structures: The What

Even without intercepting content, the setup and maintenance of communication sessions leak substantial metadata.

### QoS Class Identifier (QCI)

The network assigns a QCI value to each data bearer based on the type of traffic.[^8] QCI 1 indicates voice, QCI 7 indicates real-time gaming, QCI 9 indicates best-effort web browsing. Even if you use a VPN, the tower still sees that you are using an "interactive" or "streaming" bearer, enabling traffic classification.

### Access Point Name (APN)

The APN identifies the network you are connecting to — for example, `internet` for general web access, `ims` for Voice over LTE, or `enterprise.vpn` for corporate VPN connections.[^1] The APN reveals the type of service and can indicate your employer or service provider.

### SIP Headers in IMS

Even when voice calls are encrypted (using SRTP or similar), the Session Initiation Protocol (SIP) handshake is often visible. SIP headers contain the dialed number, call duration, and call setup timestamps. This metadata is logged by the carrier and is accessible via lawful intercept.

## Collection Mechanisms: How the Data Is Harvested

The protocol data described above flows to collectors through several distinct mechanisms, each with different capabilities and legal thresholds.

### Stingray (IMSI Catcher) — Passive and Active

The Stingray, manufactured by Harris Corporation (now L3Harris), is a device that pretends to be a legitimate cell tower. In 4G networks, it broadcasts a stronger signal than the real tower, causing nearby phones to connect to it. Once connected, the Stingray sends an Identity Request message, and the phone responds with its IMSI in plaintext, along with other identifying information.[^7]

In 5G networks, the Stingray is partially neutralized by SUCI encryption — the phone sends an encrypted identifier that only the home network can decrypt.[^5] However, the Stingray can force the phone to fall back to 4G, at which point it sends the plaintext IMSI. Additionally, even in 5G, the Stingray captures the IMEI/PEI and can measure signal strength and Timing Advance to estimate the device's location (typically 50 to 200 meter accuracy).

Modern variants include the DRT Box (Digital Receiver Technology), which performs passive capture of all phone metadata within a mile radius and is nearly undetectable, and the Hailstorm (by KeySight), which is 5G-capable and supports Multi-RTT positioning. The Hailstorm's detection methods are still immature.

### CALEA / Lawful Intercept — Core Network Tap

CALEA (Communications Assistance for Law Enforcement Act) in the United States,[^6] and equivalent legal frameworks in other countries, requires carriers to install interception capabilities at the network infrastructure level. Unlike a Stingray, which captures data over the air, a CALEA tap operates at the S1-MME interface or IMS core, inside the carrier's own network.

This tap bypasses encryption at the network edge. It captures everything: IMSI, IMEI, dialed digits, call duration, timing information accurate to 200 milliseconds, conference call participants, and data session metadata. The carrier is legally required to provide this data in real time when presented with a lawful intercept order.

The two-phone strategy fails against core network taps because Carrier A knows Phone A is at Location X, and Carrier B knows Phone B is at Location X. When law enforcement correlates both, the compartmentalization collapses.

### Core Network Correlation via S1AP

The backhaul link between the tower (eNB) and the core network (MME) uses S1AP over SCTP.[^3] The network creates a unique identifier — the eNodeB UE S1AP ID — to link your radio session to your core network session. Even if you turn off your phone, the network retains the bearer context. Analysts can trace your movement between connections by examining handover logs, revealing where you were and for how long, even across power cycles.

### Tower Dumps

A tower dump is a court order compelling a carrier to provide a list of every IMSI and IMEI that connected to a specific set of towers during a specific time window. The threshold is "reasonable suspicion," which is lower than probable cause. Tower dumps are devastating for compartmentalization because they reveal co-location: if Phone A (identified by its IMSI) appears in the dump at the same time and place as Phone B (identified by its IMEI), an investigator concludes they belong to the same person.

### Pen Register / Trap and Trace

A pen register order captures real-time metadata for a specific phone number: dialed numbers, call duration, and tower IDs. The legal threshold is a certification by law enforcement that the information is relevant to an ongoing investigation — the lowest standard for content-adjacent collection.

### Section 2703(d) Orders

Under the Stored Communications Act, a 2703(d) order requires the carrier to produce historical records for a specific account or device: full Call Detail Records, location history, subscriber information, and IP assignment logs. The threshold is "specific and articulable facts" showing reasonable grounds to believe the records are relevant. This is the most common tool for obtaining historical cell site location information. The Supreme Court confirmed in *Carpenter v. United States* that historical cell-site location records are protected under the Fourth Amendment.[^9]

### Title III Wiretap

A Title III wiretap order authorizes real-time interception of both content and metadata for a specific phone. It requires probable cause and judicial approval, making it the highest legal threshold but also the most comprehensive collection method.

## Protocol Deep Dive: Packet Structures and Wire Format

The preceding sections described what each protocol layer exposes. This section shows exactly how that data is encoded at the byte level — the actual wire format an analyst sees in a packet capture, a CALEA feed, or a baseband memory dump. References are to 3GPP TS 24.301 (NAS),[^1] TS 36.331 (RRC),[^2] TS 36.413 (S1AP),[^3] and TS 23.003 (SUCI/5G identities).[^4]

---

### 1. NAS Attach Request (3GPP TS 24.301 §8.2.4)

The Attach Request is the first NAS message a UE sends when registering with the network. In 4G it is transmitted before the security context is established, meaning it is unencrypted on the air interface. This is the message a passive interceptor or IMSI catcher targets.

```c
/*
 * NAS EMM Attach Request — 3GPP TS 24.301 §8.2.4
 * All multi-byte fields are big-endian unless noted.
 *
 * The outer NAS header (§9.3.1) precedes every NAS PDU:
 *
 * Offset  Size  Field
 * 0       1B    Security Header Type (bits 7-4) | Protocol Discriminator (bits 3-0)
 *                 Security Header Type: 0x0 = plain NAS (no integrity/cipher)
 *                 Protocol Discriminator: 0x7 = EPS Mobility Management (EMM)
 * 1       1B    Message Type: 0x41 = Attach Request
 */

typedef struct __attribute__((packed)) {
    /* NAS header */
    uint8_t  sec_hdr_and_pd;        /* 0x07 = plain NAS | EMM PD            */
    uint8_t  message_type;          /* 0x41 = Attach Request                 */

    /*
     * IE: EPS Attach Type (§9.9.3.11) + NAS KSI (§9.9.3.21)
     * Single byte, split into two 4-bit half-IEs:
     *   bits 7-4: NAS Key Set Identifier (KSI) — 0x7 = "no key available"
     *   bits 3-0: EPS Attach Type
     *             0x1 = EPS attach (data only)
     *             0x2 = combined EPS/IMSI attach (voice + data)
     *             0x6 = EPS emergency attach
     */
    uint8_t  ksi_and_attach_type;   /* offset 2                              */

    /*
     * IE: Old GUTI or IMSI (§9.9.3.12 / §9.9.3.3)
     * Length-prefixed EPS Mobile Identity IE.
     *
     * If the UE has no GUTI from a prior session it sends the IMSI here
     * in plaintext — this is the primary IMSI catcher harvest point.
     *
     * Offset  Size  Subfield
     * 3       1B    IE identifier: 0x50 = EPS Mobile Identity
     * 4       1B    IE length (n bytes follow)
     * 5       1B    bits 7-5: spare (0)
     *               bits 4-1: Type of identity
     *                         0x1 = IMSI
     *                         0x6 = GUTI
     *               bit  0:   Odd/Even indicator (1 = odd number of digits)
     * 6..n          BCD-encoded digits, two per byte, LSN first within each byte
     *               For IMSI "310150123456789":
     *                 0x13 0x10 0x51 0x21 0x43 0x65 0x87 0xF9
     *               (0xF padding when total digit count is even)
     */
    uint8_t  eps_mobile_id_iei;     /* 0x50                                  */
    uint8_t  eps_mobile_id_len;     /* e.g., 0x08 for 15-digit IMSI          */
    uint8_t  eps_mobile_id_type;    /* identity type + odd/even indicator     */
    uint8_t  mobile_id[8];          /* BCD-encoded IMSI or GUTI octets        */

    /*
     * IE: UE Network Capability (§9.9.3.34)
     * Advertises supported ciphering and integrity algorithms.
     * Forensic note: algorithm list reveals device firmware vintage.
     *
     * Offset  1B    IE identifier: 0x58
     * Offset  1B    IE length (2–14 bytes)
     * Octet 1:
     *   bit 7: EEA0 (null cipher) supported
     *   bit 6: 128-EEA1 (SNOW 3G)
     *   bit 5: 128-EEA2 (AES-CTR)
     *   bit 4: 128-EEA3 (ZUC)
     *   bit 3: EIA0 (null integrity — must be 0 except emergency)
     *   bit 2: 128-EIA1
     *   bit 1: 128-EIA2
     *   bit 0: 128-EIA3
     */
    uint8_t  ue_net_cap_iei;        /* 0x58                                  */
    uint8_t  ue_net_cap_len;        /* 0x02 minimum                          */
    uint8_t  ue_net_cap_eea_eia;    /* cipher + integrity algorithm bitmap   */
    uint8_t  ue_net_cap_uea_uia;    /* UMTS algorithm bitmap (optional)      */

    /*
     * IE: ESM Message Container (§9.9.3.15)
     * Contains a piggybacked NAS ESM PDN Connectivity Request.
     * This reveals the requested APN (Access Point Name).
     *
     * Offset  2B    IE length (big-endian)
     * Offset  nB    ESM PDU (contains APN string, PDN type, PCO)
     */
    uint8_t  esm_container_iei;     /* 0x78                                  */
    uint16_t esm_container_len;     /* big-endian length of ESM PDU          */
    uint8_t  esm_pdu[];             /* flexible array: APN, bearer params    */

    /* Additional optional IEs follow (variable length):
     *   0x52  Last visited registered TAI
     *   0x5C  DRX parameter
     *   0x31  MS network feature support
     *   0x13  TMSI status
     *   0x11  Mobile station classmark 2
     *   0x20  Mobile station classmark 3
     *   0x40  Supported codecs
     *   0xF-  Additional update type (nibble IE)
     */
} nas_attach_request_t;
```

```hexdump
; NAS Attach Request — UE has no prior GUTI; transmits IMSI 310150123456789
; Captured at air interface before security mode activation.
;
; offset  hex bytes                     annotation
  00      07                            Security Header=0 (plain) | PD=7 (EMM)
  01      41                            Message Type: Attach Request
  02      B1                            KSI=0xB (no key) | Attach Type=1 (EPS)
  03      50                            IE: EPS Mobile Identity
  04      08                            IE length: 8 bytes
  05      01                            Type=IMSI (0x1), odd digit count
  06      13 10 51 21 43 65 87 F9       BCD IMSI: 310150123456789 (padded 0xF)
  0E      58                            IE: UE Network Capability
  0F      02                            IE length: 2 bytes
  10      E0                            EEA0+EEA1+EEA2 supported; EIA1+EIA2+EIA3
  11      C0                            UEA0+UEA1; UIA1
  12      78                            IE: ESM Message Container
  13      00 0B                         ESM PDU length: 11 bytes
  15      02 DA 28 D9 11 00 0A 69 6E    ESM PDU (PDN Connectivity Req, APN=
  1E      74 65 72 6E 65 74             "internet")
```

The IMSI appears at offset 0x06 in BCD encoding. A passive capture at the air interface — before any NAS security mode command — yields the subscriber's permanent identity directly. The ESM container at the tail of the message additionally reveals the requested APN, exposing the intended service type (e.g., `internet`, `ims`, `enterprise`).

---

### 2. RRC MeasurementReport (3GPP TS 36.331 §6.7.4)

The RRC MeasurementReport is generated by the UE's baseband and transmitted to the serving eNB. It is sent unencrypted at RRC layer in many configurations and is always visible to the serving tower. It lists RSRP and RSRQ for both the serving cell and up to 16 neighbor cells, giving a precise radio fingerprint of the UE's physical position.[^2]

```c
/*
 * LTE RRC MeasurementReport — 3GPP TS 36.331 §6.7.4
 * Encoded over the air as UPER (Unaligned Packed Encoding Rules) ASN.1.
 * The C struct below reflects the decoded logical structure.
 */

/* Signal measurement for one cell */
typedef struct {
    int8_t   rsrp;          /* Reference Signal Received Power
                             * Range: -140 dBm (0) to -44 dBm (96)
                             * Wire value = (dBm + 140), e.g., -90 dBm → 50  */
    int8_t   rsrq;          /* Reference Signal Received Quality
                             * Range: -19.5 dB (0) to -3 dB (33)
                             * Wire value = (dB * 2 + 39)                     */
} meas_result_eutra_t;

/* One entry in the neighbor cell list */
typedef struct {
    uint16_t           phys_cell_id;       /* Physical Cell ID: 0–503        */
    meas_result_eutra_t meas_result;       /* RSRP + RSRQ for this neighbor  */
    /* Optional fields present when measConfig includes cellForWhichToReport: */
    uint32_t           cgi_ecgi;           /* E-UTRAN Cell Global ID (ECGI)
                                            * = MCC(3) + MNC(2-3) + ECI(28b)
                                            * Present only during CGI reporting
                                            * — exposes neighbor tower identity */
    uint16_t           tracking_area_code; /* TAC for the neighbor cell       */
} meas_result_neigh_cell_t;

/* Top-level MeasurementReport message */
typedef struct {
    uint8_t                  meas_id;          /* Links to measConfig (1–32)
                                                * Identifies which measurement
                                                * event triggered this report  */
    meas_result_eutra_t      serv_cell;        /* Serving cell RSRP/RSRQ      */
    uint8_t                  neigh_cell_count; /* Number of neighbor entries   */
    meas_result_neigh_cell_t neigh_cells[16];  /* Neighbor cell list           */

    /* Optional: UTRA (3G) neighbor results */
    /* Optional: GERAN (2G) neighbor results */
    /* Optional: CDMA2000 neighbor results   */
} rrc_measurement_report_t;
```

```hexdump
; RRC MeasurementReport UPER-encoded (simplified, byte-aligned for readability)
; measId=1, serving RSRP=-90dBm (50), serving RSRQ=-10dB (19)
; 3 neighbors: PCI=25 RSRP=-95, PCI=42 RSRP=-101, PCI=7 RSRP=-103
;
; offset  hex   annotation
  00      01    measId = 1
  01      32    serving RSRP = 50 → -90 dBm
  02      13    serving RSRQ = 19 → -10.0 dB
  03      03    neigh_cell_count = 3
  ; neighbor 0
  04      00 19 phys_cell_id = 25
  06      2D    RSRP = 45 → -95 dBm
  07      13    RSRQ = 19
  ; neighbor 1
  08      00 2A phys_cell_id = 42
  0A      27    RSRP = 39 → -101 dBm
  0B      11    RSRQ = 17
  ; neighbor 2
  0C      00 07 phys_cell_id = 7
  0E      25    RSRP = 37 → -103 dBm
  0F      0F    RSRQ = 15
```

Each neighbor cell entry exposes the physical cell ID and signal strength observed from the UE's exact position. A forensic analyst correlating PCI values against a carrier's cell database can identify which specific tower sectors the UE could hear, constraining the device's location to the geometric intersection of the reported signal footprints. When CGI reporting is active, the neighbor ECGI field directly names the neighboring tower by its global identifier.

---

### 3. S1AP Initial UE Message (3GPP TS 36.413 §9.2.5.1)

The Initial UE Message is the first S1AP message the eNB sends to the MME over the backhaul after the UE initiates a connection. It bundles the radio session identity, geographic context, and the NAS PDU from the UE into a single backhaul message. A tap on the S1-MME interface captures all of this in one frame.[^3]

```c
/*
 * S1AP InitialUEMessage — 3GPP TS 36.413 §9.2.5.1
 * Encoded as S1AP PDU using ASN.1 PER. The struct below is the decoded form.
 * Transported over SCTP (typically port 36412) between eNB and MME.
 *
 * Offset  Size   Field                        IE ID (decimal)
 */
typedef struct __attribute__((packed)) {
    /*
     * eNB-UE-S1AP-ID (Mandatory, IE ID=8)
     * 24-bit value assigned by the eNB. Unique per eNB per session.
     * Scoped to this eNB only; the MME assigns its own MME-UE-S1AP-ID.
     * Together these two IDs uniquely identify the session on the backhaul.
     */
    uint32_t enb_ue_s1ap_id;       /* bits 23-0 used, upper byte = 0x00     */

    /*
     * NAS-PDU (Mandatory, IE ID=26)
     * The raw NAS message from the UE (e.g., the Attach Request above).
     * Forwarded verbatim to the MME. At this point NAS may be plaintext
     * (before security mode) or integrity-protected/ciphered (subsequent msgs).
     */
    uint16_t nas_pdu_len;
    uint8_t  nas_pdu[];             /* flexible: contains IMSI/GUTI in NAS   */

    /*
     * TAI — Tracking Area Identity (Mandatory, IE ID=67)
     * Identifies the tracking area where the UE currently resides.
     * Composed of:
     *   PLMN-Identity: MCC (3 BCD digits) + MNC (2-3 BCD digits)
     *   TAC: Tracking Area Code (2 bytes)
     * The TAI is used for paging and mobility anchoring.
     */
    struct {
        uint8_t  plmn[3];           /* BCD: MCC+MNC, e.g., 0x31 0xF0 0x15
                                     * = MCC 310, MNC 150 (T-Mobile US)      */
        uint16_t tac;               /* Tracking Area Code, big-endian        */
    } tai;                          /* IE ID=67                               */

    /*
     * EUTRAN-CGI — E-UTRAN Cell Global Identity (Mandatory, IE ID=100)
     * Names the exact cell the UE connected through.
     * This is the single most forensically precise location datum in S1AP:
     * it maps to a specific antenna sector whose GPS coordinates are known.
     *
     *   PLMN-Identity: same BCD encoding as TAI above
     *   Cell-ID: 28-bit ECI within PLMN (bit-packed, MSB first)
     */
    struct {
        uint8_t  plmn[3];           /* BCD MCC+MNC                           */
        uint32_t cell_id;           /* bits 31-4 = 28-bit ECI, bits 3-0 = 0 */
    } eutran_cgi;                   /* IE ID=100                              */

    /*
     * RRC-Establishment-Cause (Mandatory, IE ID=134)
     * Reveals why the UE initiated the connection.
     *   0 = emergency
     *   1 = highPriorityAccess
     *   2 = mt-Access (mobile terminated — incoming call/SMS)
     *   3 = mo-Signalling (outgoing control plane, e.g., location update)
     *   4 = mo-Data (outgoing data session)
     *   5 = delayTolerantAccess
     *   6 = mo-VoiceCall
     *   7 = mo-ExceptionData
     * Cause code 2 (mt-Access) proves the device received a communication
     * at this location at this time without content interception.
     */
    uint8_t  rrc_establishment_cause;  /* IE ID=134                          */

    /*
     * Optional IEs that may follow:
     *   IE ID=96  S-TMSI (serving MME TMSI, present if UE provided one)
     *   IE ID=127 CSG-Id (Closed Subscriber Group, enterprise femtocell)
     *   IE ID=145 GUMMEI (serving MME identity)
     *   IE ID=155 Tunnel Information (for RAN-level UP path)
     */
} s1ap_initial_ue_message_t;
```

```hexdump
; S1AP InitialUEMessage (simplified, key IEs only)
; eNB-UE-S1AP-ID=0x00001A, MCC=310 MNC=150, TAC=0x0042, Cell ECI=0x0A1B2C3
; RRC cause=mo-Data (4)
;
; offset  hex                        annotation
  ; IE: eNB-UE-S1AP-ID (id=8, mandatory, criticality=reject)
  00      00 08                      IE ID = 8
  02      40                         Criticality = reject
  03      00 00 1A                   eNB-UE-S1AP-ID = 26
  ; IE: NAS-PDU (id=26, mandatory, criticality=reject)
  06      00 1A                      IE ID = 26
  08      40                         Criticality = reject
  09      00 16                      NAS-PDU length = 22 bytes
  0B      07 41 B1 50 08 01 ...      NAS Attach Request (see §1 above)
  ; IE: TAI (id=67, mandatory, criticality=reject)
  1F      00 43                      IE ID = 67
  21      40                         Criticality = reject
  22      31 F0 15                   PLMN: MCC=310, MNC=150
  25      00 42                      TAC = 0x0042
  ; IE: EUTRAN-CGI (id=100, mandatory, criticality=ignore)
  27      00 64                      IE ID = 100
  29      20                         Criticality = ignore
  2A      31 F0 15                   PLMN: MCC=310, MNC=150
  2D      0A 1B 2C 30                Cell-ID (28 bits) = 0x0A1B2C3
  ; IE: RRC-Establishment-Cause (id=134, mandatory, criticality=ignore)
  31      00 86                      IE ID = 134
  33      20                         Criticality = ignore
  34      04                         Cause = mo-Data (4)
```

An analyst extracting this single frame has: the session identifier (eNB-UE-S1AP-ID), the precise tower sector the UE is camped on (EUTRAN-CGI mapped to GPS via the carrier's cell database), the tracking area (TAI), the reason for the connection (RRC cause), and the complete NAS PDU which may contain the IMSI. The TAI narrows location to a region; the EUTRAN-CGI narrows it to a specific sector antenna.

---

### 4. SUCI Structure (5G, 3GPP TS 23.003 §2.2B)

The Subscription Concealed Identifier (SUCI) replaces the plaintext IMSI during 5G initial registration.[^4] It is generated by the UE using the home network's ECDH public key (provisioned on the USIM). The home network's AUSF/SIDF function decrypts it using the corresponding private key.[^5] The critical operational detail is the null-scheme fallback.

```c
/*
 * SUCI — Subscription Concealed Identifier
 * 3GPP TS 23.003 §2.2B, TS 24.501 §9.11.3.4
 *
 * The SUCI is a sequence of components; wire encoding is defined in
 * TS 24.501 for 5GMM (5G Mobility Management) Attach/Registration messages.
 *
 * Component         Size         Description
 * ─────────────────────────────────────────────────────────────────────────
 * SUPI Type         3 bits       0x0 = IMSI-based SUPI
 *                                0x1 = Network Specific Identifier (NAI)
 * Home Network ID   variable     MCC (3 digits) + MNC (2-3 digits), BCD
 * Routing Indicator 4 BCD digits Directs SUCI to correct AUSF instance.
 *                                Set to 0000 when not used.
 *                                Transmitted in plaintext — reveals home
 *                                network routing topology.
 * Protection Scheme 1 byte       0x00 = Null-Scheme (IMSI in plaintext)
 *                                0x01 = Profile A (ECIES, Curve25519)
 *                                0x02 = Profile B (ECIES, P-256)
 *                                Operator-configurable on USIM.
 * Home Network      1 byte       Index of HNPK used for encryption (0–255).
 * Public Key ID                  0xFF in null-scheme mode.
 * Scheme Output     variable     Null-Scheme: plaintext MSIN (subscriber ID).
 *                                Profile A/B: ephemeral public key ||
 *                                             ciphertext || MAC tag.
 */

typedef struct {
    uint8_t  supi_type;             /* 0x00 = IMSI-based                      */
    uint8_t  home_network_id[3];    /* BCD MCC+MNC (same encoding as TAI)     */
    uint8_t  routing_indicator[2];  /* BCD, 4 digits, e.g., 0x00 0x00         */
    uint8_t  protection_scheme_id;  /* 0x00=null / 0x01=Profile A / 0x02=B    */
    uint8_t  home_nw_pubkey_id;     /* Key index; 0xFF in null-scheme          */
    uint8_t  scheme_output[];       /* Plaintext MSIN or ECIES ciphertext      */
} suci_t;

/*
 * Null-Scheme SUCI (Protection Scheme = 0x00):
 *
 * scheme_output = plaintext MSIN (Mobile Subscriber Identification Number)
 *
 * The MSIN is the last 9-10 digits of the IMSI. When null-scheme is active,
 * the SUCI is functionally equivalent to a plaintext IMSI transmission.
 * A passive interceptor can reconstruct the full IMSI as:
 *   IMSI = MCC + MNC + MSIN  (all available in plaintext)
 *
 * Null-scheme is mandated for emergency calls in some network configurations
 * and may be selected by the network via USIM provisioning. An operator that
 * provisions null-scheme defeats the entire SUCI privacy guarantee.
 */

/*
 * Profile A SUCI (Protection Scheme = 0x01, Curve25519 ECIES):
 *
 * scheme_output layout:
 *   Ephemeral Public Key:  32 bytes  (Curve25519 point, compressed)
 *   Ciphertext:            len(MSIN) bytes (AES-128-CTR encrypted MSIN)
 *   MAC:                   8 bytes   (HMAC-SHA-256 truncated)
 *
 * Only the home network AUSF/SIDF can decrypt this using the HNPK private key.
 * The HNPK ID field tells the home network which key pair to use.
 */
```

```hexdump
; SUCI embedded in 5GMM Registration Request — Null-Scheme (Protection = 0x00)
; SUPI = IMSI 310150123456789, Routing Indicator = 0000
;
; offset  hex            annotation
  00      00             SUPI Type = IMSI-based
  01      31 F0 15       Home Network ID: MCC=310, MNC=150
  04      00 00          Routing Indicator = 0000
  06      00             Protection Scheme = Null (0x00) — IMSI exposed
  07      FF             Home NW Public Key ID = 0xFF (no key used)
  08      21 43 65 87 F9 Scheme Output = plaintext MSIN: 123456789

; SUCI — Profile A (Protection = 0x01, Curve25519 ECIES)
; MSIN ciphertext is opaque to passive interceptor
;
  00      00             SUPI Type = IMSI-based
  01      31 F0 15       Home Network ID: MCC=310, MNC=150
  04      00 00          Routing Indicator = 0000
  06      01             Protection Scheme = Profile A (Curve25519)
  07      02             Home NW Public Key ID = 2
  08      8F 3A ... (32B) Ephemeral public key (Curve25519)
  28      C4 7E ... (5B)  Ciphertext (encrypted MSIN)
  2D      A1 B2 C3 D4    MAC (first 8 bytes of HMAC-SHA-256)
  ..      E5 F6 07 18
```

The Routing Indicator at offset 4 is always transmitted in plaintext regardless of the protection scheme. It reveals enough about the home network's internal routing topology to identify subscriber clusters. Null-scheme SUCIs expose the full MSIN directly; when combined with the plaintext MCC+MNC prefix, the complete IMSI is trivially reconstructed with no cryptographic capability required.

---

### 5. Call Detail Record (CDR) Structure

A CDR is the canonical record produced by a carrier's billing and network management systems for every voice call, SMS event, and data session. Carriers retain CDRs in the United States and produce them in response to subpoenas, 2703(d) orders, and CALEA intercept orders.[^6] The schema below reflects the fields common across major US carrier production formats; actual field names vary by carrier but the data elements are standardized by the GSMA (IR.61).

```c
/*
 * Call Detail Record — carrier production format
 * Based on GSMA IR.61 and US carrier CDR schema (AT&T, Verizon, T-Mobile)
 *
 * "Always"   = present for every record type
 * "Voice"    = present for voice call records
 * "Data"     = present for data session records
 * "Conditional" = present when event occurs or network reports it
 *
 * Field                   Type         Size  Populated    Description
 */
typedef struct {
    /* ── Subscriber Identity ── */
    char     imsi[16];           /* NUL-terminated  Always      15-digit IMSI */
    char     imei[16];           /* NUL-terminated  Always      15-digit IMEI */
    char     msisdn[16];         /* E.164 number    Always      Subscriber MSISDN (phone number) */

    /* ── Correspondent Identity ── */
    char     calling_number[32]; /* E.164           Voice       Originating party number (A-number) */
    char     called_number[32];  /* E.164           Voice/SMS   Terminating party number (B-number) */

    /* ── Timing ── */
    uint64_t call_start_utc;     /* Unix epoch, ms  Always      First signaling event timestamp */
    uint64_t call_answer_utc;    /* Unix epoch, ms  Voice       When B-party answered (0 if unanswered) */
    uint64_t call_end_utc;       /* Unix epoch, ms  Always      Last signaling/data event timestamp */
    uint32_t duration_sec;       /* seconds         Always      Billable duration (0 for SMS, unanswered) */

    /* ── Location at Call Start ── */
    char     cell_id_start[16];  /* ECGI string     Always      Serving cell at session start */
    uint16_t ta_start;           /* TA units        Always      Timing Advance at start (78m/unit in LTE) */
    double   tower_lat_start;    /* decimal degrees Conditional Carrier maps ECGI → tower GPS */
    double   tower_lon_start;    /* decimal degrees Conditional Same source as cell_id_start */

    /* ── Location at Call End ── */
    char     cell_id_end[16];    /* ECGI string     Conditional Serving cell at session end
                                  *                             Differs from start if UE moved.
                                  *                             Absent for short events. */
    uint16_t ta_end;             /* TA units        Conditional TA at end of session */
    double   tower_lat_end;      /* decimal degrees Conditional GPS of end tower */
    double   tower_lon_end;      /* decimal degrees Conditional */

    /* ── Data Session Fields ── */
    char     apn[64];            /* ASCII           Data        Access Point Name requested by UE */
    uint64_t bytes_uplink;       /* bytes           Data        UE → network (upload) */
    uint64_t bytes_downlink;     /* bytes           Data        Network → UE (download) */
    uint8_t  rat_type;           /* enum            Always      Radio Access Technology:
                                  *                             0x06=UTRAN, 0x08=EUTRAN(4G),
                                  *                             0x11=NR(5G), 0x03=GERAN(2G) */

    /* ── Termination ── */
    uint8_t  cause_for_termination; /* enum         Always      Release reason:
                                     *                          0x00 = Normal release (call completed)
                                     *                          0x01 = Subscriber released
                                     *                          0x02 = Radio link failure
                                     *                          0x04 = QoS change
                                     *                          0x10 = Abnormal release
                                     *                          0x40 = Handover (inter-PLMN)
                                     * Abnormal release codes indicate network events
                                     * consistent with IMSI catcher interference. */

    /* ── Carrier-Specific Extension Fields (not universally present) ── */
    char     roaming_partner[32]; /* PLMN string    Conditional Set when UE is roaming */
    char     mme_id[32];          /* FQDN/IP        Conditional Serving MME, useful for jurisdiction */
    char     pgw_id[32];          /* FQDN/IP        Data        Serving P-GW, reveals traffic routing */
} call_detail_record_t;
```

The `cell_id_start` and `cell_id_end` fields are always populated when the UE is on the LTE/5G network; the `ta_start` and `ta_end` fields are populated whenever the network reports a Timing Advance measurement, which is the case for nearly all LTE connections. Together these four fields place the subscriber at a specific distance band from a known tower location at the precise start and end of every session. The `cause_for_termination` field carries diagnostic value beyond billing: a pattern of abnormal release codes (0x10) across multiple devices in the same location is a documented indicator of active IMSI catcher operation, as the catcher's session teardown produces non-standard release sequences that differ from legitimate MME behavior.[^10]

---

[^1]: 3GPP TS 24.301, "Non-Access-Stratum (NAS) protocol for Evolved Packet System (EPS); Stage 3," defines all NAS EMM and ESM messages including Attach Request (§8.2.4), Tracking Area Update, and PDN Connectivity Request. Available at https://www.3gpp.org/dynareport/24301.htm.

[^2]: 3GPP TS 36.331, "Evolved Universal Terrestrial Radio Access (E-UTRA); Radio Resource Control (RRC); Protocol specification," defines MeasurementReport (§6.7.4), Timing Advance, RSRP/RSRQ measurement encoding, and neighbor cell reporting. Available at https://www.3gpp.org/dynareport/36331.htm.

[^3]: 3GPP TS 36.413, "Evolved Universal Terrestrial Radio Access Network (E-UTRAN); S1 Application Protocol (S1AP)," defines InitialUEMessage (§9.2.5.1), EUTRAN-CGI, TAI, and RRC Establishment Cause IEs. Available at https://www.3gpp.org/dynareport/36413.htm.

[^4]: 3GPP TS 23.003, "Numbering, addressing and identification," defines IMSI, SUPI, SUCI (§2.2B), GUTI, TMSI, IMEI, and PEI structures. Available at https://www.3gpp.org/dynareport/23003.htm.

[^5]: 3GPP TS 33.501, "Security architecture and procedures for 5G System," specifies SUCI generation using ECIES (Profile A: Curve25519; Profile B: P-256), null-scheme behavior, and AUSF/SIDF decryption procedures. Available at https://www.3gpp.org/dynareport/33501.htm.

[^6]: Communications Assistance for Law Enforcement Act (CALEA), 47 U.S.C. §§ 1001–1010 (1994). Mandates that telecommunications carriers maintain real-time interception capability for law enforcement upon lawful authorization.

[^7]: Altaf Shaik, Ravishankar Borgaonkar, N. Asokan, Valtteri Niemi, and Jean-Pierre Seifert, "Practical Attacks Against Privacy and Availability in 4G/LTE Mobile Communication Systems," *Network and Distributed System Security Symposium (NDSS)* 2016. Demonstrates active IMSI-catcher downgrade attacks forcing 4G → 2G fallback to extract plaintext IMSI.

[^8]: NIST SP 800-187, "Guide to LTE Security," National Institute of Standards and Technology, December 2017, §4 (EPC architecture and bearer management). Available at https://doi.org/10.6028/NIST.SP.800-187.

[^9]: *Carpenter v. United States*, 585 U.S. 296 (2018). Held that historical cell-site location information (CSLI) is protected by the Fourth Amendment, requiring a warrant based on probable cause.

[^10]: Ravishankar Borgaonkar, Lucca Hirschi, Shinjo Park, and Altaf Shaik, "New Privacy Threat on 3G, 4G, and Upcoming 5G AKA Protocols," *Proceedings on Privacy Enhancing Technologies* (PoPETs), 2019(3):108–127. Analyzes how abnormal session termination sequences from IMSI catchers differ from legitimate MME behavior and are detectable in CDR termination codes.
