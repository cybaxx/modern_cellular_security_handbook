# Chapter 28: The Citizen's Guide — The 80/20 Rule of Privacy

You have just read a forensic-level analysis that would make anyone want to throw their phones into a river. But here is the truth: most of those threats do not apply to you as a normal citizen. This guide cuts through the paranoia and tells you exactly what to focus on — and what to ignore — for maximum practical privacy.

---

## The Hard Truth: Threat Modeling for Citizens

Before implementing anything, ask yourself one question:

> **"Who is actually trying to track me?"**

The answer determines everything. Not all threats are equal, and not all adversaries have the same resources or motivations. Most privacy guides fail because they treat the journalist, the activist, the fugitive, and the suburban parent as identical threat models. They are not. The technical measures you need against an abusive ex-partner are completely different from what you need against a nation-state intelligence agency. Applying the wrong threat model leads to wasted effort, unnecessary inconvenience, and — worst of all — a false sense of security.

Threat modeling is the practice of identifying who your specific adversaries are, what capabilities they have, what motivates them, and what they would gain by targeting you. The answers to these questions drive every security decision you make. Without a threat model, you are flying blind — implementing random security measures based on fear rather than reason.

| If your answer is... | Your real threat is... | You do NOT need to worry about... |
|---|---|---|
| "Advertisers, data brokers, creepy apps" | Companies selling your attention | 5G Multi-RTT, Stingrays, tower dumps |
| "My employer or school" | Network monitoring, device management | State-level baseband exploits |
| "A stalker or abusive ex" | Physical surveillance, account access | CALEA wiretaps |
| "Local police (non-targeted)" | Pulling your phone records during an investigation | Nation-state zero-days |
| "The government is after me specifically" | You need a lawyer, not a privacy guide | Everything — get professional help |

For 95% of citizens, the answer is the first bullet: advertisers and data brokers. The strategies below focus on that threat model. If you are being specifically targeted by a nation-state, a privacy guide will not save you. You need legal protection, operational security training, and potentially physical relocation from a hostile jurisdiction. No amount of app configuration or browser extensions will protect you from a determined state actor with legal authority to compel your cooperation.[^1]

The most dangerous mistake in privacy is defending against the wrong adversary. If you spend your energy worrying about Stingrays while handing all your data to Meta for free, you have lost the game before it began. This is not hypothetical — it is what the vast majority of privacy-conscious people actually do. They buy VPNs and worry about ISP surveillance while simultaneously running Facebook and Instagram on their phones, logged into Google Chrome, with location permissions granted to every app that asks. The cognitive dissonance is staggering.

Privacy professionals have a saying: "Your threat model is not Edward Snowden's threat model." It is a joke because it is painfully true. The default privacy advice on the internet assumes you are a journalist in an authoritarian regime. The overwhelming majority of readers are not. If you work a normal job, live in a normal house, and have normal hobbies, you have an advertiser threat model. Defend accordingly.

---

## The 80/20 Rule of Privacy

You can achieve 80% of the privacy benefit with 20% of the effort. The remaining 20% of benefit requires 80% of the effort — two phones, faraday bags, burner SIMs, Tails OS, and constant vigilance.

This is the Pareto Principle applied to personal privacy. It holds true across every dimension of privacy: the first few changes you make deliver disproportionate results, while the last few require exponentially more work for marginally smaller gains. Understanding this curve is essential to making rational decisions about where to invest your time and money.

The curve is steep at the beginning: simple changes like switching browsers, locking down permissions, and using encrypted messaging eliminate the vast majority of data leakage that affects normal citizens. These changes cost nothing, take an evening to implement, and immediately stop the most aggressive data collection. A person who switches from Chrome to Firefox with uBlock Origin,[^2] replaces WhatsApp with Signal,[^3] and locks down their phone permissions has eliminated 80% or more of their privacy exposure.

The tail, however, is long and painful. Getting from "reasonably private" to "forensically opaque" requires exponentially more work for diminishing returns. The person who wants to go from the 80% level to the 95% level needs to buy a dedicated phone, install a custom ROM, use a VPN, manage multiple identities, scrub EXIF data from every photo, use different browsers for different contexts, maintain separate email addresses for different purposes, and develop operational security habits that govern every digital interaction. The person who wants to go from 95% to 99% needs to use Tor exclusively, never carry a phone, pay with cash only, use burner SIMs that are destroyed regularly, and maintain a level of paranoia that is genuinely exhausting.

Most people should stop at the 80% mark. The remaining 20% is for journalists, activists, whistleblowers, and people with specific, credible threats against them. If you are not in those categories, the extra effort creates inconvenience without meaningful benefit — and in some cases, it actually makes you more conspicuous. A person carrying two phones, using faraday bags, and paying for everything in cash does not look like a normal citizen. They look like someone with something to hide, which paradoxically makes them more interesting to the very surveillance systems they are trying to evade.

### The "Citizen Max" Stack (80% Solution)

| Component | What to do | Why | Cost |
|---|---|---|---|
| **Phone** | One phone. Not two. | Two phones double your OpSec burden and create twice as many failure points. You must never carry them together, never use them on the same network, and never let their locations correlate. One mistake collapses the entire strategy. | $0 |
| **OS** | iPhone with Lockdown Mode, or Android with GrapheneOS (if tech-savvy) | Both options significantly limit tracking APIs and enforce granular app permissions. Lockdown Mode on iOS is particularly aggressive — it blocks most tracking and exploitation vectors with a single toggle. | Free |
| **Messaging** | Signal for everything. Delete SMS, WhatsApp, and Facebook Messenger. | Signal provides end-to-end encryption by default for all communications. It collects almost no metadata — only the phone number you registered with and the last time you connected.[^4] | Free |
| **Browser** | Firefox + uBlock Origin + Privacy Badger (desktop); Brave (mobile) | uBlock Origin blocks ads, trackers, and malicious domains.[^5] Privacy Badger learns to block trackers that uBlock's filter lists might miss. Brave has built-in tracker blocking and fingerprinting protection. | Free |
| **Search** | DuckDuckGo or Startpage | No search history linked to your identity. DuckDuckGo does not personalize results or save your searches. Startpage uses Google results anonymously. | Free |
| **Email** | ProtonMail (free tier) or Tutanota | Both provide zero-access encryption — the provider cannot read your emails. Both are based in jurisdictions with strong privacy laws (Switzerland and Germany, respectively).[^6] | Free |
| **VPN** | Mullvad or ProtonVPN (paid) | Hides your IP address from websites you visit. Mullvad accepts cash and requires no email address to sign up. Both have been independently audited and maintain strict no-log policies.[^7] | $5–10/mo |
| **DNS** | Cloudflare 1.1.1.1 or Quad9 (encrypted DNS) | Prevents your ISP from seeing which domains you query. Encrypted DNS (DNS-over-HTTPS or DNS-over-TLS) closes a common data leakage path. | Free |
| **Permissions** | Deny location to all apps unless absolutely necessary (maps, rideshare) | Location data is the most sensitive permission on your phone. It reveals where you live, work, sleep, socialize, and seek healthcare. Most apps have no legitimate need for it.[^8] | Free |
| **Photos** | Disable camera location tagging; use Scrambled EXIF before sharing | Photos contain embedded metadata (EXIF) that includes GPS coordinates, camera model, and timestamp. Stripping this before sharing prevents location leakage through casual image uploads. | Free |

**Total monthly cost: $5–10 (VPN)**

**Time to set up: 2–3 hours**

**Ongoing effort: Minimal — approximately 10 minutes per week**

This stack covers the overwhelming majority of privacy threats faced by a normal citizen. Every component is free except the VPN, which costs less than a streaming subscription. The setup can be completed in a single evening, and after that, maintenance is nearly zero. You might spend ten minutes a week updating passwords, reviewing permissions, or occasionally checking that your tools are still configured correctly.

The beauty of the 80/20 approach is that it does not require perfection. If you slip up occasionally — you open a link in Google Chrome, or you forget to use Signal for one conversation — the system does not collapse. You are protected by the aggregate of your habits, not the perfection of any single one. This is a critical point that distinguishes practical privacy from theoretical privacy: the best system is the one you will actually maintain. A perfect system that is too burdensome to sustain is worse than a good system that you follow consistently.

---

## When to Actually Worry (Red Flags)

Most people do not need extreme privacy. The "Citizen Max" stack is sufficient for everyday life. But certain situations call for escalation. Here is when you should move beyond the 80/20 solution:

| Red Flag | Action Required |
|---|---|
| You are a journalist covering corruption | Implement a two-phone strategy, use Signal with a burner number, never work from home or on your home network, and use Tails OS for research. Consult a journalism defense organization. |
| You are a domestic violence survivor hiding from an abuser | Get a new phone, a new number, a new email address, and create new accounts for everything. Do not transfer any data from your old phone. Use a PO Box for mail. Contact a domestic violence shelter for guidance. |
| You are applying for asylum or have immigration concerns | Consult a lawyer immediately. Do not post on social media. Do not use apps that share data internationally. Use Signal for all communications. Do not discuss your case on any unencrypted channel. |
| You have received a subpoena or search warrant | Contact a lawyer immediately. Do not talk to police. Do not delete anything — destroying evidence is a separate crime. Follow your lawyer's instructions precisely. |
| You are being investigated for a crime (innocent or not) | Contact a lawyer. Do not speak to law enforcement. Do not consent to phone searches. Do not unlock your phone for anyone. Your Fifth Amendment rights exist for a reason. |
| You are a whistleblower | Contact a lawyer and a journalism defense fund before doing anything. Do not use personal devices for any communication related to the disclosure. Do not discuss your plans on any digital channel. |

If none of these apply, the "Good Citizen" level is sufficient. If one of these applies, do not rely on a privacy guide alone — seek professional legal and operational security advice. The tools described in this book are a foundation, but high-risk situations demand customized support from people who understand the specific legal and technical landscape you are navigating.

The key insight is that privacy escalation should be driven by your actual threat model, not by fear of hypothetical scenarios. Most people who buy faraday bags and burner phones have no realistic need for them. They have been sold a solution in search of a problem by privacy influencers who make money by amplifying fear. Do not let fear dictate your security posture. Let reality do that.

---

## The Privacy Paradox: Blending In

One last thing to internalize before moving on: the more you try to hide, the more suspicious you become. If you use Tor, a VPN, Signal, encrypted email, and no social media — you look exactly like someone with something to hide. This is the privacy paradox: the measures that protect you also mark you as someone who needs protection.

For normal citizens, the goal is to **blend in**. Use Signal (many people do). Use a VPN (common and increasingly mainstream). Do not use two phones unless you actually need to hand one over at a border crossing. Do not use Tor for everyday browsing unless you have a specific reason to anonymize your traffic. The goal is to be indistinguishable from the background noise of millions of other normal users.

The best privacy is being boring. Your data is valuable because it is normal — advertisers want to sell you things, and they need normal data to do that. If you make yourself weird (two phones, faraday bags, no digital footprint), you attract exactly the attention you are trying to avoid. You move from the noise to the signal. You become interesting. And in the world of surveillance, being interesting is the last thing you want.

The most private person is not the one with the most sophisticated tools. It is the one who looks exactly like everyone else.

Stay boring. Stay private. Stay safe.

---

[^1]: EFF, "Surveillance Self-Defense," ssd.eff.org. Provides threat-modeling frameworks and documents the capabilities of state-level adversaries that exceed what consumer privacy tools can mitigate. https://ssd.eff.org

[^2]: Raymond Hill (gorhill), uBlock Origin, github.com/gorhill/uBlock. Open-source content blocker documented to block third-party tracking scripts, ads, and malicious domains with minimal performance overhead. https://github.com/gorhill/uBlock

[^3]: Signal Foundation, "What Does Signal Know About Me?" signal.org/bigbrother. Documents Signal's end-to-end encryption architecture and the minimal metadata it retains. https://signal.org/bigbrother/

[^4]: Signal Foundation, "What Does Signal Know About Me?" signal.org/bigbrother. Confirms the only metadata Signal retains is the registered phone number and last-connected date, making it the lowest-metadata major messaging platform. https://signal.org/bigbrother/

[^5]: Raymond Hill (gorhill), uBlock Origin, github.com/gorhill/uBlock. Documented blocking effectiveness against ad networks, tracking scripts, and fingerprinting endpoints across major filter lists. https://github.com/gorhill/uBlock

[^6]: Proton AG, "Transparency Report," proton.me/legal/transparency. Documents ProtonMail's zero-access encryption architecture and its responses to legal requests under Swiss law, demonstrating provider-side inability to read user email content. https://proton.me/legal/transparency

[^7]: Cure53, "Mullvad VPN Security Audit Report," 2022. Independent penetration test and no-log audit of Mullvad's infrastructure confirming the absence of user-identifiable connection logs. https://cure53.de/audit-report_mullvad_2022.pdf

[^8]: Narseo Vallina-Rodriguez et al., "An Analysis of Pre-installed Android Software," IEEE S&P 2020. Documents that the majority of third-party and pre-installed apps request location permissions beyond their stated functional requirements. https://ieeexplore.ieee.org/document/9152763
