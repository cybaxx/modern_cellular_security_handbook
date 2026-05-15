# Chapter 35: The Faraday Bag Discipline

## The Foundation of Physical OpSec

The faraday bag is the most underestimated component of the two-phone strategy. Many users treat it as an accessory, an optional convenience for when they happen to remember it. This is a catastrophic misunderstanding. The faraday bag is not optional. It is as essential as the phones themselves.

A faraday bag is a pouch made of conductive material that blocks electromagnetic fields.[^1] When a phone is inside a functioning faraday bag, it cannot communicate with any external device. It cannot reach cell towers, Wi-Fi access points, Bluetooth devices, or GPS satellites. From the perspective of the network, the phone does not exist.

This capability is critical for both phones, but for different reasons. Phone A in the faraday bag prevents tower triangulation and creates gaps in location history.[^2] Phone B in the faraday bag prevents Wi-Fi probe requests that could reveal its identity and location.[^3] Both phones in their faraday bags, properly separated, maintain the compartmentalization that the strategy depends on.

## Which Bags Work and How to Test Them

Not all faraday bags are created equal. The market is flooded with products that claim to block signals but provide minimal actual protection. Some bags lose effectiveness over time. Others work only for certain frequencies. Proper selection and testing are essential.

**What to look for.** A functional faraday bag should:

- Block all cellular frequencies (700 MHz to 2600 MHz) across the 2G, 3G, 4G, and 5G bands.
- Block Wi-Fi frequencies (2.4 GHz and 5 GHz).
- Block GPS frequencies (1.2 GHz and 1.5 GHz).
- Have a secure closure that maintains electrical contact across the entire opening. Velcro closures are common but degrade over time. Zipper closures with conductive gaskets are more reliable.
- Be large enough to hold the phone without forcing the closure, but not so large that the phone rattles around inside.

**Recommended sources.** Mission Darkness and Silent Pocket are two manufacturers with a track record of producing reliable faraday bags. The specific models to look for are those designed for cell phones rather than laptops, as the smaller bags maintain better electrical contact. Avoid no-name products from discount retailers unless you can verify their performance.

**The testing protocol.** You must test every faraday bag before relying on it, and you must retest regularly. The testing procedure is simple:

1. Put the phone inside the faraday bag and seal it completely.
2. Have someone call the phone from another device.
3. If the phone rings, the bag is failing. Adjust the position of the phone and the closure and test again.
4. If the phone does not ring, attempt to call it from a second number to confirm the first test was not a fluke.
5. Leave the phone in the bag for 10 minutes and test again. Some bags work initially but leak over time as the phone settles.

Repeat this test weekly. Bags that pass consistently can be tested monthly, but weekly testing is safer.

**The signal check.** For a more rigorous test, use a phone with a signal strength indicator app. Place the phone in the bag, seal it, and check whether the signal drops to zero. If any signal bars remain, the bag is not blocking effectively.

**Degradation warning.** Faraday bags degrade. The conductive fabric wears at fold points and closures. Velcro loses its conductive coating. Zipper teeth bend. Replace bags every six months or sooner if testing reveals degradation. Do not wait for a visible failure. By the time you notice a failure, the bag may have been leaking for weeks.[^4]

## Transport Protocols for Both Phones

The faraday bag is only useful if it is used correctly during transport. The protocol for moving between locations is specific and must be followed precisely.

**For Phone A (the burner):**

- Phone A lives in its faraday bag whenever it is not in active use. This is the default state.
- When you need to make a call or send an SMS, remove Phone A from the bag, use it, and return it to the bag immediately after.
- When carrying Phone A in public, the bagged phone goes in a different compartment from your other belongings. It should not be visible as a phone-shaped object.

**For Phone B (the private hub):**

- Phone B goes into its faraday bag before you leave the location where it was used.
- The bagged Phone B is placed in a bag or pocket that is not associated with Phone A or with your primary identity.
- Travel to the next location with Phone B in the faraday bag, sealed and silent.
- Only remove Phone B from the faraday bag when you are seated in your next use location and ready to begin your session.

**Never carry both phones in the same bag, even if both are in faraday bags.** Faraday bags are not perfect. A sufficiently determined adversary with sensitive equipment can sometimes detect signals through a partially degraded bag. Two phones in the same physical container create a correlation risk that is unacceptable.

## Failure Consequences of Forgetting the Bag

Forgetting the faraday bag is one of the most common failures in two-phone OpSec, and one of the most damaging.

**What happens when Phone B is carried without the bag.** Phone B's Wi-Fi chip continuously probes for known networks. This probing is automatic and cannot be fully disabled. Each probe request broadcasts the MAC address of the device and, on some devices, the names of previously connected networks (probe request frames).[^5]

As you move through public spaces, these probe requests are captured by Wi-Fi access points, commercial tracking systems, and potentially surveillance equipment. If you pass near your home while carrying Phone B without the faraday bag, your home router's BSSID may be logged in the phone's memory. Later, that BSSID is uploaded to geolocation databases through other devices you use (if you have any Google or Apple device that shares location data). The result is that your home address becomes linked to Phone B.

**What happens when Phone A is carried without the bag.** Phone A communicates with cell towers continuously when out of the bag. This creates a precise record of your movements.[^6] If Phone A is tracked to locations that match your home or work, then later linked to Phone B through a correlation attack, the entire strategy fails.

**Recovery from a forgotten bag.** If you realize you have transported a phone without its faraday bag, the phone is potentially compromised. The severity depends on how long it was out of the bag, where it was carried, and what networks it may have encountered. In most cases, the safest response is to replace the compromised phone. See Chapter 39 for detailed failure assessment procedures.

## The Safe House Rule Context

The faraday bag discipline ties directly into the Safe House Rule, which is covered in detail in Chapter 36. The connection between the two concepts is simple: the faraday bag is what allows you to transport Phone B to its use locations without revealing those locations through passive scanning.

When you travel to a coffee shop to use Phone B, the phone must be in the faraday bag for the entire journey. If you remove it early, even for a moment, the phone's Wi-Fi chip may probe nearby networks, potentially revealing a network that is linked to you or capturing a BSSID that later geolocates to your starting point.[^7]

The faraday bag creates a bubble of silence around the phone. In that bubble, the phone cannot see and cannot be seen. This is the only way to move a phone that must never be linked to your locations.

## Never Power On Phone B Within 1km of Home or Work

This is the specific operational rule that combines faraday bag discipline with the Safe House Rule. Phone B must never be powered on within 1 kilometer of any location linked to your identity.

**Why 1km?** The 1 kilometer radius accounts for the range of cell tower sectors and the resolution of tower-based location tracking. If Phone B is powered on within this radius, there is a non-trivial risk that a tower records its presence and that record correlates to your known home or work location.[^8]

For power-on events, the risk is even higher because device registration is a discrete event that towers log precisely. If Phone B registers with a tower that serves your home, the ISP-verified location of that tower is now linked to Phone B's IMSI/IMEI.

**The protocol.** When traveling to a use location for Phone B:
1. Phone B is in its faraday bag, powered off or in airplane mode, for the entire journey.
2. Do not power on Phone B until you are at least 1km from any identity-linked location.
3. Ideally, do not power on Phone B until you are seated in your use location and ready to begin.

**The return protocol is equally important.** When you finish using Phone B:
1. Put Phone B back in the faraday bag.
2. Power it off or leave it in airplane mode inside the bag.
3. Do not remove it from the bag or power it on again until you are at your next use location, again at least 1km from any identity-linked location.

Every power-on event leaves a record. Minimize power-on events. Batch your Phone B usage into sessions, with one power-on per session and one power-off per session, rather than multiple on-off cycles throughout the day.

## How to Travel To and From Use Locations Safely

The final layer of faraday bag discipline involves the physical act of traveling with the bagged phone.

**Choose indirect routes.** Do not travel directly from your home to your Phone B use location. Take an indirect route that passes through areas not associated with you. This prevents pattern analysis by physical surveillance or CCTV.

**Vary your mode of transport.** Do not always walk, always drive, or always take the same bus line. Variation in transport mode makes it harder to predict or track your Phone B sessions.

**The bag goes in a separate compartment.** The faraday bag containing Phone B should not be in your pocket, wallet, or bag that contains any identifying documents. If you are stopped and searched, the faraday bag should not be in the same place as your ID, credit cards, or work badge.

**Never open the bag in transit.** Do not check your phone, respond to a notification, or make a quick call while en route. The bag stays sealed until you arrive. Any opening en route defeats the purpose.

The faraday bag discipline is tedious. It is inconvenient. It requires constant attention. That is precisely why most people fail at it, and why those who succeed achieve genuine compartmentalization. The faraday bag is not an accessory. It is the physical foundation of the entire two-phone strategy.

[^1]: Faraday cage shielding effectiveness is grounded in electromagnetic theory; see NIST FIPS 140-2, "Security Requirements for Cryptographic Modules," Level 4 physical security requirements, which define standards for electromagnetic shielding of sensitive equipment.
[^2]: Continuous tower registration creates a persistent location record; see *Carpenter v. United States*, 585 U.S. 296 (2018), describing carriers' automatic logging of cell-site location information.
[^3]: Wi-Fi probe requests broadcast device MAC addresses and previously connected network names; see Mathy Vanhoef et al., "Why MAC Address Randomization is Not Enough," *AsiaCCS 2016*.
[^4]: Physical security standards for shielded enclosures are addressed in NIST FIPS 140-2, which requires periodic testing of physical security mechanisms.
[^5]: Probe request frames containing network names (SSIDs) and MAC addresses are documented in Mathy Vanhoef et al., "Why MAC Address Randomization is Not Enough," *AsiaCCS 2016*, and Jeremy Martin et al., "A Study of MAC Address Randomization in Mobile Devices and When it Fails," *PoPETs* 2017.
[^6]: Carrier location logging is described in *Carpenter v. United States*, 585 U.S. 296, 297 (2018): "each time a phone connects to a cell site, it generates a time-stamped record known as cell-site location information (CSLI)."
[^7]: BSSID geolocation databases maintained by Google and Apple can resolve Wi-Fi access point identifiers to physical locations; see Mathy Vanhoef et al., "Why MAC Address Randomization is Not Enough," *AsiaCCS 2016*.
[^8]: Tower sector resolution and CSLI precision are discussed in *Carpenter v. United States*, 585 U.S. 296 (2018), and *In re Application of U.S. for Historical Cell Site Data*, 724 F.3d 600 (5th Cir. 2013).
