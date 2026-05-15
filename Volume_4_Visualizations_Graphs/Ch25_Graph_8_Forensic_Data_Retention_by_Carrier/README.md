# Graph 8: Forensic Data Retention by Carrier (US vs EU vs CN)

## Purpose

This bar chart compares how long mobile carriers in three jurisdictions retain forensic data that can be used to locate, identify, and track a phone. The graph is essential for understanding the temporal window of vulnerability: data that still exists on a carrier's servers is data that can be subpoenaed. Once data is deleted (per retention policy), it becomes unavailable to even the most determined adversary.

## The Graph

```
Data Type               US Carrier     EU Carrier     CN Carrier
                        (Verizon/TMO/  (GDPR limits)  (State access)
                        AT&T)
─────────────────────────────────────────────────────────────────
Call detail records     ████████ 18mo  ████ 6mo       ██████████████ indefinite
SMS metadata           ████████ 18mo  ████ 6mo       ██████████████ indefinite
Tower dumps            ████████ 12mo  ██████ 12mo    ██████████████ indefinite
Timing Advance (TA)    ██████ 6mo     ███ 3mo        ██████████████ indefinite
5G Multi-RTT           ████ 3mo      ██ 1mo         ██████████████ indefinite
Wi-Fi BSSID logs       ███ 90d       ██ 30d         ██████████████ indefinite
IP assignment logs     ████████ 18mo ████ 6mo       ██████████████ indefinite
DNS queries (if kept)  ██ 30-90d     █ 7-14d        ██████████████ indefinite
─────────────────────────────────────────────────────────────────
Total exposure risk:    HIGH          MEDIUM         EXTREME
                        (18mo window) (6mo window)   (permanent)
```

## Jurisdiction Analysis

### United States: High Risk (18-Month Retention Window)

US carriers retain the widest range of data for the longest periods among Western jurisdictions. The retention periods shown are typical for major carriers (Verizon, T-Mobile, AT&T) and are driven by:

- **No comprehensive federal data retention law**: Unlike the EU, the US does not mandate specific retention periods. Carriers retain data based on their own business needs (billing disputes, fraud investigation, network optimization) and voluntary cooperation with law enforcement.
- **Section 2703 of the Stored Communications Act**: Allows the government to compel disclosure of stored communications and records with a subpoena (for basic subscriber information), a court order (for logs up to 180 days), or a warrant (for content).
- **Industry practice**: Most US carriers have converged on 18 months for CDRs and IP assignment logs, 12 months for tower dumps, and shorter periods for higher-resolution data types like Timing Advance and 5G positioning measurements.

The 18-month retention of CDRs means that an adversary can subpoena Phone A's location history from a year and a half ago. For a user who carried Phone A to a sensitive location 17 months ago, that data is still available. The two-phone strategy must assume that all historical data is permanent for legal purposes.

### European Union: Medium Risk (6-Month Retention Window)

EU data retention is shaped by:

- **GDPR (General Data Protection Regulation)**: Requires data minimization and limits retention to what is "necessary" for the stated purpose. Carriers must justify each data type's retention period.
- **ePrivacy Directive and national implementations**: Some EU member states have data retention mandates (typically 6-12 months), but these have been challenged in the Court of Justice of the European Union. The CJEU has repeatedly struck down blanket data retention mandates as disproportionate (Digital Rights Ireland, Tele2 Sverige, La Quadrature du Net).
- **Practical results**: EU carriers typically retain CDRs and IP assignment logs for 6 months, tower dumps for 12 months (for billing and network planning), and higher-resolution data (TA, 5G Multi-RTT) for shorter periods. DNS query retention is rare and short-lived.

The 6-month window provides a meaningful but limited protection. If the user can avoid carrying Phone A to sensitive locations for 6 months, historical data may have been deleted. However, the adversary may still obtain 6 months of location history, which may be sufficient for pattern analysis.

### China: Extreme Risk (Indefinite Retention)

Chinese carriers (China Mobile, China Unicom, China Telecom) operate under:

- **The Cybersecurity Law of 2017**: Requires carriers to retain logs for at least 6 months and to cooperate with state security investigations.
- **The National Intelligence Law of 2017**: Requires carriers to support state intelligence activities. There is no meaningful limitation on retention for national security purposes.
- **The Social Credit System**: Carrier data is integrated into the national social credit database. Call records, location data, and messaging metadata are retained permanently and are accessible to multiple government agencies.
- **Practical reality**: "Indefinite" retention means data is kept as long as the carrier operates. There is no deletion timeline. Historical data from years or decades ago remains accessible to the Ministry of State Security (MSS) and other state actors.

For users operating in or transiting through China, the assumption must be that all carrier data is permanent and accessible to the state. The two-phone strategy provides minimal protection because both phones' carrier data is retained indefinitely.

## Data Type Analysis

### Call Detail Records (CDRs)

CDRs contain: calling party number, called party number, call start time, call duration, cell tower ID at call start, and sometimes cell tower ID at call end.

**Forensic value**: High. CDRs reveal who the user communicates with, for how long, and approximately where they were during the call. Pattern analysis over 18 months (US) can identify contacts, routines, and sensitive locations.

**Retention**: 18 months (US), 6 months (EU), indefinite (CN).

### SMS Metadata

SMS metadata includes: sender number, recipient number, timestamp, and message length. Content is not included in metadata (content requires a warrant), but metadata alone reveals communication patterns.

**Forensic value**: High. SMS metadata can identify close contacts, relationship patterns, and timing of communications. In bulk, it can reconstruct social networks.

**Retention**: 18 months (US), 6 months (EU), indefinite (CN).

### Tower Dumps

A tower dump is a record of every IMSI that connected to a specific cell tower during a specific time window. Carriers retain these for billing and network optimization.

**Forensic value**: Very high. Tower dumps reveal who was in a specific area at a specific time. This is the primary tool for placing a suspect at a location.

**Retention**: 12 months (US), 12 months (EU), indefinite (CN).

### Timing Advance (TA)

TA data measures the distance from the phone to the tower with precision of approximately 50-150 meters. Available from standard 4G signaling messages.

**Forensic value**: High for geolocation. TA can place a phone within a specific range ring around a tower, narrowing the possible location from kilometers (cell ID alone) to hundreds of meters.

**Retention**: 6 months (US), 3 months (EU), indefinite (CN).

### 5G Multi-RTT

Multi-RTT positioning provides 1-10 meter accuracy by measuring signal propagation time from the phone to multiple transmission points.

**Forensic value**: Extremely high. Near-GPS precision from the network itself, without any user consent or app involvement. Subject to short retention in Western jurisdictions (3 months US, 1 month EU), but indefinite in China.

**Retention**: 3 months (US), 1 month (EU), indefinite (CN).

### Wi-Fi BSSID Logs

BSSID logs record which Wi-Fi access points the phone has seen (from probe request/beacon exchange). These can be cross-referenced with geolocation databases.

**Forensic value**: High for passive location tracking. Can identify visits to specific establishments (coffee shops, hotels, offices).

**Retention**: 90 days (US), 30 days (EU), indefinite (CN).

### IP Assignment Logs

Carriers log which IP address was assigned to which IMSI at which time. This links the phone's cellular identity to its internet activity.

**Forensic value**: Essential for correlating cellular activity with internet activity. Links Phone A to specific websites and services.

**Retention**: 18 months (US), 6 months (EU), indefinite (CN).

### DNS Queries

DNS query logs (if kept) reveal every domain the phone resolves. Most carriers do not systematically log DNS, but if they do, the data provides a comprehensive internet browsing history.

**Forensic value**: Extremely high — a complete record of every website visited. Retention is short or nonexistent in Western jurisdictions due to privacy concerns.

**Retention**: 30-90 days (US), 7-14 days (EU), indefinite (CN).

## Forensic Implication for Legal Process Timing

The retention window determines the adversary's timeline for data collection:

- **In the US**: An adversary has up to 18 months to subpoena Phone A's location data. The user would need to stop carrying Phone A for 18 months before their historical location data becomes unavailable. Most investigations complete within 18 months, making the retention window effectively unlimited from the adversary's perspective.

- **In the EU**: The 6-month window provides a meaningful but tight defense. A user who can avoid sensitive locations for 6 months may have their historical data deleted. However, the adversary who initiates an investigation within the 6-month window can still obtain comprehensive records.

- **In China**: There is no defense through time. Data is permanent. Sensitive locations visited years ago remain accessible to state security investigations.

## Strategic Implications

1. **Assume all data is permanent for legal purposes.** The retention windows may shrink (due to legal challenges or corporate policy changes) or expand (due to new data retention laws). The conservative assumption for any privacy strategy is that historical data will be available to a determined adversary.

2. **Time is not a reliable defense.** Even in the EU with 6-month retention, many investigations complete within the window. The US 18-month window is effectively unlimited for most investigations.

3. **Higher-resolution data types have shorter retention.** Timing Advance and 5G Multi-RTT data are more precise but retained for shorter periods (3-6 months in the US, 1-3 months in the EU). An adversary who acts quickly can obtain near-GPS precision location data. An adversary who delays may only obtain cell-ID level data.

4. **China is a no-win scenario for carrier data privacy.** Any phone with a Chinese carrier generates permanent records accessible to the state. The two-phone strategy provides no protection against this.
