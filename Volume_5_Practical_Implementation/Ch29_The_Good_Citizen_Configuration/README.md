# Chapter 29: The Good Citizen Configuration

The single biggest privacy mistake people make is focusing on what to add rather than what to remove. You do not need a complicated setup with multiple phones, custom ROMs, and encrypted DNS tunnels. You need to stop doing the things that leak your data in the first place.

Think of it like water damage in a house. You can buy expensive sensors, install automatic shutoff valves, and build a sophisticated monitoring system — or you can just fix the leak. Most people spend their privacy budget on the monitoring system while the leak continues to pour data into the advertising ecosystem every single day.

This chapter covers two things: the habits you must break, and the settings you must change. Follow both, and you will achieve more privacy than 99% of the population with less than an hour of configuration.

---

## What to STOP Doing (Biggest Wins)

These habits leak more data than everything else combined. Fix these first before you spend a single dollar on privacy tools. The return on investment for these changes is higher than anything else you can do.

### Stop Using These Apps (or Use Them Differently)

Some applications are fundamentally incompatible with privacy. They are not "free" — you pay with your data, your location, your contacts, and your behavior. Their engineering teams are optimized to extract as much information from you as possible, and their legal teams have structured their privacy policies to permit essentially unlimited data collection and sharing.

Here is what to replace and why:

| App | Problem | Alternative |
|---|---|---|
| **WhatsApp** | Owned by Meta. Collects metadata: who you talk to, when, how long, and from where. While message content is encrypted, the fact that you communicate with specific people at specific times is not hidden. Meta uses this to build the social graph that powers its advertising network. | Signal |
| **Facebook / Meta apps** | Track everything you do, even when the app is not in use. Facebook builds shadow profiles of non-users using contact data uploaded by users. The Facebook app has been documented accessing the camera, microphone, clipboard, and phone sensors in ways that have nothing to do with its stated functionality. | Delete them. Use the web browser in private mode if you absolutely must access Facebook. |
| **Google Maps** | Sends your precise location to Google constantly, even when you are not actively navigating. Google stores this data indefinitely and correlates it with every other Google service to build a complete behavioral profile. | Apple Maps (better privacy-by-default) or OsmAnd~ (open source, fully offline maps with no tracking) |
| **Chrome / Google Search** | Ties everything you do to your Google account. Every search, every click, every page visit, every video watched is logged and used for ad targeting. Chrome's "Incognito Mode" does not hide browsing from Google — it only prevents local history storage. | Firefox + DuckDuckGo |
| **Gmail (app)** | While Google now claims it does not scan email content for ad targeting (a policy change from 2017), the Gmail app still links your communications to your core identity and provides Google with metadata about who you communicate with. | ProtonMail, or use the Gmail website in a Firefox container tab |
| **TikTok** | Extensive data collection far beyond what most users understand. ByteDance's data collection includes clipboard contents, keystroke timing patterns, device sensor data, and network information. The Chinese government can legally demand access to all data held by Chinese companies under the National Intelligence Law. | Do not install the app. Use the web browser if you must view content. |
| **Instagram** | Meta tracking on steroids. Instagram scrapes location data, contacts, browsing behavior, and camera roll metadata. It also serves as a social graph that reveals your relationships, routines, and personal interests. The app has access to your camera, microphone, storage, and location — all of which it can use at any time. | Delete the app. Use the web browser rarely. Turn off location tagging before posting anything. |

The common thread across all of these apps is that they are not designed to serve you. They are designed to extract value from you. The product is not the app — you are the product. Every feature, every notification, every interface decision is optimized to maximize data collection while minimizing your awareness of it. The only winning move is to remove them from your phone entirely.

### Stop Using "Sign in with Google / Facebook / Apple"

Every time you click "Sign in with Google," you tell Google:

- Which site you visited
- When you visited it
- What you did there (if the site implements further tracking via Google Analytics or other embedded Google services)
- Your browser fingerprint — a unique identifier derived from your browser configuration, screen resolution, installed fonts, and dozens of other attributes
- Your IP address and approximate location

This single convenience feature is one of the most effective cross-site tracking mechanisms ever created. It links your identity across every website that offers OAuth login, creating a comprehensive map of your internet activity. Google knows which news sites you read, which shopping sites you browse, which forums you participate in, and which services you use — all from the "Sign in with Google" button.

The tracking does not stop at the sites you explicitly log into. Many sites embed Google's OAuth JavaScript even when you do not click the button. This allows Google to observe your visit regardless of whether you authenticate. It is a tracking beacon disguised as a convenience feature.

**Fix:** Use "Sign in with email" and a unique password for every account. Use Bitwarden or another password manager to generate and store these passwords. The extra ten seconds it takes to type your email address is a small price to pay for preventing Google, Facebook, and Apple from mapping your entire internet life into a single searchable profile.

OAuth-based login is convenient, but it comes at a privacy cost that most users never see. Each time you use it, you are telling a third party exactly where you are going and what you are doing. Over months and years, this builds a dossier more detailed than anything a government investigator could compile without a warrant — and unlike a government investigator, these companies face no legal restrictions on how they use this data.

### Stop Giving Apps Unnecessary Permissions

Go to your phone settings right now. Check these permission categories:

- **Location:** Which apps have "Always" access? Change them to "While Using" or "Never." No app needs your location in the background except possibly weather or fitness tracking apps that you have explicitly chosen to use. Be especially suspicious of apps that request "Always" location access at first launch — before you have even used the app's core functionality.
- **Contacts:** Does your flashlight app need contacts? Does your game need contacts? Does your calculator need contacts? No. No app needs contacts unless its primary function is messaging or social networking. Even then, consider whether it genuinely needs access to your entire address book or just the specific contacts you choose to share.
- **Camera / Microphone:** Only your camera app, messaging apps (for video calls and photos), and possibly a QR code reader genuinely need these permissions. If a random game, shopping app, or social media app asks for camera access, that is a massive red flag. These apps have been caught activating the camera without user interaction.
- **Photos / Media:** Many apps request full media access simply to allow you to upload a profile picture. iOS now offers "Selected Photos" access — grant this instead of full library access. Android should implement similar granularity in future versions.
- **Bluetooth:** Increasingly used for proximity tracking and beacon interaction. Retail apps, in particular, use Bluetooth to track your location within stores. Deny Bluetooth access to all apps that do not explicitly need it for pairing with a device.

**On iPhone:** Settings → Privacy & Security → Review each category individually

**On Android:** Settings → Privacy → Permission manager

The principle is simple: deny by default, grant only when necessary, and revoke when no longer needed. Treat app permission requests the same way you would treat a stranger asking to look through your windows. The fact that an app asks for a permission does not mean it needs it. The vast majority of permission requests from apps are for data collection purposes, not functional necessity.

### Stop Using SMS for Anything Important

Short Message Service (SMS) is not encrypted. It was designed in the 1980s for a completely different security landscape. Your mobile carrier reads every message — not manually, but through automated systems that scan for spam, fraud, and content violations. These same systems are accessible to carrier employees with sufficient privileges and to law enforcement with a subpoena.

SMS is also vulnerable to SIM-swapping attacks, where an attacker convinces your carrier to transfer your phone number to a SIM card they control. This is alarmingly easy to do — carriers often require only minimal verification (name, address, date of birth — all of which are publicly available from data brokers). Once the attacker has your number, they can receive your SMS-based two-factor authentication codes and take over your email, banking, social media, and any other account that uses SMS for account recovery.

SIM-swapping is one of the most common and damaging account takeover vectors today. Victims have lost cryptocurrency fortunes, had their social media accounts held for ransom, and suffered identity theft that took years to unwind. Every single one of these attacks could have been prevented by using an authenticator app instead of SMS for 2FA.

**Fix:** Use Signal for all messaging. Signal can replace SMS on Android (set it as the default SMS app). On iPhone, Signal handles Signal-to-Signal messages separately from SMS, but the app is free and the experience is seamless for other Signal users. For the people in your life who do not use Signal, consider whether SMS is truly necessary for those conversations, or whether a phone call would serve the same purpose with better security.

For two-factor authentication, switch to an authenticator app. Aegis (Android, open source) and Google Authenticator (both platforms) generate time-based one-time passwords that are not vulnerable to SIM-swapping. If a service only offers SMS for 2FA, consider whether that service is worth using at all. Many banks and financial institutions still rely on SMS — push them to adopt app-based 2FA by choosing competitors that offer it.

---

## The "Good Enough" Phone Configuration

You do not need a custom ROM. You do not need to flash GrapheneOS unless you are a journalist or activist. The following settings take ten minutes and provide substantial privacy improvements on stock operating systems.

### For iPhone Users (Easiest for Most People)

iOS has strong privacy defaults but requires configuration to reach its full potential:

| Setting | Path | Action |
|---|---|---|
| **Lockdown Mode** | Settings → Privacy & Security → Lockdown Mode | Enable. This blocks most tracking vectors and exploitation techniques. It disables JavaScript JIT compilation, blocks most attachment types, prevents incoming FaceTime calls from unknown numbers, and disables link previews. Some websites may not render correctly — you can add exceptions on a per-domain basis. |
| **App Tracking Transparency** | Settings → Privacy & Security → Tracking | Turn OFF "Allow Apps to Request to Track." This prevents apps from asking for permission to track you across other companies' apps and websites. Apps that previously asked for tracking permission will be denied automatically. |
| **Location Services** | Settings → Privacy & Security → Location Services | Review each app individually. Set most to "Never" or "While Using." The default of "Always" is almost never necessary and should be reserved exclusively for navigation apps that need background location. |
| **Significant Locations** | Settings → Privacy & Security → Location Services → System Services → Significant Locations | Turn OFF. This feature tracks the places you visit frequently — home, work, gym, doctor — and stores them on your device. Even if you trust Apple, this data can be subpoenaed. |
| **Product Improvement** | Settings → Privacy & Security → Analytics & Improvements | Turn OFF "Share iPhone Analytics," "Improve Privacy," and "Share iCloud Analytics." These send usage data to Apple. |
| **Apple ID Personalization** | Settings → Privacy & Security → Apple Advertising | Turn OFF "Personalized Ads." This prevents Apple from using your App Store and Apple News activity to target advertisements. |

**Time: 10 minutes**

These settings do not break normal phone functionality. Lockdown Mode is the most aggressive option and may cause some websites to render differently, but for most users, the tradeoff is barely noticeable. If you find a specific site does not work, you can temporarily disable Lockdown Mode for that domain in Safari's per-site settings.

### For Android Users (Stock, Not De-Googled)

Stock Android leaks more data by default than iOS. This is not an accident — Google's business model is advertising and data collection. Android is the vehicle through which Google collects data from billions of users. Here is how to lock it down:

| Setting | Path | Action |
|---|---|---|
| Remove Google account | Settings → Accounts → Google → Remove Account | The single most effective change. If you can use your phone without logging into Google, you eliminate the primary tracking vector. You can still download apps from the Play Store (purchased apps remain available), and most phone functionality works without a Google account. |
| Disable Google Play Services | Settings → Apps → Google Play Services → Disable | Breaks some apps but kills most Google background tracking. Google Play Services is the backbone of Google's data collection on Android. Disabling it is a nuclear option — only recommended if you are willing to lose some app functionality. |
| Opt out of ads | Settings → Google → Ads | Enable "Opt out of Ads Personalization." Then tap "Reset Advertising ID" to generate a new anonymous identifier. Your old advertising ID — which may have been linked to years of browsing and app usage — is discarded. |
| Location | Settings → Location → App permission | Review all apps. Deny location access to everything except maps and rideshare apps. Pay attention to system apps that may have location access enabled by default. |
| Google Location Accuracy | Settings → Location → Advanced → Google Location Accuracy | Turn OFF. This feature uses Wi-Fi and Bluetooth scanning to improve location accuracy, but it requires sending location data to Google servers. The tradeoff is rarely worth the marginal accuracy improvement. |
| Wi-Fi scanning | Settings → Location → Advanced → Wi-Fi scanning | Turn OFF. This prevents Google from scanning nearby Wi-Fi networks for location purposes. It also prevents the phone from sending lists of visible BSSIDs to Google's geolocation servers. |
| Bluetooth scanning | Settings → Location → Advanced → Bluetooth scanning | Turn OFF. Same principle as Wi-Fi scanning, but for Bluetooth beacons. Many retail stores and public spaces deploy Bluetooth beacons for location tracking. |
| Usage and diagnostics | Settings → Google → Usage and diagnostics | Turn OFF. Prevents Google from collecting device usage data, crash logs, and diagnostic information. |

**Better option: Buy a Google Pixel and install GrapheneOS.** It is easier than you think and removes Google entirely. GrapheneOS is a security-hardened version of Android that strips out Google services and adds substantial privacy improvements. The installation process takes about one hour, requires no special tools (just a computer and a USB cable), and the result is a phone that treats Google as what it is: a threat, not a partner. Pixels are the recommended hardware because they have the best bootloader unlocking support and driver compatibility.

---

## The Bottom Line

The configuration changes described in this chapter take less than an hour combined. They cost nothing. They do not require technical expertise. And they eliminate the vast majority of data leakage that affects normal citizens every day.

If you do nothing else after reading this book, do this: delete the Facebook and Instagram apps, install Signal, lock down your permissions, and turn off personalized ads. That single set of changes will do more for your privacy than any VPN, burner phone, or faraday bag ever could. The simplest changes are often the most effective.
