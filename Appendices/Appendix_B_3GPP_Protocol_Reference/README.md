# Appendix B: 3GPP Protocol Reference

## Introduction

This appendix provides references to the 3GPP standards documents that define the protocols discussed in the forensic analysis chapters. Understanding these specifications is essential for researchers conducting independent investigations of cellular network data collection.

3GPP specifications are organized by series. The most relevant series for forensic analysis are the 24-series (NAS, core network protocols), 36-series (4G LTE radio protocols), 38-series (5G NR radio protocols), and 37-series (positioning protocols).

All specifications are publicly available from the 3GPP website at https://www.3gpp.org/specifications.

## NAS Protocol (Non-Access Stratum)

NAS is the signaling layer between the phone (UE) and the core network (MME in 4G, AMF in 5G). It handles authentication, mobility management, and session management.

### 4G LTE NAS: TS 24.301

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 24.301 | Non-Access-Stratum (NAS) protocol for Evolved Packet System (EPS) | Defines all NAS messages for 4G, including Attach Request (contains IMSI or GUTI), Tracking Area Update, Service Request, and Detach. The IMSI is transmitted in plain text during initial attach. |
| 3GPP TS 24.008 | Mobile radio interface Layer 3 specification; Core network protocols | Earlier 2G/3G NAS specification. Still relevant for legacy network fallback behavior. Many 4G-only phones also reference this for circuit-switched fallback (CSFB). |

### 5G NAS: TS 24.501

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 24.501 | Non-Access-Stratum (NAS) protocol for 5G System (5GS) | Defines all NAS messages for 5G, including Registration Request (contains SUPI/SUCI or 5G-GUTI), Service Request, and Deregistration. For 5G SA networks. |
| 3GPP TS 33.501 | Security architecture and procedures for 5G System | Defines the security framework for 5G, including SUCI encryption (using ECIES), home network public key distribution, and the null-scheme fallback. |

### Key NAS Messages for Forensic Analysis

| Message | Protocol | Data Exposed |
|---|---|---|
| Attach Request (4G) | NAS (TS 24.301) | IMSI (or GUTI), IMEI, UE capabilities, last visited TAI |
| Registration Request (5G) | NAS (TS 24.501) | SUPI/SUCI (or 5G-GUTI), PEI, UE capabilities, requested NSSAI |
| Tracking Area Update | NAS (TS 24.301) | GUTI, last visited TAI, UE status |
| Service Request | NAS (TS 24.301 / 24.501) | GUTI/5G-GUTI, establishment cause |
| Identity Request / Response | NAS (TS 24.301 / 24.501) | IMSI (requested by network when GUTI is invalid) |
| Authentication Request | NAS (TS 24.301 / 24.501) | Authentication parameters, KSI (key set identifier) |

## RRC Protocol (Radio Resource Control)

RRC is the signaling layer between the phone (UE) and the base station (eNB in 4G, gNB in 5G). It handles connection establishment, measurement reports, handovers, and system information broadcast.

### 4G LTE RRC: TS 36.331

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 36.331 | Evolved Universal Terrestrial Radio Access (E-UTRA); Radio Resource Control (RRC) | Defines all RRC messages for 4G LTE, including RRC Connection Setup, Measurement Reports (neighbor cell signal strengths), RRC Connection Reconfiguration (handover commands), and System Information Blocks (MIB/SIB). |
| 3GPP TS 36.300 | Overall description of E-UTRAN | Higher-level description of the 4G radio access network. Useful for understanding where RRC fits in the protocol stack. |

### 5G NR RRC: TS 38.331

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 38.331 | NR; Radio Resource Control (RRC) protocol specification | Defines all RRC messages for 5G NR, including RRC Setup, Measurement Reports, Reconfiguration, and System Information. 5G RRC is more complex due to beam management and carrier aggregation. |
| 3GPP TS 38.300 | NR; Overall description of Stage 2 | Higher-level description of the 5G radio access network. Reference for understanding protocol architecture. |

### Key RRC Messages for Forensic Analysis

| Message | Protocol | Data Exposed |
|---|---|---|
| RRC Connection Request | RRC (TS 36.331 / 38.331) | UE identity (TMSI/GUTI or random value), establishment cause |
| RRC Connection Setup Complete | RRC (TS 36.331 / 38.331) | Contains NAS message (Attach Request / Registration Request) with IMSI/SUPI |
| Measurement Report | RRC (TS 36.331 / 38.331) | Neighbor cell IDs (ECGI/NCGI), signal strength (RSRP/RSRQ), timing information. The "snitch" signal that reveals movement patterns. |
| RRC Connection Reconfiguration | RRC (TS 36.331 / 38.331) | Handover commands, measurement configuration. Reveals network topology. |
| System Information Block Type 1 (SIB1) | RRC (TS 36.331 / 38.331) | Cell identity, PLMN list, tracking area code. Broadcast by every cell. |
| UE Capability Enquiry / Information | RRC (TS 36.331 / 38.331) | Device capabilities (supported bands, protocols, features). Device fingerprinting information. |

## S1AP and NGAP (Backhaul Protocols)

These protocols operate between the base station and the core network. They are not visible to the phone, but they are the most valuable forensic intercept point because they contain unencrypted subscriber information from both NAS and RRC layers.

### 4G S1AP: TS 36.413

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 36.413 | Evolved Universal Terrestrial Radio Access (E-UTRA); S1 Application Protocol (S1AP) | Defines signaling between the eNB (base station) and the MME (core network). Carries NAS messages transparently, plus additional radio-level information. |
| 3GPP TS 36.410 | S1 general aspects and principles | Architecture overview for the S1 interface between eNB and EPC. |

S1AP is the most valuable protocol for forensic interception because:

- It carries the unencrypted NAS messages (containing IMSI/IMEI)
- It includes the eNB UE S1AP ID, which links all messages for a specific device session
- It includes cell identification (ECGI) and tracking area information
- It is intercepted at lawfully tapped lines in the carrier infrastructure (not over the air)

### 5G NGAP: TS 38.413

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 38.413 | NG-RAN; NG Application Protocol (NGAP) | Defines signaling between the gNB (base station) and the AMF (core network). 5G equivalent of S1AP. Part of the 5G NG-RAN architecture. |
| 3GPP TS 38.410 | NG-RAN; NG general aspects and principles | Architecture overview for the NG interface between gNB and 5GC. |

Key NGAP procedures for forensic analysis:

- **Initial UE Message:** Carries the NAS Registration Request (with SUCI/5G-GUTI) from the phone
- **Initial Context Setup:** Establishes the UE context in the gNB, includes security keys and capabilities
- **UE Context Release:** Releases the UE context, includes cause and location information
- **Handover Preparation:** Includes target cell ID, source cell ID, and handover type
- **Path Switch Request:** Updates the core network with the new cell location after handover

## Positioning Protocols

### LTE Positioning Protocol (LPP): TS 36.355

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 36.355 | Evolved Universal Terrestrial Radio Access (E-UTRA); LTE Positioning Protocol (LPP) | Defines positioning message exchange between the phone and the location server (E-SMLC). Used for OTDOA, ECID, and other location methods. |

LPP carries:

- OTDOA measurement requests and responses
- ECID measurements (Cell ID, RSRP, RSRQ, timing advance)
- A-GNSS (Assisted GPS) assistance data and measurements
- Location information transfer from phone to network

### NR Positioning Protocol (NRPPa): TS 38.455

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 38.455 | NG-RAN; NR Positioning Protocol Annex (NRPPa) | Defines positioning information exchange between the gNB and the location server (LMF). Carries measurement data not available via LPP alone. |

### LTE Positioning Protocol Annex (LPPa): TS 36.455

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 36.455 | Evolved Universal Terrestrial Radio Access (E-UTRA); LTE Positioning Protocol Annex (LPPa) | Defines positioning information exchange between the eNB and the location server (E-SMLC). Similar to NRPPa but for 4G. |

## Additional Relevant Standards

### UE Capabilities and Identifiers

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 22.101 | Service aspects; Service principles | Defines requirements for emergency services (E911 location accuracy requirements). |
| 3GPP TS 23.271 | Location Services (LCS) | Defines the location services architecture including privacy controls and positioning methods. |
| 3GPP TS 23.501 | System architecture for the 5G System | Defines the 5G system architecture including network functions (AMF, SMF, UDM, LMF). |
| 3GPP TS 23.502 | Procedures for the 5G System | Defines registration, connection, and mobility procedures for 5G. |

### Lawful Interception

| Specification | Title | Relevance |
|---|---|---|
| 3GPP TS 33.107 | Lawful interception architecture and functions | Defines the architecture for lawful interception in 3GPP networks. Reference for understanding how CALEA taps are implemented. |
| 3GPP TS 33.108 | Handover interface for lawful interception | Defines the interface between carriers and law enforcement for delivering intercepted communications. |

## How to Read a 3GPP Specification

3GPP specifications can be thousands of pages. To find specific information:

1. **Start with the stage 2 specification** (e.g., TS 23.501 for 5G architecture) for a high-level overview of procedures and information flows.

2. **Search for specific parameters** in the stage 3 specification (e.g., TS 24.501 for 5G NAS) for message structures, information element encoding, and field values.

3. **Look for ASN.1 definitions** in the annexes. Most 3GPP protocols use ASN.1 (Abstract Syntax Notation One) for message encoding.

4. **Check the "p-cr" database** at https://portal.3gpp.org for change requests that modify specifications between releases.

5. **Version numbering**: 3GPP specifications use the format VXX.Y.Z where XX is the release number (e.g., V16.0.0 = Release 16, the first version). Higher Y numbers indicate later versions with approved changes.
