# Chapter 30: What to Ignore — Threats That Don't Apply

One of the hardest skills in privacy is learning what to ignore. The security world is filled with frightening scenarios, sophisticated attacks, and genuinely terrifying capabilities. Most of them have nothing to do with you.

Based on the forensic analysis in earlier volumes, here is what you can safely stop worrying about as a normal citizen. This is not to say these threats do not exist — they are very real for certain people. But for a citizen whose threat model is advertisers and data brokers, these threats are a distraction from the basics that actually matter.

---

## Threats You Can Safely Ignore

### 5G Multi-RTT Positioning

| You can ignore it because | Who actually needs to worry |
|---|---|
| Your carrier already knows your location via cell towers. The extra precision that 5G Multi-RTT provides is a refinement, not a revolution. For ad tracking purposes, standard cell tower triangulation is more than sufficient to target you with ads. The difference between knowing you are within 50 meters versus within 5 meters does not change the advertising experience. | Journalists in hostile countries, fugitives actively avoiding law enforcement, and anyone trying to evade physical surveillance that uses cell network data. |

Multi-RTT (Round Trip Time) positioning is a 5G feature that allows carriers to determine a phone's location with remarkable precision — down to a few meters in ideal conditions. It sounds terrifying. But here is the reality: your carrier already knows where you are. Every time your phone connects to a cell tower, the carrier logs which tower and sector you used. With multiple towers, they can triangulate your position. Multi-RTT just makes this slightly more accurate. For the purposes of ad tracking, data brokerage, or even law enforcement investigation, the old methods were already good enough. Multi-RTT does not create a new surveillance capability; it marginally improves an existing one that was already pervasive.

### Stingray / IMSI Catchers

| You can ignore it because | Who actually needs to worry |
|---|---|
| Local police rarely use these devices outside major cities. When they do, they target specific suspects in criminal investigations — not random citizens. Deploying an IMSI catcher requires resources, training, and in many jurisdictions, a court order. They are not used for mass surveillance of ordinary people. | Criminal suspects in active investigations, particularly in drug and organized crime cases. Also relevant for journalists covering protests or sensitive topics. |

IMSI catchers (also known as Stingrays, after the Harris Corporation product) impersonate cell towers to force nearby phones to connect to them. Once connected, the device can intercept phone numbers, SMS metadata, and in some configurations, call content. They are a real tool used by law enforcement. But they are expensive, legally risky to deploy, and primarily used in serious criminal investigations. If a police department is going to spend tens of thousands of dollars and navigate a court order to deploy a Stingray, they are not targeting people who just need better privacy settings. They are targeting drug dealers, robbery suspects, and in some cases, protesters. You are not on their radar.

### Tower Dumps

| You can ignore it because | Who actually needs to worry |
|---|---|
| Tower dumps require a court order. Law enforcement must demonstrate probable cause to a judge to obtain all device identifiers connected to a specific cell tower during a specific time window. These are not used to find normal people going about their daily lives. | Criminal suspects in serious investigations, particularly when police are trying to identify which phones were present at a crime scene. |

A tower dump is a request to a carrier for every phone number, IMSI, and IMEI that connected to a particular tower during a specific time period. This is the digital equivalent of asking "who was in this neighborhood at this time?" It is a powerful forensic tool, but it comes with significant legal hurdles. Courts require probable cause, and the requests are typically limited to specific time windows in specific locations. If you are not a suspect in a serious crime, no one is requesting tower dumps to find you. The data brokers you should actually worry about do not use tower dumps — they get your data through far simpler and completely legal channels.

### Baseband Exploits

| You can ignore it because | Who actually needs to worry |
|---|---|
| Baseband exploits are nation-state capability. They require finding and weaponizing vulnerabilities in the low-level firmware that controls a phone's cellular radio. These are among the most expensive and carefully guarded exploits in existence. They are not used against citizens without a very specific and compelling reason. | Whistleblowers, activists, journalists covering sensitive topics, and targets of nation-state surveillance. |

The baseband processor is the separate chip in your phone that handles cellular communication. It runs its own operating system, has direct access to the phone's memory, and operates at a privilege level that the main operating system cannot easily monitor. Exploiting the baseband is the holy grail of phone surveillance — it allows an attacker to bypass all operating system security and gain complete control of the device. These exploits are used by agencies like the NSA, GCHQ, and their counterparts in other countries. They are worth millions of dollars and are deployed sparingly. If someone is using a baseband exploit against you, you have bigger problems than a privacy guide can solve.

### Wi-Fi BSSID Geolocation Databases

| You can ignore it because | Who actually needs to worry |
|---|---|
| Google already has this data. It is how "Find My Phone" works. Apple and Google have been collecting Wi-Fi BSSID locations for over a decade by wardriving with Street View cars and by collecting data from Android and iOS devices. This is not a new threat. | People hiding from stalkers, domestic violence survivors who need to maintain location privacy, and anyone in witness protection. |

Every Wi-Fi access point has a unique identifier called a BSSID. Google, Apple, and Microsoft have mapped the physical location of hundreds of millions of these access points. When your phone scans for Wi-Fi networks (even when not connected), it checks the BSSIDs it sees against this database to estimate your location. This is how Google Location Services and Find My Device work. It is also how your phone knows where it is when GPS is unavailable. This capability has been built into every smartphone for years. It is not a new vulnerability; it is a feature that you can disable by turning off Wi-Fi scanning as described in the previous chapter.

### Two-Phone Compartmentalization

| You can ignore it because | Who actually needs to worry |
|---|---|
| Two-phone compartmentalization is overkill for a normal citizen. You do not need to hide your identity from your ISP if you are not doing anything illegal. The operational security burden of managing two phones — keeping them separate, never carrying them together, remembering which one to use for which purpose — is significant and error-prone. | Border crossers in hostile countries, journalists in repressive regimes, whistleblowers, and people with specific, targeted surveillance threats. |

The two-phone strategy is the subject of the earlier chapters of this book, and it is a powerful tool for those who need it. But it comes with real costs: the financial cost of a second device and service plan, the cognitive load of maintaining separation, and the risk that a single mistake (carrying both phones together, using the wrong phone for a call) collapses the entire strategy. For most people, locking down a single phone achieves 90% of the benefit with 10% of the effort.

### Faraday Bags

| You can ignore it unless | Who actually needs them |
|---|---|
| Unless you are actively avoiding physical tracking — meaning someone is trying to locate you via your phone's radio emissions in real time — you do not need a faraday bag. They are an inconvenience (you have to take your phone out every time you want to use it) and they provide no benefit against the threats most people actually face. | Same as two-phone compartmentalization: border crossers, journalists, whistleblowers. |

### Burner SIMs

| You can ignore it because | Who actually needs to worry |
|---|---|
| Burner SIMs are illegal in many places due to mandatory SIM registration laws. In the United States, while not federally illegal, many carriers require identification to purchase prepaid SIMs. Moreover, burner SIMs do not protect you against the threats most people face — they prevent a phone number from being linked to your identity, but they do nothing about app tracking, browser fingerprinting, data brokers, or account security. | Same groups as above, plus people who need to make anonymous inquiries or contacts that cannot be traced back to their identity. |

---

## If you are a normal citizen, the threats above are like worrying about a nuclear bomb while ignoring a house fire. Focus on the basics first.

---

## The Threat You Actually Face (And How to Fix It)

### The Real Enemy: Data Brokers

While you have been worrying about Stingrays and 5G positioning, a far more mundane and pervasive surveillance infrastructure has been quietly compiling your entire life into a searchable database.

Companies like LiveRamp, Oracle, Experian, Palantir, Acxiom, and Epsilon buy and sell your data. They know:

- Your name, address, phone number, email addresses (current and past)
- Your income range, home value, estimated net worth, credit score
- Your shopping habits — what you buy, where you buy it, how much you spend
- Your political donations and party registration
- Your health conditions (inferred from purchases, search history, and location data)
- Every website you visit (via third-party trackers embedded on millions of sites)
- Your relationships — who you live with, who you call, who you email
- Your travel patterns — where you go, when you go, how you get there
- Your social media activity, even if your profiles are set to private

### How They Get It

| Source | What they get |
|---|---|
| **Data breaches** | Equifax, Marriott, Target, and hundreds of other breaches have leaked names, SSNs, addresses, and financial data. Brokers buy these datasets on the dark web and incorporate them into their profiles. |
| **Loyalty cards** | Grocery store loyalty cards, pharmacy discount cards, coffee shop punch cards — every purchase is tracked and sold. |
| **Public records** | Property tax records, voter registration, marriage and divorce records, business licenses, professional certifications. All public, all aggregated. |
| **Apps you installed** | Free weather apps, games, flashlight apps, keyboard apps, wallpaper apps — many of them are data collection tools disguised as utilities. |
| **Browsing trackers** | Third-party cookies, tracking pixels, fingerprinting scripts. These are the backbone of the data broker industry. |

### The Fix: Attack the Data Brokers

| Action | Difficulty | Effectiveness |
|---|---|---|
| Opt out of people search sites (Whitepages, Spokeo, BeenVerified, Intelius, PeopleFinder) | Medium — there are dozens of sites | High — removes you from the most commonly used public lookup services |
| Use a data broker removal service (DeleteMe or OneRep) | Easy — paid service handles everything | High — continuously monitors and removes your data |
| Freeze your credit at Equifax, Experian, TransUnion | Easy | Medium — prevents new accounts from being opened in your name |
| Remove your info from voter rolls (state-dependent) | Hard — varies by state, may require notarized forms | Low — many states do not allow removal |
| Use a PO Box for all registrations and deliveries | Easy | Medium — keeps your physical address off databases |

**Recommended service:** DeleteMe ($129/year) or OneRep ($99/year). These services continuously scan data broker sites and submit opt-out requests on your behalf. They are worth every penny for anyone who does not want to spend hours manually submitting opt-out forms.

The data broker industry is the most significant privacy threat facing normal citizens today. It is legal, it is pervasive, and it is almost entirely unregulated in the United States. Fighting it requires persistence, but the tools are simpler and more effective than worrying about baseband exploits or Stingrays.

Focus your energy where it matters. The nuclear bomb is not coming for you. The house fire is already burning.
