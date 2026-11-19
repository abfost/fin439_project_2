# Portfolio Stability Results

- Data file: `prices.csv`
- Price dates: September 30, 2021 through September 30, 2026
- All-months window: 60 monthly returns
- Minimum expected annual return: 6.50%
- Minimum reserve-eligible weight: 3.00%

| Result | All months | Last 36 months |
|---|---:|---:|
| SGOV weight | 65.00% | 85.00% |
| IEF weight | 0.00% | 0.00% |
| AGG weight | 0.00% | 0.00% |
| VT weight | 35.00% | 15.00% |
| Estimated annual return | 6.58% | 6.81% |
| Estimated volatility | 5.29% | 1.79% |
| Reserve-eligible weight | 65.00% | 85.00% |
| Meets both thresholds shown above | Yes | Yes |

Switching to the last 36 months increased the SGOV allocation by 20 percentage points and decreased the VT allocation by 20 percentage points. The allocation is sensitive to the lookback window.


## Baseline Comparison

All four portfolios use the same 60 monthly returns, 6.50% return target, and 3.00% reserve minimum.

| Portfolio | Estimated annual return | Annual volatility | Reserve weight | Return and reserve checks |
|---|---:|---:|---:|---|
| Equal weight | 3.35% | 6.67% | 50.00% | Fails return target |
| Inverse volatility | 3.37% | 1.34% | 90.67% | Fails return target |
| 40% AGG / 60% VT benchmark | 6.97% | 10.97% | 0.00% | Fails reserve minimum |
| Optimized portfolio | 6.58% | 5.29% | 65.00% | Passes both checks |

## Point-in-Time Signal

The October 5, 2026 ALFRED vintage showed a 10-year U.S. Treasury yield of 5.28% for October 2, up from 5.17% five observations earlier. The 11-basis-point increase triggered a review of IEF duration exposure. The signal did not change the allocation.

## Pilot Decision

Pilot the 65% SGOV / 35% VT allocation only while its estimated annual return net of modeled costs remains at least 6.50% and the allocation meets the applicable mandate rules. At an illustrative annual implementation cost of 10 basis points, the original allocation returned 6.48% net. Reoptimizing produced 60% SGOV / 40% VT at 6.89% net, with estimated volatility rising from 5.29% to 6.03%. Pause the original pilot and review the extra equity risk before approving a change.

[See the full stress tests and locked prediction](validation-and-ai-use.md).
