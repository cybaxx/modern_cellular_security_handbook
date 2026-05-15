# Appendix C: Carrier Data Retention Policies

## Introduction

The effectiveness of any privacy strategy depends critically on how long carriers retain subscriber data. This appendix documents the known retention periods for major carriers in the United States, European Union, and China.

Note that retention periods are not always published. Some carriers disclose them in privacy policies or in response to lawful process. Others do not. Where precise figures are unavailable, we provide estimates based on forensic experience, published research, and freedom of information requests.

## United States Carriers

US carriers generally retain data for 6 to 18 months, depending on the data type. Retention is driven by business requirements (billing, fraud detection) and legal mandates (CALEA, ECPA). There is no federal data retention mandate comparable to the EU's, but carriers retain data voluntarily to avoid losing it when law enforcement requests it.

### Verizon

| Data Type | Retention Period | Notes |
|---|---|---|
| Call detail records | Up to 18 months | Includes IMSI, IMEI, called number, duration, timestamp |
| SMS metadata | Up to 18 months | Includes sender, recipient, timestamp |
| Data session logs | Up to 18 months | IP assignment, session start/end, bytes transferred |
| Location data (Cell ID, TA) | Up to 12 months | For active subscribers |
| Tower dumps | Up to 12 months | Maintained in response to specific legal requests |
| 5G positioning data | Unknown | Newer data type, retention policy not yet standardized |
| Wi-Fi BSSID logs | Up to 90 days | From Verizon Wi-Fi hotspots |
| DNS queries | Up to 30–90 days | Unless using Verizon's DNS services |
| Subscriber info (name, address) | Indefinite | Retained for billing and legal compliance |
| Prepaid subscriber info | Min required by law | Prepaid may require less data if cash-purchased |

### T-Mobile

| Data Type | Retention Period | Notes |
|---|---|---|
| Call detail records | Up to 18 months | T-Mobile, including former Sprint accounts |
| SMS metadata | Up to 18 months | |
| Data session logs | Up to 18 months | IP assignment logs |
| Location data | Up to 12 months | Cell ID and timing advance |
| Tower dumps | Up to 12 months | |
| 5G positioning data | Unknown | T-Mobile was first to deploy 5G SA in US |
| Wi-Fi BSSID logs | Up to 90 days | Via T-Mobile Wi-Fi calling |
| DNS queries | Varies | Using T-Mobile DNS servers |
| Subscriber info | Indefinite | |
| Prepaid subscriber info | Min required by law | Prepaid is anonymous if cash-purchased |

### AT&T

| Data Type | Retention Period | Notes |
|---|---|---|
| Call detail records | Up to 18 months | AT&T publishes a transparency report |
| SMS metadata | Up to 18 months | |
| Data session logs | Up to 18 months | |
| Location data | Up to 12 months | Cell ID and timing advance |
| Tower dumps | Up to 12 months | |
| 5G positioning data | Unknown | AT&T 5G deployment includes SA in select markets |
| Wi-Fi BSSID logs | Up to 90 days | Via AT&T Wi-Fi hotspots |
| DNS queries | Varies | |
| Subscriber info | Indefinite | |
| Prepaid (Cricket Wireless) | Min required by law | Cricket is AT&T's prepaid brand |

### Legal Access to US Carrier Data

US carriers receive thousands of legal requests per month. The standard process is:

- **Subpoena:** Basic subscriber info (name, address, phone number). Standard of proof is relevance.
- **§2703(d) order:** Historical records (CDRs, location data, IP logs). Standard is "specific and articulable facts."
- **Title III warrant:** Real-time content and location. Standard is probable cause.
- **CALEA intercept:** Real-time metadata and location. Carrier infrastructure tap.

Most carriers have dedicated legal compliance teams and automated systems for fulfilling orders. Response times range from hours (emergency requests) to weeks (standard orders).

## European Union Carriers (Under GDPR)

EU carriers operate under stricter data protection rules. The GDPR limits data collection to what is necessary and imposes retention limits. However, member states have data retention laws that sometimes conflict with GDPR requirements.

### General EU Retention Framework

| Data Type | Typical Retention Period | Legal Basis |
|---|---|---|
| Call detail records | Up to 6 months | Most EU countries require 6 months under national data retention laws |
| SMS metadata | Up to 6 months | |
| Data session logs | Up to 6 months | |
| Location data (Cell ID) | Up to 3–6 months | |
| 5G positioning data | Up to 1–3 months | Newer, shorter retention |
| Wi-Fi BSSID logs | Up to 30 days | |
| DNS queries | Up to 7–14 days | GDPR minimum, some countries longer |
| IP assignment logs | Up to 6 months | |
| Subscriber info | Duration of contract + legal hold | |

### Note on EU Data Retention Laws

The European Court of Justice (CJEU) ruled in 2014 (Digital Rights Ireland) and 2020 (Tele2 Sverige) that blanket data retention is incompatible with EU fundamental rights. However, several member states (UK prior to Brexit, France, Germany with restrictions, Netherlands) have maintained or reintroduced targeted retention laws. The situation varies by country.

### Notable EU Carrier Policies

- **Deutsche Telekom (Germany):** 4–10 weeks for traffic data, longer for billing data. Germany's data retention law is currently suspended pending CJEU review.
- **Orange (France):** 12 months for all traffic data under French law. France has one of the most aggressive data retention regimes in the EU.
- **Vodafone (UK, EU):** 6 months in UK under Investigatory Powers Act. In EU, follows local laws.
- **Telefonica (Spain):** 12 months for traffic data under Spanish law.

### GDPR Rights Applicable to Carrier Data

| Right | Description |
|---|---|
| Article 15 (Right of access) | Request all personal data held by the carrier, including location records |
| Article 16 (Right to rectification) | Correct inaccurate data |
| Article 17 (Right to erasure) | Request deletion of data not required for legal compliance |
| Article 18 (Right to restriction) | Restrict processing of disputed data |
| Article 20 (Right to portability) | Receive data in machine-readable format |
| Article 22 (Automated decisions) | Object to automated processing |

Filing a GDPR data subject access request with your carrier is the best way to determine exactly what data they retain about you.

## China Carriers

China has the most aggressive data retention regime among major economies. Carriers are required to retain all subscriber data indefinitely under multiple laws and regulations.

### China Mobile, China Unicom, China Telecom

| Data Type | Retention Period | Legal Basis |
|---|---|---|
| Call detail records | Indefinite | Telecommunications Regulations, Counter-Terrorism Law |
| SMS metadata | Indefinite | |
| Data session logs | Indefinite | |
| Location data (all methods) | Indefinite | Including Cell ID, TA, AoA, 5G positioning |
| Wi-Fi logs | Indefinite | |
| DNS queries | Indefinite | |
| IP assignment logs | Indefinite | |
| Subscriber info | Indefinite | Including government ID linked to all SIMs |
| Real-name registration data | Indefinite | Mandatory since 2013 for all SIMs |

### Real-Name Registration

Since 2013, China requires real-name registration for all SIM cards. This means:

- Every prepaid SIM must be registered with a government ID
- No anonymous cash purchases are possible
- Foreign visitors must present passports
- The carrier links every IMSI to a specific individual
- Data sharing with government agencies is mandatory

### Social Credit Integration

Carrier data in China is integrated with the Social Credit System. This means:

- Location history may affect credit scores
- Travel to certain areas may trigger alerts
- Communication patterns with specific individuals may be flagged
- Data is shared across government databases

### Legal Framework

- **Cybersecurity Law (2017):** Requires data localization and government access to data
- **Counter-Terrorism Law (2016):** Mandates data retention and real-name registration
- **Telecommunications Regulations:** Require carriers to retain all data indefinitely
- **National Intelligence Law (2017):** Requires companies to cooperate with intelligence agencies
- **Data Security Law (2021):** Expanded data retention requirements

## Data Retention Comparison Table

| Data Type | US (Verizon/TMO/AT&T) | EU (GDPR) | China |
|---|---|---|---|
| Call detail records | 18 months | 6 months | Indefinite |
| SMS metadata | 18 months | 6 months | Indefinite |
| Tower dumps | 12 months | 12 months | Indefinite |
| Timing Advance (TA) | 6 months | 3 months | Indefinite |
| 5G Multi-RTT | 3 months | 1 month | Indefinite |
| Wi-Fi BSSID logs | 90 days | 30 days | Indefinite |
| IP assignment logs | 18 months | 6 months | Indefinite |
| DNS queries | 30–90 days | 7–14 days | Indefinite |
| **Total exposure risk** | **HIGH** | **MEDIUM** | **EXTREME** |
| **Retention window** | **18 months** | **6 months** | **Permanent** |

## Forensic Implications

The retention period directly affects the privacy value of the burner strategy:

- **US:** Phone A data from 18 months ago can still be subpoenaed. A burner phone replaced every 90 days limits exposure to a 90-day window within the carrier's 18-month retention period.
- **EU:** Data is retained for less time, but GDPR requests can be filed to determine exactly what data is kept.
- **China:** Permanent retention means data never expires. This has implications for anyone traveling to or through China.

### Key Takeaway

The two-phone strategy must assume that all data generated by Phone A is permanent for legal purposes. Carriers retain data for months or years, and legal process can compel its disclosure long after the fact. Device rotation limits the window of available data but does not eliminate it.
