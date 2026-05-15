# Chapter 49: Real-World Failures and Lessons

## What This Chapter Is

Every chapter before this one has described surveillance mechanisms, legal authorities, and failure modes in the abstract. The threat model is accurate. The forensic analysis is accurate. But abstraction has limits. The natural response to reading about ISP metadata logs or CSLI data collection is to imagine these as hypothetical risks — threats that exist in principle but that happen to other people.

They do happen to other people. The cases below are in the public record. They appear in court filings, congressional testimony, FOIA releases, published journalism, and Supreme Court opinions. No case study below is hypothetical. The exact mechanisms described elsewhere in this handbook were used, in documented form, against real individuals and institutions.

The purpose of this chapter is not to sensationalize these cases or to characterize the people involved. The purpose is to make the abstract concrete. When Ch46 describes location dwell time correlation, Case 1 shows what that correlation looks like in practice. When Appendix I categorizes Tier 0 threats, Case 5 shows that a Tier 0 actor successfully deanonymized a specific individual using a $100 commercial data purchase.

Each case is documented with the primary source. Each lesson maps directly to a specific handbook chapter or section.

---

## Case 1: Ross Ulbricht / Silk Road (2013)

**Context.** Ulbricht operated the Silk Road darknet marketplace from approximately 2011 to 2013. He was arrested in San Francisco in October 2013. The prosecution relied on digital evidence obtained before and during arrest.

**What happened.** FBI investigators identified Ulbricht through a layered correlation process, not a single technical exploit. Early in the investigation, Ulbricht had posted questions under his real name on a programming forum, then deleted the post — but Google's cache preserved it. Separately, forum posts on Silk Road-adjacent sites contained linguistic patterns and technical details consistent with the operator. These were application-layer traces.

The decisive physical correlation came from café Wi-Fi. Ulbricht logged into Silk Road's administration panel regularly from a San Francisco public library and from a neighborhood café. The IP address logs from those sessions matched the IPs assigned by those locations' public Wi-Fi networks at the times of the logins. **The pattern of connection timestamps, geographic location, and forum post timing created a correlation that narrowed his location to a specific neighborhood, then to specific venues.**

At arrest, agents waited until he was logged into the Silk Road admin panel — mid-session — before physically grabbing the laptop. The device was seized with an active, authenticated session. Encryption was irrelevant because the device was unlocked.

**Handbook layer exploited.**
- ISP / Application layer: IP address logs from café Wi-Fi tied session times to physical locations
- Application layer: Forum post metadata, cached content
- Physical: Location dwell time correlation (Ch46); seizure of an unlocked, in-use device

**Key failure.** He used the same public Wi-Fi locations repeatedly. A single café visit produces a data point. Returning to the same café at the same times produces a pattern. **Location dwell time correlation works because human behavior is predictable. The same person tends to use the same coffee shop on the same schedule.** A single data point is not identifying. Twenty data points at the same location are.

**Lesson.** Ch46 describes location dwell time correlation as a documented investigative technique. This is the documented example. Public Wi-Fi is not anonymous — IP address logs at the provider level link your session to a physical access point, and physical access points have known locations. Rotating venues and sessions breaks the pattern. Using the same location repeatedly is functionally equivalent to using home Wi-Fi.

---

## Case 2: Signal Subpoena Response (2016)

**Context.** A federal grand jury in the Eastern District of Virginia subpoenaed Signal (Open Whisper Systems) for user data related to an investigation. The subpoena was later unsealed, and Signal published its complete response.

**What happened.** Signal complied with the subpoena and produced everything it had. Signal's complete response to a federal grand jury subpoena for user account data was: **account creation date and last connection date. Nothing else existed to produce.**

No message content. No contact list. No IP address history. No device identifiers beyond what Signal already disclosed publicly in its architecture documentation. Signal's server-side architecture does not store this data, so it could not be produced. The subpoena returned two timestamps.

**Handbook layer.** This is the application layer — but this case documents a success, not a failure. It demonstrates that app selection at the application layer produces measurable, legally-documented outcomes.

**Key finding.** A federal grand jury subpoena carries legal force that no app can refuse. **The question is not whether a company will comply — they will — but what data exists to hand over.** Signal's architecture means the answer to that question is: almost nothing. The same subpoena to WhatsApp or Meta would yield message frequency metadata, contact graph (who you communicate with), IP address history, device identifiers, and account recovery information.

**Lesson.** The application layer is defensible. The defense is architectural: choose apps whose server-side data collection is minimal by design, not by policy. Policies change under legal pressure. Architecture is harder to change. Signal's 2016 response is primary source evidence, not marketing copy.

---

## Case 3: Associated Press Phone Records (2013)

**Context.** The Department of Justice secretly subpoenaed two months of call records for approximately 20 AP phone lines, including lines used by individual reporters. The AP learned about the subpoena only after the records had already been collected and reviewed.

**What happened.** DOJ obtained the records through administrative subpoena — a lower standard than a warrant, not requiring judicial approval or notification to the target. The subpoena covered office lines, individual desk lines, and reporters' personal cell phone lines. The stated justification was a national security leak investigation.

**The AP had no opportunity to contest the subpoena before the records were collected.** The first notification they received was a letter from DOJ informing them that the records had already been obtained.

**Handbook layer exploited.**
- Cellular: Call Detail Records (CDRs) — who called whom, duration, timestamp, tower location
- Legal access: Administrative subpoena, below the warrant threshold, with no prior notification requirement

**Key failure.** No compartmentalization between reporters' work identities and their source communication patterns. Reporters used their professionally-identified phone numbers — the same numbers on press credentials, business cards, and editorial directories — as their primary contact numbers. A subpoena targeting the institutional phone records captured the full CDR history for every number on those lines.

**The two-phone strategy for journalists (Ch32) exists in direct response to cases like this.** If a reporter's source communications occur on a separate, unregistered device that is operationally isolated from their professional identity, a subpoena targeting their AP press credentials does not capture their source network.

**Lesson.** Administrative subpoenas for phone records do not require a warrant, do not require advance notice, and can be issued broadly. A journalist's Phone A — their professional-identity device — is a permanent subpoena target. Phone B, if properly compartmentalized, is outside the scope of a subpoena issued against the journalist's known identity. The legal mechanism that makes this attack possible has not changed since 2013.

---

## Case 4: Carpenter v. United States (2018)

**Context.** Timothy Carpenter was charged in connection with a series of armed robberies. Investigators obtained 127 days of Cell Site Location Information (CSLI) from his carrier using a court order — not a warrant. CSLI records showed which cell towers his phone pinged, at what times, across four months.

**What happened.** Using 127 days of CSLI, investigators mapped Carpenter's location with enough precision to place him near the robbery locations at the relevant times. The records were obtained under the Stored Communications Act, which requires only "reasonable grounds" — a lower threshold than the Fourth Amendment's probable cause standard for a warrant.

The Supreme Court ruled 5-4 in Carpenter v. United States that warrantless collection of CSLI violates the Fourth Amendment. Chief Justice Roberts, writing for the majority, held that **seven days of CSLI is enough to reveal a detailed, comprehensive picture of a person's life** — home, work, church, medical providers, political associations — and that this level of granularity requires a warrant.

**Handbook layer exploited.** Cellular: Tower location data (CSLI). This is Tier 2 in the handbook's threat taxonomy — carrier-level data available to law enforcement through legal process.

**Significance.** Carpenter drew the sharpest post-digital line between metadata and constitutionally-protected location information. Before Carpenter, CDRs including tower location required no warrant. After Carpenter, CSLI does. The ruling did not address real-time tracking, precise GPS data from carriers, or data obtained through third parties.

**The retrospective exposure problem is documented here.** Carpenter's CSLI was collected before the Supreme Court ruled that such collection requires a warrant. The ruling did not suppress the evidence retroactively. **Data collected under the legal standard that existed at the time of collection is not affected by later legal developments.** This is why the handbook's Tier 2 section reflects current post-Carpenter law while acknowledging that carrier infrastructure capable of generating this data has existed for decades.

**Lesson.** Cellular CSLI is a constitutionally significant data category. A warrant is now required for historical CSLI. That requirement did not exist when the data in Carpenter was collected. The legal landscape changes, but collected data does not disappear when the law changes.

---

## Case 5: Grindr Location Data (2020–2021)

**Context.** The Pillar, a Catholic news outlet, published an article in July 2021 identifying a senior official of the United States Conference of Catholic Bishops as a user of the Grindr dating app. The identification was made using commercially purchased location data, not law enforcement tools.

**What happened.** The Pillar obtained a dataset of location data and app usage signals from a commercial data broker. The data had been sourced, through the broker chain, from Grindr. Using the dataset, The Pillar identified a mobile device that appeared at the official's home address, his workplace, and locations consistent with Grindr usage over a period of weeks. **The combination of home address, employer location, and app-associated location data was sufficient to identify a specific individual without any law enforcement involvement.**

No warrant. No subpoena. No court order. No law enforcement agency. The data was purchased commercially.

**Handbook layer exploited.**
- Application: Location permissions granted to Grindr, which sold or shared data with broker networks
- Physical: Location correlation (home, workplace, recurring locations) enabling deanonymization

**Key mechanism.** The individual's device was not identified by name. It was identified by behavior. A device that sleeps at address X, works at address Y, and appears at location Z with Grindr signals is identifiable if X and Y are uniquely associated with one person. The app did not need to know the user's name. **Location pattern correlation did the identification work.**

This is Tier 0 in the handbook's threat taxonomy: a non-state actor with a commercial data purchase and a motivated researcher. The cost of this deanonymization is estimated in the low hundreds of dollars.

**Lesson.** Location permissions granted to any app are not contained to that app. Data broker pipelines route location data from apps to aggregators to resellers to end buyers. The buyer does not need to be a government agency. The data does not need to be linked to a name at purchase — location patterns provide the name. Appendix I's Tier 0 threat description is not abstract. This case is the documented example.

---

## Case 6: Cellebrite UFED at US Border Crossings (2017–2023)

**Context.** The ACLU and other organizations obtained records through FOIA requests documenting Customs and Border Protection's use of Cellebrite UFED (Universal Forensic Extraction Device) tools at US ports of entry. CBP has confirmed that it conducts device searches at the border under the border search exception, which generally does not require a warrant or probable cause for routine searches.

**What happened.** Multiple documented cases across the FOIA record show phones presented at border crossings subjected to Cellebrite extraction. The extraction process takes approximately 5–10 minutes per device. The UFED tool extracts data without requiring device unlock in some configurations, depending on the device model, OS version, and encryption state.

**What Cellebrite UFED extracts from a cooperating or vulnerable device:**
- Call logs and SMS
- Contacts and calendar
- Photos and videos (including deleted, if not overwritten)
- App data for installed applications
- Browser history
- Cached location data
- Device identifiers

**What Cellebrite UFED does not reliably extract as of 2024–2026:** Properly encrypted Signal messages on a locked GrapheneOS device. Cellebrite's published extraction capabilities documentation indicates limited support for GrapheneOS. Encrypted message content stored only on the device and not backed to any cloud service is not accessible through documented Cellebrite methods against a locked, properly configured GrapheneOS installation.

**Handbook layer exploited.**
- Physical: Device seizure and forensic extraction
- Legal: Border search exception (no warrant required at port of entry)

**Lesson.** The border crossing use case for the two-phone strategy (Ch32) is not theoretical. CBP has documented, operational capability to extract data from phones at the border in minutes. The clean Phone A strategy — handing over a device with nothing of investigative value — directly addresses this attack. A locked GrapheneOS device with full-disk encryption and no logged-in sessions provides meaningful resistance to documented Cellebrite methods. **The specific combination of device, OS, and encryption state matters.** A stock Android or iOS device in a standard configuration provides substantially less resistance.

---

## Comparative Summary

| Case | Tier | Primary Layer Exploited | Could Two-Phone Strategy Have Helped? | Key Lesson |
|------|------|------------------------|---------------------------------------|------------|
| Ulbricht / Silk Road (2013) | Tier 3 | ISP + Application + Physical | Partially — compartmentalization helps; location discipline required separately | Repeated same-location Wi-Fi creates a trackable pattern |
| Signal Subpoena (2016) | Tier 3 | Application (server-side) | N/A — this is a success case | App architecture determines what a subpoena can return |
| AP Phone Records (2013) | Tier 3 | Cellular (CDRs) + Legal | Yes — Phone B source network is outside scope of Phone A subpoena | Administrative subpoenas require no warrant and no notice |
| Carpenter v. US (2018) | Tier 2 | Cellular (CSLI) | Partially — reduces CSLI volume; does not eliminate it | CSLI now requires a warrant; pre-Carpenter data is not retroactively suppressed |
| Grindr Location Data (2020–21) | Tier 0 | Application (location permissions) | Partially — Phone B isolation limits exposure; app permissions must also be restricted | Commercial data brokers enable deanonymization without law enforcement |
| Cellebrite at Border (2017–23) | Tier 2 | Physical (device seizure) | Yes — Phone A as clean surrender device is precisely designed for this attack | GrapheneOS + full encryption + locked device limits documented Cellebrite extraction |

---

## What These Cases Establish Collectively

**The threat model is not constructed from hypotheticals.** Every surveillance layer described in this handbook has a documented real-world deployment. The cases above span six different attack vectors, three different actor types (federal law enforcement, commercial data brokers, border enforcement), and two different legal frameworks (warrant-required and warrant-not-required).

**The two-phone strategy addresses some of these attacks directly, and others only partially.** It is not a universal solution. The Grindr case was not a two-phone failure — it was an app permissions failure that a two-phone strategy alone would not have prevented without also restricting location permissions on Phone B. The Ulbricht case required location discipline that goes beyond device compartmentalization.

**Legal authority expands and contracts.** Carpenter changed the legal standard for CSLI, but not retroactively. Signal's 2016 subpoena response demonstrated that architecture constrains what legal authority can compel. These two cases together suggest that the most durable protection combines minimal data generation with strong encryption — so that even where legal authority is clear, there is little data to produce.

**Tier 0 threats require no law enforcement involvement.** The Grindr case cost the actor a commercial data purchase. The mechanism required no special authority, no warrant, no subpoena, no hacking. This is the most underappreciated threat category in most risk frameworks. Location data granted to an app is, in documented practice, available to any motivated buyer.
