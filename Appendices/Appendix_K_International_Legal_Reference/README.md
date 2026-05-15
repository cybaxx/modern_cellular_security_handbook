# Appendix K: Legal Reference — International Jurisdictions

## Introduction

This appendix documents the legal frameworks governing law enforcement and intelligence access to phone data in the United Kingdom, European Union, Canada, and Australia. These four jurisdictions are the most relevant non-US legal environments for journalists, activists, and researchers using this handbook — collectively covering the majority of Five Eyes partners and the largest democratic legal markets outside the United States.

Appendix E covers US law. This appendix assumes familiarity with the US baseline and focuses on how each jurisdiction diverges from it. The divergences are often significant: Australia mandates two years of metadata retention and has a statutory encryption-assistance regime; the EU prohibits bulk carrier metadata retention after a series of CJEU rulings; Canada requires a warrant for ISP subscriber data in a way the US does not.

Two limitations apply throughout. First, this appendix covers the law as it stood on the document date. Surveillance law changes faster than almost any other area of statutory law — verify current text before relying on any specific provision. Second, classified or confidential implementing regulations may exist that modify the practical operation of these statutes; what is described here is the public legal framework.

---

## United Kingdom

### Primary Statutes

The UK's surveillance framework is primarily governed by two acts: the Investigatory Powers Act 2016 (IPA) and the residual Regulation of Investigatory Powers Act 2000 (RIPA). Data retention obligations are set by the Communications Data (Retention and Acquisition) Regulations 2018 (SI 2018/disposing of the former Data Retention and Investigatory Powers Act 2014, itself a replacement for the EU Data Retention Directive following its invalidation).

### Investigatory Powers Act 2016 — Key Powers

| Power | IPA Part/Chapter | Description | Oversight |
|---|---|---|---|
| Targeted interception | Part 2, Chapter 1 | Interception of content of specific individual's communications | Warrant signed by Secretary of State, then reviewed by Judicial Commissioner |
| Bulk interception | Part 6, Chapter 1 | Mass interception of overseas-related communications | Secretary of State warrant + Judicial Commissioner |
| Equipment interference (targeted) | Part 5 | "Hacking warrants" — access to devices, networks, or software | Secretary of State + Judicial Commissioner |
| Equipment interference (bulk) | Part 6, Chapter 3 | Mass device exploitation | Secretary of State + Judicial Commissioner |
| Targeted communications data | Part 3 | Acquisition of specific subscriber's metadata | Designated senior officer (internal authorisation); judicial approval for certain categories |
| Bulk communications data | Part 6, Chapter 2 | Acquisition of large datasets of metadata | Secretary of State + Judicial Commissioner |
| National Security Notices | Part 9, Chapter 2 | Secret orders compelling providers to maintain or modify technical capabilities | Secretary of State only; no judicial review at issuance |

### Internet Connection Records (ICRs)

The IPA introduced Internet Connection Records — a data category with no direct US equivalent. An ICR captures the destination of every internet connection made by a device: which websites or services were visited, at what time, and for how long. It does not capture full browsing history (specific URLs within a site) but does capture the domain or IP contacted.

Retention period: **12 months** under the 2018 Regulations.

This is materially more granular than US Call Detail Records. US CDRs show who was called; UK ICRs show which websites were visited. The practical implication for the two-phone strategy is addressed in the final section.

### Communications Data Retention Requirements

| Data Category | Retention Period | Legal Basis |
|---|---|---|
| Internet Connection Records (ICRs) | 12 months | Communications Data (Retention and Acquisition) Regulations 2018 |
| Call Detail Records (CDRs) | 12 months | Same |
| SMS metadata | 12 months | Same |
| Subscriber identity (name, address) | 12 months | Same |
| Cell location records | 12 months | Same |
| IP address assignment logs | 12 months | Same |

### National Security Notices

National Security Notices (NSNs) under IPA Part 9, Chapter 2 are the UK equivalent of US National Security Letters. Key characteristics:

- Issued by the Secretary of State, not a court
- Recipient is prohibited from disclosing existence of the notice
- No judicial review at the point of issuance (Judicial Commissioners conduct retrospective review)
- Can compel providers to maintain interception capabilities, retain data beyond standard periods, or modify their technical architecture

Unlike NSLs, NSNs are not limited to a specific subscriber's records — they can impose systemic capability requirements on an entire provider.

### Critical Difference from US Law

The UK has no constitutional equivalent of the Fourth Amendment. The "reasonable expectation of privacy" doctrine from *Katz v. United States* (1967) does not apply. Article 8 of the European Convention on Human Rights (ECHR) provides a privacy right, but:

- The IPA was specifically designed to satisfy the Article 8 proportionality test
- Metadata is afforded substantially less protection than content
- The third-party doctrine equivalent is even broader: data held by a carrier is accessible with significantly lower process than content

The Investigatory Powers Tribunal (IPT) provides oversight of complaints, but it is not a prior-restraint mechanism.

---

## European Union

### Jurisdictional Note

EU law applies to member states directly (regulations) or through transposition (directives). Surveillance law sits at the intersection of EU-level instruments and national-level implementing legislation. What follows describes the EU framework; member states may implement it differently within permitted margins.

### GDPR and Its Limits

The General Data Protection Regulation (EU 2016/679) is the world's most comprehensive commercial data protection law. It governs how companies collect, process, and retain personal data. What it does **not** govern is equally important:

| Scope | GDPR Applies? | Governing Instrument Instead |
|---|---|---|
| Commercial data collection (advertising, analytics) | Yes | GDPR |
| Carrier billing and service data | Yes | GDPR + ePrivacy Directive |
| Law enforcement access to commercial data | No | Law Enforcement Directive (LED) |
| National security / intelligence collection | No | Member state law (outside EU competence) |
| Cross-border law enforcement data sharing | Partially | LED + individual MLATs |

GDPR rights — access, erasure, portability, objection — are suspended when law enforcement exercises them under LED authority. A person cannot invoke GDPR to compel deletion of data held by police.

### Law Enforcement Directive (LED) — 2016/680

The LED governs how police and prosecutors collect, process, and retain personal data. Key provisions:

| Provision | Article | Requirement |
|---|---|---|
| Purpose limitation | Art. 4(1)(b) | Data collected for law enforcement must be used only for the specific purpose collected |
| Data minimisation | Art. 4(1)(c) | Only data necessary for the purpose may be retained |
| Retention limits | Art. 5 | Data must be deleted when no longer necessary; periodic review required |
| Distinction of data subjects | Art. 6 | Police must distinguish suspects from witnesses, victims, and third parties |
| Sensitive categories | Art. 10 | Special categories (race, religion, health) require additional safeguards |
| Individual rights | Arts. 14–18 | Rights of access, rectification, erasure — exercisable against law enforcement |

### Data Retention — CJEU Case Law Sequence

The Court of Justice of the EU (CJEU) has progressively restricted bulk metadata retention across three landmark rulings:

| Case | Year | Holding |
|---|---|---|
| *Digital Rights Ireland v. Minister for Communications* (C-293/12) | 2014 | Invalidated the EU Data Retention Directive (2006/24/EC) — bulk retention of all subscriber metadata by all carriers for 6–24 months was disproportionate and violated EU Charter Arts. 7 and 8 |
| *Tele2 Sverige AB v. Post- och telestyrelsen; Watson v. Secretary of State* (C-203/15, C-698/15) | 2016 | National laws requiring general and indiscriminate retention of traffic and location data by carriers are incompatible with EU law; only targeted retention for serious crime is permissible |
| *La Quadrature du Net v. Premier ministre* (C-511/18, C-512/18, C-520/18) | 2020 | Reaffirmed Tele2/Watson; general retention prohibited even for national security unless facing serious threat; IP address retention for serious crime and child abuse permitted under strict conditions; real-time traffic data access for national security requires prior review |

**Current status:** EU member state carriers cannot lawfully impose general bulk metadata retention equivalent to US or UK regimes. Permitted retention is targeted, time-limited, and predicated on serious crime or specific national security threats. Traffic and location data outside these categories must be deleted as a matter of EU law.

### Notable Member State Exceptions

| Country | Instrument | Practice |
|---|---|---|
| France | SREN (loi visant à sécuriser et réguler l'espace numérique, 2024); CNR surveillance framework | Broad algorithmic surveillance authority for terrorism; real-time access to network metadata without prior judicial authorisation in some circumstances |
| Germany | §100g StPO (Strafprozessordnung) | Court-ordered traffic data collection for serious crime; Federal Constitutional Court (BVerfG) has imposed proportionality requirements narrowing scope |
| Sweden | FRA Law (Lag om signalspaning, 2008) | Signals intelligence collection at internet exchange points — bulk interception of cross-border communications |

### Practical Difference from US

An EU carrier operating in compliance with post-*La Quadrature* CJEU case law retains substantially less metadata than a US or UK carrier. ISP-layer attacks (reconstructing network activity from carrier records) are weaker against a target in France or Germany than against a target in the United States or United Kingdom. However, GDPR protections do not protect against law enforcement access — and national security operations fall outside EU law entirely.

---

## Canada

### Primary Statutes

| Statute | Scope |
|---|---|
| Criminal Code, Part VI (ss. 183–196) | Interception of private communications — warrant required for content |
| Privacy Act (RSC 1985, c. P-21) | Federal government handling of personal information |
| Personal Information Protection and Electronic Documents Act (PIPEDA) / Consumer Privacy Protection Act (Bill C-27) | Commercial data protection |
| National Security Act, 2017 (Bill C-59) | CSE (Communications Security Establishment) foreign intelligence and cybersecurity powers |
| Canadian Security Intelligence Service Act (CSIS Act, RSC 1985, c. C-23) | Domestic intelligence collection |

### Interception of Private Communications — Criminal Code Part VI

Interception of the content of private communications requires a judicial warrant under Criminal Code s. 186. Requirements:

| Requirement | Criminal Code Provision | Standard |
|---|---|---|
| Judicial authorization | s. 186(1) | Superior court judge must be satisfied there are reasonable grounds to believe an offence has been or will be committed and that interception will afford evidence |
| Named persons or place | s. 186(4)(b) | Warrant must identify person(s) whose communications will be intercepted or the place |
| Duration | s. 186(4)(e) | Maximum 60 days; renewable |
| Reporting | s. 195 | Annual reports to Parliament on number of authorizations |

### R v Spencer — The ISP Subscriber Warrant Requirement

The Supreme Court of Canada's ruling in *R v Spencer* (2014 SCC 43) fundamentally differs from the US third-party doctrine established in *Smith v. Maryland* (1979):

| Jurisdiction | Rule | Legal Basis |
|---|---|---|
| United States | No reasonable expectation of privacy in subscriber identity voluntarily disclosed to ISP; warrant not required | *Smith v. Maryland* (1979); third-party doctrine |
| Canada | Subscriber identity (IP address to name) carries a reasonable expectation of privacy; production order or warrant required | *R v Spencer* (2014 SCC 43); s. 8 Charter |

In practice: Canadian law enforcement cannot obtain ISP subscriber records (linking an IP address to a name and address) without judicial process. This closes one of the most commonly exploited gaps in US law enforcement practice.

### Data Retention — No Mandatory Retention Law

Canada has no mandatory carrier data retention law. Unlike the US (18 months for some categories), UK (12 months), or Australia (24 months), Canadian carriers retain data at their own discretion according to their internal policies. This means:

- Retention periods vary by carrier and data category
- Historical metadata records may not exist if the carrier does not retain them
- Law enforcement must act quickly to preserve records via production order before they are deleted

### CSE Powers Under Bill C-59

The Communications Security Establishment (CSE) is Canada's signals intelligence agency (equivalent to NSA/GCHQ/ASD). Under Bill C-59 (National Security Act 2017):

| Power | Authorization Required |
|---|---|
| Foreign intelligence collection | Ministerial authorization |
| Cybersecurity assistance to federal departments | Ministerial authorization |
| Active and defensive cyber operations | Ministerial authorization + Attorney General |
| Assistance to CSIS or RCMP | Requires Federal Court warrant for activities that affect Canadians |

Canadian persons and permanent residents are legally protected from being the targets of CSE collection. Collection that incidentally captures Canadian communications requires specific handling procedures.

---

## Australia

### Primary Statutes

| Statute | Scope |
|---|---|
| Telecommunications (Interception and Access) Act 1979 (TIA Act) | Primary interception and stored communications law |
| Australian Security Intelligence Organisation Act 1979 (ASIO Act) | Domestic intelligence collection |
| Intelligence Services Act 2001 | ASD (Australian Signals Directorate) foreign intelligence |
| Telecommunications and Other Legislation Amendment (Assistance and Access) Act 2018 (AAA) | Technical assistance framework — encryption and device access |
| Privacy Act 1988 | Commercial data protection |

### Mandatory Metadata Retention — TIA Act Part 5-1A

Australia's 2015 amendments to the TIA Act imposed the most aggressive mandatory metadata retention regime in the Five Eyes:

| Data Category | Retention Period | TIA Act Reference |
|---|---|---|
| Call records (parties, duration, time) | 2 years | s. 187AA, Item 1 |
| SMS/MMS metadata (parties, time) | 2 years | s. 187AA, Item 2 |
| IP address assignment logs | 2 years | s. 187AA, Item 3 |
| Email metadata (parties, time, size) | 2 years | s. 187AA, Item 4 |
| Cell location at call start/end | 2 years | s. 187AA, Item 5 |
| Subscriber account information | 2 years | s. 187AA, Item 6 |

Access to retained metadata does not require a warrant for most agencies — an authorisation from a senior officer within the agency is sufficient for criminal investigation purposes (TIA Act s. 178). Content interception requires a warrant (TIA Act Part 2-2).

### Assistance and Access Act 2018 (AAA)

The AAA created three tiers of technical assistance that can be compelled from communications providers:

| Instrument | AAA Provision | Description | Voluntary? | Judicial Review? |
|---|---|---|---|---|
| Technical Assistance Request (TAR) | s. 317C | Request for voluntary assistance with specific capability | Yes — voluntary | No |
| Technical Assistance Notice (TAN) | s. 317E | Notice compelling use of existing capabilities to assist | No — compelled | Limited review |
| Technical Capability Notice (TCN) | s. 317G | Notice compelling provider to build new capability | No — compelled | Attorney-General + industry panel |

A TCN can require a provider to remove "a form of electronic protection" — i.e., weaken or bypass encryption. Providers subject to a TCN are prohibited from disclosing its existence. The AAA applies to any provider with Australian users, including offshore VPN providers and encrypted messaging services with Australian customers.

### ASIO Warrant Powers

The ASIO Act allows ASIO to obtain warrants for surveillance activities that would otherwise require a court order:

| Warrant Type | Issuing Authority | Scope |
|---|---|---|
| Computer access warrant | Attorney-General | Access to a specific computer or network |
| Surveillance device warrant | Attorney-General | Installation of listening or tracking devices |
| Named person warrant | Attorney-General | Comprehensive surveillance of a named individual |
| Questioning warrant | Federal Court | Compelled questioning of a person without suspicion of offence |

ASIO warrants are issued by the Attorney-General, not a court — though judicial officers act as an additional safeguard for questioning warrants. There is no requirement for ASIO to establish probable cause in the criminal law sense.

---

## Comparative Table — Five Jurisdictions

| Criterion | United States | United Kingdom | European Union | Canada | Australia |
|---|---|---|---|---|---|
| Mandatory carrier data retention period | 18 months (some categories, CVSA 2022) | 12 months (IPA / 2018 Regs) | Prohibited in general; targeted only post-CJEU | None (carrier discretion) | 24 months (TIA Act s. 187AA) |
| Warrant required for content interception? | Yes (Title III / 18 U.S.C. §2518) | Yes (IPA s. 19) — Secretary of State + Judicial Commissioner | Yes (member state law; LED Art. 4) | Yes (Criminal Code s. 186) | Yes (TIA Act Part 2-2) |
| Warrant required for metadata? | No for historical (§2703(d) order sufficient); Yes for real-time CSLI (*Carpenter*) | No for targeted CDR/ICR access (designated officer authorisation) | Generally yes under LED; national security may differ | Yes for subscriber identity (*R v Spencer*); production order for records | No — senior officer authorisation sufficient (TIA Act s. 178) |
| Bulk collection permitted? | Yes (Section 702 FISA, EO 12333) | Yes (IPA Part 6) | No (prohibited post-*Digital Rights Ireland*) | Limited — CSE foreign intelligence; not domestic | Limited — ASD foreign signals |
| Encryption backdoor / assistance law? | No (CALEA excludes OTT; no TCN equivalent) | Yes — National Security Notices under IPA Part 9 | No EU-level law; proposed (Chat Control) | No | Yes — AAA 2018, including TCN mechanism |
| Secret orders with gag (NSL equivalent)? | Yes — National Security Letters (18 U.S.C. §2709) | Yes — National Security Notices (IPA Part 9) | No EU-level instrument; national security law varies | Limited — CSIS Act judicial warrants are sealed | Yes — TAN/TCN non-disclosure obligation (AAA s. 317ZF) |
| ISP subscriber identity (IP to name) requires warrant? | No (*Smith v. Maryland* third-party doctrine) | No (designated officer authorisation) | Varies by member state; post-*La Quadrature* stricter | Yes (*R v Spencer* 2014 SCC 43) | No |

---

## Practical Implications for the Two-Phone Strategy

### United Kingdom

The ICR regime is the most operationally significant difference from US law. UK carriers retain a record of every internet destination contacted — not just phone calls — for 12 months. A UK mobile carrier's retained data includes which VPN endpoints were contacted, when, and for how long. This means the ISP-layer record in the UK is closer in granularity to a full browsing log than to a US CDR. The two-phone strategy's network separation is effective against content interception but does not prevent ICR-based confirmation that a device connected to a VPN or Tor at a specific time. National Security Notices also mean that a UK-based VPN provider may have been secretly compelled to retain additional data or provide access — with no public disclosure possible.

### European Union

The post-*La Quadrature* environment means a compliant EU carrier retains far less metadata than US or UK carriers. ISP-layer reconstruction of communications patterns is correspondingly harder — the data may simply not exist. This strengthens the two-phone strategy's baseline: if the carrier has deleted traffic metadata under GDPR + CJEU requirements, law enforcement cannot subpoena what does not exist. The significant caveat is that GDPR protections do not apply to law enforcement access, national security collection falls outside EU law entirely, and member states like France and Sweden maintain broader surveillance authorities than the EU framework requires.

### Canada

*R v Spencer* means that the IP-to-identity linkage that is trivially available to US law enforcement requires judicial process in Canada. The absence of mandatory retention law means historical carrier records may be sparse or nonexistent beyond the carrier's internal retention schedule. The two-phone strategy benefits from both: the legal standard for subscriber identity is higher, and the factual record available to investigators is thinner. The risk vector in Canada is more likely to be device seizure and forensic analysis than carrier-record reconstruction — shifting the operational priority toward device security over network separation.

### Australia

Australia presents the most aggressive statutory environment in the Five Eyes for the purposes of this handbook. The 24-month mandatory retention period (twice the US 18-month baseline) means two years of call records, IP assignments, and location data at call start and end are available without a warrant. More critically, the AAA's Technical Capability Notice mechanism means any technology provider with Australian users — including VPN services, encrypted messaging applications, and device manufacturers — may have been secretly compelled to build interception capability or remove encryption protections, with a statutory prohibition on disclosure. The two-phone strategy's reliance on encrypted applications and VPNs cannot be verified as effective if any component in the chain has received a TCN. Australian-resident users of this handbook should treat any commercially operated VPN or messaging service as potentially compromised at the infrastructure level and preference self-hosted, open-source solutions where the software supply chain can be independently audited.
