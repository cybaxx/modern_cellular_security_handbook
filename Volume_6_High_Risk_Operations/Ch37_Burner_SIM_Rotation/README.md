# Chapter 37: Burner SIM Rotation

## The Weakest Link in the Chain

The SIM card is the component most likely to compromise your anonymity. Unlike the phone itself, which can be bought, used, and discarded with relative anonymity, the SIM card creates a persistent link between your device and the cellular network. Every time the phone registers with a tower, the SIM identifies itself through the IMSI.[^1] Every call and SMS is logged with the SIM's identity. The carrier maintains records of which IMSI was active at which tower at which time, for as long as the law requires.[^2]

The goal of burner SIM rotation is to limit the window of exposure. If a SIM is used for 90 days and then destroyed, the carrier records for that SIM cover at most 90 days of activity. If the SIM were used indefinitely, an investigator with a subpoena could reconstruct years of your location history and communication patterns.

## Cash Purchase: The Only Safe Acquisition Method

The purchase of the SIM card is the moment when most users unintentionally link themselves to their burner. It is also the moment that requires the most careful operational planning.

**Pay with cash.** This is non-negotiable. Any electronic payment method is a link to your identity. Credit cards, debit cards, and digital wallets all carry your name, account number, and purchase history. Even prepaid debit cards can sometimes be traced back to the point of purchase, and some require identification to activate.

Cash is the only anonymous payment method. The physical bill carries no identifying information. When you hand cash to a retailer, you leave no paper trail.[^3]

**Where to buy.** The ideal purchase location is a convenience store, electronics retailer, or grocery store that sells prepaid SIMs over the counter without requiring identification. Look for stores in neighborhoods you do not normally frequent. Avoid purchasing the SIM within your home neighborhood or near your workplace.

**What to say.** Do not provide any information beyond what is strictly necessary to complete the transaction. If the retailer asks for your name, decline and go to another store. In jurisdictions where registration is not required, no information should be needed.

**Do not buy multiple SIMs at once.** Buying several SIMs in a single transaction creates a bulk purchase that might be remembered by the retailer or captured on CCTV. Buy one SIM at a time, from different stores, on different days.

## No Registration Jurisdictions

The legal landscape for SIM registration varies dramatically by country. Understanding the laws in your jurisdiction is essential before committing to a burner SIM strategy.

**Jurisdictions where prepaid SIM registration is not required.** In many countries, including the United States (at the federal level), prepaid SIMs can still be purchased anonymously over the counter. However, some individual states and countries have enacted registration laws, and the trend is toward increasing regulation.[^4]

**Jurisdictions where registration is required.** Many countries now require photo ID to activate a prepaid SIM. These include India, Australia, most of the European Union (under varying national implementations), South Africa, Japan, South Korea, and numerous others. In these jurisdictions, the burner SIM strategy is significantly more difficult.

**Options in registration-required jurisdictions:**

- Use a SIM from a jurisdiction that does not require registration. This is possible if you travel or have a trusted contact in a no-registration jurisdiction. The SIM will work on roaming networks in your home country, though roaming data is typically logged more extensively.

- Purchase a pre-activated SIM through informal channels. In some countries, there is a gray market for SIMs that have been activated with false or stolen identities. This is legally risky and should be undertaken only with full understanding of the risks.

- Accept the registration requirement and plan accordingly. If you must register, use a minimum of identifying information. Some jurisdictions accept minimal information. Never provide your real address if the system allows a different address.

- Consider whether the two-phone strategy is viable in your jurisdiction at all. If the legal environment makes anonymous SIM acquisition impossible, the strategy may need to be reconsidered or modified.

## The 30 to 90 Day Replacement Cycle

The optimal replacement cycle for a burner SIM balances two competing concerns: limiting historical exposure and maintaining operational practicality.

**30 days.** A 30-day cycle provides the strongest protection. The carrier has at most one month of records associated with your burner SIM. If the SIM is seized or subpoenaed, the exposure window is minimal. The trade-off is operational burden. Every 30 days, you must purchase a new SIM, transfer your essential contacts, and destroy the old SIM.

**60 days.** A reasonable compromise for most users. Two months of records is still a relatively short window for forensic analysis, and the monthly burden is halved.

**90 days.** The maximum recommended cycle. Beyond 90 days, the volume of accumulated location data and communication metadata becomes significant enough to enable meaningful pattern analysis.[^5] An investigator with three months of tower records can identify your routines, frequent locations, and regular contacts.

**Do not replace on the same day of the week or month.** If you always replace the SIM on the first of the month, an investigator monitoring your phone activity will notice the pattern of service gaps. Introduce random variation into your replacement schedule, with a window of plus or minus one to two weeks from your target date.

**Transition procedure.** When replacing the SIM:

1. Activate the new SIM before deactivating the old one, if possible, to maintain service continuity.
2. Call or message your essential contacts from the new number to inform them of the change.
3. Do not transfer the old SIM to a new phone. The old SIM and the old phone should be destroyed together.
4. Destroy the old SIM immediately after the transition is complete.

## Destruction Protocols for Old SIMs

Deactivating the SIM is not enough. A deactivated SIM card can still be read with the right equipment. The card's memory chips retain data even without power, and specialized forensic tools can extract IMSI, ICCID, stored contacts, and SMS messages from deactivated SIMs.[^6]

**Physical destruction is required.** The SIM card must be physically destroyed to the point where the chip cannot be read. Acceptable destruction methods include:

- **Shredding.** A cross-cut shredder that can handle plastic cards will destroy the SIM into small pieces. Verify that the chip section is completely fractured.

- **Burning.** Burn the SIM card in a fire until the plastic is consumed and the chip is visibly damaged. Dispose of the ashes in separate locations.

- **Chemical destruction.** Acid etching or similar chemical treatment will destroy the chip. This is more effort than is typically necessary but is effective.

- **Mechanical destruction.** Smashing the SIM with a hammer until the chip is in multiple pieces is acceptable if done thoroughly. The chip must be visibly fragmented.

**Do not simply cut the SIM with scissors.** Scissors may leave the chip intact, and the two halves can be reassembled or read individually. Destruction must be comprehensive.

**Disposal.** Dispose of the destroyed SIM fragments in separate trash bins, ideally on different days and in different neighborhoods. This prevents an adversary from reconstructing the SIM from collected fragments.

## Prepaid vs. Postpaid Considerations

The choice between prepaid and postpaid service is simple for the burner phone: always prepaid. Postpaid service requires a billing relationship with the carrier, which means your name, address, and payment method are on file. This is incompatible with the goal of anonymity.

**Prepaid advantages:**

- No credit check or identity verification (in permissive jurisdictions).
- No monthly bill that reveals your name and address.
- Service can be activated and deactivated at any time.
- No recurring payment that creates a financial paper trail.
- Can be purchased with cash from third-party retailers.[^7]

**Prepaid limitations:**

- Typically higher per-minute and per-SMS costs.
- Data may be more expensive or unavailable.
- Coverage may be limited to a specific carrier's network.
- Service may expire if not refilled regularly, causing loss of the number.

**Never use postpaid for Phone A.** If you are using postpaid service on any phone that could be linked to Phone A, the link between you and the burner is established through the carrier's billing records. Even using the same carrier for postpaid and prepaid service creates correlation risk if the carrier cross-references accounts.

**For Phone B, cellular is disabled anyway.** Phone B does not need a SIM card at all. Its connectivity is exclusively over Wi-Fi. The Signal registration number used on Phone B should be from a VoIP provider or a one-time-use prepaid SIM that is destroyed after registration. The SIM rotation protocol described in this chapter applies primarily to Phone A.

## Maintaining the Rotation Calendar

Keeping track of SIM replacement dates without creating a digital record that links to your identity requires careful planning.

**Do not use a digital calendar.** Do not set a reminder in your phone, email, or any online service. The reminder itself creates a record that links the burner schedule to your identity.

**Use a physical calendar or notebook.** A paper calendar with a mark on the planned replacement date is safe, as long as the calendar is stored in a location not linked to your digital identity.

**Use a mnemonic pattern.** Associate the replacement with a recurring physical event that is not digitally tracked. For example, replace the SIM on the first full moon after the equinox, or on a specific day of the month that you can remember without writing down.

**The burn-after-reading rule.** Once the SIM is replaced and the old SIM is destroyed, any paper record of the replacement date should also be destroyed. Do not maintain a historical log of SIM identities. What you do not know, you cannot be compelled to reveal.

## The Cost of Burner SIM Rotation

A burner SIM rotation strategy has real financial costs:

- SIM purchase: $5-20 per SIM, depending on jurisdiction and carrier.
- Service refill: $10-30 per month for basic talk and text.
- Replacement frequency: 4-12 SIMs per year.

The annual cost of SIM rotation alone is approximately $200-500, depending on your jurisdiction and replacement frequency. This does not include the cost of the phone hardware, VPN service, or faraday bags.[^8]

For a high-risk user, this cost is justified. For a casual user, it may be a significant factor in deciding whether the two-phone strategy is right for you. If the cost or operational burden prevents you from maintaining the rotation schedule, a simpler single-phone strategy may be more sustainable.

## The Bottom Line

Burner SIM rotation is the discipline that protects you from retrospective surveillance. Every day you use the same SIM, you add to a growing body of evidence that an adversary could use to reconstruct your movements and relationships. Rotation limits this evidence window, ensuring that even if the SIM is compromised, the damage is contained to the most recent 30-90 days.

If you cannot commit to regular SIM rotation with proper destruction of old SIMs, you are exposing yourself to unnecessary risk. The discipline is straightforward but unforgiving. Execute it perfectly or do not do it at all.

[^1]: The IMSI is transmitted to the network on every tower registration event; see 3GPP TS 22.261, "Service Requirements for the 5G System," and GSMA PRD TS.06, "IMEI Allocation and Approval Guidelines."
[^2]: Carrier retention of CSLI and call detail records is described in *Carpenter v. United States*, 585 U.S. 296, 297–98 (2018): "CSLI is generated automatically" and carriers retain it for business purposes.
[^3]: Michael Bazzell, *Extreme Privacy*, 5th ed. (2025), inteltechniques.com, identifies cash SIM purchase as the foundational step in anonymous prepaid acquisition.
[^4]: SIM registration requirements and trends are surveyed in FTC, "Mobile Security Updates: Understanding the Issues" (2018).
[^5]: The evidentiary value of CSLI accumulated over time is central to *Carpenter v. United States*, 585 U.S. 296, 310 (2018): "seven days of CSLI data is enough to show 'a detailed chronicle of a person's physical presence.'"
[^6]: Cellebrite UFED and similar forensic tools extract data from deactivated SIM cards including IMSI, ICCID, contacts, and SMS; see Cellebrite UFED capabilities documentation (Cellebrite Ltd.).
[^7]: CTIA, "Best Practices for IoT Security," and carrier account security guidance recognize prepaid accounts as having reduced identity-verification requirements compared to postpaid service.
[^8]: Michael Bazzell, *Extreme Privacy*, 5th ed. (2025), inteltechniques.com, provides cost estimates for maintaining a two-device strategy including SIM rotation.
