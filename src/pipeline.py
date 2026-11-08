import pandas as pd

from src.preprocessing import preprocess_data

from src.change_detection import (
    detect_changes,
    analyze_changes
)

from src.anomaly_detection import detect_anomalies

from src.risk_scoring import (
    calculate_fatigue_score,
    calculate_ctr_change,
    calculate_cpc_change,
    get_risk_level,
    get_performance_trend
)


def run_pipeline(raw_df):

    # STEP 1: PREPROCESS DATA
    df = preprocess_data(raw_df)

    # STEP 2: DETECT ANOMALIES
    df = detect_anomalies(df)

    results = []
    all_change_points = {}
    all_change_analysis = {}

    # STEP 3: ANALYZE EACH ADVERTISEMENT
    for ad_id, ad_data in df.groupby("ad_id"):

        ad_data = ad_data.sort_values("date")

        # Detect changes using PELT
        changes = detect_changes(ad_data)

        # Classify each change
        change_analysis = analyze_changes(
            ad_data,
            changes
        )

        all_change_points[ad_id] = changes
        all_change_analysis[ad_id] = change_analysis

        # Calculate actual percentage changes
        ctr_change = calculate_ctr_change(ad_data)
        cpc_change = calculate_cpc_change(ad_data)

        # Calculate fatigue risk
        fatigue_score = calculate_fatigue_score(
            ad_data,
            change_analysis
        )

        risk_level = get_risk_level(fatigue_score)

        performance_trend = get_performance_trend(
            ad_data,
            change_analysis
        )

        # Count anomalies
        anomaly_count = int(
            (ad_data["anomaly"] == -1).sum()
        )

        # Count improvements
        improvements = sum(
            change["classification"] == "Improvement"
            for change in change_analysis
        )

        # Count deteriorations
        deteriorations = sum(
            change["classification"] == "Deterioration"
            for change in change_analysis
        )

        results.append({
            "ad_id": ad_id,
            "fatigue_score": fatigue_score,
            "risk_level": risk_level,
            "performance_trend": performance_trend,
            "ctr_change": ctr_change,
            "cpc_change": cpc_change,
            "num_anomalies": anomaly_count,
            "num_change_points": len(changes),
            "num_improvements": improvements,
            "num_deteriorations": deteriorations
        })

    results_df = pd.DataFrame(results)

    results_df = results_df.sort_values(
        "fatigue_score",
        ascending=False
    ).reset_index(drop=True)

    return (
        df,
        results_df,
        all_change_points,
        all_change_analysis
    )