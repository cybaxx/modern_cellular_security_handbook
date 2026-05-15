# Chapter 36: The Safe House Rule

## The Most Important Rule in the Strategy

The Safe House Rule is the single most important operational constraint in the two-phone strategy. It is not a suggestion. It is not a guideline. It is a hard boundary that, if crossed, destroys the entire compartmentalization you have built.

The rule is simple: Phone B never touches any location linked to your identity.

This means Phone B is never at your home, your workplace, your school, your regular coffee shop, your gym, or any other location that can be associated with your name. It never connects to a network that serves those locations. It never passes through those neighborhoods. It never powers on within range of a cell tower that also serves those locations.

The reason this rule exists is the same reason the two-phone strategy exists: correlation. If Phone B can be linked to a location that is linked to you, then Phone B is linked to you. Every location leaves a forensic trace, and those traces compound over time.[^1]

## Why Location Correlation Is Fatal

Location data is one of the most powerful forensic tools available to investigators. Phone B can avoid creating carrier CDRs by using Wi-Fi only, but it still creates location data through other mechanisms:

**Wi-Fi probe requests.** Every phone with Wi-Fi enabled broadcasts probe requests to discover nearby networks. These requests include the device's MAC address. Even with MAC randomization, the randomization is not perfect on all devices, and some implementations have been shown to be deanonymizable.[^2]

**Wi-Fi connection logs.** When Phone B connects to a public Wi-Fi network, that network's logs record the connection. If the network has any form of authentication that links to your identity (a loyalty program, a social login, or a payment method), the connection links Phone B to you.

**BSSID geolocation.** When Phone B's Wi-Fi chip detects an access point, it records the BSSID. Later, that BSSID can be looked up in geolocation databases maintained by Google, Apple, and others.[^3] If the BSSID corresponds to a location that is linked to you, Phone B has just revealed its approximate location at the time of detection.

**Physical surveillance.** If an investigator observes you at a location and then observes Phone B activity at that same location, the correlation is direct. Physical surveillance does not require a warrant or any technical sophistication.

**CCTV.** Public and private camera systems record people at locations. If Phone B's usage pattern can be correlated with CCTV footage that shows you at those locations, the link is established.

Every time Phone B enters a location that can be linked to you, it creates a potential correlation point. The Safe House Rule eliminates all of these by ensuring that Phone B exists only in locations that cannot be linked to you.

## Prohibited Locations: The Complete List

The following locations are permanently off-limits for Phone B:

**Your home.** This includes the building, the property, and the surrounding area up to at least 1 kilometer. Phone B never enters your home. It never charges at home. It never powers on within 1 kilometer of home. If you live in an apartment building, the entire building is off-limits, and ideally the entire block.

**Your workplace.** Same as home. Phone B never enters the building, never connects to the corporate network, and never powers on within 1 kilometer of the office.

**Your school or university.** Campus networks, library Wi-Fi, and student housing are all linked to your identity through enrollment records.

**Your regular coffee shop.** If you are a regular at a specific coffee shop and you use a loyalty card, pay by card, or are recognized by staff, that coffee shop is linked to you. Phone B cannot be used there.

**Your gym.** Gym membership records link you to that location. If Phone B is ever detected at the gym, the correlation is trivial.

**Your car.** If your car has Bluetooth, it broadcasts a unique identifier. If it has a license plate, it is recorded by cameras. Phone B should never be in your car. If it must be transported by car, it must be in a faraday bag and the car must not be registered to you or linked to your home address.

**Your friends' homes.** If you visit friends regularly, their homes may become linked to you through association. Phone B should not be used there.

**Your relatives' homes.** Same concern, with the additional risk that relatives may be under surveillance if you are.

**Any location where you have an account.** If you have a membership, a subscription, a loyalty program, a library card, a gym membership, or any account that ties your name to an address, that location is off-limits for Phone B.

## Acceptable Locations: How to Choose Them

Phone B should be used exclusively in random public locations that cannot be linked to you. The key criteria are:

**No registration required.** The location must not require you to provide identification, sign in, or create an account. Paying with cash is ideal.

**No loyalty programs.** Do not use loyalty cards, frequent buyer programs, or any form of customer tracking at Phone B locations.

**No predictable patterns.** Do not use the same location twice in the same week. Rotate through different neighborhoods, different types of locations, and different times of day.

**Good options include:**

- **Different coffee shop each time.** Choose independent shops in different neighborhoods. Avoid chain coffee shops that may have comprehensive Wi-Fi logging and camera systems.

- **Public library, different branch.** Public libraries typically offer free Wi-Fi with no registration. Rotate through branches in different parts of the city.

- **Park bench with no cameras.** Outdoor locations with public Wi-Fi from nearby businesses can work, but verify that there are no cameras covering the area.

- **Hotel lobby.** Many hotels have free Wi-Fi in their lobbies. Pay cash for a day pass if the hotel requires one. Rotate through different hotels.

- **Coworking space (day pass, cash).** Some coworking spaces offer day passes for cash. Read the terms carefully to ensure no identity tracking.

- **University campus (open areas).** Some university campuses have open Wi-Fi networks in common areas. Use only if you are not a student or employee of that university.

- **Airport terminal (departures/arrivals).** Airport Wi-Fi is generally open and heavily trafficked, providing good cover. Use only if you are not traveling yourself, and be aware of CCTV density.

## Travel Without Phone B in Your Pocket

The Safe House Rule applies not just to Phone B's usage, but to its movement. You cannot carry Phone B through prohibited locations even if it is not in use.

**The protocol for traveling to a use location:**

1. Phone B is in its faraday bag, powered off.
2. The faraday bag is in a bag or compartment that you do not normally carry.
3. You travel to your chosen location using a route that does not pass through prohibited areas.
4. You do not remove Phone B from the faraday bag until you are seated at the use location.
5. You power on Phone B only when ready to begin your session.

**The protocol for traveling from a use location:**

1. Power off Phone B.
2. Place it in the faraday bag and seal it.
3. Keep it in the faraday bag until you reach your next destination.

**What if you need to pass through a prohibited area on the way?** Choose a different location. There is no safe way to transport Phone B through an area where it could be correlated to you. Even in a faraday bag, the risk of the bag failing, being opened accidentally, or being detected by sensitive equipment is too high.

## The Faraday Bag Until Arrival

The faraday bag is the enabler of the Safe House Rule. Without it, you cannot safely transport Phone B through public spaces without risking passive detection.[^4]

The bag must be tested regularly (see Chapter 35) and replaced at the first sign of degradation. The bag must be the correct size for your phone, must seal completely, and must block all relevant frequencies.

**Do not use the same faraday bag for Phone A and Phone B.** Each phone should have its own dedicated bag, stored in different locations. This prevents confusion and eliminates the risk of one phone accidentally ending up in the other's bag.

## What Happens If You Break the Safe House Rule

Breaking the Safe House Rule is a catastrophic failure. There is no partial recovery. Once Phone B has been at a location linked to your identity, the correlation potential exists permanently.

**If Phone B was powered on at a prohibited location.** The phone has registered on networks, sent probe requests, and potentially connected to access points.[^5] The location data exists in the phone's memory and in external logs. The phone is burned. It must be destroyed and replaced.

**If Phone B was transported through a prohibited area in a faraday bag.** The risk is lower but not zero. The phone should be considered potentially compromised. A careful assessment is needed: was the bag tested recently? Was it properly sealed? Were there any electronic detection devices at the location? In most cases, the safest approach is to replace the phone.

**If Phone B was used at a location that later becomes linked to you.** If you return to a coffee shop where you previously used Phone B and later become a regular at that shop, the location now has both your identity and Phone B in its logs. Phone B at that location should be considered burned.

The Safe House Rule is unforgiving because location correlation is permanent. A single mistake creates a link that can be exploited at any point in the future, as long as the records exist.[^6] The only safe response is to assume the compromise is permanent and act accordingly.

## The Discipline Required

The Safe House Rule is the most demanding part of the two-phone strategy. It requires constant spatial awareness. You must always know where you are, where Phone B is, and whether the two can be correlated. You must plan your Phone B sessions in advance, choosing locations, routes, and timing to avoid accidental correlations.

This is not a rule that can be followed casually. It requires deliberate effort every time you use Phone B. If you are not prepared to commit to this level of discipline, you are not ready for the two-phone strategy. A single de-Googled phone with Signal and a VPN will serve you better than a two-phone strategy where you cannot maintain the Safe House Rule.

[^1]: Location correlation through historical cell site data is addressed in *Carpenter v. United States*, 585 U.S. 296 (2018), and through tower dumps in *In re Application of U.S. for Historical Cell Site Data*, 724 F.3d 600 (5th Cir. 2013).
[^2]: MAC randomization failures that allow device re-identification are documented in Mathy Vanhoef et al., "Why MAC Address Randomization is Not Enough," *AsiaCCS 2016*, and Jeremy Martin et al., "A Study of MAC Address Randomization in Mobile Devices and When it Fails," *PoPETs* 2017.
[^3]: Google and Apple maintain Wi-Fi positioning databases that resolve BSSID to physical location; see Mathy Vanhoef et al., "Why MAC Address Randomization is Not Enough," *AsiaCCS 2016*, for an analysis of how these databases are populated and queried.
[^4]: The role of RF shielding in blocking passive scanning is grounded in standard electromagnetic shielding principles; see NIST FIPS 140-2 physical security requirements for shielded enclosures.
[^5]: When a device powers on, it transmits its IMSI and IMEI to the nearest tower; see 3GPP TS 22.261 and GSMA PRD TS.06, "IMEI Allocation and Approval Guidelines."
[^6]: ISP retention of connection logs and the durability of CSLI records are addressed in *Carpenter v. United States*, 585 U.S. 296 (2018), and *In re Application of U.S. for Historical Cell Site Data*, 724 F.3d 600 (5th Cir. 2013).
