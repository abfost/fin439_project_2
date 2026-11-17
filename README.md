# FIN 439 Project 2 — Portfolio Stability Decision

I used ChatGPT to help set up the repository and write the run instructions. The analysis and final decision are mine.

For education only. This is not investment advice.

## Run the app

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
4. Scroll down to **All months vs. last 36 months** to compare the two portfolios.
