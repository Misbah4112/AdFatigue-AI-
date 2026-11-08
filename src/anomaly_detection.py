import numpy as np
import pandas as pd

from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


FEATURES = [
    "ctr",
    "cpc",
    "frequency"
]


def detect_anomalies(df, contamination=0.1):
    """
    Detect unusual advertising observations using Isolation Forest.

    Returns a DataFrame with anomaly predictions and scores.
    """

    df = df.copy()

    # Select numerical features
    X = df[FEATURES].copy()

    # Replace infinite values with missing values
    X = X.replace([np.inf, -np.inf], np.nan)

    # Fill missing values using median
    imputer = SimpleImputer(strategy="median")
    X_imputed = imputer.fit_transform(X)

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_imputed)

    # Initialize Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=contamination,
        random_state=42
    )

    # Train model
    model.fit(X_scaled)

    # Generate predictions
    df["anomaly"] = model.predict(X_scaled)

    # Higher scores indicate more unusual observations
    df["anomaly_score"] = -model.score_samples(X_scaled)

    return df