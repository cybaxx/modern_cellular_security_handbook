# Graph 5: Threat Model Effectiveness by Adversary Type

## Purpose

This radar chart evaluates how well the mitigated two-phone strategy performs against different categories of adversaries. The effectiveness score ranges from 0% (complete failure) to 100% (complete protection against that adversary's capabilities). The graph reveals a hard truth: the strategy is highly effective against commercial adversaries but degrades rapidly as the adversary's legal authority and technical capability increase.

## The Graph


> *See the figure generated below.*


## Adversary Level Analysis

### Advertisers (95% Effectiveness)

This is the adversary the two-phone strategy defeats most thoroughly. Advertisers and data brokers operate through:

- Cross-site tracking cookies
- Advertising IDs (Google AAID, Apple IDFA)
- Device fingerprinting (browser, OS, screen resolution, installed fonts)
- IP address correlation across websites

The two-phone strategy defeats all of these because Phone B and the Computer use separate browsing profiles, separate IP addresses (VPN), and no advertising ID. Phone A has no browser capability at all. Advertisers cannot correlate activity across the two devices because they never see both devices from the same tracking identifier.

The 5% residual risk comes from: IP address overlap if both devices use the same VPN exit node, behavioral patterns (same browsing hours, same sites), and payment information leaks if the user purchases items on Phone B that link back to their real identity.

### Local Police (60% Effectiveness)

Local police have limited resources, limited legal jurisdiction, and typically lack sophisticated forensic capabilities. They operate within a single jurisdiction and must follow relatively strict probable cause requirements.

The two-phone strategy provides moderate protection because:

- Local police can subpoena the carrier for Phone A's data (which will identify Phone A's user)
- Local police can request tower dumps from the area of an incident
- Local police generally cannot conduct multi-jurisdiction, multi-carrier, multi-ISP investigations
- Local police rarely have the budget for advanced forensic tools like cell-site simulators or RF fingerprinting

The strategy fails if the user is already a person of interest in a local investigation. A single subpoena for Phone A's subscriber information reveals the user's identity, and a follow-up search warrant for the home address may recover Phone B.

### Civil Litigation (70% Effectiveness)

Civil litigation adversaries include divorce attorneys, private investigators hired for civil cases, and corporate legal departments engaged in discovery. These adversaries operate through:

- Subpoenas for phone records, email metadata, and ISP logs
- Private investigators conducting physical surveillance
- Background check databases

The two-phone strategy is moderately effective here because civil discovery typically targets a named individual. If the adversary knows the individual's name, they subpoena everything associated with that name — including Phone A's carrier records. However, if Phone B is registered under no name (purchased with cash, using burner SIMs), it may not appear in discovery responses.

The 30% failure rate comes from physical surveillance. A private investigator following the subject may observe them using both phones, especially if the subject is careless about when and where they switch between devices.

### Cybercriminal (85% Effectiveness)

Cybercriminals — ranging from casual hackers to organized ransomware groups — operate through technical exploitation rather than legal process. Their toolset includes:

- Malware, phishing, credential theft
- SIM swapping
- Exploitation of cloud account recovery processes
- Purchase of leaked credentials on dark web markets

The two-phone strategy is highly effective here because an attacker who compromises Phone B (through a malicious app, phishing link, or Signal vulnerability) gains access only to Phone B's data. They do not learn Phone A's number, the user's real name, or the user's home address — provided Phone B has never been linked to the user's identity.

The 15% residual risk comes from: SIM swapping against Phone A's carrier (if the attacker identifies Phone A's number), cloud account recovery attacks that compromise the email used for both devices, and physical access to both devices if the attacker burglarizes the user's home.

### Corporate Espionage (40% Effectiveness)

Corporate espionage adversaries are better funded and more persistent than typical cybercriminals. They may have:

- Physical surveillance teams
- Access to cellular interception equipment (IMSI catchers)
- Relationships with insiders at carriers or ISPs
- Legal teams that can craft pretextual subpoenas

Protection drops to 40% because a determined corporate adversary will eventually identify the subject, place them under physical surveillance, and observe the two-phone pattern. Once observed, they may plant a bug in the subject's vehicle (which tracks both phones together) or compromise a location both phones visit regularly.

### Federal Law Enforcement (25% Effectiveness)

Federal agencies (FBI, DHS, NSA, Secret Service, and equivalents in other nations) have:

- Full legal authority for wiretaps, subpoenas, and search warrants
- Access to national security letters (NSLs) that prohibit the ISP from notifying the target
- Relationships with foreign carriers and intelligence-sharing agreements (Five Eyes)
- Advanced forensic capabilities including cell-site simulators, RF fingerprinting, and zero-day exploits
- Dedicated surveillance teams for physical follow

The two-phone strategy provides minimal protection (25%) against a federal investigation because:

- An NSL to the ISP immediately reveals the user's identity
- A pen register or trap-and-trace on Phone A captures all dialed numbers
- Physical surveillance observes the user carrying both devices
- Forensic analysis of Phone A's physical location (through tower data) reveals the home address
- A search warrant for the home recovers Phone B

### State Actor (15% Effectiveness)

State actors (MSS, GRU, Mossad, GCHQ, etc.) represent the most capable adversary. They have:

- All the capabilities of federal law enforcement, plus
- Access to global telecommunications infrastructure (SS7 signaling, lawful intercept gateways)
- Offensive cyber capabilities (zero-day exploits against GrapheneOS, mobile malware)
- Legal authority in their home jurisdiction to compel carrier cooperation
- Physical surveillance teams operating across international borders
- Diplomatic cover and false documentation for operations

Two-phone protection is essentially ineffective (15%) against a state actor for two reasons:

1. **SS7 attacks**: A state actor with SS7 access can locate Phone A anywhere in the world by sending a Location Information Request to the home network. This works on any phone with a cellular radio, including a flip phone. The phone cannot refuse or detect this query.

2. **Cascade deanonymization**: Once a state actor identifies Phone A (through any means — SS7, subscriber records, physical surveillance), they trace the device to the home location, identify all devices at that location, and correlate every phone present. The two-phone compartmentalization collapses because both devices share a physical location.

The 15% residual represents scenarios where the state actor lacks motivation, resources, or legal authority to pursue a full investigation — for example, a low-priority target in a jurisdiction where the actor has limited influence.

## Strategic Implication

The graph reveals a clear boundary: **the two-phone strategy works well against adversaries who lack legal process and physical surveillance capabilities.** Once the adversary has subpoena power and a budget for physical surveillance, the strategy degrades to ineffective.

This does not mean the strategy is worthless. It means the user must calibrate their threat model. For a journalist covering local corruption, two phones may be adequate against local police. For a whistleblower leaking classified documents, two phones are insufficient against a state actor.

## The Adversary Capability Spectrum

The seven adversary types in the graph exist along a spectrum of capability and resources. Understanding where each adversary falls on this spectrum helps the user calibrate their threat model:


> *See the figure generated below.*


### Advertisers and Data Brokers (95% Protection)

Advertisers are the least capable adversary on the spectrum. They have:

- No legal process (they cannot subpoena carriers or ISPs)
- No physical surveillance capability
- No network-layer access (they cannot capture Wi-Fi probe requests or cellular signaling)
- Only the data voluntarily shared by websites, apps, and advertising SDKs

The two-phone strategy defeats advertisers because Phone A and Phone B have no common advertising identifiers. Phone A has no browser, no apps, and no advertising ID. Phone B uses a VPN and has advertising ID disabled (GrapheneOS removes Google Play Services entirely). An advertiser who sees traffic from Phone B's VPN exit node cannot correlate it with Phone A's cellular identity.

The 5% residual risk for advertisers comes from:

- **Payment information**: If the user makes a purchase on Phone B using a credit card linked to their real name, the advertiser can correlate the purchase with other data sources.
- **Account recovery**: If the user registers Phone B's email on a service that already knows Phone A's identity (e.g., using the same email for a newsletter signup on both phones), the link is established.
- **Behavioral fingerprinting**: If the user consistently visits the same websites at the same times on both phones, a pattern-matching algorithm could infer a connection.

### Cybercriminals (85% Protection)

Cybercriminals are more capable than advertisers but still lack legal process and physical access. Their toolset:

- **Phishing and social engineering**: Tricking the user into revealing Phone A's number or Phone B's location
- **Credential stuffing**: Using leaked passwords to access the user's accounts
- **SIM swapping**: Convincing the carrier to port Phone A's number to a SIM controlled by the attacker
- **Malware**: Infecting Phone B with spyware that exfiltrates call logs, contacts, and location

The two-phone strategy is strong against cybercriminals because:

- Compromising Phone B does not reveal Phone A's identity (if the strategy is maintained)
- Compromising Phone A (through SIM swapping, for example) only reveals the carrier-side data for Phone A
- The attacker must compromise both devices independently — a significant increase in attack cost

The 15% failure rate comes from scenarios where the attacker identifies the link between the two devices. For example, if the attacker SIM-swaps Phone A and then uses SMS verification to reset Phone B's Signal account, the attacker now controls both identities.

### Civil Litigation Adversaries (70% Protection)

Civil litigation adversaries (divorce attorneys, corporate legal departments, private investigators) have limited legal process:

- They can issue subpoenas for records (phone records, ISP logs, bank records)
- They can hire private investigators for physical surveillance
- They cannot obtain criminal warrants or wiretaps

The strategy provides moderate protection because civil discovery targets the named individual. If the adversary knows the subject's name, they subpoena everything associated with that name. Phone A's carrier records are discoverable. Phone A's tower data reveals the home address. A follow-up subpoena to the ISP reveals all devices connected to the home network — including Phone B's MAC address.

The 30% failure rate primarily comes from physical surveillance. A private investigator following the subject can observe the two-phone pattern, note the times when the subject uses each device, and report the correlation to the client.

### Local Police (60% Protection)

Local police have criminal subpoena power (which requires lower legal standards than a warrant in many jurisdictions) and can:

- Subpoena carrier records for Phone A (subscriber information, CDRs, tower dumps)
- Request "tower dumps" for specific locations and times
- Use cell-site simulators (Stingrays / IMSI catchers) to locate devices in real time
- Deploy limited physical surveillance

The strategy provides moderate protection against local police because:

- Most local police departments lack the resources for multi-carrier, multi-jurisdiction investigations
- Local police rarely have the technical capability to exploit Wi-Fi probe requests or BSSID databases
- Local police typically focus on Phone A (the phone number they have from witnesses or records) and may not discover Phone B

The 40% failure rate reflects cases where local police connect Phone A to the home address (through tower records), execute a search warrant, and recover both devices.

### Corporate Espionage (40% Protection)

Corporate espionage adversaries are better funded and more persistent than local police. They may:

- Deploy physical surveillance teams
- Use IMSI catchers to track Phone A
- Exploit insider access at carriers or ISPs
- Use pretexting to obtain phone records from carriers
- Deploy keyloggers or spyware on the subject's work computer

The 60% failure rate reflects the persistence and resources of corporate espionage. A well-funded corporate adversary will eventually identify the subject, place them under surveillance, and observe the two-phone pattern. Once observed, the adversary may:

- Plant a tracking device on the subject's vehicle (which reveals both phones' locations simultaneously)
- Compromise the subject's home network through a targeted attack
- Bribe or coerce an insider at the carrier to provide Phone A's records

### Federal Law Enforcement (25% Protection)

Federal agencies have:

- Full criminal and national security investigative authority
- Access to National Security Letters (NSLs) that prohibit the ISP from notifying the target
- Wiretap authority under Title III (criminal) and FISA (national security)
- Relationships with foreign intelligence services through Five Eyes and other alliances
- Dedicated physical surveillance teams
- Advanced forensic capabilities (cell-site simulators, zero-day exploits, RF fingerprinting)

The 75% failure rate reflects the reality that a federal investigation will eventually identify the subject and all their devices. The two-phone strategy may delay this identification but cannot prevent it:

1. The NSL to the ISP reveals the subject's identity and all devices connected to the home network
2. Physical surveillance confirms the subject carries both phones
3. Tower records for Phone A reveal the subject's home address and movement patterns
4. A FISA order for a cell-site simulator can track Phone A in real time
5. A search warrant recovers both devices, and forensic analysis of Phone B reveals its contents

### State Actors (15% Protection)

State actors represent the apex of adversary capability. They combine all the capabilities of federal law enforcement with additional resources unique to nation-states:

- **Global SS7 access**: Can locate any phone on any network worldwide by querying the home network's HLR or MSC
- **Lawful intercept gateways**: Carriers in many countries are required to provide direct government access to call content and metadata
- **Offensive cyber capabilities**: Zero-day exploits against mobile operating systems, including GrapheneOS and iOS
- **Diplomatic cover**: Operatives can operate under diplomatic immunity in most countries
- **Physical surveillance across borders**: Teams can follow a subject across international borders
- **No legal constraints**: State actors operating through intelligence agencies are not bound by the criminal procedure laws that constrain domestic law enforcement

The 85% failure rate is not a suggestion that the strategy is useless — it is a realistic assessment that a state actor with sufficient motivation will always succeed. The two-phone strategy may buy time (hours to weeks) before the state actor identifies the subject and all devices. It cannot prevent the identification.

## Cross-Adversary Defense Strategies

Given the varying effectiveness across adversary types, a layered defense approach is necessary:

### Tier 1: Defeat Advertisers and Cybercriminals (95%/85% effective)

These adversaries are defeated by:

- **Basic compartmentalization**: Separate devices for identity-linked and anonymous activities
- **VPN on Phone B**: Prevents IP-based tracking
- **No Google/Apple services on Phone B**: Removes the primary advertising identifier
- **GrapheneOS or similar hardened OS**: Reduces attack surface for malware
- **Signal for sensitive communications**: End-to-end encryption with minimal metadata

### Tier 2: Defeat Civil Litigation and Local Police (70%/60% effective)

These adversaries require additional mitigations:

- **No home Wi-Fi for Phone B**: Prevents ISP-based correlation (the single point of failure)
- **Cash purchase of devices and prepaid SIMs for both phones**: Breaks the financial paper trail
- **Quarterly device and SIM rotation**: Limits the historical window of carrier data
- **Faraday bags**: Prevents remote tracking and forensic extraction when devices are not in use
- **Separate Signal identities per device with no cross-contact**: Prevents social graph correlation

### Tier 3: Defeat Corporate Espionage (40% effective)

Some additional defenses help against corporate espionage:

- **No predictable schedule**: Varying routines prevents pattern-based targeting
- **Dedicated work devices only**: No personal communications on company equipment
- **Physical security**: Locked cases, privacy screens, avoidance of fixed surveillance locations

### Tier 4: Federal and State Actors (25%/15% effective)

No additional consumer-grade defenses are effective. The realistic assessment is:

- **The strategy will eventually fail. Plan for it.** What information will the adversary learn? What can be done to limit the damage when the identification occurs?
- **Use multiple identities, not just multiple phones.** True compartmentalization requires separate identities: different names, addresses, and life details for each identity.
- **Accept the timeline.** The two-phone strategy may delay identification by days or weeks. It will not prevent it.

## Practical Guidance

Based on this graph, the mitigation priorities are:

1. **Against advertisers (95% effective)**: The strategy works out of the box. No special mitigations needed beyond basic compartmentalization.

2. **Against local police (60% effective)**: Requires strict OpSec: no home Wi-Fi for Phone B, cash purchase of devices and SIMs, no linkage between Phone A and the user's home address (use a prepaid purchased with cash).

3. **Against cybercriminals (85% effective)**: Good protection, but requires keeping Phone A's number completely separate from any online account. If the user ever uses Phone A's number for SMS verification on Phone B, the compartmentalization is broken.

4. **Against federal/state actors (15-25% effective)**: The two-phone strategy is not sufficient. Additional countermeasures required: multiple identities, physical security, encrypted communications using protocols the adversary cannot intercept (e.g., Signal's sealed sender, Tor over bridges), and acceptance that the adversary will eventually identify the user.
