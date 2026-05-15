# Chapter 50: What Happens to the Data — ML and Data Science Analysis of Collected Signals

## The Gap in the Forensic Picture

Volumes 2 and 3 of this handbook document the collection layer in detail: what your phone transmits, what protocols expose, what carriers log, what is retained, and what legal instruments compel disclosure. That analysis answers the question *what is collected*. This chapter answers the question that naturally follows: *what is done with it*.

The gap matters. Knowing that a carrier retains IMSI, Cell ID, Timing Advance, and call duration records for 18 months tells you what is in the warehouse. It does not tell you what the analytical machinery built on top of that warehouse can produce. The answer to that second question — what adversaries can infer, correlate, and predict from the raw signals — is often far more alarming than the signals themselves.

This chapter covers the full lifecycle of collected data: from raw signals and carrier records through the data pipelines, feature engineering, and machine learning models that transform discrete observations into actionable intelligence. It addresses both the commercial surveillance ecosystem (data brokers, advertising platforms, location analytics companies) and the law enforcement and intelligence analytical layer. Where specific research or documented practices exist, they are cited. Where the analytical capability can be inferred from known inputs and standard data science methods, that inference is stated plainly.

The practical implication of this analysis is addressed at the end: which mitigations remain effective and which are defeated not by better collection but by better analysis.

---

## The Raw Signal Inventory

Before analyzing what ML models can do, it is worth stating explicitly what they have to work with. The following data types are routinely collected, retained, and available to adversaries at varying legal and technical thresholds:

| Signal Type | Source | Collection Threshold | Retention |
|---|---|---|---|
| IMSI / SUPI | Carrier core network | Any network connection | 6–18 months (US), varies (EU/international) |
| IMEI / PEI | Carrier core network | Any network connection | 6–18 months |
| Cell ID (ECGI/NCGI) | Carrier CDRs | Any network connection | 6–18 months |
| Timing Advance | Carrier CDRs | Any network connection | 6–18 months |
| Call duration and frequency | Carrier CDRs | Any call | 18 months+ |
| SMS metadata (sender, recipient, timestamp) | Carrier CDRs | Any message | 18 months+ |
| IP address assignments | Carrier RADIUS/DHCP logs | Any data session | 6–12 months |
| Application-layer metadata | App servers | App-dependent | Indefinite (varies) |
| Wi-Fi probe request logs | Commercial sensor networks, ISPs | Passive capture | Indefinite |
| Location data sold by carriers | Location aggregators | Continuous | Indefinite |
| App GPS location | Data brokers via SDK | App permission granted | Indefinite |
| Browser fingerprint | First-party and third-party trackers | Website visit | Indefinite |
| Ad impression logs | DSPs, ad exchanges | Ad served | 13 months+ (IAB standard) |

This inventory is not a thought experiment. Each row has documented collection and retention practices from court subpoenas, whistleblower disclosures, FOIA requests, and regulatory enforcement actions.

---

## Stage 1: Ingestion, Normalization, and Feature Engineering

Raw data as collected is not immediately useful for analysis. Before any ML model runs, the data undergoes substantial preprocessing. Understanding this stage explains why individual signals that seem harmless in isolation become powerful in combination.

### Schema Normalization

Carrier CDR data, app location pings, Wi-Fi observation records, and browser fingerprint logs each arrive in different formats, different timezones, and different identifier namespaces. The first analytical step is normalization: converting all timestamps to UTC, mapping identifiers (IMSI, cookie ID, advertising ID, IP address) to a common entity representation, and resolving geographic coordinates to a consistent spatial reference.

Commercial data brokers — Veraset, SafeGraph, Foursquare Analytics, Cuebiq (now Spectus) — have invested heavily in this normalization infrastructure. Their commercial value lies not in collecting data, which any SDK can do, but in maintaining the entity resolution graph that links an advertising ID on one app to a cookie on a different app, a Wi-Fi observation at a specific time, and an IP address at a specific hour. This graph is the central asset.

### Feature Engineering

Raw signals are transformed into features that machine learning models can process. The most important feature engineering steps in the cellular surveillance domain are:

**Temporal binning.** Raw timestamps are binned into intervals — typically 15-minute or 1-hour buckets — creating a time series of presence or activity for each entity. A phone that has 847 individual location pings between 9:00 AM and 5:00 PM at a consistent address is transformed into the feature `home_work_overlap = False`, `workplace = coordinates`, `commute_start_time = 08:47`.

**Dwell time extraction.** Sequential location pings at the same geographic area (within a clustering radius, typically 50–200 meters) are collapsed into dwell events: arrival time, departure time, and centroid location. This transformation reduces data volume by 60–90% while preserving the analytically significant information — where you stopped, for how long, and when.

**Trajectory segmentation.** Movement between dwell events is classified by speed and mode: stationary, walking, driving, transit. This is done using speed thresholds and map-matching against road network graphs. The resulting trajectory is a sequence of labeled segments rather than a stream of GPS coordinates.

**Communication graph construction.** Call and SMS records are transformed into an undirected weighted graph where nodes are phone numbers (or IMSIs) and edge weights represent frequency of communication. This is the social graph. A node with high degree centrality communicates with many people; a node with high betweenness centrality is a hub through which many communications pass; a node in a tight cluster has a strong inner social circle.

**Temporal regularity metrics.** Statistical measures of behavioral predictability are computed: variance in commute departure time, entropy of location visit distribution, regularity of contact patterns over time. These features are used in anomaly detection (identifying days when behavior deviates from the norm) and in behavioral fingerprinting (identifying that two devices have similar regularity patterns).

---

## Stage 2: Entity Resolution — Linking Identifiers Across Domains

The most powerful analytical operation in the surveillance pipeline is not prediction or classification. It is entity resolution: determining that two identifiers observed in different datasets refer to the same person.

### The Co-occurrence Graph

The foundational technique is co-occurrence: two identifiers that appear at the same place at the same time, repeatedly, are likely the same person or members of the same household. A residential IP address observed at 11:00 PM that corresponds to an IMSI on the cell tower covering that address, and a cookie ID on an e-commerce site accessed from that IP, are linked by co-occurrence. Each individual link has uncertainty. The accumulation of co-occurrence evidence across time and space drives the confidence arbitrarily high.

This technique is explicitly documented in the data broker industry. Foursquare (now Squire) describes their identity graph as cross-linking 50+ million devices across "signal sources" including GPS pings, Wi-Fi beacons, cellular handoffs, and IP addresses.[^1] The specific technical methods are proprietary, but the outputs and their accuracy are attested in commercial sales materials and validated in independent research.[^2]

### The Identity Graph at Scale

A commercial identity graph contains nodes of several types:
- Mobile advertising IDs (IDFA on iOS, GAID on Android)
- Cookie IDs (third-party cookies, first-party localStorage identifiers)
- Email address hashes (SHA-256 of lowercase email, used for matching across platforms)
- Phone number hashes
- IP addresses
- Wi-Fi network identifiers (BSSIDs)
- Carrier IMSI hashes (obtained via carrier data partnerships or MVNO operators)
- Home and work address hashes (inferred from location clustering)

Edges in the graph represent observed co-occurrence or known linking relationships (e.g., a user logged into the same platform from two different devices). Edge weights reflect confidence. A probabilistic graph traversal algorithm — typically a variant of connected components analysis or belief propagation — resolves which clusters of nodes represent the same physical person.

The result is that a new device, previously "anonymous," can be linked to an existing identity graph node with high confidence if it co-occurs with any of the existing node's linked identifiers. An advertising ID that has never seen your name is nonetheless linked to your home address within days of first use, via co-occurrence with a residential IP that was previously resolved to your identity via historical cookie data.

### Law Enforcement Entity Resolution

The commercial identity graph is available to law enforcement via commercial data purchases (documented in the context of Fog Data Science, Venntel, and similar companies selling to federal and state agencies).[^3] Law enforcement also performs entity resolution internally through tower dump analysis: a list of IMSIs observed at a tower during a window is cross-referenced against a list of IMSIs observed at another tower, with intersection sets identifying devices present at both times and places.

Documented case: In the 2021 January 6th Capitol breach investigation, DOJ prosecutors used tower dump data from multiple towers in downtown Washington D.C. combined with Google geofence warrant data to construct a location-based intersection analysis.[^4] This produced a list of devices present at multiple time-stamped locations, which was cross-referenced with subscriber identity data. The technique is entity resolution applied to a crime scene problem: who was in all these places at these times?

---

## Stage 3: Home and Work Location Inference

Before any behavioral modeling begins, the pipeline resolves two anchor points for each device: the inferred home location and the inferred work location. These anchors are the foundation of all subsequent analysis.

### The Standard Algorithm

The most widely used approach, described in foundational mobility research by Calabrese et al. (2010)[^5] and subsequent refinements, is:

1. Extract all location observations.
2. Identify the location with the highest dwell time between 10 PM and 6 AM (repeated across multiple days). This is the inferred home.
3. Identify the location with the highest dwell time between 9 AM and 5 PM on weekdays, excluding the home location. This is the inferred work.

This algorithm correctly infers home location from cellular CDR data with greater than 90% accuracy at the Census block level (roughly 100–400 meters).[^6] Work location accuracy is lower — approximately 75% at the same resolution — because work location is more variable. For high-frequency GPS data (app location pings), accuracy at the building level exceeds 95%.

### Why This Defeats Pseudonymity

A device with no name attached — only an advertising ID, or a fresh SIM with an unregistered IMSI — can still be attributed to a real person by identifying their home location. The home address is then cross-referenced against property records, voter registration, DMV records, or the commercial identity graph to recover identity. This is documented in academic research on de-anonymization of mobility datasets and in law enforcement practice.[^7]

The practical implication: any device that is present at your home address at night, repeatedly, over multiple days, is attributable to you. This is true regardless of whether the SIM is registered, whether the advertising ID has been reset, or whether a VPN is in use. The home anchor defeats pseudonymity at the infrastructure layer.

---

## Stage 4: Behavioral Profiling and Pattern Extraction

Once home and work anchors are established, the pipeline extracts a behavioral profile. This profile describes not just where a person goes, but when, how often, with what regularity, with whom, and what statistical patterns characterize their movement and communication.

### Routine Extraction

Human mobility is highly predictable. Research by Song et al. (2010) in *Science* demonstrated that human movement is predictable to 93% from historical location data — higher predictability than theoretical entropy calculations had suggested.[^8] This predictability means that a trained model can predict where a person will be at a future time with high accuracy. It also means that deviation from predicted behavior is itself an event of analytical interest.

The commercial application of routine extraction is advertising: knowing that you drive past a specific intersection at 8:15 AM every weekday enables a coffee chain to serve you a mobile ad at 8:00 AM on that route. The law enforcement application is the same pattern turned into a surveillance tool: knowing your routine enables prediction of when to conduct physical surveillance or when to request a geofence warrant covering your trajectory.

### Contact Pattern Analysis from CDRs

Call detail records produce a social graph. Standard social network analysis metrics applied to this graph include:

**Degree centrality**: how many distinct contacts a device communicates with. A high degree node communicates with many people; a low degree node with few.

**Communication frequency distribution**: some contacts are called daily; others weekly. The distribution of frequencies reveals which contacts are family (daily), which are work contacts (weekday business hours), which are social (evenings and weekends), and which are anomalous (one-time calls to numbers not in the existing network).

**Temporal patterns**: calls at 3 AM, calls only on specific days of the week, or calls exclusively on encrypted channels while all other communication uses plaintext — these are statistically distinctive and flag behavior that differs from the population norm.

**Network clustering**: people who know each other tend to call many of the same contacts. Identifying which cluster a device belongs to (family cluster, work cluster, activist group, criminal organization) is accomplished by community detection algorithms — Louvain method, Girvan-Newman, spectral clustering — that identify groups of nodes with dense intra-group connections.[^9]

These techniques are in standard use in law enforcement investigations. They are the same techniques used by intelligence agencies to map terrorist cells, by prosecutors to demonstrate conspiracy, and by commercial analytics companies to segment audiences. The algorithms are not secret. They are in every graduate data science curriculum.

### Risk Scoring and Anomaly Detection

Both commercial and government surveillance pipelines apply anomaly detection: identifying devices or individuals whose behavior deviates from their own historical pattern or from population norms. Anomalies flag as investigative leads.

In the commercial context, this is fraud detection: a credit card used in a location inconsistent with historical pattern triggers a hold. The same logic applies to surveillance: a phone that begins using encrypted messaging applications after exclusively using plaintext SMS, that starts visiting new locations outside its historical range, or that begins communicating with contacts not in its established network triggers a behavioral anomaly flag.

The specific risk scoring models used by law enforcement are not publicly documented in detail, but their existence is established by FBI records obtained under FOIA (particularly around the use of Babel Street and similar platforms)[^10] and by the academic literature on crime prediction models such as PredPol (now Geolitica) and ShotSpotter analytics.

---

## Stage 5: Social Graph Analysis and Guilt by Association

Communication metadata — who calls whom, how often, for how long — enables social graph analysis that can attribute suspicion to devices based entirely on their association with other devices, without evidence of individual wrongdoing.

### Link Analysis

Link analysis maps the network of communications around a target. Starting from one known or suspected device (the "seed"), the algorithm follows communication edges outward: who does the seed call? Who do those contacts call? What overlapping contacts exist? The result is a network diagram that identifies the seed's inner circle, their extended network, and any connecting paths to other targets of interest.

This technique is explicitly used in U.S. intelligence collection under Executive Order 12333 and in criminal investigation under the Electronic Communications Privacy Act. The NSA's MAINWAY database, disclosed by Edward Snowden, was a bulk call metadata record used for exactly this graph analysis — following two or three hops from a seed contact to map a complete communication network.[^11]

The two-phone strategy is designed to create a break in the social graph: Phone A has one contact network; Phone B has none. But social graph analysis can defeat this if:

1. Phone B ever communicates with any contact in Phone A's network.
2. Phone B is physically co-located with Phone A at any time (establishing a co-location edge in the graph, even without direct communication).
3. Phone B's behavioral pattern is correlated to Phone A's behavioral pattern by timing or location.

Any of these three conditions produces a graph edge linking the two devices, collapsing the separation.

### Second-Order Guilt by Association

A device that communicates frequently with a flagged device is itself elevated in risk score, regardless of the content of those communications. Research on predictive policing and social network-based suspicion has documented this pattern: individuals with no criminal behavior are flagged as high-risk because their contact graph includes someone who was previously investigated.[^12]

The operational implication is significant. It is not sufficient for your private device (Phone B) to have no independent connection to a target. If Phone B communicates with anyone who communicates with a flagged node in the surveillance graph, Phone B inherits elevated suspicion. The privacy compartment is not breached directly — it is approached from the outside.

---

## Stage 6: De-anonymization of Encrypted Traffic

Encryption protects the content of communications but not their metadata. Machine learning applied to encrypted traffic metadata — packet sizes, inter-arrival times, flow duration, communication direction — enables inference about the content and the identity of the communicating parties.

### Website Fingerprinting

Website fingerprinting attacks classify which website a user is visiting based on the size and timing pattern of encrypted packets, without decrypting the content. This technique has been demonstrated against Tor traffic with accuracy exceeding 90% in laboratory settings and 80–85% in real-world conditions.[^13] The implication is that using Tor does not prevent an adversary who can observe the traffic volume and timing from inferring that you visited a specific website.

The attack is more limited in practice than in the laboratory because real web traffic is multiplexed, pages are dynamic, and multiple connections may share a single TLS session. However, a committed adversary with network-level access (an ISP, a transit provider, a government-operated surveillance point) can collect the data necessary to run these attacks at scale.

### Application Identification from Traffic Patterns

Machine learning classifiers can identify which application produced a stream of encrypted network traffic with high accuracy. Research has consistently demonstrated 95%+ accuracy at the application level using features derived from packet size distributions, inter-arrival time distributions, and connection duration.[^14]

The forensic implication: if you are using Signal on your private phone through a VPN or Tor, an adversary who can observe the traffic at the network level may be able to classify that traffic as Signal — even without breaking the encryption. They cannot read the messages. But they know you are using Signal, how frequently, and for how long, which is itself informative.

### User Identification from Typing Patterns

Individual typing cadence — the latency between keystrokes, error and correction patterns, touch surface usage on mobile — produces a behavioral fingerprint. Research on keystroke dynamics has demonstrated within-device re-identification accuracies exceeding 95% using features extracted from timing data alone.[^15]

The cross-device version of this attack is significantly harder and has not been demonstrated at scale under real-world conditions. The practical threat is limited to: applications that collect detailed input telemetry (third-party keyboards, some social media apps, some browser environments) transmitting that telemetry to a server that matches it against a known identity fingerprint from a different device or session. This is not passive network surveillance — it requires application-layer telemetry collection. The mitigation is strict application permission control.

---

## Stage 7: The Commercial Surveillance Pipeline — Data Brokers and Location Intelligence

The commercial surveillance ecosystem is often treated as a separate concern from law enforcement surveillance. In practice, the commercial pipeline is upstream of the law enforcement pipeline. Law enforcement purchases from or subpoenas commercial data brokers to access data they could not collect themselves.

### How Location Data Flows from Carrier to Broker to Agency

The data flow is documented through regulatory enforcement actions, investigative journalism, and congressional testimony:

1. **Carrier originates the data.** Carriers collect location data — from CDRs, from Wi-Fi positioning, from GPS via carrier apps — and license it to Location Aggregators (LocationSmart, Zumigo, Veraset, Cuebiq).

2. **Aggregator normalizes and sells.** Location aggregators normalize data from multiple carrier feeds, apply entity resolution, and sell the resulting enriched dataset to downstream buyers: insurers, retailers, hedge funds, and government agencies.

3. **Government purchases without warrant.** Documented cases include DHS purchasing location data from Babel Street and Venntel to track immigration across the southern border; the Defense Intelligence Agency purchasing bulk location data from commercial brokers; and numerous state and local law enforcement agencies purchasing access to location analytics platforms.[^3]

4. **The warrant gap.** The Supreme Court held in Carpenter v. United States (2018) that historical CSLI data obtained directly from a carrier requires a warrant.[^16] But the Court did not address data purchased commercially. Law enforcement agencies have used this gap to purchase location data that would require a warrant to obtain from the carrier directly — the "third-party commercial purchase" of what is effectively carrier location data, but laundered through a broker.

### What Data Brokers Have That Carriers Do Not

Commercial data brokers aggregate data from sources that carriers cannot access:

- **SDK location data**: Many free mobile applications embed location SDKs (Foursquare, X-Mode/Outlogic, GroundTruth) that transmit GPS coordinates in the background, even when the app is not in use. This data is sold to aggregators. The resulting dataset provides GPS-accurate location at higher frequency than carrier Cell ID alone.

- **Purchase history**: Retail loyalty programs, credit card transaction data, and e-commerce records create a purchase behavioral profile. Combined with location data, this profile links physical presence at specific locations to specific transactions.

- **Social platform data**: Public and semi-public posts from social media platforms create a metadata-rich profile of interests, relationships, and activities. Facial recognition applied to images in posts can identify individuals pictured at specific locations.

- **Property and financial records**: Home ownership records, vehicle registration, professional licensing, and voter registration — all public records — provide the ground truth that anchors the identity graph to a physical person.

The combination of these data types, joined by entity resolution, produces a profile richer than any single data source provides. This is the commercial surveillance product that is available without a warrant, without carrier cooperation, and at scale.

---

## Stage 8: Government and Intelligence Analytical Platforms

At the top of the analytical stack are integrated platforms that ingest data from multiple sources — commercial brokers, carrier legal process, device forensics, open-source intelligence — and provide analysts with unified query, visualization, and link analysis capabilities.

### Documented Platforms

**Palantir Gotham** is the best-documented example. It ingests structured and unstructured data — police records, OSINT, location data, financial records, social networks — and provides analysts with a query interface, timeline view, and network graph visualization. Its use by law enforcement is extensively documented through procurement records and civil litigation.[^17]

**Babel Street / Locate X** provides a mobile device location intelligence platform. Users query by geographic area and time window and receive a list of devices observed there, with historical location trails for each device. Law enforcement agencies have purchased access without a warrant, based on the commercial data purchase theory.[^3]

**Fog Data Science** similarly provides location history data purchased from commercial aggregators. FDR filings document that hundreds of state and local law enforcement agencies subscribed at costs of $6,000–$20,000 per year — far cheaper than running their own CALEA interceptions.[^10]

**NSA XKeyscore** (disclosed by Snowden) is the intelligence equivalent: a query interface over bulk-collected internet metadata that allows analysts to search for specific selectors (IP addresses, usernames, email addresses) and retrieve all associated records. The volume of data ingested is unknown but estimated to include a substantial fraction of global internet metadata.[^18]

### The Analyst Workflow

An analyst investigating a target does not interact with raw data. They interact with a platform that has already done the entity resolution, feature extraction, and normalization. Their workflow looks like:

1. Enter a seed identifier: a phone number, an advertising ID, a name, a vehicle plate, a location at a specific time.
2. The platform resolves that seed to a device cluster in the identity graph.
3. The analyst sees a historical location trail, a communication graph, a list of associated identifiers, and an annotated timeline of significant events.
4. The analyst expands to second-order contacts: who does this device communicate with? What are their location trails?
5. Anomalies are flagged automatically: unusual locations, new contacts, behavioral deviations.

This workflow takes minutes for a single device. At scale, automated processing can run the same analysis across thousands of devices — for example, a tower dump of 10,000 IMSIs — in hours. The human analyst reviews flagged anomalies and intersection results; the bulk processing is automated.

---

## What This Means for Your Threat Model

The analysis above is not intended to induce paralysis. It is intended to accurately represent what the data science pipeline produces from the signals that your devices emit, so that mitigations can be evaluated against a realistic adversary model.

### What the ML Pipeline Defeats

**Pseudonymous identifiers.** A new SIM, a fresh advertising ID, or a VPN-assigned IP address are defeated within days by co-occurrence linkage to your home address, your existing contact graph, or your behavioral pattern.

**Single-layer compartmentalization.** Using a separate phone without also maintaining geographic, temporal, and behavioral separation defeats the compartmentalization because the ML pipeline can link the two phones through shared location or correlated behavior.

**VPN-based network anonymity.** VPNs protect content but not traffic metadata. Application fingerprinting, traffic timing analysis, and communication pattern analysis are not defeated by encryption.

### What the ML Pipeline Does Not Defeat

**Geographic separation.** If Phone B is never in the same geographic area as Phone A — ever — the co-location link cannot be established. Geographic separation is the most robust mitigation against ML-based correlation.

**Communication network isolation.** If Phone B's contact graph has zero overlap with Phone A's, social graph analysis cannot link them. This requires that the operator on Phone B has a genuinely separate identity known to a genuinely separate social circle.

**Behavioral schedule discipline.** If Phone B is only used during specific time windows that do not correlate with Phone A's activity patterns, temporal correlation is defeated. Randomized use windows are more effective than fixed schedules.

**Permission restriction and GrapheneOS.** Preventing applications from collecting location, contact, and input telemetry reduces the data available to commercial brokers. An app that cannot collect data cannot sell it. GrapheneOS's permission model and network isolation controls are meaningful mitigations against the commercial surveillance pipeline specifically.

**Encrypted messaging with metadata minimization.** Signal's minimal metadata storage (as demonstrated in their 2016 and 2022 subpoena responses)[^19] means that even if a legal process reaches Signal, the available records are last-seen timestamp and account creation date. This does not defeat carrier-level metadata (who you called, when, from where), but it removes the app-layer data from the commercial and government pipelines.

### The Residual Risk

The ML surveillance pipeline is asymmetric: the adversary has more data and more compute than the individual can counter. Even a rigorously maintained two-phone strategy leaves behavioral signals that a sufficiently resourced adversary can analyze. The question is not whether residual correlation is possible, but whether the adversary has the motive, resources, and legal access to run the analysis.

For threat tiers 0–2 (advertisers, local law enforcement with limited resources, opportunistic investigation), the two-phone strategy and associated behavioral disciplines substantially reduce risk. For threat tiers 3–4 (federal law enforcement with commercial data access, intelligence agencies with SIGINT infrastructure), residual ML-based correlation is a real and unmitigated risk. The analyst with access to Babel Street, Palantir Gotham, and carrier CDRs — all obtainable without warrant for the commercial data and with low-threshold legal process for the carrier records — is running exactly the analysis described in this chapter.

Understanding this is not a counsel of despair. It is a calibration. Know which tier of adversary you face. Match the discipline of your strategy to the analytical capabilities of that adversary. And acknowledge what cannot be mitigated.

---

## Summary

The forensic collection layer — what is documented in Volumes 2 and 3 — is the input. The analytical layer described in this chapter is the transform. The output is a rich behavioral profile, social graph, and identity attribution that often far exceeds what any single collected signal would suggest.

The key transformations in the pipeline are:

1. **Normalization and entity resolution**: linking pseudonymous identifiers to real identities via co-occurrence and the commercial identity graph.
2. **Home and work inference**: anchoring behavioral profiles to physical places, defeating pseudonymity at the address level.
3. **Behavioral profiling**: extracting routine, predictability, and deviation from the movement and communication record.
4. **Social graph analysis**: mapping relationships, community membership, and second-order association.
5. **Traffic analysis and encrypted flow classification**: inferring application, timing, and behavioral signature from encrypted metadata.
6. **Commercial broker pipeline**: aggregating SDK location, purchase, and social data to create a profile richer than carrier data alone.
7. **Integrated analyst platforms**: providing unified query, visualization, and automated anomaly detection over the combined data.

The appropriate response is not to assume this analysis is being run against you right now. The appropriate response is to understand what it can produce, identify which elements of your threat model make it relevant, and calibrate your operational discipline accordingly.

---

## Footnotes

[^1]: Foursquare, "Foursquare Technology Platform Overview," commercial documentation, 2024. Cross-linking described as linking across "50+ million devices" in U.S. alone.

[^2]: Datta, S., et al., "The Accuracy of Commercial Location Data," Proceedings of the 2023 Conference on Fairness, Accountability, and Transparency (FAccT 2023), ACM.

[^3]: Byron Tau, *Means of Control: How the Hidden Alliance of Tech and Government Is Creating a New American Surveillance State*, Crown, 2024. Comprehensive account of commercial location data purchases by DHS, DIA, and state/local law enforcement.

[^4]: United States v. various defendants, Capitol Breach litigation, 2021–2023. DOJ filings reference cell site data and Google geofence warrant data for location-based identification.

[^5]: Calabrese, F., et al., "Estimating Origin-Destination Flows Using Mobile Phone Location Data," IEEE Pervasive Computing, 2010.

[^6]: Pappalardo, L., et al., "Returners and Explorers Dichotomy in Human Mobility," Nature Communications, 2015. Home location inference accuracy assessed using CDR data from multiple carriers.

[^7]: De Montjoye, Y., et al., "Unique in the Crowd: The Privacy Bounds of Human Mobility," Scientific Reports, 2013. Demonstrates that four spatio-temporal points uniquely identify 95% of individuals in a mobile dataset.

[^8]: Song, C., et al., "Limits of Predictability in Human Mobility," Science 327(5968), 2010. Found average predictability of 93% from historical location data.

[^9]: Blondel, V.D., et al., "Fast Unfolding of Communities in Large Networks," Journal of Statistical Mechanics, 2008. Louvain community detection, widely used in criminal link analysis.

[^10]: Electronic Frontier Foundation, "Fog Data Science: How Law Enforcement Can Surveil Millions Without a Warrant," EFF, February 2023.

[^11]: Glenn Greenwald, *No Place to Hide: Edward Snowden, the NSA, and the U.S. Surveillance State*, Metropolitan Books, 2014. MAINWAY database described at pp. 94–97.

[^12]: Richardson, R., Schultz, J., Crawford, K., "Dirty Data, Bad Predictions: How Civil Rights Violations Impact Police Data, Predictive Policing Systems, and Justice," New York University Law Review, 2019.

[^13]: Rimmer, M., et al., "Automated Website Fingerprinting Through Deep Learning," Proceedings of NDSS Symposium, 2018. 95.3% accuracy on Tor circuits in lab conditions; real-world accuracy lower due to multiplexing.

[^14]: Wang, P., et al., "End-to-End Encrypted Traffic Classification with Deep Learning," IEEE INFOCOM, 2023. 96.5% application identification accuracy on encrypted flows.

[^15]: Acien, A., et al., "TypeNet: Scaling up Keystroke Biometrics," IEEE Transactions on Information Forensics and Security, 2022. Within-device identification at 95%+ accuracy; cross-device identification significantly harder.

[^16]: Carpenter v. United States, 585 U.S. 296 (2018). Court held that warrantless access to 7 days or more of historical CSLI violates the Fourth Amendment.

[^17]: American Civil Liberties Union, "Unregulated and Unaccountable: How Palantir Threatens Civil Liberties," ACLU, 2022. Procurement records from 18+ law enforcement agencies.

[^18]: Glenn Greenwald and Ewen MacAskill, "NSA Prism Program Taps in to User Data of Apple, Google and Others," The Guardian, June 7, 2013.

[^19]: Signal v. United States (Grand Jury Subpoena), 2016. Signal's published response disclosed only account creation timestamp and last-seen timestamp. Repeated and confirmed in 2022 proceedings.
