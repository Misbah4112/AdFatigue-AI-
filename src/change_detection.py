import numpy as np
import pandas as pd
import ruptures as rpt


def detect_changes(ad_data, penalty=1, min_size=5):
    """
    Detect CTR change points using PELT.
    """

    ad_data = ad_data.sort_values("date")

    ctr_values = ad_data["ctr"].to_numpy(dtype=float)

    if len(ctr_values) < 2 * min_size:
        return []

    if not np.isfinite(ctr_values).all():
        return []

    model = rpt.Pelt(
        model="l2",
        min_size=min_size
    )

    model.fit(ctr_values)

    change_points = model.predict(pen=penalty)

    return change_points[:-1]


def classify_change(ad_data, change_point, window=10):
    """
    Classify a detected change as:
    - Improvement
    - Deterioration
    - Mixed Change
    - No Significant Change

    Compare observations immediately before and after
    the detected change point.
    """

    ad_data = ad_data.sort_values("date").reset_index(drop=True)

    before = ad_data.iloc[
        max(0, change_point - window):change_point
    ]

    after = ad_data.iloc[
        change_point:change_point + window
    ]

    if len(before) < 3 or len(after) < 3:
        return {
            "change_point": change_point,
            "classification": "Insufficient Data",
            "ctr_change_pct": 0,
            "cpc_change_pct": 0
        }

    before_ctr = before["ctr"].mean()
    after_ctr = after["ctr"].mean()

    before_cpc = before["cpc"].mean()
    after_cpc = after["cpc"].mean()

    def percentage_change(old, new):
        if pd.isna(old) or pd.isna(new) or old <= 0:
            return np.nan

        return ((new - old) / old) * 100

    ctr_change = percentage_change(before_ctr, after_ctr)
    cpc_change = percentage_change(before_cpc, after_cpc)

    # Minimum relative change to consider meaningful
    threshold = 5

    ctr_improved = pd.notna(ctr_change) and ctr_change >= threshold
    ctr_worsened = pd.notna(ctr_change) and ctr_change <= -threshold

    cpc_improved = pd.notna(cpc_change) and cpc_change <= -threshold
    cpc_worsened = pd.notna(cpc_change) and cpc_change >= threshold

    positive = ctr_improved or cpc_improved
    negative = ctr_worsened or cpc_worsened

    if positive and not negative:
        classification = "Improvement"

    elif negative and not positive:
        classification = "Deterioration"

    elif positive and negative:
        classification = "Mixed Change"

    else:
        classification = "No Significant Change"

    return {
        "change_point": change_point,
        "classification": classification,
        "ctr_change_pct": (
            round(float(ctr_change), 2)
            if pd.notna(ctr_change) else None
        ),
        "cpc_change_pct": (
            round(float(cpc_change), 2)
            if pd.notna(cpc_change) else None
        )
    }


def analyze_changes(ad_data, change_points):
    """
    Classify every detected change point.
    """

    return [
        classify_change(ad_data, point)
        for point in change_points
    ]