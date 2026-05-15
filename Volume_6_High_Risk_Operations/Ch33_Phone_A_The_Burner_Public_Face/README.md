# Chapter 33: Phone A — The Burner Public Face

## The Role of Phone A

Phone A is the phone you show to the world. It is the device that crosses borders, sits on your desk at work, appears in your daily carry, and satisfies any demand to inspect your phone. Its purpose is not to protect your data. It barely carries any data to protect. Its purpose is to be surrendered without consequence.

Everything about Phone A is designed around a single principle: it must contain nothing that links you to Phone B or to any sensitive activity in your life. Phone A is bait. It is the decoy. It must look convincing as a daily driver while revealing absolutely nothing of value.

## Device Selection: Nokia 225 4G or Similar

The ideal Phone A has a specific set of characteristics. It must be a dumb phone. Not a smartphone with the apps disabled, not an old iPhone wiped clean, but a genuine feature phone that cannot run modern applications and cannot generate the rich metadata that smartphones produce.

**Nokia 225 4G** is the gold standard for this role, but any equivalent dumb phone will work. The critical requirements are:

- **No apps.** The phone should not support installing third-party applications. This eliminates the risk of app-based tracking, metadata leakage, and account associations that could link the device to your identity.

- **No GPS.** The phone should have no GPS receiver. This prevents location logging by the device itself. If the device does not record location, it cannot reveal it later.

- **No Wi-Fi.** This is possibly the most important requirement. Many feature phones now include Wi-Fi, and that is a dealbreaker. A phone with Wi-Fi can probe for networks, log BSSIDs, and create a forensic trail of location data.[^1] Phone A must have no Wi-Fi capability at all.

- **Basic cellular only.** The phone should support voice calls and SMS on standard cellular networks. Nothing more. No data connectivity. No app store. No browser.

The Nokia 225 4G meets these criteria well. It supports 4G calling and SMS, has no app ecosystem, no GPS, and the Wi-Fi variant must be specifically avoided. The 4G capability is important because it means the phone works on modern networks that are phasing out 3G, ensuring you can maintain service without upgrading.

Other acceptable options include the Alcatel Go Flip, the Light Phone II (if configured correctly), or any basic feature phone that strips out smart capabilities. The key is to verify before purchase that Wi-Fi is either absent or can be permanently disabled.

## SIM: Prepaid, Cash Purchase, No Registration

The SIM card in Phone A is the link between the device and the cellular network. That link can also link the device to you. The goal is to sever that connection completely.

**Prepaid SIM, cash purchase.** The SIM must be purchased with cash at a retail location that does not require identification. In many jurisdictions, prepaid SIMs are available at convenience stores, electronics retailers, and vending machines. The purchase should leave no paper trail.[^2]

**No registration.** Some countries require SIM registration by law. In those jurisdictions, the two-phone strategy becomes significantly more difficult, though not impossible. Options include using a SIM from a jurisdiction that does not require registration, purchasing a SIM that has already been activated by a third party through unofficial channels, or accepting the risk that a registered SIM creates a paper trail and planning your operational security accordingly.

**Refill with cash.** When the prepaid balance runs low, refill with cash at a retail location. Do not use a credit card, debit card, or any online payment method. The refill should be as anonymous as the original purchase.

**Burner number behavior.** The number assigned to Phone A should never be used to register for any service. It should never be linked to any account, never used for two-factor authentication, never given to any service that asks for a phone number. It is used exclusively for voice calls and SMS, and only with contacts who do not need to know your real identity.

## Usage: Calls and SMS Only, No Data, No Apps

The operational discipline for Phone A usage is straightforward but absolute:

- **Voice calls only for communication.** When you need to make a call, use Phone A. Keep calls brief and businesslike. Do not discuss sensitive topics on Phone A calls. Assume the call is monitored.

- **SMS for basic text communication.** SMS is not encrypted and is stored by the carrier.[^3] Treat every SMS sent from Phone A as public. No sensitive information, no planning messages, no references to Phone B or any opsec activity.

- **No data.** Phone A should never have its data connection enabled. If the phone supports mobile data, disable it permanently through the settings menu or by having the carrier block data on the line. Data usage creates metadata trails, IP logs, and the potential for app-based tracking.

- **No apps.** Do not install any applications on Phone A. If the phone has preinstalled apps, do not open them. Do not create accounts. Do not sign in. Every app is a potential data leak.

- **No accounts.** Never log into any account on Phone A. No email, no social media, no messaging apps, no cloud storage. The phone should never know your name, your email address, or your usernames.

## Replacement: Every 90 Days

Phone A has a limited lifespan. The longer a device exists, the more data accumulates. Tower location records, call logs, SMS metadata, and the device's own unique identifiers create a growing historical record.[^4] The solution is regular replacement.

**Replace both the phone and the SIM every 90 days.** This limits the historical exposure to three months. If your Phone A is ever seized, the investigator gets at most three months of data. If an adversary is building a pattern of your behavior, they have at most three months of patterns.

**Do not replace at regular intervals that match your calendar.** If you replace every 90 days on a fixed schedule, an adversary monitoring your phone activity will notice the gap. Replace on a slightly irregular schedule, with a random offset of one to two weeks, to make pattern detection harder.

**Destroy the old device before activating the new one.** Do not keep old phones in a drawer. Do not reset them and give them away. Physical destruction is the only safe disposal method. The old SIM must also be physically destroyed, not just deactivated. A deactivated SIM can still be read with the right equipment.[^5]

## Transport: Faraday Bag When Not in Use

When Phone A is not actively being used, it should be in a faraday bag. This serves multiple purposes:

- **Prevents tower triangulation when idle.** When Phone A is in your pocket, it is communicating with nearby cell towers, allowing the carrier to track your location continuously.[^6] A faraday bag blocks this communication, creating gaps in your location history that make pattern analysis harder.

- **Prevents passive scanning.** Even when idle, the phone emits signals that can be detected by IMSI catchers and other surveillance equipment.[^7] The faraday bag blocks all emissions.

- **Creates operational discipline.** The habit of putting the phone in the faraday bag reinforces the separation between Phone A and Phone B. It becomes a ritual that reduces the chance of accidental co-location.

The faraday bag should be tested regularly to confirm it still works. Faraday bags degrade over time, especially at the seams and closures. See Chapter 35 for detailed testing procedures.

## Co-Location: Never in Same Building as Phone B

This is the rule that most users struggle with, and it is also the most important. Phone A and Phone B must never be in the same physical location at the same time.

**Why this matters.** If Phone A and Phone B are ever at the same location at the same time, tower records will show both devices connecting to the same cell towers at the same times. Any investigator who obtains a tower dump for either device can correlate them.[^8] Once correlated, the entire compartmentalization strategy collapses. The investigator now knows that the person carrying Phone A is also the person who controls Phone B.

**What same building means.** It is not enough to keep them in different rooms. If they are in the same building, they are at the same location. Tower records do not distinguish between floors or rooms. The phones must be in different physical structures, ideally at least several hundred meters apart.

**Practical implementation.** If you live alone, Phone B should be stored elsewhere perhaps with a trusted contact, in a secured locker, or in a location that is not your residence. If you live with others, Phone B can be stored in a place you do not typically occupy, but extreme care is needed to ensure both devices are never present simultaneously.

## Mitigated Architecture Reference

The following table from the forensic analysis summarizes the revised requirements for Phone A in the mitigated architecture:

| Original | Revised Requirement | Rationale |
|---|---|---|
| Dumb flip phone | Burner flip phone, purchased with cash | No identity link to carrier |
| Carrier plan (postpaid) | Prepaid SIM, cash purchase, refilled with cash | Anonymous activation |
| Used freely | Faraday bag when not in active use | Prevents tower tracking when idle |
| Kept indefinitely | Destroyed and replaced every 30-90 days | Limits historical exposure |
| Carried with Phone B | Never carried with Phone B | Prevents correlation |

Phone A is only as strong as your discipline in maintaining these requirements. Every deviation creates a forensic link. The phone itself is cheap. The security it provides is only as valuable as the operational integrity with which it is managed.

[^1]: Wi-Fi probe requests from devices expose MAC addresses and known-network SSIDs; see Mathy Vanhoef et al., "Why MAC Address Randomization is Not Enough: An Analysis of Wi-Fi Network Discovery Mechanisms," *AsiaCCS 2016*.
[^2]: Michael Bazzell, *Extreme Privacy*, 5th ed. (2025), inteltechniques.com, recommends cash SIM acquisition as a foundational step in the two-device strategy.
[^3]: SMS messages are stored by carriers as part of standard Call Detail Records; see *Carpenter v. United States*, 585 U.S. 296 (2018), which describes carriers' routine retention of subscriber communications metadata.
[^4]: Historical cell site location information (CSLI) is retained by carriers and constitutes a "detailed, encyclopedic, and effortlessly compiled" record of movements; *Carpenter v. United States*, 585 U.S. 296, 309 (2018).
[^5]: Cellebrite UFED and similar forensic tools are capable of extracting data from deactivated SIM cards; see Cellebrite UFED capabilities documentation (Cellebrite Ltd.).
[^6]: Carriers log tower registration events continuously, creating a location history; see *Carpenter v. United States*, 585 U.S. 296 (2018).
[^7]: IMSI catchers (cell-site simulators) passively capture device identifiers from nearby phones; see EFF, "Stingray Tracking Devices: Who's Got Them?" eff.org/pages/cell-site-simulators-imsi-catchers.
[^8]: Tower dump records linking co-located devices are addressed in *In re Application of U.S. for Historical Cell Site Data*, 724 F.3d 600 (5th Cir. 2013).
