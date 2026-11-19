# Decision Memo — Meridian Foundation Reserve

I used ChatGPT to help develop the dashboard, check portfolio calculations, and draft the documentation. The analysis and final decision are mine.

For education only. This is not investment advice.

## Recommendation

Approve a 90-day monitoring pilot using 65% SGOV and 35% VT as the reference allocation. Before committing capital, confirm actual implementation costs, verify the ETF price inputs against the provider, and check liquidity and turnover against current holdings.

Use 60%–65% SGOV and 35%–40% VT as the range to review during the pilot. Start the analysis at 65% SGOV and 35% VT. Require committee approval before moving to 60% SGOV and 40% VT because that mix increases equity exposure and estimated volatility.

## Why this allocation

Meridian has a seven-year horizon, annual rebalancing, and an objective of CPI plus 4% annually, net of costs, over rolling five-year periods. The dashboard uses 6.50% as a screening target based on assumed CPI of 2.50%. It also requires a minimum 3.00% reserve to cover four quarterly distributions. The historical annualized estimates screen candidate portfolios and do not establish that Meridian will achieve its rolling five-year objective.

| Portfolio | Estimated annual return | Annual volatility | Reserve weight | Screening result |
|---|---:|---:|---:|---|
| Equal weight | 3.35% | 6.67% | 50.00% | Fails return target |
| Inverse volatility | 3.37% | 1.34% | 90.67% | Fails return target |
| 40% AGG / 60% VT benchmark | 6.97% | 10.97% | 0.00% | Fails reserve minimum |
| 65% SGOV / 35% VT | 6.58% | 5.29% | 65.00% | Passes return and reserve screens before additional costs |

The optimizer uses 60 monthly returns through September 30, 2026. The selected mix clears both numeric screens with lower estimated volatility than the benchmark. Its annual return cushion is only about 8 basis points before additional implementation costs.

## What would change the decision

- **Costs.** At an illustrative annual cost of 10 basis points, the reference mix earns 6.48% net and fails the 6.50% screen. Reoptimizing gives 60% SGOV and 40% VT at 6.89% net, with estimated volatility rising from 5.29% to 6.03%.
- **Estimation risk.** The 36-month window moved 20 percentage points from VT to SGOV. Lowering VT's estimated annual return to 9.90% pushed the optimizer in the opposite direction, to 50% VT, to clear the target. That allocation falls outside the proposed pilot review range.
- **Feasibility.** Raising the reserve minimum to 90% produced no feasible portfolio at the 6.50% return target. If constraints make the portfolio infeasible, stop and bring the trade-off to the committee.

## Monitoring and approval

Review estimated net return, reserve weight, volatility, and the difference between estimation windows monthly during the pilot. Pause the reference allocation if its estimated annual return after costs falls below 6.50% or its reserve weight falls below 3.00%. Bring any replacement allocation to the committee before implementation.

The October 5, 2026 ALFRED vintage showed the 10-year Treasury yield had risen 11 basis points over five available observations. That triggered an IEF duration review without changing portfolio weights. Before any capital allocation, confirm the assumed liquidity treatment and check turnover using current holdings. Ask the CIO to clarify how the calendar-year loss language should be applied.

[Dashboard results](visible-output.md) · [Validation and stress tests](validation-and-ai-use.md)
