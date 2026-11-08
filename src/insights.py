import pandas as pd


def generate_ad_insights(ad_results):
    """
    Convert existing advertisement analysis results
    into simple, non-technical explanations.

    This function does NOT modify ML predictions,
    anomaly detection, or fatigue scoring.
    """

    ad_id = ad_results["ad_id"]
    trend = ad_results["performance_trend"]
    risk = ad_results["risk_level"]

    ctr_change = float(ad_results["ctr_change"])
    cpc_change = float(ad_results["cpc_change"])

    anomaly_count = int(ad_results["num_anomalies"])

    # ------------------------------------------
    # 1. HEADLINE
    # ------------------------------------------

    if trend == "Deteriorating":
        headline = "Your advertisement needs attention"
        status = "🔴"

    elif trend == "Improving":
        headline = "Your advertisement is improving"
        status = "🟢"

    elif trend == "Mixed":
        headline = "Your advertisement shows mixed results"
        status = "🟡"

    else:
        headline = "Your advertisement is relatively stable"
        status = "🔵"

    # ------------------------------------------
    # 2. EXPLAIN CTR
    # ------------------------------------------

    if ctr_change <= -5:
        ctr_explanation = (
            f"📉 Your click-through rate decreased by "
            f"{abs(ctr_change):.2f}%. "
            "Fewer people are clicking relative to impressions."
        )

    elif ctr_change >= 5:
        ctr_explanation = (
            f"📈 Your click-through rate increased by "
            f"{ctr_change:.2f}%. "
            "More people are clicking relative to impressions."
        )

    else:
        ctr_explanation = (
            "➡️ Your click-through rate has remained "
            "relatively stable."
        )

    # ------------------------------------------
    # 3. EXPLAIN CPC
    # ------------------------------------------

    if cpc_change >= 5:
        cpc_explanation = (
            f"💰 Your cost per click increased by "
            f"{cpc_change:.2f}%. "
            "You're paying more for each click."
        )

    elif cpc_change <= -5:
        cpc_explanation = (
            f"💚 Your cost per click decreased by "
            f"{abs(cpc_change):.2f}%. "
            "You're paying less for each click."
        )

    else:
        cpc_explanation = (
            "➡️ Your cost per click has remained "
            "relatively stable."
        )

    # ------------------------------------------
    # 4. EXPLAIN ANOMALIES
    # ------------------------------------------

    if anomaly_count == 0:
        anomaly_explanation = (
            "No unusual performance observations were detected."
        )

    elif anomaly_count == 1:
        anomaly_explanation = (
            "We detected 1 unusual performance observation. "
            "This does not necessarily indicate a problem."
        )

    else:
        anomaly_explanation = (
            f"We detected {anomaly_count} unusual performance "
            "observations. These may represent positive or "
            "negative changes."
        )

    # ------------------------------------------
    # 5. PERFORMANCE SUMMARY
    # ------------------------------------------

    if trend == "Deteriorating":
        summary = (
            "Your advertisement is showing signs of weaker "
            "performance. Some important advertising metrics "
            "have moved in an unfavorable direction."
        )

    elif trend == "Improving":
        summary = (
            "Your advertisement is showing signs of stronger "
            "performance. Recent changes suggest that its "
            "effectiveness has improved."
        )

    elif trend == "Mixed":
        summary = (
            "Your advertisement has experienced both positive "
            "and negative performance changes. Some metrics "
            "have improved while others have worsened."
        )

    else:
        summary = (
            "Your advertisement has not shown a major "
            "performance shift according to the current "
            "change-detection analysis."
        )

    # ------------------------------------------
    # 6. RECOMMENDED ACTION
    # ------------------------------------------

    if risk == "High":
        recommendation = (
            "Review your advertising creative, audience "
            "targeting, and recent campaign changes. "
            "Consider testing a refreshed creative. "
            "This pattern may indicate advertising fatigue."
        )

    elif risk == "Medium":
        recommendation = (
            "Monitor this advertisement closely. "
            "Review recent performance changes and "
            "consider testing alternative creatives "
            "if the negative trend continues."
        )

    elif trend == "Improving":
     summary = (
        "Your advertisement is showing signs of stronger "
        "performance. Recent changes suggest that its "
        "effectiveness has improved. A low fatigue-risk score "
        "means our current rules found few warning signs, "
        "not that your advertisement has poor performance."
    )

    elif trend == "Mixed":
        recommendation = (
            "Review the metrics individually before making "
            "changes. Identify which performance indicators "
            "are improving and which need attention."
        )

    else:
        recommendation = (
            "Continue monitoring performance. "
            "No immediate action is suggested by the "
            "current fatigue-risk assessment."
        )

    return {
        "ad_id": ad_id,
        "status": status,
        "headline": headline,
        "summary": summary,
        "ctr_explanation": ctr_explanation,
        "cpc_explanation": cpc_explanation,
        "anomaly_explanation": anomaly_explanation,
        "recommendation": recommendation,
        "risk_level": risk,
    }