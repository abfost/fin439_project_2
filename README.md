# FIN 439 Project 2 — Meridian Portfolio Dashboard

I used ChatGPT to help develop the Streamlit app, write the documentation, and check portfolio calculations. The analysis and final decision are mine.

For education only. This is not investment advice.

## Run the app on Windows

1. Install Python if it is not already installed.
2. On the GitHub repository page, click **Code → Download ZIP**.
3. In Downloads, right-click the ZIP and choose **Extract All**.
4. Open the extracted folder containing `app.py` and `requirements.txt`. Keep `portfolio.py`, `prices.csv`, and `dgs10_asof_2026-10-05.csv` in that folder.
5. Click the File Explorer address bar, type `cmd`, and press **Enter**.
6. In Command Prompt, run these commands one at a time:

   ```cmd
   python -m pip install -r requirements.txt
   python -m streamlit run app.py
   ```

7. Open the **Local URL** shown in Command Prompt if the browser does not open automatically. Leave Command Prompt running while using the dashboard.

## Reproduce the results

In the left sidebar, upload the bundled `prices.csv`. Set the minimum annual return estimate to **6.50%** and the minimum reserve-eligible weight to **3.00%**. Leave **Use last 36 months** unchecked.

| Tab | What to check |
|---|---|
| Portfolio overview | The optimized allocation is 65% SGOV and 35% VT, with 6.58% estimated annual return and 5.29% volatility. The comparison shows which rules each baseline passes or fails. |
| Window stability | The last 36 months produce 85% SGOV and 15% VT, a 20-percentage-point shift from the full window. |
| Return target test | At a 7.00% target, the optimizer selects 55% SGOV and 45% VT. |
| Point-in-time signal | The October 5, 2026 ALFRED vintage shows a latest available Treasury yield of 5.28% and a rise of 11 basis points over five observations. |
| Cost stress | With an illustrative annual cost of 10 basis points, the original mix earns 6.48% net and falls below the target. Reoptimizing produces 60% SGOV and 40% VT at 6.89% net. |

## Committee decision

Consider a conditional pilot at **65% SGOV / 35% VT**. Pause and reassess if the allocation's estimated annual return after modeled costs falls below **6.50%** or if it breaches an applicable mandate rule. Review the higher equity exposure and volatility before approving a replacement allocation.

- [Visible results](docs/visible-output.md)
- [Validation, stress tests, and locked prediction](docs/validation-and-ai-use.md)
