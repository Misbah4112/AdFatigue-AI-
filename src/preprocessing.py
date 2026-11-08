import pandas as pd
import numpy as np


def preprocess_data(df):

    df = df.copy()

    # Convert date column into datetime format
    df["date"] = pd.to_datetime(df["date"])

    # Sort advertisements chronologically
    df = df.sort_values(["ad_id", "date"])

    # Calculate advertising metrics
    df["ctr"] = (df["clicks"] / df["impressions"].replace(0, np.nan)) * 100

    df["cpc"] = df["spend"] / df["clicks"].replace(0, np.nan)

    df["cpm"] = (df["spend"] / df["impressions"].replace(0, np.nan)) * 1000

    df["cpa"] = df["spend"] / df["conversions"].replace(0, np.nan)

    return df