# Graph 9: Cost-Benefit Analysis (Two-Phone Strategy)

## Purpose

This graph plots the annual cost (in USD) against the privacy benefit (as a percentage improvement over a stock smartphone) for each privacy strategy. It provides the financial and time-cost data necessary for a rational decision about whether the two-phone strategy is worth implementing. The graph reveals that privacy improvements follow a curve of diminishing returns: each additional increment of privacy costs significantly more than the previous one.

## The Graph

```
Annual Cost ($USD) vs. Privacy Benefit (%)

$2000 ┤
      │                                    ● Two-Phone + Mitigations
$1500 ┤                               ●     (Privacy: 85%, Cost: $1800)
      │                          ●
$1000 ┤                     ●
      │                ●
 $800 ┤           ●──────────● Two-Phone original (Privacy: 75%, Cost: $800)
      │      ●
 $600 ┤ ●───●
      │●
 $400 ┤  ●
      │   ●
 $200 ┤    ●──────────────────● Single de-Googled (Privacy: 65%, Cost: $200)
      │
   $0 └────┬────┬────┬────┬────┬────┬────→
         0%   20%  40%  60%  80%  100%
                Privacy Benefit (vs stock)
```

## Cost Breakdown

### Single De-Googled Phone: ~$200/year

| Item | Cost |
|------|------|
| GrapheneOS-compatible Pixel (one-time, amortized over 3 years) | $200 |
| VPN subscription (Mullvad, IVPN, or similar, cash payment) | $60 |
| Signal usage | $0 |
| DNS over HTTPS | $0 |
| Total annualized | ~$200 |

The single de-Googled phone strategy is the most cost-effective privacy option. The primary expense is the device itself (a used Pixel 6 or 7 for approximately $400-600, amortized over 3 years). VPN costs are modest ($5-10/month, less if paid annually). All software — GrapheneOS, Signal, Orbot, Tor Browser — is free and open source.

This strategy delivers 65% privacy benefit (relative to a stock smartphone) for $200/year. The cost-to-benefit ratio is $3.08 per percentage point of privacy improvement.

### Two-Phone Strategy (Original): ~$800/year

| Item | Cost |
|------|------|
| Phone A (burner flip phone, annual) | $100 |
| Phone A prepaid SIM (annual) | $120 |
| Phone B (Pixel + Graphene, one-time amortized over 3 years) | $200 |
| VPN subscription | $60 |
| Faraday bag (one-time) | $30 |
| Additional public Wi-Fi data costs | ~$300 |
| Total | ~$800 |

The original two-phone strategy costs 4x the single-phone approach. The additional expenses come from maintaining two devices (two phone purchases, two SIMs), the convenience tax of relying on public Wi-Fi (coffee shop purchases, mobile hotspot fees), and the OpSec accessories (Faraday bag to prevent remote wiping or tracking when phones are not in use).

The original strategy delivers 75% privacy benefit — only 10 percentage points more than the single-phone strategy — at 4x the cost. The marginal cost per additional privacy point is $60.

### Two-Phone Strategy with Mitigations: ~$1,800/year

| Item | Cost |
|------|------|
| Phone A (burner flip): $50 x 4/year | $200 |
| Phone A prepaid SIM: $30 x 4/year | $120 |
| Phone B (Pixel + Graphene, one-time amortized) | $200 |
| Faraday bags (2): $60 one-time amortized | $20 |
| VPN (no-log, cash paid) | $60 |
| Burner SIM for Signal: $30 x 2/year | $60 |
| Public Wi-Fi costs (coffee): ~$500/year | $500 |
| Tails USB + Qubes licenses | $0 |
| --- | --- |
| TOTAL | ~$1,800/year |

The mitigated version adds significant recurring costs:

- **Quarterly phone replacement**: $50 flip phone replaced every 3 months prevents accumulation of long-term behavioral data on Phone A. This adds $150/year over the original strategy.
- **Quarterly SIM replacement**: Prepaid SIM replaced every 3 months prevents carrier-side accumulation of call records and location data. $120/year.
- **Dual Faraday bags**: Two bags (one for each phone) for physical isolation. Minimal cost.
- **Two burner Signal accounts**: Signal registered to a burner number, replaced twice yearly.
- **Daily public Wi-Fi costs**: This is the largest hidden expense. The mitigated strategy assumes Phone B never uses home or work Wi-Fi. The user must obtain internet access through public Wi-Fi — coffee shops, libraries, public spaces. At $3-5 per visit (the implied cost of buying a coffee to justify occupying table space), daily usage adds $500-800/year.
- **Hundreds of hours of OpSec time**: Not captured in dollar costs but arguably the most significant expense. Maintaining strict OpSec — planning each network connection, managing two devices, switching between identities — costs hours per week that could be spent on work, family, or leisure.

At $1,800/year, the mitigated strategy delivers 85% privacy benefit — only 10 percentage points more than the original two-phone strategy (75%) and only 20 percentage points more than a single de-Googled phone (65%). The marginal cost per additional privacy point from original to mitigated is $100. The marginal cost from single-phone to original is $60. The marginal cost from stock to single-phone is $3.08.

## Value Proposition Assessment

The graph demonstrates a harsh economic reality: **the two-phone strategy suffers from severe diminishing returns.**

| Strategy | Privacy | Cost | Cost per % point | Cumulative cost |
|----------|---------|------|-----------------|-----------------|
| Stock phone | 0% (baseline) | $0 | $0 | $0 |
| Single de-Googled | 65% | $200 | $3.08 | $200 |
| Two-phone original | 75% | $800 | $60.00 | $800 |
| Two-phone mitigated | 85% | $1,800 | $100.00 | $1,800 |

The jump from stock to a single de-Googled phone captures 65 percentage points of privacy improvement at a trivial cost. The jump from single-phone to two-phone costs 4x more for only 10 additional points. The jump to mitigated costs 2.25x more for another 10 points.

## When the Cost Is Justified

The mitigated two-phone strategy costs $1,800/year plus hundreds of hours of OpSec time. This is justified only when:

1. **The threat model specifically requires physical compartmentalization.** If the user faces border searches, police seizures, or hostile workplace device inspections, software-only privacy (encryption, VPN, Signal) does not solve the problem. A second device that can be hidden or handed over while the primary device remains secure is the only solution.

2. **The user's privacy requirement is 80% or higher.** For users who need protection against local police, private investigators, and corporate espionage (but not state actors), the two-phone strategy may be necessary. Below this threshold, a single de-Googled phone provides adequate protection at dramatically lower cost.

3. **The user's time has low opportunity cost.** The hundreds of hours of OpSec maintenance per year must be weighed against the user's other priorities. For a well-compensated professional, the cost of OpSec time may exceed $1,800/year by a factor of 10 or more.

4. **The user accepts the strategy's limitations against state actors.** Even at $1,800/year and maximum OpSec effort, the strategy provides approximately 15% protection against state actors (Graph 5). If the user's adversary is a nation-state, this is not a cost-effective investment.

## Cost Reduction Strategies

For users who need two phones but cannot justify $1,800/year:

- **Reduce phone replacement frequency**: Replace Phone A every 6 months instead of quarterly ($100/year savings).
- **Use fewer public Wi-Fi visits**: Bulk Wi-Fi access at libraries or free public hotspots (saves $300-500/year).
- **Skip the dual Faraday bags**: Store phones in different rooms instead (saves $60 one-time).
- **Use a single burner SIM for Signal**: Replace annually instead of semi-annually ($30/year savings).

These reductions lower the total to approximately $1,000-1,200/year while maintaining approximately 80% privacy — a 5% reduction in effectiveness for a 33% reduction in cost.

## Non-Financial Costs

The graph necessarily omits the non-financial costs:

- **Cognitive load**: Managing two phones, remembering which identity is active, checking which device is in which bag.
- **Social costs**: Explaining to friends and family why you have two phones, why you don't use WhatsApp, why your Signal number changes.
- **Operational risk**: The constant danger of a single slip — an accidental connection, a misdirected call, a forgotten device — destroying months or years of careful OpSec.
- **Opportunity cost**: The time spent on OpSec maintenance is time not spent on career, relationships, or personal development.

These costs cannot be quantified in dollars but may exceed the financial costs for many users.

## The Time Cost Calculation

The most significant cost of the two-phone strategy is not financial but temporal. The OpSec maintenance hours represent a recurring time tax on every day of the user's life:

### Daily OpSec Overhead (Mitigated Strategy)

- **Morning setup**: Remove phones from Faraday bags, power on, connect Phone B to public Wi-Fi (selected manually), connect VPN (verify connection), check for messages on Signal. **10-15 minutes.**
- **Daytime management**: Decide which phone to carry to each meeting, ensure the other phone is in its Faraday bag, avoid checking Phone B in identifiable locations (near home, near work). **5-10 minutes of continuous awareness.**
- **Evening shutdown**: Disconnect Phone B from Wi-Fi, power off both phones, place in Faraday bags, verify bags are sealed. **5-10 minutes.**
- **OpSec audits**: Weekly review of saved Wi-Fi networks, monthly review of connection logs, quarterly device replacement and data wipe. **30-60 minutes per week.**

**Total estimated time cost: 3-5 hours per week (150-250 hours per year).**

At a conservative valuation of $25/hour (the opportunity cost of time that could be spent on work, leisure, or sleep), the time cost adds $3,750-$6,250 per year to the strategy. Total effective cost (financial + time): $5,500-$8,000 per year.

### Comparison with Single De-Googled Phone

- **Daily setup**: 2-3 minutes (verify VPN is connected, check Signal).
- **No device management**: Single phone, single charger, single battery.
- **Weekly maintenance**: Minimal (update apps, review permissions).

Total time cost: 15-30 minutes per week (13-26 hours per year). Time value at $25/hour: $325-$650 per year.

## The Cost of Getting It Wrong

The graph's privacy dimension assumes the strategy is implemented correctly. If the user makes a mistake (the inevitable "just once" connection to home Wi-Fi), the cost structure changes dramatically:

### Cost of a Single Mistake

- **Direct financial loss**: $1,800/year in strategy costs are now wasted. The strategy has failed; the user is deanonymized.
- **Device replacement**: Both phones may need to be replaced if the MAC addresses are compromised. One-time cost: $500-$800.
- **Identity transition**: If the user's operational identity has been deanonymized, they may need to establish a new identity (new addresses, new accounts, new contacts). Cost: hundreds to thousands of dollars depending on the complexity.
- **Legal costs**: If the deanonymization leads to legal consequences (subpoena, investigation, prosecution), legal fees can run $5,000-$50,000+.

### Expected Loss from Mistakes

If the probability of a critical OpSec failure over a one-year period is 30% (a conservative estimate based on user reports and the difficulty of maintaining strict OpSec), the expected loss from mistakes is:

- Strategy cost: $1,800 (certain)
- Mistake cost: $500-$50,000 (30% probability) = $150-$15,000 expected

Total expected annual cost: $1,950-$16,800.

## Break-Even Analysis

The two-phone strategy breaks even with the single de-Googled phone strategy when the privacy benefit justifies the cost differential:

| Strategy | Annual Cost | Privacy | Cost per % point |
|----------|------------|---------|-----------------|
| Single de-Googled | $200 | 65% | $3.08 |
| Two-phone mitigated | $1,800 | 85% | $21.18 |
| Difference | $1,600 | 20 pp | $80.00 per point |

The user pays $1,600 more per year for an additional 20 percentage points of privacy. Whether this is worthwhile depends on the user's valuation of privacy at the margin.

### Privacy Valuation Threshold

For the mitigated two-phone strategy to be "worth it" compared to a single de-Googled phone:

- The user must value the marginal 20% privacy improvement at $1,600/year
- This implies the user values their total privacy at approximately $8,000/year (5x the marginal cost)
- Or, framed differently: the user is paying $80 per percentage point of additional privacy

If the user's threat model justifies this cost — border searches, active investigation, surveillance risk — then the strategy is financially rational. If the user is pursuing two phones for "general privacy" without a specific threat, the $1,600/year cost is likely irrational.

## Non-Financial Benefits

The graph does not capture non-quantifiable benefits:

- **Peace of mind**: For a user under active surveillance, the knowledge that Phone B is compartmentalized provides psychological relief that cannot be priced.
- **Legal protection**: The two-phone strategy may prevent self-incrimination (Fifth Amendment in the US). If Phone A contains nothing sensitive, the user can unlock it without fear. Phone B's encryption protects its contents, and the user may have a stronger legal argument for not disclosing the password (since the device is authenticated to a different identity).
- **Operational flexibility**: Having two devices allows the user to hand over one (Phone A) while retaining the other (Phone B). In a border search, this may be the difference between maintaining communications and losing all access.

These benefits are real but subjective. They cannot be plotted on the cost-benefit graph but may be the deciding factor for users with specific threat models.

## Final Assessment

The two-phone strategy with mitigations is a high-cost, high-effort approach that delivers marginal privacy improvements over simpler strategies. Its value proposition is weak for most users. The primary justification is not cost-effectiveness but necessity: when the threat model requires physical compartmentalization, no software-only strategy can substitute.
