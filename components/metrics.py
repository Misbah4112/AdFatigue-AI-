import streamlit as st


def render_metrics(results_df, processed_df):

    total_ads = len(results_df)

    improving_ads = (
        results_df["performance_trend"] == "Improving"
    ).sum()

    deteriorating_ads = (
        results_df["performance_trend"] == "Deteriorating"
    ).sum()

    high_risk_ads = (
        results_df["risk_level"] == "High"
    ).sum()

    avg_score = results_df["fatigue_score"].mean()

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "TOTAL ADS",
            total_ads
        )

    with col2:
        st.metric(
            "IMPROVING",
            int(improving_ads)
        )

    with col3:
        st.metric(
            "DETERIORATING",
            int(deteriorating_ads)
        )

    with col4:
        st.metric(
            "HIGH RISK",
            int(high_risk_ads)
        )

    with col5:
        st.metric(
            "AVG FATIGUE SCORE",
            f"{avg_score:.1f}/100"
        )