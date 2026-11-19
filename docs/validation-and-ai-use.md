# Validation and AI Use

## Lab 20 Partner Cold Run

- Commands run: python -m pip install -r requirements.txt  and  python -m streamlit run app.py
- First issue: None.
- Elapsed time: About 45 seconds.
- Results location: In the Streamlit app, below Current Selection in the All months vs. last 36 months table after uploading prices.csv

- Fix and rerun: The cold run was successful. No fix was needed.

## Locked Changed-Input Record

- [Original pre-run prediction, November 17, 2026](https://github.com/abfost/fin439_project_2/commit/fbddbf0f3a146faef80bd94ddc05164901c0cc9e)
- [Recorded before-and-after results, November 17, 2026](https://github.com/abfost/fin439_project_2/commit/0fb2946c0fa2ee60c45b1a2d3f436d34873cf0f6)

### Changed-Input Prediction

I’ll raise the minimum expected annual return from 6.50% to 7.00%.
I’ll use the same prices.csv, keep All Months selected, and leave the
minimum reserve-eligible weight at 3.00%.

My current portfolio is 65% SGOV and 35% VT, with an estimated annual
return of 6.58% and volatility of 5.29%. I expect it to fall short of the
new 7.00% target. I predict the app will find a mix with more VT and less
SGOV, which would raise both estimated return and volatility.

I would keep the original mix for the 6.50% target. If the committee
required 7.00%, I would reconsider the mix and review the added volatility
before recommending a change.

### Changed-Input Result

I raised the minimum expected annual return from 6.50% to 7.00%
using the same prices.csv, All Months, and a 3.00% reserve minimum.

| Measure | Before: 6.50% target | After: 7.00% target |
|---|---:|---:|
| SGOV weight | 65.00% | 55.00% |
| VT weight | 35.00% | 45.00% |
| Estimated annual return | 6.58% | 7.40% |
| Estimated annual volatility | 5.29% | 6.77% |
| Reserve-eligible weight | 65.00% | 55.00% |

The result matched my prediction. The original portfolio fell short of
the 7.00% target. The new mix met that target and the 3.00% reserve
minimum, with estimated volatility rising by 1.48 percentage points.
I would keep the original mix for the 6.50% target. If the committee
required 7.00%, I would review the added volatility before recommending
the 55% SGOV / 45% VT mix.

## Lab 20 Committee Decision

I recommend piloting the 65% SGOV / 35% VT mix under the 6.50% return target.
I would pause the pilot and reassess the allocation if the committee raised
the target to 7.00%, because the current mix's estimated return is 6.58%.
