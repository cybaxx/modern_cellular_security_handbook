# Chapter 38: The Unbreakable OpSec Rules

## The Ten Commandments of Two-Phone Security

The two-phone strategy is unforgiving. It does not allow for partial compliance, occasional exceptions, or just-this-once compromises. The forensic analysis identified ten rules that form the backbone of the strategy. Break any one of them, and the entire edifice collapses.

This chapter presents each rule with its forensic rationale and the precise consequence of failure. Read these rules carefully. If any of them feel inconvenient, impractical, or excessive, you are not ready for a two-phone strategy. There is no shame in that. It is better to know your limits before you commit than to discover them through failure.

## Rule 1: Never Carry Both Phones at the Same Time

The fundamental premise of the two-phone strategy is compartmentalization. Phone A is your public identity. Phone B is your private self. These two identities must never be physically co-located.

**Forensic rationale.** Cellular towers continuously log the presence of every device in their coverage area. These logs, called Call Detail Records or tower dumps, contain the IMSI, IMEI, timestamp, and sector of each device. If Phone A and Phone B are ever present in the same tower sector at the same time, an investigator with access to tower records can correlate them.

The correlation is permanent. Once two devices are linked in a tower dump, every location where either device has ever been can be cross-referenced. An investigator can reconstruct years of movement patterns for both devices and confirm that they belong to the same person.

**Consequence of breaking.** Both phones linked to the same person forever. The compartmentalization is permanently destroyed. Even if you immediately separate the phones, the historical correlation remains. The only recovery is to destroy both devices and start over with new phones and new SIMs.

## Rule 2: Phone B Never Connects to Home Wi-Fi

Phone B exists exclusively on public Wi-Fi networks. It never connects to any network that can be linked to your identity.

**Forensic rationale.** When a device connects to a Wi-Fi network, the router logs the connection. If that router is your home router, the log includes your device's MAC address, the connection timestamp, and the IP address assigned by your ISP. Your ISP knows which IP address was assigned to your home at that time, and your ISP knows your name and billing address.

A subpoena to your ISP yields the association: on this date, at this time, IP address X was assigned to customer Y. A subpoena to your router manufacturer or cloud service (if your router syncs logs) confirms Device Z connected at that time. Phone B is now linked to your name and address.

This link is permanent. Even if you change routers, change ISPs, or move to a new home, the historical record of that single connection exists in ISP logs, router logs, and any cloud-synced device management platforms.

**Consequence of breaking.** Your name and address are permanently attached to Phone B. The entire compartmentalization strategy is rendered meaningless.

## Rule 3: Phone B Never Powered On at Home

Even without connecting to your home Wi-Fi, simply powering on Phone B at home reveals its presence.

**Forensic rationale.** When a phone powers on, it immediately begins searching for networks. The Wi-Fi chip sends probe requests that include the device's MAC address. If there are any Wi-Fi access points nearby including your router but also your neighbors' routers and any commercial Wi-Fi tracking systems these probe requests are captured.

Each captured probe request includes the device's MAC address and the signal strength. Commercial Wi-Fi tracking systems, such as those used for foot traffic analytics, can triangulate the device's location within the building. If any of these systems upload data to a cloud service, Phone B's MAC address and approximate location are stored indefinitely.

Furthermore, the act of powering on creates a cellular registration event if the cellular radio is active. Even if Phone B is Wi-Fi only, the initial power-on sequence may briefly activate the radio before the OS loads the disabled state.

**Consequence of breaking.** Your home location is linked to Phone B's MAC address through probe request logs and Wi-Fi geolocation databases. The device is burned.

## Rule 4: Phone A Has No Apps, No Accounts

Phone A is a communication tool only. It runs no applications beyond its built-in calling and SMS functions.

**Forensic rationale.** Applications are data leaks waiting to happen. Every app installed on a phone creates metadata: installation timestamps, usage patterns, crash reports, network connections, and account associations. Many apps phone home regularly with device identifiers, IP addresses, and location data.

If Phone A has a browser, any website visited creates a log entry. If it has a messaging app, the app's servers log account activity. If it has any account signed in, that account's provider now knows the device's IP address and can correlate it with other logins from your known devices.

The cumulative effect of app metadata is a rich forensic profile that can link Phone A to your identity through multiple independent channels.

**Consequence of breaking.** App metadata links Phone A to your identity through account associations, device fingerprints, and network logs. The burner is no longer anonymous.

## Rule 5: Phone A SIM Purchased with Cash

The SIM card in Phone A must be acquired without creating any link to your identity.

**Forensic rationale.** When a SIM is purchased through any method other than anonymous cash, a record is created. Credit card purchases generate billing records with your name and address. Online purchases create shipping records. Even some prepaid card purchases can be traced through the card's activation and refill history.

The carrier knows which SIM is in which phone through the IMSI-IMEI pairing. If the SIM can be linked to your identity through purchase records, then the phone can be linked to your identity.

**Consequence of breaking.** A carrier subpoena reveals your name, address, and payment history. Phone A is no longer a burner. It is a phone registered to you.

## Rule 6: Phone A Replaced Every 30-90 Days

Phone A has a limited useful lifespan. Beyond 90 days, the accumulated records create unacceptable exposure.

**Forensic rationale.** Every day Phone A is active, it adds records to carrier logs. These records include tower locations, call timestamps and durations, SMS metadata, and IMSI-IMEI pairings. Over time, these records build a detailed picture of your routines, frequent locations, and communication patterns.

An 18-month record of Phone A activity would allow an investigator to reconstruct your daily habits, identify your home and work locations, map your social network, and predict your future movements. A 90-day record provides a much smaller window for analysis.

**Consequence of breaking.** 18 months of location history and communication patterns become available for forensic analysis. The value of the burner diminishes with every day of extended use.

## Rule 7: Phone B Uses Signal with Burner Number

All sensitive communication on Phone B happens through Signal, and Signal is registered with a phone number that is not linked to your identity.

**Forensic rationale.** Signal provides end-to-end encryption, but it still maintains some metadata: account creation timestamps, last-seen timestamps, and the phone number used for registration. A legal order to Signal can reveal this metadata.

If the phone number used for Signal registration can be linked to you through carrier records or VoIP provider records, then Signal knows you are the account holder. If Signal knows your identity, and Signal knows that your account communicates with specific other accounts, then your communication network is exposed.

**Consequence of breaking.** Your contact graph and communication patterns within Signal are exposed via court order. The anonymity of Phone B is compromised.

## Rule 8: Phone B Never Takes Photos

The camera on Phone B is permanently disabled. No exceptions.

**Forensic rationale.** Digital photos contain EXIF metadata: device make and model, serial number, timestamp, GPS coordinates (if location services are enabled), and camera sensor fingerprints. The sensor fingerprint is unique to each individual camera sensor and can be used to match photos to the device that took them.

A photo taken on Phone B and shared through Signal, email, or any other channel carries this metadata. If the photo is ever leaked, seized, or uploaded to a service that analyzes EXIF data, the link between the photo and Phone B is established.

Even if you strip EXIF data before sharing, the photo's content may reveal location, timing, or personal details that can be used for correlation.

**Consequence of breaking.** EXIF metadata exposes location, device identity, and camera fingerprint. If the photo is ever accessed by an adversary, Phone B is identified.

## Rule 9: Faraday Bags for Transport

Both phones are transported in faraday bags whenever they are not in active use.

**Forensic rationale.** When a phone is on and not in a faraday bag, it communicates with its environment. Cellular radios register with towers. Wi-Fi chips send probe requests. Bluetooth transceivers broadcast device identifiers. Each of these emissions can be detected, logged, and used for tracking.

For Phone A, emissions create a continuous location history that carriers capture. For Phone B, emissions risk exposure of the device to networks and tracking systems that could link it to your identity.

The faraday bag creates a gap in this tracking. When the phone is in the bag, it generates no emissions and leaves no trail.

**Consequence of breaking.** MAC addresses and other device identifiers are captured at transit points, potentially linking phones to locations and to each other.

## Rule 10: Destroy Phone A Before Replacing

When Phone A reaches the end of its life cycle, it must be physically destroyed. A factory reset is not enough.

**Forensic rationale.** Factory resets do not permanently erase data. Forensic tools can recover deleted files, residual data, and device identifiers from reset phones. Studies have shown that significant amounts of user data survive factory resets on many devices.

The device's unique identifiers the IMEI, the serial number, the Wi-Fi MAC address, and the Bluetooth MAC address cannot be changed (on most devices). If the device is later seized, these identifiers link it to all previous activity.

Physical destruction of the device ensures that no data can be recovered and that the device identifiers cannot be used to link past activity to a person.

**Consequence of breaking.** The old device is seized and forensic analysis recovers data and device identifiers, revealing your full history of burner activity.

## The Cumulative Cost of Breaking Rules

Each of these rules is individually important. But the real danger is that breaking multiple rules creates compounding effects. Phone A that has apps and a registered SIM and is not replaced on schedule is not just a little compromised. It is a forensic goldmine. Phone B that has been used at home, on home Wi-Fi, with a real Signal number, and has taken photos is no longer a secure device at all. It is a complete record of your private life in the hands of anyone who seizes it.

The ten rules are not a checklist where 8 out of 10 is passing. They are a chain where every link must hold. Break any one, and the strategy fails. The only question is how quickly you discover the failure and how much damage has accumulated when you do.
