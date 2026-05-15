# Appendix E: Legal Reference — United States

## Introduction

This appendix documents the US legal framework governing law enforcement access to phone data. Understanding these laws is essential for threat modeling because they define what legal process is required for different types of data access. The level of legal protection varies dramatically depending on the type of data sought.

The key principle is that the legal standard rises with the intrusiveness of the access. Metadata and subscriber records require less legal process than content. Real-time access requires more than historical access. Location data occupies an ambiguous middle ground that courts are still defining.

## CALEA (Communications Assistance for Law Enforcement Act)

### Overview

CALEA, enacted in 1994, requires telecommunications carriers to ensure their networks are designed to support lawful interception. It does not grant law enforcement new surveillance authority but requires carriers to have the technical capability to comply with legal orders.

### Key Requirements

| Requirement | Detail |
|---|---|
| Capability requirement | Carriers must be able to isolate and deliver call content and call-identifying information to law enforcement |
| Real-time delivery | Intercepted communications must be delivered to law enforcement in real-time |
| Encryption accommodation | Carriers must decrypt or provide decrypted versions when encryption is used and they hold the keys |
| Network design | New network services must be designed with CALEA intercept capability from the start |
| Cost reimbursement | Carriers are reimbursed for the cost of implementing CALEA compliance |

### What CALEA Intercept Delivers

From the carrier infrastructure, a CALEA intercept can provide:

- Call content (audio for voice calls)
- SMS content and metadata
- Data session content (if within the scope of the order)
- Real-time location (Cell ID, Timing Advance, and in 5G SA, more precise positioning)
- Dialed number and calling number
- Call duration and timing
- Conference call participation

### Limitations

- CALEA intercepts require a separate legal order (wiretap, Title III). CALEA itself authorizes no surveillance.
- Over-the-top services (Signal, WhatsApp, FaceTime) are not covered by CALEA unless the carrier is also providing the service.

## Stored Communications Act (18 U.S.C. §2701–2712)

The Stored Communications Act (SCA) is part of the Electronic Communications Privacy Act of 1986. It governs government access to stored communications and subscriber records held by third-party providers.

### Key Sections

| Section | Subject | Standard |
|---|---|---|
| §2701 | Unauthorized access to stored communications (criminalizes hacking) | N/A |
| §2702 | Voluntary disclosure of communications by providers (prohibits sharing without customer consent, with exceptions) | N/A |
| §2703(a) | Disclosure of stored communications content to government | Warrant (probable cause) for communications stored <180 days; §2703(d) order for >180 days |
| §2703(b) | Disclosure of stored communications content to government (pertains to remote computing services) | §2703(d) order or notice to subscriber |
| §2703(c) | Disclosure of subscriber records and metadata | §2703(d) order |
| §2703(d) | Standard for court order (see below) | Specific and articulable facts |
| §2704 | Backup preservation orders | |
| §2705 | Delayed notice (gag orders) | |
| §2706 | Cost reimbursement | |
| §2707 | Civil action (individuals can sue providers for violating SCA) | |
| §2708-2710 | Definitions and other provisions | |

### §2703(d) Orders

The most common tool for obtaining historical phone records. The standard is lower than probable cause but higher than a mere subpoena.

**Requirements:**
- The government must offer "specific and articulable facts" showing there are reasonable grounds to believe that the records are "relevant and material to an ongoing criminal investigation."
- This is a lower standard than probable cause (required for a search warrant).
- No judicial finding of probable cause is required.

**What can be obtained:**
- Call detail records (CDRs)
- SMS metadata (sender, recipient, timestamp)
- Subscriber information (name, address, billing info)
- IP address assignment logs
- Cell tower and location records (contested, but generally allowed)
- Tower dumps (all devices associated with a specific tower during a time window)

**Not available via §2703(d):**
- Content of communications (requires warrant under §2703(a))
- Real-time location (requires warrant or Title III order)
- Real-time content (requires Title III order)

## Pen Register / Trap and Trace (18 U.S.C. §3121–3127)

### Overview

A Pen Register captures outgoing call information (numbers dialed). A Trap and Trace captures incoming call information (numbers calling the target). These are real-time metadata collection tools that do not capture content.

### Legal Standard

| Requirement | Detail |
|---|---|
| Authorization | Court order based on certification by law enforcement |
| Standard | The government certifies that the information likely to be obtained is "relevant to an ongoing criminal investigation" |
| Judicial role | Judge must issue the order if the certification is proper (minimal review) |
| Duration | 60 days, renewable |

### What Is Collected

- Numbers dialed from the target phone
- Numbers calling the target phone
- Duration of calls
- Timestamps
- Cell tower IDs (in some interpretations)

### What Is NOT Collected

- Call content (audio)
- SMS content or SMS metadata (ambiguous in some circuits)
- Location data (beyond cell tower ID — contested)
- Data session content

### Relationship to CALEA

CALEA requires carriers to have the technical ability to implement Pen Register/Trap and Trace intercepts. The authority to order the intercept comes from the Pen Register statute, not CALEA.

## Title III Wiretap (18 U.S.C. §2510–2522)

### Overview

Title III (also called the Wiretap Act) governs the real-time interception of the content of communications. It is the highest legal standard for surveillance and requires the most rigorous process.

### Requirements

| Requirement | Detail |
|---|---|
| Authorization | Court order from a federal or state judge |
| Standard | Probable cause to believe a crime has been or is being committed AND that communications about the crime will be intercepted AND normal investigative procedures have failed or are unlikely to succeed |
| Exhaustion requirement | The government must show why less intrusive methods (subpoenas, pen register, search warrants) are insufficient |
| Minimization | Intercepted communications unrelated to the crime must be minimized (not recorded or destroyed) |
| Duration | 30 days, renewable |
| Notice | Target must be notified within 90 days after the order expires (unless delayed notice is authorized) |

### What Can Be Intercepted

- Real-time call content (audio)
- Real-time SMS content
- Real-time data session content (including browsing, messaging app content)
- Real-time location (precise positioning)
- Real-time metadata (who, when, duration)

### Limitations

- Title III orders are time-consuming to obtain. Most law enforcement agencies use them only for major investigations.
- The minimization requirement reduces operational value.
- Encryption (Signal, WhatsApp) frustrates wiretap effectiveness. The government cannot decrypt content if the provider does not have the keys.
- Approximately 3,000–4,000 Title III orders are issued annually in the US (federal and state combined).

## Tower Dump Court Orders

### Overview

A tower dump is a court order compelling a carrier to produce records for ALL devices that connected to a specific cell tower (or set of towers) during a specific time window. It is not targeted at a specific subscriber or device.

### Legal Basis

Tower dumps are typically obtained under §2703(d) of the Stored Communications Act. The legal basis is that the records are "relevant and material to an ongoing investigation" because a crime occurred in the coverage area of the specified towers.

### What Is Returned

- IMSI and IMEI for every device that connected to the specified towers
- Timestamps for each connection (attach, handover, detach)
- Timing Advance values (indicating distance from tower)
- Call and SMS metadata for each device during the window
- Subscriber information (name, address) for devices with postpaid accounts

### Key Characteristics

| Characteristic | Detail |
|---|---|
| Scope | Not targeted. Every device in the area is collected. |
| Retention | Carriers may retain tower dump data indefinitely after responding to the order. |
| Privacy impact | Anyone in the area during the window is swept up, not just suspects. |
| Judicial oversight | The standard is §2703(d) ("specific and articulable facts"), not probable cause. |
| Duration | Typically 1–4 hours, but can extend to multiple days. |

## National Security Letters (NSL)

### Overview

National Security Letters are administrative subpoenas used by the FBI (and other intelligence agencies) to obtain subscriber records in national security investigations. They do not require judicial approval.

### Key Characteristics

| Characteristic | Detail |
|---|---|
| Legal authority | Multiple statutes including 18 U.S.C. §2709 (SCA NSL) |
| Standard | "Relevant to an authorized national security investigation" |
| Judicial review | None required. Submit to FBI, not a judge. |
| Gag order | Automatic — the recipient (carrier, ISP) cannot disclose the NSL's existence. |
| Data obtainable | Subscriber name, address, length of service, toll billing records (not content). |
| Frequency | Thousands issued per year. |

## Legal Standard Summary

| Data Type | Legal Instrument | Standard | Historical or Real-Time |
|---|---|---|---|
| Subscriber info (name, address) | Subpoena | Relevance | Historical |
| Subscriber info (enhanced) | §2703(d) order | Specific and articulable facts | Historical |
| Call detail records | §2703(d) order | Specific and articulable facts | Historical |
| SMS metadata | §2703(d) order | Specific and articulable facts | Historical |
| Cell tower location (historical) | §2703(d) or warrant (varies by circuit) | Specific and articulable facts or probable cause | Historical |
| Cell tower location (real-time) | Warrant or Title III | Probable cause | Real-time |
| GPS location (real-time) | Warrant (Supreme Court requirement) | Probable cause | Real-time |
| Toll records | NSL | National security relevance | Historical |
| Real-time metadata | Pen Register / Trap and Trace | Certification (low standard) | Real-time |
| Real-time content | Title III wiretap | Probable cause + exhaustion | Real-time |

## Practical Implications for Threat Modeling

| Your Scenario | Likely Legal Instrument | Risk Level |
|---|---|---|
| Normal citizen, no investigation | None | Very low |
| Suspect in local crime investigation | Subpoena to carrier for subscriber info, §2703(d) for CDRs | Medium |
| Suspect in federal investigation | §2703(d) + potentially Title III | High |
| National security target | NSL + FISA warrants | Very high |
| Someone else's investigation (collateral) | Tower dump (if in the area) | Low but real |

The key insight: the legal standard for obtaining your Phone A records is low. A §2703(d) order requires "specific and articulable facts" — a standard that most investigations meet easily. The records obtained include your name, address, call records, SMS metadata, and tower-level location data for up to 18 months.
