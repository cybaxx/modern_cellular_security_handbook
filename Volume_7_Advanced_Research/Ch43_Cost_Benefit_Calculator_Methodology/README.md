# Chapter 43: Cost-Benefit Calculator Methodology

## How We Arrived at the $1,800/Year Estimate

The two-phone strategy with full mitigations carries a significant financial cost. This chapter breaks down every expense, explains our assumptions, and provides a framework for calculating your own costs. We estimate the fully mitigated strategy at approximately $1,800 per year, plus hundreds of hours of operational security time.

This figure is not arbitrary. It is based on specific hardware choices, replacement cycles, service costs, and the opportunity cost of OpSec labor. We present it transparently so you can decide whether the investment matches your threat model.

## Cost Breakdown

### Phone A: Burner Flip Phone — $200/year

| Item | Unit Cost | Replacement Cycle | Annual Cost |
|---|---|---|---|
| Dumb flip phone (Nokia 225 4G or equivalent) | $50 | Every 90 days (4 per year) | $200 |

The flip phone is treated as a consumable. It is destroyed and replaced every 90 days to limit historical exposure. This is not optional. Carrier logs retain tower data for 6–18 months.[^1] A phone used for a full year gives an adversary 12 months of location history. A phone replaced every 90 days limits exposure to 90 days maximum.

We recommend devices in the $40–60 range. The Nokia 225 4G is a solid choice — it has no apps, no GPS, no Wi-Fi, and a removable battery. Avoid smartphones repurposed as dumb phones they retain too many tracking vectors.

### Phone A Prepaid SIM — $120/year

| Item | Unit Cost | Replacement Cycle | Annual Cost |
|---|---|---|---|
| Prepaid SIM with talk/text | $30 | Every 90 days (4 per year) | $120 |

The prepaid SIM must be purchased with cash. No registration. No identity link. The SIM is destroyed with the phone at each replacement cycle.

Costs vary by carrier. T-Mobile prepaid, AT&T prepaid, and various MVNOs offer plans in the $25–40 range for 90 days of service. We use $30 as a representative figure. Some carriers require monthly refills, which changes the cost structure slightly.

### Phone B: Pixel + GrapheneOS — $400 (One-Time)

| Item | Unit Cost | Replacement Cycle | Annualized Cost |
|---|---|---|---|
| Google Pixel (6a, 7a, or equivalent) | $350–500 | Every 12 months | $350–500 |

Phone B is the most expensive single component. We recommend a Google Pixel for GrapheneOS compatibility. The Pixel 6a or 7a offers the best price-to-security ratio. Purchase with cash if possible.

GrapheneOS is free and open source. Installation takes approximately one hour. The bootloader must be unlocked during installation and should be re-locked afterward. This is a one-time setup cost.

We annualize the phone cost because the device should be replaced every 6–12 months. After 12 months, the MAC address, baseband firmware version, and physical condition create a pattern that can be used for device fingerprinting.

### Faraday Bags — $60 (One-Time)

| Item | Unit Cost | Quantity | Total |
|---|---|---|---|
| Verified faraday bag (dual-layer) | $30 | 2 | $60 |

You need two faraday bags — one for each phone. They should never share a bag. Each bag should be tested with a phone that is actively transmitting (make a call while inside the bag if the call drops, the bag works).

Cheap faraday bags from generic manufacturers may have inconsistent shielding. We recommend brands that have been independently tested. The cost difference between a $10 bag and a $30 bag is negligible compared to the cost of a failed mitigation.

Bags should be replaced every 6–12 months as the shielding fabric degrades with folding and use.

### VPN Service — $60/year

| Item | Unit Cost | Cycle | Annual Cost |
|---|---|---|---|
| VPN (Mullvad, IVPN, or equivalent) | $5/month | Monthly | $60 |

We recommend Mullvad or IVPN. Both accept cash payments and have published, audited no-log policies.[^2] Mullvad charges a flat €5/month (approximately $5.50). IVPN is slightly more expensive at approximately $100/year for the standard plan.

Free VPNs are not acceptable. They monetize user data or sell to larger companies. The VPN is a critical trust anchor — do not compromise on this line item.

### Burner SIM for Signal — $60/year

| Item | Unit Cost | Replacement Cycle | Annual Cost |
|---|---|---|---|
| Prepaid SIM or VoIP number for Signal | $30 | Every 6 months (2 per year) | $60 |

Signal requires a phone number for registration. Using your real number defeats the purpose. A burner SIM used once for registration and then discarded is the gold standard. The SIM does not need ongoing service after registration Signal works over Wi-Fi.[^3]

VoIP numbers (Google Voice, Skype) are cheaper but may be rejected by Signal or linked to your identity via the account used to create them.

### Public Wi-Fi Costs — $500/year

| Item | Unit Cost | Frequency | Annual Cost |
|---|---|---|---|
| Coffee shop purchases | $5–10 | ~60–100 visits per year | $300–500 |

Phone B must be used on public Wi-Fi only. Most public Wi-Fi networks are in businesses that expect you to be a customer. Buying a coffee or tea at $5–10 per visit is the cost of access.

This is the most variable line item. If you live in a city with free public library Wi-Fi, you can reduce this cost significantly. If you live in a suburban or rural area with limited public Wi-Fi, this cost may be higher.

### Tails USB and Software — $0

| Item | Cost | Notes |
|---|---|---|
| Tails OS (USB live boot) | $0 | Free, open source |
| GrapheneOS | $0 | Free, open source |
| Signal | $0 | Free, open source |
| Orbot (Tor for Android) | $0 | Free, open source |
| Bitwarden | $0 | Free tier available |

All critical software is open source and free. The only cost is a USB drive (approximately $10–15, one-time) for Tails OS.

### OpSec Time Cost — Hundreds of Hours per Year

This is the largest cost and the one most frequently ignored. The two-phone strategy requires significant ongoing time investment:

| Activity | Frequency | Time per Session | Annual Time |
|---|---|---|---|
| Faraday bag discipline | Daily | 5 minutes | 30 hours |
| Device rotation (Phone A) | Every 90 days | 2 hours | 8 hours |
| Device rotation (Phone B) | Every 6–12 months | 4 hours | 8 hours |
| SIM purchase trips | Every 90 days | 1 hour | 4 hours |
| Public Wi-Fi travel | 2–3 times per week | 2 hours | 250 hours |
| VPN/OS updates | Monthly | 30 minutes | 6 hours |
| Threat model review | Quarterly | 2 hours | 8 hours |
| **Total** | | | **~314 hours** |

At a conservative valuation of $25/hour (the opportunity cost of your time), the OpSec time cost is approximately $7,850/year in addition to the financial costs.

## The $1,800 Breakdown Table

| Category | Annual Cost | Notes |
|---|---|---|
| Phone A (burner flip × 4) | $200 | $50 per device |
| Phone A prepaid SIM × 4 | $120 | $30 per SIM |
| Phone B (Pixel + GrapheneOS) | $400 | Annualized, one device per year |
| Faraday bags (2) | $60 | One-time, replace every 12 months |
| VPN (Mullvad) | $60 | $5/month |
| Burner SIM for Signal × 2 | $60 | $30 per SIM |
| Public Wi-Fi costs | $500 | $5–10 per visit, ~60–100 visits |
| Software licenses | $0 | All open source |
| **Total financial cost** | **$1,800/year** | |
| OpSec time cost | ~300 hours/year | ~$7,850 at $25/hour |

## Is It Worth It?

### Threat Model Alignment

| Your Annual Privacy Budget | Strategy | Cost | Protection Level |
|---|---|---|---|
| $0–100 | Single de-Googled phone + Signal + free VPN (ProtonVPN free tier) | $0 | 65% vs. advertisers |
| $100–500 | Single phone + paid VPN + data broker removal | $200–500 | 70% vs. advertisers, 40% vs. local police |
| $500–1,000 | Single de-Googled phone + paid VPN + advanced OpSec | $500–1,000 | 75% vs. advertisers, 50% vs. local police |
| $1,800+ | Two-phone mitigated strategy | $1,800 + 300 hours | 85% vs. advertisers, 80% vs. local police, 25% vs. federal |

### Diminishing Returns

The two-phone strategy provides approximately 10–15 percentage points of additional privacy protection over a well-configured single phone, at approximately 10 times the financial cost and 50 times the time cost.

This is not a critique of the strategy. For specific threat models (border crossing, journalism, active investigations), the additional protection is essential. But the cost-benefit calculation must be honest:

| Question | Answer |
|---|---|
| Does the two-phone strategy protect better than a single phone? | Yes |
| Is it 10x better? | No |
| Is the extra cost worth it for a normal citizen? | No |
| Is the extra cost worth it for a journalist crossing borders? | Yes |
| Does the strategy pay for itself in avoided risk? | Depends on your risk level |

### How to Calculate Your Own Cost

Use this formula:

```
Hardware costs:
  (Phone A price × replacements per year) +
  (SIM price × replacements per year) +
  (Phone B price ÷ years between replacements) +
  (Faraday bag price ÷ years between replacements)

Service costs:
  (VPN monthly cost × 12) +
  (Burner SIM cost × replacements per year) +
  (Average public Wi-Fi spend × visits per week × 52)

Time costs:
  (Hours per week × $YOUR_HOURLY_RATE × 52)

Total annual cost = Hardware + Service + Time
```

If your total is higher than the value of the privacy you gain, consider the single-phone approach instead.

[^1]: US carriers generally retain call detail records — including IMSI, IMEI, tower ID, and timing advance — for up to 18 months. See CALEA, 47 U.S.C. §§ 1001–1010; Appendix C of this handbook for carrier-specific retention periods.
[^2]: Mullvad's no-logs policy has been confirmed by independent audits (Cure53, 2020 and 2022). IVPN's no-logs policy has similarly been verified by Cure53. Both services accept anonymous cash and cryptocurrency payments.
[^3]: Confirmed by Signal's 2016 response to a federal grand jury subpoena (Eastern District of Virginia), in which Signal produced only two data points — account creation date and last connection date — because that is all the server retains. See signal.org/bigbrother/. The Signal protocol operates over standard internet connectivity (Wi-Fi) after initial registration.
