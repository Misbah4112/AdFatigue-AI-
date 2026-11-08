import numpy as np
import pandas as pd

# Reproducible random numbers
rng = np.random.default_rng(42)

num_ads = 10
num_days = 60

dates = pd.date_range(
    start="2026-08-01",
    periods=num_days,
    freq="D"
)

records = []
ground_truth = []

for ad_num in range(1, num_ads + 1):

    ad_id = f"AD_{ad_num:03d}"

    # Different simulated behavior for each ad
    if ad_num <= 4:
        behavior = "stable"
        fatigue_start = None

    elif ad_num <= 7:
        behavior = "gradual_fatigue"
        fatigue_start = 30

    else:
        behavior = "sudden_fatigue"
        fatigue_start = 35

    base_ctr = rng.uniform(0.015, 0.035)
    base_cpm = rng.uniform(8, 25)

    for day, date in enumerate(dates):

        impressions = int(rng.integers(3000, 10000))

        # Simulate increasing ad exposure
        frequency = 1.1 + (day * 0.035)

        frequency += rng.normal(0, 0.08)
        frequency = max(1.0, frequency)

        ctr = base_ctr

        if behavior == "gradual_fatigue" and day >= 30:

            days_after = day - 30

            ctr *= max(
                0.35,
                1 - days_after * 0.022
            )

        elif behavior == "sudden_fatigue" and day >= 35:

            ctr *= 0.50

        # Add normal daily variation
        ctr *= rng.normal(1, 0.08)

        ctr = np.clip(ctr, 0.001, 0.15)

        clicks = rng.binomial(impressions, ctr)

        # Simulate changing advertising costs
        cpm = base_cpm * rng.normal(1, 0.08)

        if behavior != "stable" and fatigue_start is not None:
            if day >= fatigue_start:
                cpm *= 1.15

        spend = (impressions / 1000) * cpm

        # Assume a conversion probability per click
        conversion_rate = 0.06

        conversions = rng.binomial(
            clicks,
            conversion_rate
        )

        records.append({
            "date": date,
            "ad_id": ad_id,
            "impressions": impressions,
            "clicks": clicks,
            "spend": round(spend, 2),
            "conversions": conversions,
            "frequency": round(frequency, 2),
            "behavior": behavior
        })

    ground_truth.append({
        "ad_id": ad_id,
        "behavior": behavior,
        "fatigue_start_day": fatigue_start
    })

df = pd.DataFrame(records)

truth_df = pd.DataFrame(ground_truth)

df.to_csv(
    "data/ad_performance.csv",
    index=False
)

truth_df.to_csv(
    "data/ground_truth.csv",
    index=False
)

print("Dataset generated successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nFirst five rows:")
print(df.head())

print("\nSimulated behavior:")
print(truth_df)