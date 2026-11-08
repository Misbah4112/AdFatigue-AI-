import pandas as pd


# --------------------------------------------------
# 1. CALCULATE ACTUAL CTR CHANGE
# --------------------------------------------------

def calculate_ctr_change(ad_data):
    """
    Compare average CTR in the first 15 observations
    with the last 15 observations.

    Positive = CTR improved
    Negative = CTR deteriorated
    """

    ad_data = ad_data.sort_values("date")

    first_ctr = ad_data["ctr"].iloc[:15].mean()
    last_ctr = ad_data["ctr"].iloc[-15:].mean()

    if pd.isna(first_ctr) or first_ctr <= 0 or pd.isna(last_ctr):
        return 0.0

    change = ((last_ctr - first_ctr) / first_ctr) * 100

    return round(float(change), 2)


# --------------------------------------------------
# 2. CALCULATE ACTUAL CPC CHANGE
# --------------------------------------------------

def calculate_cpc_change(ad_data):
    """
    Compare average CPC in the first 15 observations
    with the last 15 observations.

    Negative = CPC decreased (generally good)
    Positive = CPC increased (generally bad)
    """

    ad_data = ad_data.sort_values("date")

    first_cpc = ad_data["cpc"].iloc[:15].mean()
    last_cpc = ad_data["cpc"].iloc[-15:].mean()

    if pd.isna(first_cpc) or first_cpc <= 0 or pd.isna(last_cpc):
        return 0.0

    change = ((last_cpc - first_cpc) / first_cpc) * 100

    return round(float(change), 2)


# --------------------------------------------------
# 3. RETAIN ORIGINAL RISK CALCULATIONS
# --------------------------------------------------

def calculate_ctr_decline(ad_data):
    return max(0, -calculate_ctr_change(ad_data))


def calculate_cpc_increase(ad_data):
    return max(0, calculate_cpc_change(ad_data))


# --------------------------------------------------
# 4. IDENTIFY NEGATIVE ANOMALIES
# --------------------------------------------------

def calculate_negative_anomalies(ad_data):

    ad_data = ad_data.sort_values("date")

    if ad_data.empty:
        return 0

    baseline = ad_data.iloc[:15]

    baseline_ctr = baseline["ctr"].mean()
    baseline_cpc = baseline["cpc"].mean()

    if (
        pd.isna(baseline_ctr)
        or pd.isna(baseline_cpc)
        or baseline_ctr <= 0
        or baseline_cpc <= 0
    ):
        return 0

    negative_anomalies = ad_data[
        (ad_data["anomaly"] == -1)
        &
        (
            (ad_data["ctr"] < baseline_ctr * 0.95)
            |
            (ad_data["cpc"] > baseline_cpc * 1.05)
        )
    ]

    return int(len(negative_anomalies))


# --------------------------------------------------
# 5. CALCULATE FATIGUE SCORE
# --------------------------------------------------

def calculate_fatigue_score(ad_data, change_analysis):

    if ad_data.empty:
        return 0.0

    ctr_decline = calculate_ctr_decline(ad_data)
    cpc_increase = calculate_cpc_increase(ad_data)

    negative_anomalies = calculate_negative_anomalies(ad_data)
    anomaly_rate = negative_anomalies / len(ad_data)

    deteriorating_changes = sum(
        change["classification"] == "Deterioration"
        for change in change_analysis
    )

    ctr_score = min(40, ctr_decline * 0.8)
    cpc_score = min(20, cpc_increase * 0.2)
    change_score = 20 if deteriorating_changes > 0 else 0
    anomaly_score = min(20, anomaly_rate * 100)

    total_score = (
        ctr_score
        + cpc_score
        + change_score
        + anomaly_score
    )

    return round(float(total_score), 2)


# --------------------------------------------------
# 6. RISK LEVEL
# --------------------------------------------------

def get_risk_level(score):

    if score >= 70:
        return "High"

    elif score >= 40:
        return "Medium"

    return "Low"


# --------------------------------------------------
# 7. PERFORMANCE TREND
# --------------------------------------------------

def get_performance_trend(ad_data, change_analysis):

    if not change_analysis:
        return "Stable"

    latest_change = change_analysis[-1]
    classification = latest_change["classification"]

    if classification == "Improvement":
        return "Improving"

    elif classification == "Deterioration":
        return "Deteriorating"

    elif classification == "Mixed Change":
        return "Mixed"

    return "Stable"