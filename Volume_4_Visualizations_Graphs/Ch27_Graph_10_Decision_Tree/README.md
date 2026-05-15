# Graph 10: Decision Tree — Should You Use Two Phones?

## Purpose

This decision tree guides the user through a structured series of questions to determine whether the two-phone strategy is appropriate for their specific threat model. It is the capstone graph of the volume because it synthesizes the findings of all previous graphs into an actionable personal recommendation. Unlike the preceding graphs, which present forensic and analytical data, this graph provides a direct answer to the question most users ask: "Should I actually do this?"

## The Graph


> *See the figure generated below.*


## Decision Point 1: Targeted Surveillance?

The first and most important question: **Do you face targeted surveillance from police, employer, or stalker?**

This is the threshold question because the two-phone strategy is a response to a specific, targeted threat — not a general privacy enhancement. If the answer is "No," the decision tree terminates immediately with a single-phone recommendation.

Targeted surveillance means:

- **Law enforcement**: You are under active investigation, you have been questioned, your associates have been contacted, or you have reason to believe your communications are being monitored.
- **Employer monitoring**: Your employer has a history of monitoring employee communications, you are in a sensitive role, or you have a non-disclosure or non-compete that creates an adversarial relationship.
- **Stalking or domestic abuse**: A specific individual is monitoring your location, communications, or activities with the intent to harm, control, or intimidate.

General privacy concerns ("I don't like being tracked by Google") do not constitute targeted surveillance and do not justify two phones.

### Expected Privacy If "No"

If you do not face targeted surveillance, a single phone with privacy enhancements provides adequate protection:

- **Expected privacy**: 60-70% against non-state threats
- **Adversaries defeated**: Advertisers, data brokers, casual hackers
- **Adversaries not defeated**: Law enforcement (if you become a target later), determined stalkers, corporate espionage

## Decision Point 2: Border or Law Enforcement Seizure?

If you face targeted surveillance, the next question is: **Will you ever need to hand over your primary phone at a border or to law enforcement?**

This is the only scenario where two phones are truly required rather than merely beneficial. A border agent or police officer can compel you to unlock your phone (in many jurisdictions), and no amount of encryption or software hardening prevents this in practice. Physical seizure defeats all software-based privacy protections.

If "Yes," the strategy is **TWO PHONES REQUIRED**. You need a phone to hand over (Phone A) that contains nothing sensitive, and a phone to keep hidden (Phone B) that contains your actual communications.

### Border Considerations

- **US border (CBP)**: Customs and Border Protection can detain your electronic devices for "reasonable" periods and search them without a warrant under the border search exception. You may be asked to unlock your phone. Refusal can result in device seizure, detention, or denial of entry.
- **UK border**: Schedule 7 of the Terrorism Act 2000 allows border officials to search electronic devices and require passwords. Refusal is a criminal offense.
- **China border**: Phones are routinely inspected. VPNs are blocked. Social media accounts may be audited.
- **EU border**: Less aggressive than the US, UK, or China, but device searches do occur, particularly at external EU borders.

In all cases, a "clean" phone (Phone A) that contains no sensitive contacts, no encrypted communication apps, and no travel-related information is the only safe approach.

If "No" — you face targeted surveillance but do not face border or seizure risk — proceed to the third question.

## Decision Point 3: Willingness to Accept Extreme OpSec?

The third question: **Will you accept extreme OpSec (no home Wi-Fi, faraday bags, burner SIMs)?**

This is the practical question. The two-phone strategy fails if the user is unwilling to maintain its operational security requirements. The strategy's effectiveness is directly proportional to the user's OpSec discipline. A user who connects Phone B to home Wi-Fi "just once" has destroyed the entire strategy (Graph 6).

### "Yes" — Implement the Mitigated Strategy

If the user accepts the OpSec burden, the recommended approach is the mitigated two-phone strategy:

- Phone A: Burner flip phone, replaced every 3 months, prepaid SIM, no data
- Phone B: GrapheneOS smartphone, never on identity-linked Wi-Fi
- Faraday bags for both devices when not in use
- VPN on Phone B, paid with cash
- Signal on Phone B with burner number
- Regular device replacement (Phone B annually, Phone A quarterly)
- No crossover: Phone A never used for sensitive communications, Phone B never used for identity-linked calls

**Expected privacy**: 70-85% against Level 2 adversaries (local police, private investigators, corporate espionage). Expect failure against state actors (15% effectiveness per Graph 5).

### "No" — Use a Single Phone with Maximum OpSec

If the user faces targeted surveillance but is unwilling to accept the extreme OpSec burden of two phones, the recommended approach is to maximize privacy on a single device:

- GrapheneOS or CalyxOS
- Google services removed or sandboxed
- Signal for all sensitive communications
- VPN always on (no-log provider, paid anonymously)
- No Google account on device
- Tor Browser for sensitive browsing
- Camera and microphone permissions strictly controlled
- Minimal app installation
- Regular privacy audits

This strategy does not provide physical compartmentalization. If the device is seized, everything is compromised. However, for a user who will not maintain two-phone discipline, this is far better than a stock smartphone.

**Expected privacy**: 60-70% against Level 2 adversaries. Adequate for most non-state threats.

## Expected Privacy Levels by Path

| Path | Privacy vs Local Police | Privacy vs Advertisers | Privacy vs Cybercriminals | Privacy vs State Actors |
|------|------------------------|----------------------|-------------------------|----------------------|
| Single stock phone | 10% | 5% | 15% | 5% |
| Single de-Googled + OpSec | 65% | 90% | 75% | 10% |
| Two-phone (original, flawed) | 50% | 90% | 65% | 10% |
| Two-phone (mitigated) | 75% | 95% | 85% | 15% |
| Two-phone (mitigated + state counters) | 80% | 95% | 88% | 30% |

## Final Recommendation Matrix

| If you... | And you... | Then... |
|-----------|-----------|---------|
| Face targeted surveillance | Must cross borders where phone can be seized | Two phones required |
| Face targeted surveillance | Will accept extreme OpSec | Two phones with mitigations |
| Face targeted surveillance | Will not accept extreme OpSec | Single phone with maximum OpSec |
| Do not face targeted surveillance | Want better privacy than stock | Single de-Googled phone |
| Do not face targeted surveillance | Do not want to change behavior | Stock phone is fine |

## The Bottom Line

Graph 10 distills the entire volume into a single actionable recommendation:

1. **If you face border searches or device seizure**: Two phones are required. There is no software-only alternative.

2. **If you face targeted surveillance but no seizure risk**: Two phones are optional. A single de-Googled phone with strong OpSec may suffice. Only pursue two phones if you are willing to maintain extreme OpSec discipline.

3. **If you do not face targeted surveillance**: A single de-Googled phone provides excellent privacy improvement at minimal cost and effort. Two phones are unnecessary overhead.

## Appendix: Decision Matrix Data

Key numbers used in the analysis:

- Two-phone mitigated cost: ~$1,800/year + hundreds of OpSec hours (Graph 9)
- Two-phone mitigated effectiveness vs state actors: 15% (Graph 5)
- Time to cascade from a single mistake: 24 hours (Graph 6)
- US carrier data retention: 18 months (Graph 8)
- 5G cellular accuracy without GPS: 5-30 meters (Graph 2)

## Walkthrough Examples

### Example A: Journalist Covering Local Government Corruption

- Faces targeted surveillance from local police? **Yes** (police have asked about sources)
- Faces border seizure risk? **No** (operates domestically)
- Will accept extreme OpSec? **Yes** (already uses Signal, encrypted laptop)
- **Recommendation**: Two phones with mitigations. Phone A for public identity and calls with sources (under the assumption it may be monitored), Phone B for sensitive communications and document storage.

### Example B: Privacy-Conscious Professional

- Faces targeted surveillance? **No** (no specific threat)
- **Recommendation**: Single de-Googled phone. Install GrapheneOS, use Signal and VPN, remove Google services. Excellent privacy at low cost.

### Example C: Activist in a Hostile Jurisdiction

- Faces targeted surveillance? **Yes** (government monitoring activists)
- Faces border seizure risk? **Yes** (may need to travel internationally)
- Will accept extreme OpSec? **Yes**
- **Recommendation**: Two phones with mitigations, plus additional countermeasures: multiple identities, dead drop procedures, and acceptance that the strategy will fail against the state if the investigation becomes a priority.

### Example D: College Student

- Faces targeted surveillance? **No**
- **Recommendation**: Single de-Googled phone. Install Signal, use a VPN, and stop using Google Chrome. This provides 60-70% of the two-phone benefit at 10% of the cost.
