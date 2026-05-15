# Chapter 2: Threat Modeling for Privacy

## The First Question: Who Is Actually Trying to Track Me?

Before implementing any privacy strategy, you must answer one question honestly:

> **"Who is actually trying to track me?"**

The answer determines everything: which mitigations are necessary, which threats you can ignore, how much money and time you need to invest, and whether two phones are appropriate or overkill.

Most privacy guides skip this step. They assume a one-size-fits-all adversary -- usually "the government" -- and recommend extreme measures that 95% of users do not need. This creates a paradox: users burn out on excessive OpSec and abandon privacy altogether, or they implement weak measures against a threat model they never defined.

This chapter gives you the framework to define your actual adversary.

## The Adversary Identification Framework

| If your answer is... | Your real threat is... | You do NOT need to worry about... |
|---|---|---|
| "Advertisers, data brokers, creepy apps" | Companies selling your attention | 5G Multi-RTT, Stingrays, tower dumps |
| "My employer or school" | Network monitoring, device management | State-level baseband exploits |
| "A stalker or abusive ex" | Physical surveillance, account access | CALEA wiretaps |
| "Local police (non-targeted)" | Pulling your phone records during an investigation | Nation-state zero-days |
| "The government is after me specifically" | You need a lawyer, not a privacy guide | Everything -- get professional help |

For 95% of citizens, the answer is the first bullet: advertisers and data brokers. The strategies in this handbook focus on that threat model first, then escalate.

## Three Levels of Adversary

We categorize adversaries by capability. The two-phone strategy's effectiveness depends entirely on which adversary you face.

### Adversary Level 1: Low-Risk (Advertisers, Data Brokers, Casual Stalker)

These adversaries have no legal process and no physical access. They rely on tracking pixels, advertising IDs, browser fingerprinting, data brokerage, and public records. Their technical capability is limited to commercially available tools and services. They cannot compel a carrier or ISP to produce records. They cannot physically seize devices. They cannot deploy IMSI catchers or Stingray devices.[^1]

For this adversary, the threat is almost entirely economic: your attention and your personal data are commodities. The adversary wants to build a profile of your interests, habits, and demographics to sell ads or data products. They do not want to arrest you, expose your communications, or track your physical location in real time -- they simply want to know what you might buy next.

| Goal | Phone A (Flip) | Phone B (Custom OS) | Computer | Success Rate |
|---|---|---|---|---|
| Track browsing habits | N/A | Low (GrapheneOS + VPN) | Medium (browser fingerprint) | 20% |
| Build advertising profile | Medium (SMS metadata) | Low (no Google services) | Medium (IP geolocation) | 30% |
| Correlate devices | Low (requires carrier access) | Low | Low | 10% |

**Verdict: Effective against low-risk adversaries.** The lack of Google services on Phone B severely limits ad tracking. For this threat level, two phones are almost certainly overkill. A single de-Googled phone with Signal and a VPN provides 90% of the privacy benefit with 10% of the effort.

### Adversary Level 2: Medium-Risk (Local Police with Court Order)

These adversaries have legal process -- subpoenas, court orders, or warrants -- but limited technical capability and jurisdiction. They can compel carriers, ISPs, and platforms to produce records.[^2] They may use forensic tools like Cellebrite UFED or GrayKey on seized devices. They typically operate within a single jurisdiction and cannot coordinate across multiple legal frameworks.

This adversary does not need technical exploits. They use the legal system as their primary attack vector. A subpoena to a carrier produces call records and tower location data. A subpoena to an ISP produces subscriber identity and IP logs.[^2] A warrant authorizes physical device seizure and forensic examination. The adversary succeeds not by breaking encryption, but by compelling someone else to hand over the keys or the data.

| Goal | Phone A (Flip) | Phone B (Custom OS) | Computer | Success Rate |
|---|---|---|---|---|
| Obtain subscriber identity | 100% (carrier subpoena) | 0% (no SIM) | 100% (ISP subpoena, if used at home) | 67% (2 of 3 devices) |
| Obtain location history | 100% (tower dump + TA) | 70% (Wi-Fi geolocation, if public networks used) | 0% (unless IP logged) | Variable |
| Correlate Phone A to Phone B | 80% (if carried together or both used at home) | | | High |
| Extract device contents (seizure) | 100% (flip phone, no encryption) | Variable (GrapheneOS encryption resists Cellebrite) | Variable (full-disk encryption) | Depends on seizure |

**Verdict: Partially effective if strict OpSec is followed. Fails completely if Phone B ever touches home Wi-Fi or is carried with Phone A.** This is the critical threshold. For journalists, activists, and whistleblowers facing local police, the two-phone strategy can work -- but only with every mitigation in place. A single mistake collapses the entire compartmentalization.

### Adversary Level 3: High-Risk (Federal LE / Intelligence / State Actor)

These adversaries have unlimited resources, legal authority across multiple jurisdictions, physical surveillance capabilities including CCTV networks and license plate readers, technical exploitation teams capable of developing zero-day exploits, and the ability to coordinate multiple legal instruments simultaneously -- often across international borders via mutual legal assistance treaties (MLATs).[^3]

This adversary does not need to break your OpSec through technical means alone. They will combine: legal process against carriers, ISPs, and platforms; physical surveillance (teams, cameras, trackers); financial tracking (credit card records, bank subpoenas); human intelligence (informants, undercover operations); and technical exploitation (zero-day exploits against baseband, Wi-Fi chipset, or browser). They have the patience and resources to wait for you to make a mistake -- and if the two-phone strategy requires perfect behavioral discipline, the state adversary only needs you to slip once.

| Goal | Phone A (Flip) | Phone B (Custom OS) | Computer | Success Rate |
|---|---|---|---|---|
| Obtain subscriber identity | 100% | 0% (no SIM) | 100% (ISP backdoor) | 67% |
| Obtain real-time location | 100% (CALEA, Stingray) | 100% (Wi-Fi geolocation + physical surveillance) | 100% (ISP NetFlow + IP geolocation) | 100% (all devices) |
| Correlate all devices | 100% (tower dumps, ISP logs, surveillance cameras, financial records) | | | 100% |
| Defeat encryption | 100% (flip phone, no encryption) | Variable (GrapheneOS + strong passphrase resists most forensic tools) | Variable (Qubes/Tails resists, Windows/Mac does not) | Device-dependent |
| Zero-day exploitation | 100% (baseband) | 80% (baseband if cellular present; 0% if Wi-Fi only + hardened) | 70% (browser, email client) | High |

**Verdict: The two-phone strategy does not protect against a state-level adversary.** They will obtain your identity from Phone A's carrier or your ISP, correlate Phone B's Wi-Fi BSSIDs to your home address, obtain a warrant for physical seizure of all devices, and exploit baseband (Phone A) or browser (Computer) to install surveillance malware.[^4]

At this threat level, the recommendation is stark: no electronic strategy is sufficient. Use offline communication, pre-arranged codes, and face-to-face meetings in random public locations.

## The Decision Matrix: Should You Use This Strategy?

| Your Threat Profile | Recommended Action | Expected Privacy Level |
|---|---|---|
| Casual user (avoid ads, data brokers) | Single de-Googled phone + Signal + VPN (two phones unnecessary) | 90% of benefit with 10% of effort |
| Journalist / activist (avoid local police, corporate surveillance) | Two-phone strategy with all mitigations (burner SIMs, faraday bags, no home use) | 80% effective against Level 2 adversaries |
| Whistleblower (avoid federal LE) | Two-phone strategy + extreme OpSec + assume eventual compromise | 50% effective; use dead drops, no electronics |
| State-level target (intelligence agencies) | No electronic strategy is sufficient. Use offline communication, pre-arranged codes, face-to-face in random public locations. | Less than 10% |

## Threat Modeling Questions to Ask Yourself

A proper threat model answers these questions honestly and documents the answers. Writing them down is important because it forces specificity -- vague threats produce vague defenses, and vague defenses fail against concrete adversaries.

### Question 1: Who Is My Adversary?

Not in general terms like "the government," but specifically. Name the institution or type of actor. What is their legal authority? What tools do they have access to? How much budget do they have? Do they have physical surveillance capability? Can they compel third parties (carriers, ISPs, platforms) to produce records? Are they limited to a single jurisdiction, or can they operate across borders?

Be honest with yourself. If you are a journalist writing about municipal corruption, your adversary is local police and the city government -- not the NSA. If you are an activist organizing a protest, your adversary is local law enforcement with possibly state-level resources -- not a three-letter intelligence agency. If you are a source in a federal investigation, your adversary is the FBI -- and you need a different set of mitigations entirely.

### Question 2: What Assets Am I Protecting?

Messages, contacts, location history, identity, reputation, financial records, medical information? Each asset has a different value to different adversaries. Your location history is valuable to a stalker but irrelevant to an advertiser. Your message content is valuable to law enforcement but irrelevant to a data broker. Your contacts list is valuable to both.

List your assets in priority order. The most valuable assets deserve the strongest protections. Assets you are willing to lose can be left with weaker protections or none at all. This is how you avoid the trap of trying to protect everything equally and ending up with security theater across the board.

### Question 3: What Happens If I Lose This Asset?

Is the consequence embarrassment, job loss, legal liability, physical danger, or loss of liberty? The severity determines the appropriate response. Embarrassment from a data broker knowing your shopping habits does not justify a two-phone strategy with faraday bags and burner SIMs. Physical danger from a stalker with access to your location history absolutely does.

Map each asset to a consequence severity. Assets whose compromise leads to physical danger or legal liability require the highest level of protection. Assets whose compromise leads to inconvenience or embarrassment can tolerate commodity protections.

### Question 4: How Much Effort Am I Willing to Invest?

Privacy is not binary -- it is a sliding scale of effort versus protection. The 80/20 rule is the most important concept in this handbook: 80% of privacy benefit comes from 20% of the effort (a single de-Googled phone, Signal, a VPN, basic digital hygiene). The remaining 20% of benefit requires 80% of the effort (two phones, faraday bags, burner SIMs, Tails OS, constant OpSec discipline).

Be honest about how much effort you will actually sustain over months and years. A strategy that requires daily vigilance will fail on day 47 when you are tired and just want to check your email on the wrong device. A strategy that requires weekly maintenance will fail on week 12 when you forget to rotate a burner SIM. Privacy strategies fail not because the adversary is powerful, but because the user is human.

### Question 5: What Is My Acceptable Failure Scenario?

No strategy is perfect. You must decide in advance: at what point does the adversary win, and what happens then? If you are a journalist, the acceptable failure may be that your source's identity is revealed -- and you need a plan for that scenario (legal support, rapid document destruction, communication with editors). If you are a domestic violence survivor, the acceptable failure may be that your location is revealed -- and you need a safety plan that includes a pre-arranged safe location and emergency contacts.

Defining the failure scenario in advance lets you test your strategy against it. If your strategy fails catastrophically under conditions you consider acceptable, you need a different strategy. If it survives those conditions, you can accept the residual risk and move forward.

## Why Threat Modeling Matters More Than Tools

Most privacy discussions focus on tools -- which phone, which OS, which VPN, which messenger. But tools are meaningless without a threat model. A whistleblower facing a state actor and a journalist covering local politics face completely different adversaries. The whistleblower needs dead drops and pre-arranged codes. The journalist needs a burner SIM and a faraday bag. The casual user needs none of these things.

The tools are the same: two phones, Signal, VPNs, encryption. The threat model determines which subset of mitigations applies and how strictly they must be followed.

## The "Who Is Actually Trying to Track Me" Framework

Here is a practical, step-by-step framework for identifying your adversary and calibrating your privacy strategy accordingly.

### Step 1: Start with the Lowest Plausible Adversary

Most people overestimate their threat level. The media and privacy community disproportionately focus on state-level surveillance, but for the vast majority of users, the real threat is advertising and data brokerage. Begin by assuming your adversary is a data broker or advertiser. Implement the basic stack: one de-Googled phone, Signal with a strong PIN and registration lock, a reputable no-logs VPN, a privacy-focused browser with fingerprinting protection, and basic digital hygiene (unique passwords, two-factor authentication, regular data cleanup).

This stack handles 80% of privacy threats for 95% of users. Implement it, use it for 30 days, and honestly assess whether your concerns are addressed before escalating.

### Step 2: Ask: Does This Fail?

After 30 days with the basic stack, assess whether your threat model requires escalation. Ask specific questions:

- Am I being actively followed or surveilled? If yes, you need physical OpSec (faraday bags, route variation, safe locations) in addition to technical protections.
- Have I received legal process (subpoena, court order, warrant) or credible threats of legal action? If yes, you need legal support and a strategy that assumes eventual compromise.
- Am I crossing borders with sensitive data? If yes, you need a burner flip phone and a separate travel device with minimal data.
- Am I communicating with sources or subjects that, if revealed, would cause physical danger? If yes, you need Signal with disappearing messages, a burner phone number, and strict compartmentalization.

If the answer to all of these is no, you do not need two phones. You are in the 95% for whom a single de-Googled phone provides adequate privacy.

### Step 3: Escalate Deliberately, Not Preemptively

If your circumstances warrant escalation -- you are a journalist covering organized crime, an activist facing police surveillance, a source in a leak investigation -- escalate one tier at a time. Do not jump directly to the full "Compartmentalized Burner" model unless a Level 2 adversary is confirmed.

Escalate in this order: (1) add a VPN if you have not already, (2) switch to a privacy-focused OS, (3) add a dedicated Signal number not linked to your identity, (4) introduce a second device with strict usage rules, (5) add faraday bag discipline, (6) implement burner SIM rotation, (7) adopt Tails or Qubes for computer use.

Each tier adds complexity and failure risk. Only add a tier when you are certain the previous tier is insufficient against your actual adversary.

### Step 4: Test Your Assumptions

The best way to understand your actual threat level is to test it empirically:

- Request your data from carriers. In the US, there is no simple way to do this, but you can file a privacy request. The response will show you what data the carrier retains and for how long.
- Capture your own Wi-Fi probe requests. Use Wireshark or a similar tool on a laptop to see what your phone broadcasts when Wi-Fi is enabled. You will likely be surprised by how many remembered SSIDs are revealed.[^5]
- Check your browser fingerprint at fingerprinting detection sites. See how unique your browser configuration is compared to other users.
- Review your Signal privacy settings. Check whether registration lock is enabled, whether disappearing messages is on, and whether you have linked devices you forgot about.[^6]

The threats documented in this handbook are real, but they apply differently depending on who you are and what you do. Testing your assumptions prevents both paranoia and complacency.

### Step 5: Accept That Perfect Privacy Is Impossible

The final step in every proper threat model is acceptance: you cannot eliminate all risk. You can only reduce it to a level that matches the value of what you are protecting and the capability of your adversary.

This is the hardest step because it requires acknowledging that no technical configuration -- no operating system, no encryption protocol, no faraday bag, no burner SIM rotation -- can protect against a sufficiently determined adversary with sufficient resources. Privacy is risk management, not risk elimination. The goal is to make the cost of compromising you higher than the value of what you are protecting. That is the real work of threat modeling, and it is never truly finished.

[^1]: ACLU, "Stingray: The Surveillance Tool the Government Has Been Hiding" (2014). Documents that IMSI catchers (Stingrays) are law enforcement tools unavailable to private commercial actors; their deployment requires legal authority not available to advertisers or data brokers.
[^2]: 18 U.S.C. § 2703(d) (Stored Communications Act). Authorizes government entities to compel ISPs and carriers to disclose subscriber records and connection logs through a court order based on "specific and articulable facts." See also Carpenter v. United States, 585 U.S. 296 (2018), which held that obtaining historical cell-site location information requires a warrant.
[^3]: U.S. Department of Justice, "Obtaining Electronic Evidence from Foreign Countries: MLAT and Other Mechanisms" (Office of International Affairs). MLATs allow federal agencies to request records from foreign carriers and ISPs through treaty-based legal cooperation.
[^4]: EFF, "Stingray Tracking Devices: Who's Got Them?" (eff.org, updated). Documents the use of cell-site simulators by federal and state agencies to track device location in real time; see also NIST SP 800-187, "Guide to LTE Security" (2017), §6.
[^5]: Mathy Vanhoef et al., "Why MAC Address Randomization is Not Enough: An Analysis of Wi-Fi Network Discovery Mechanisms," ACM Asia CCS 2016. Demonstrates that probe request SSID lists are a unique per-device fingerprint visible to any passive Wi-Fi listener within range.
[^6]: Signal Foundation, "Government Requests," signal.org/bigbrother (updated periodically). Describes what account metadata Signal retains and can produce under valid legal process, and documents how registration lock and other settings affect that exposure.
