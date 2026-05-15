# Chapter 31: The One-Week Privacy Upgrade Plan

Theory is useless without execution. This chapter provides a day-by-day plan to transform your digital privacy in one week. Each step builds on the last, and by the end of seven days, you will have achieved the "Good Citizen" level of privacy with minimal effort and zero paranoia.

Do these in order. Do not skip ahead. Each day requires the previous day's changes to be in place.

---

## Day 1: Browser & Search (1 hour)

Your browser is the single most attacked piece of software on your computer. Every website you visit attempts to track you through cookies, fingerprinting, and third-party scripts. Day 1 fixes this at the source.

### Steps

1. **Install Firefox (desktop) or Brave (mobile).** Firefox is the most privacy-respecting major browser with the strongest extension ecosystem. Brave is a Chromium-based browser with built-in tracker blocking. Both are free and open source.

2. **Install uBlock Origin extension.** This is the single most effective privacy tool available. It blocks ads, trackers, malicious domains, and cryptominers. It is open source, has near-zero performance impact, and works on Firefox, Chrome, and Edge. Do not use AdBlock Plus or similar alternatives — uBlock Origin is strictly better in every dimension.

3. **Install Privacy Badger (EFF).** Developed by the Electronic Frontier Foundation, Privacy Badger learns to block trackers as you browse. It complements uBlock Origin by catching trackers that uBlock's filter lists may miss. It also replaces social media share buttons with placeholders, preventing them from tracking you before you click.

4. **Set default search to DuckDuckGo.** DuckDuckGo does not track your searches, does not create a search history, and does not personalize results based on your profile. The search quality is comparable to Google for most queries. If you need Google results, use `!g` before your search query in DuckDuckGo to redirect anonymously.

5. **Clear all cookies and browsing history.** This wipes any existing tracking data. From here forward, you start fresh with your new privacy tools in place.

6. **Enable "Delete cookies on close" (optional).** This setting ensures that cookies do not persist between browsing sessions. You will need to log into websites each time you restart the browser, but the privacy benefit is substantial. Most browsers now offer "cookie containers" or "site isolation" features that provide similar benefits with less inconvenience.

### What You Have Achieved

By the end of Day 1, your browsing activity is no longer being fed into the advertising ecosystem. Websites cannot track you across sessions, search engines cannot build a profile of your interests, and third-party scripts are blocked from monitoring your behavior. This single day of work eliminates more tracking than any other change you can make.

---

## Day 2: Messaging & Email (1 hour)

Your messaging apps and email are the most intimate digital services you use. They contain your conversations, your relationships, your personal details, and often your authentication codes. Day 2 moves these communications to platforms that respect your privacy.

### Steps

1. **Install Signal on your phone.** Signal is the gold standard for private messaging. It provides end-to-end encryption for messages, calls, video calls, and file transfers. It is open source, audited, and operated by a nonprofit foundation. It collects almost no metadata — Signal knows only the phone number you registered with and the last time you connected to the server.

2. **Migrate important contacts to Signal.** Send a message to your most frequent contacts asking them to install Signal. Signal does not require an account creation process beyond phone number verification. Most people already have it installed but may not be actively using it.

3. **Set Signal as default SMS app (Android only).** On Android, Signal can replace the default SMS app, allowing you to send both Signal messages (encrypted) and SMS messages (unencrypted but necessary for non-Signal contacts) from a single app. On iPhone, SMS and Signal remain separate.

4. **Create a ProtonMail account (free).** ProtonMail provides end-to-end encryption for emails between ProtonMail users, and it does not scan your email for ad targeting. The free tier includes 500 MB of storage and up to 150 messages per day, which is sufficient for most users.

5. **Start forwarding important email to ProtonMail.** Configure your existing email accounts to forward critical messages to ProtonMail. Update accounts that matter (banking, healthcare, government services) to use your ProtonMail address as the primary contact.

6. **Turn off read receipts in Signal.** Go to Signal settings → Privacy → Read receipts and disable it. This prevents senders from knowing when you have read their messages, a small but meaningful metadata control.

### What You Have Achieved

Your messaging traffic is now encrypted end-to-end, your email is hosted by a privacy-respecting provider, and you have begun the migration away from platforms that monetize your communications. If a contact is also on Signal, your conversations with them are invisible to Signal itself, let alone advertisers or data brokers.

---

## Day 3: Phone Permissions (30 minutes)

Your phone's operating system includes a sophisticated permission system designed to protect your privacy. The problem is that most apps request far more permissions than they need, and most users approve these requests without thinking. Day 3 fixes this.

### Steps

1. **Review all app permissions.** Open your phone's permission manager:
   - iPhone: Settings → Privacy & Security
   - Android: Settings → Privacy → Permission manager

2. **Deny location to all non-maps apps.** No game, social media app, or utility needs your location in the background. Change "Always" to "While Using" or "Never." Pay special attention to apps that request "Always" location access — weather apps, shopping apps, and social media are the most common offenders.

3. **Deny contacts to all non-messaging apps.** No game, photo editor, or calculator needs access to your contacts list. Apps use contact access to upload your address book to their servers, building social graphs that include people who never consented to be tracked.

4. **Deny camera and microphone to all apps except your camera app and Signal.** Any app that can access your camera or microphone can potentially record without your knowledge. Grant these permissions only to apps that genuinely need them for their primary function.

5. **Turn off personalized ads.** On iPhone: Settings → Privacy & Security → Apple Advertising → turn off "Personalized Ads." On Android: Settings → Google → Ads → enable "Opt out of Ads Personalization" and reset your advertising ID.

### What You Have Achieved

Your phone is no longer leaking location, contact, and sensor data to every app you have installed. The advertising ID that allowed ad networks to track you across apps has been reset or disabled. This is the single highest-impact configuration change you can make, and it takes only 30 minutes.

---

## Day 4: Social Media (1 hour)

Social media platforms are the most aggressive data collectors in the technology industry. Their business model depends on knowing everything about you. Day 4 reduces their access to your data dramatically.

### Steps

1. **Delete Facebook and Meta apps from your phone.** The Facebook and Instagram apps are among the most data-hungry applications ever created. They track your location, your browsing, your contacts, your messages, your phone's accelerometer data, and more. Removing them from your phone eliminates the majority of their data collection capability.

2. **Use Facebook only in a browser private tab (if you must).** If you need to access Facebook for events, groups, or messaging, use the mobile website in a private or incognito tab. This prevents the persistent cookies and tracking that the app relies on. On desktop, use Firefox containers to isolate Facebook from your other browsing.

3. **Turn off location tagging in Instagram and Twitter.** Go to privacy settings on each platform and disable location tagging for posts. Review past posts and remove location data from any that have it.

4. **Remove old posts with location or personal information.** Go through your post history and delete or archive anything that reveals your home address, workplace, travel plans, family relationships, or other personally identifiable information. This is tedious, but it is also the only way to remove data that has already been shared.

5. **Set all accounts to private.** Private accounts significantly reduce the surface area for data collection. They prevent third-party tools from scraping your content and limit who can see your posts, photos, and personal information.

### What You Have Achieved

You have cut off the most aggressive data collectors from your phone. The apps that were reporting your location, contacts, and behavior to Meta and other platforms are gone. Your social media presence is now restricted to browser access with limited tracking capability.

---

## Day 5: Data Broker Removal (2 hours + ongoing)

Data brokers have been compiling dossiers on you for years. Day 5 begins the process of removing your information from these databases. This is the most time-consuming step, but it is also one of the most effective.

### Steps

1. **Sign up for a data broker removal service.** DeleteMe ($129/year) and OneRep ($99/year) continuously monitor data broker sites and submit opt-out requests on your behalf. They handle the dozens of data broker sites that exist, including Whitepages, Spokeo, BeenVerified, Intelius, PeopleFinder, MyLife, Radaris, and many others. The cost is worth it — manual opt-out from each site would take dozens of hours.

2. **If you prefer the free route, manually opt out.** Visit each data broker site and submit their individual opt-out process. The process varies by site: some require you to verify your identity, some require you to confirm via email, and some require a mailed request. Keep a spreadsheet tracking which sites you have completed.

3. **Freeze your credit at Equifax, Experian, and TransUnion.** Credit freezes prevent anyone from opening new accounts in your name. They are free under federal law (the Economic Growth, Regulatory Relief, and Consumer Protection Act of 2018). You will receive a PIN from each bureau that you can use to temporarily lift the freeze when you need to apply for credit. This is one of the best free privacy protections available.

### What You Have Achieved

You have begun the process of removing your personal information from the commercial surveillance ecosystem. Data broker removal is not instant — it can take weeks for opt-out requests to be processed — but it is a critical step in reducing your exposure to identity theft, targeted advertising, and unwanted public scrutiny.

---

## Day 6: Wi-Fi & Network (30 minutes)

Your home network is the gateway to all your devices. If it is compromised, no amount of phone-level privacy protection will save you. Day 6 secures your home network.

### Steps

1. **Change your home Wi-Fi password.** Use a strong, unique password — at least 16 characters, including uppercase, lowercase, numbers, and symbols. Do not reuse this password anywhere else. A password manager makes this trivial.

2. **Enable WPA3 if your router supports it.** WPA3 is the current Wi-Fi security standard and provides significant improvements over WPA2, including stronger encryption and protection against offline dictionary attacks. If your router does not support WPA3, ensure WPA2 is enabled and upgrade your router when possible.

3. **Turn off WPS (Wi-Fi Protected Setup).** WPS is a convenience feature that allows devices to connect to your network via a PIN or button press. It is also a well-known security vulnerability — the PIN can be brute-forced in hours, giving an attacker your Wi-Fi password. Every security guide recommends disabling WPS. Do it now.

4. **Update router firmware.** Router manufacturers release firmware updates to patch security vulnerabilities. Most routers allow automatic updates, but many require manual initiation. Check your router admin panel and apply any pending updates.

5. **Consider buying a VPN.** If you use public Wi-Fi frequently (coffee shops, airports, hotels), a VPN encrypts your traffic and prevents snooping on open networks. Mullvad ($5/month) and ProtonVPN (free tier available) are recommended. Install the VPN app on your phone and laptop.

### What You Have Achieved

Your home network is now secured against the most common attack vectors. Your Wi-Fi password is strong, your encryption is up to date, and your router firmware is patched. If you added a VPN, your traffic on public networks is encrypted and protected from interception.

---

## Day 7: Password Manager (1 hour)

Weak or reused passwords are the single most common cause of account compromise. When one site is breached, attackers try the same email and password combination on other sites. Day 7 eliminates this vulnerability.

### Steps

1. **Install Bitwarden.** Bitwarden is free, open source, and audited. It generates and stores strong, unique passwords for every account. It syncs across all your devices and includes a browser extension for autofill. Unlike proprietary alternatives (LastPass, 1Password), Bitwarden's code is publicly reviewed and independently audited.

2. **Generate strong, unique passwords for all accounts.** Start with your most important accounts: email, banking, Signal, social media, and any account that contains personal or financial information. Generate passwords that are at least 16 characters with mixed case, numbers, and symbols. Do not reuse passwords between accounts.

3. **Enable two-factor authentication (2FA).** For your most important accounts, enable 2FA:
   - **Email** (your ProtonMail or primary email): This is the most critical account because password resets for all other accounts go through it.
   - **Signal:** Prevents someone from registering your number on another device.
   - **Banking and financial accounts:** Obvious.
   - **Password manager:** Your Bitwarden master password and 2FA protect all your other passwords.

4. **Use Aegis (Android) or a dedicated authenticator app for 2FA codes.** Aegis is open source and supports encrypted backups. Google Authenticator works too, though it lacks backup functionality. Avoid using SMS for 2FA whenever possible — authenticator apps are more secure and not vulnerable to SIM-swapping attacks.

### What You Have Achieved

Your accounts are now protected by strong, unique passwords and two-factor authentication. If one of your accounts is compromised in a data breach, attackers cannot use those credentials to access your other accounts. Your digital identity is substantially more secure than it was a week ago.

---

## The Final Checklist (Print This)

### Minimum Viable Privacy (MVP) — Do This Today

- [ ] Install Signal. Delete WhatsApp.
- [ ] Turn off location for all apps except maps.
- [ ] Install uBlock Origin on your browser.
- [ ] Switch default search to DuckDuckGo.
- [ ] Turn off personalized ads (Google/Apple settings).

**Time: 30 minutes | Cost: $0**

### Intermediate Privacy — Do This This Week

- [ ] All of MVP
- [ ] Create ProtonMail account
- [ ] Review all app permissions (deny unnecessary)
- [ ] Install Bitwarden password manager
- [ ] Enable 2FA on email and Signal
- [ ] Opt out of data brokers (DeleteMe or manual)
- [ ] Freeze credit reports

**Time: 3 hours | Cost: $0–$129/year (if using DeleteMe)**

### Advanced Privacy — Do This If You Have a Specific Threat

- [ ] All of Intermediate
- [ ] Install GrapheneOS on a Pixel phone
- [ ] Subscribe to a VPN (Mullvad)
- [ ] Remove Google account from phone
- [ ] Turn off Wi-Fi and Bluetooth scanning
- [ ] Use Firefox containers for different identities
- [ ] Scramble EXIF before sharing photos

**Time: 5+ hours | Cost: $5–10/month + potential new phone**

### Extreme Privacy (Two-Phone Strategy) — Only for High-Risk Profiles

- [ ] All of Advanced
- [ ] Purchase burner flip phone with cash
- [ ] Purchase prepaid SIM with cash
- [ ] Buy faraday bags (2)
- [ ] Never carry both phones together
- [ ] Never use Phone B at home or work
- [ ] Destroy and replace phones every 30–90 days
- [ ] Use Tails OS for your computer

**Time: Ongoing, high burden | Cost: ~$1,800/year**

---

## Final Verdict: What a Citizen Should Focus On

Your maximum privacy leverage is not technology — it is behavior.

The single most effective thing you can do is:

1. **Stop using Facebook, Instagram, and TikTok apps** (use the web browser if needed)
2. **Use Signal for all messaging** (encrypted, minimal metadata)
3. **Deny location permissions to almost everything** (maps and rideshare only)
4. **Use a password manager and 2FA** (prevents account takeover, which leaks everything)

Everything else is diminishing returns. The forensic analysis you read about 5G Multi-RTT, Stingrays, and tower dumps? Ignore it. Those threats are for journalists, activists, and fugitives — not for you. You are not that important to the government. You are very important to advertisers. Defend against them first.

---

## The Privacy Paradox

The more you try to hide, the more suspicious you become. If you use Tor, a VPN, Signal, encrypted email, and no social media — you look exactly like someone with something to hide.

For normal citizens: blend in. Use Signal (many people do). Use a VPN (common). Do not use two phones unless you actually need to hand one over at a border.

The best privacy is being boring. Your data is valuable because it is normal — advertisers want to sell you things. If you make yourself weird (two phones, faraday bags, no digital footprint), you attract exactly the attention you are trying to avoid.

Stay boring. Stay private. Stay safe.
