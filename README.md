# FIN 439 Project 2 — Portfolio Stability Decision

I used ChatGPT to help set up the repository, write the run instructions, and develop the dashboard code and presentation. The analysis and final decision are mine.

For education only. This is not investment advice.

## Run the app

Python must be installed before running these commands.

1. On the repo page, click **Code → Download ZIP**.
2. Open Downloads, right-click the ZIP file, and choose **Extract All**.
3. Open the extracted folder that contains `app.py` and `requirements.txt`.
4. On Windows, press **Alt + D**, type `cmd`, and press **Enter**.
5. Run these commands one at a time:

   ```text
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
   ```

6. Open the **Local URL** shown in Command Prompt if the app does not open automatically.

## Reproduce the portfolio results

1. In the app sidebar, click **Upload** and select `prices.csv` from the extracted folder.
2. Keep the minimum expected return at **6.50%** and the minimum reserve-eligible weight at **3.00%**.
3. Leave **Use last 36 months** unchecked for the all-months result.
4. Open the **Window stability** tab to compare all months with the last 36 months.
5. Open the **Return target test** tab to compare the 6.50% and 7.00% targets.

## Lab 20 Readiness Summary

| Check | Evidence |
|---|---|
| Partner cold run | Completed in about 45 seconds with no issues reported |
| Changed input | Minimum estimated annual return target increased from 6.50% to 7.00% |
| Allocation response | VT increased from 35% to 45%; SGOV decreased from 65% to 55% |
| Risk response | Estimated volatility increased from 5.29% to 6.77% |
| Committee decision | Pilot the 65% SGOV / 35% VT mix under the 6.50% target |
| Reassessment trigger | Committee raises the return target to 7.00% |

The higher target required 10 percentage points more equity exposure.
Estimated annual return rose by 0.82 percentage points, while estimated
volatility rose by 1.48 percentage points.

[Read the validation record](docs/validation-and-ai-use.md)

[View the baseline results](docs/visible-output.md)
