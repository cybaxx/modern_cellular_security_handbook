# Appendix I: Minimum Viable Privacy

## Who This Is For

This appendix is written for one specific reader: a person who has skimmed this handbook, found it overwhelming, and is about to close it and do nothing.

That is the worst outcome. Doing nothing means staying fully exposed to the passive commercial surveillance that affects every person with a smartphone. Doing a little — even just the three actions in the first section below — is dramatically better than nothing. This appendix makes the case for starting small and gives you the smallest meaningful starting point possible.

If you are already implementing the Citizen Max stack from Chapter 28, you do not need this appendix. This is a floor, not a ceiling.

---

## The Minimum Viable Stack

Three changes. This is the absolute minimum that provides meaningful privacy improvement for a normal citizen facing Tier 0 threats (advertisers, data brokers, commercial tracking).

> **A note from practitioners:** Michael Bazzell — former FBI agent and author of *Extreme Privacy* (5th ed., 2025) — argues that data broker removal often delivers more practical privacy benefit for normal people than device hardening. The reasoning: your carrier CDR data, voter registration, property records, and commercial purchase history are frequently more actionable to an adversary than whether you use Brave or Firefox. The minimum viable stack below reflects this priority ordering. Start with what removes the most accessible data first.

### Change 1: Messaging — Replace WhatsApp with Signal

**Time required:** 15 minutes.
**Cost:** Free.

WhatsApp is owned by Meta. It collects your contact list, message metadata (who you message, when, and how often), and location data. This information is used to build advertising profiles. End-to-end encryption protects message content, but the metadata — who you talk to and when — is retained and used commercially.

Signal collects nothing. It does not know who you talk to. It does not know your contacts. It retains only one data point: the phone number you registered with, and the last date you connected to its servers. That is all it has. That is all a subpoena to Signal yields. This has been demonstrated in practice: Signal has responded to government subpoenas with two data points, because that is the entirety of what they hold.

Replace WhatsApp with Signal. Ask the people you message to do the same. This is not a significant inconvenience — Signal works identically to any other messenger. It simply does not harvest your data.

### Change 2: Browser — Add uBlock Origin

**Time required:** 5 minutes.
**Cost:** Free.

uBlock Origin is a browser extension available for Firefox, Chrome, Edge, and Brave. It blocks advertising networks, tracking scripts, and data collection infrastructure at the network request level. The average webpage makes 50–150 network requests on load; uBlock Origin blocks 30–70% of them on most sites. This eliminates the majority of cross-site tracking that follows you across the internet.

Installation takes under five minutes. After installation, no configuration is required. It works automatically and silently.

If you use a mobile browser, switch to Brave (iOS or Android). Brave includes equivalent tracker blocking built in, without requiring an extension.

This single change eliminates more commercial tracking than most people's entire current privacy setup.

### Change 3: Location Permissions — Revoke and Lock Down

**Time required:** 10–20 minutes (depends on number of installed apps).
**Cost:** Free.

Location data is the most commercially valuable data your phone generates. It reveals where you sleep (home address), where you work, where you seek healthcare, where you worship, who you associate with, and what your daily schedule looks like. Apps that have location permission sell this data to data brokers. Data brokers aggregate it, sell it to advertisers, and in some cases provide it to law enforcement without a warrant.

Go to your phone's Settings > Privacy/Permissions > Location. Review every app with location access. Apply the following rules:

| Permission Level | Grant to... |
|---|---|
| **Always** (background location) | Nothing. There is no consumer app that legitimately requires always-on background location. If an app demands it, delete the app. |
| **While Using** | Only: maps/navigation apps (Google Maps, Apple Maps, Waze), rideshare apps (Uber, Lyft) while actively using them, weather apps (optional — you can type a city instead) |
| **Denied** | Everything else. Social media, games, shopping apps, food delivery (type your address manually), news apps, fitness apps (use GPS only during workouts), browsers |

This takes 15 minutes once. After that, review new app installs before granting location.

---

## The Three Changes, Summarized

| Change | Time | Cost | What it stops |
|---|---|---|---|
| Switch to Signal | 15 min | Free | Contact graph harvesting, message metadata tracking by Meta |
| Install uBlock Origin / use Brave | 5 min | Free | 30–70% of cross-site advertising trackers per page load |
| Revoke location permissions | 15 min | Free | Commercial location data sales; data broker location profiles |

**Total time: Under 35 minutes.**

### Change 4 (High-Impact, Often Overlooked): Remove Yourself from Data Brokers

**Time required:** 2–4 hours initially; 30 minutes quarterly.
**Cost:** Free (manual) or $129/year (DeleteMe automated).

Before you configure a VPN or install a new browser, consider where the most actionable data about you actually lives. Data brokers — Spokeo, Radaris, Whitepages, Intelius, BeenVerified, Acxiom, TruePeopleSearch, LexisNexis — aggregate your name, address history, phone numbers, family members, employer, and in some cases financial and criminal records. This data is purchased by private investigators, stalkers, process servers, and advertisers. It requires no subpoena. It is for sale to anyone who asks.

Removing yourself from the major data brokers is one of the highest-impact privacy actions a normal person can take. Each broker has an opt-out form (most are free). A prioritized removal list, with direct opt-out links, is maintained in Michael Bazzell's *Personal Data Removal Workbook* (v5.0, free download at inteltechniques.com). The highest-priority targets: **Spokeo, Radaris, Whitepages, Intelius, BeenVerified, TruePeopleSearch, Acxiom, Infotracer**.

Automated services (DeleteMe, Kanary, Incogni) will perform and re-run removals on your behalf for an annual fee. For most people, the time savings justify the cost.

These three changes do not make you forensically opaque. They do not protect you against targeted law enforcement surveillance. They do not address cellular metadata. They address the single biggest privacy threat facing a normal citizen: the passive commercial surveillance ecosystem that monetizes your behavior, your location, and your communications.

After these three, stop and live with them for a month. If privacy matters to you and the changes have been painless (they will be), add the next layer.

---

## The Next Layer: Three More Hours

If the minimum viable stack is working and you want more, the following additions require approximately three hours total and cost $5–10 per month:

| Addition | Time | Cost | What it stops |
|---|---|---|---|
| Switch to DuckDuckGo or Startpage for search | 5 min | Free | Search history profiling; personalized ad targeting from search behavior |
| Set up encrypted DNS (Cloudflare 1.1.1.1 or Quad9) | 15 min | Free | ISP selling your DNS query log; basic ISP-level traffic analysis |
| Sign up for a reputable VPN | 30 min | $5–10/mo | Hiding your real IP address from websites; ISP seeing destination websites. Mullvad (Sweden, no account required, accepts cash) and ProtonVPN (Switzerland) are recommended for users with jurisdictional concerns. Private Internet Access (PIA, US-based) is simpler and lower-cost and is Bazzell's recommendation for normal citizens where jurisdiction is not the primary concern. |
| Create a ProtonMail account for sensitive email | 30 min | Free | Email provider reading and indexing your email content |
| Install a password manager (Bitwarden) | 30 min | Free | Password reuse; credential stuffing attacks |
| Enable two-factor authentication on critical accounts | 30 min | Free | Account takeover after credential breach |

These six additions, combined with the minimum viable stack, constitute the full "Citizen Max" stack described in Chapter 28. They cover approximately 80% of the privacy threats faced by a normal citizen.

---

## What This Does Not Do

Honest assessment: the minimum viable stack and the Citizen Max stack do not protect you against:

- **Law enforcement with legal authority to subpoena your carrier.** Your cellular CDRs, tower location data, and subscriber identity are available to law enforcement with a subpoena. Your carrier cooperates with lawful requests. This requires a much more significant strategy change — see Volume 6.

- **A stalker or abusive partner with physical access to your phone.** Stalkerware installed directly on your device bypasses all the protections above. If you suspect physical access has been exploited, see Tier 1 in Chapter 47 and consider a fresh device.

- **Your employer's device management profile.** If your employer installed an MDM profile on your phone, they have visibility that supersedes these protections. Use a separate personal device for private communications.

- **The data that already exists about you.** Data brokers already have years of location history, purchase history, and behavioral data. The changes above prevent future collection; they do not erase the past. Manually opting out of major data brokers (Acxiom, LexisNexis, Spokeo, Whitepages, etc.) is a separate, time-consuming process. DeleteMe ($129/year) automates much of this.

- **Perfect privacy.** There is no such thing. The goal is to be harder to track than average, to be less commercially valuable, and to make targeted surveillance more expensive. These goals are achievable. Complete invisibility is not.

---

## For the Person Who Will Do Nothing Else

If you close this appendix having done only one thing, do this:

**Install uBlock Origin.**

It takes five minutes. It requires no maintenance. It silently blocks thousands of tracking requests per day. It makes you immediately harder to track across the internet than the vast majority of users. It costs nothing.

Privacy is not binary. Every improvement you make reduces your exposure. Start somewhere. Start here.
