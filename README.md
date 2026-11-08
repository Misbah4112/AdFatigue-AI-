# AdFatigue-AI-
Ad performance analysis made easier.

AdFatigue AI is an interactive Streamlit application that helps identify improving ads, declining performance, unusual activity, and potential ad fatigue from uploaded advertising data.
## What it does
- Tracks performance: Compares changes in click-through rate (CTR) and cost per click (CPC).
- Detects changes: Uses PELT to identify shifts in CTR patterns.
- Flags unusual activity: Uses Isolation Forest to detect anomalous observations.
- Highlights risk: Assigns a rule-based fatigue-risk score and performance trend to each ad.
- Explains results: Provides plain-language insights, interactive charts, and downloadable analysis.
## Built with
Python · Streamlit · Pandas · NumPy · Scikit-learn · Ruptures · Plotly
## Run locally
pip install -r requirements.txt
streamlit run app.py
Upload a CSV containing these columns:

date, ad_id, impressions, clicks, spend, conversions, frequency

# The app includes a User Guide and Technology & Algorithms tab for more details.
# Note: This is a portfolio prototype tested with synthetic advertising data. Its fatigue-risk score is rule-based and indicates potential warning signs, not a confirmed diagnosis or prediction of ad fatigue.
