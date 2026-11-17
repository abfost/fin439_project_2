# Validation and AI Use

## Lab 20 Partner Cold Run

- Commands run: python -m pip install -r requirements.txt  and  python -m streamlit run app.py
- First issue: None.
- Elapsed time: About 45 seconds.
- Results location: In the Streamlit app, below Current Selection in the All months vs. last 36 months table after uploading prices.csv

- - Fix and rerun: The cold run was successful. No fix was needed.

## Lab 20 Changed-Input Prediction

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
