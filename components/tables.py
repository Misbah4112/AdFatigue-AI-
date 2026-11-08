import streamlit as st


def render_risk_table(results_df):

    st.markdown("### Advertisement Performance Overview")

    display_df = results_df[
        [
            "ad_id",
            "performance_trend",
            "fatigue_score",
            "risk_level",
            "ctr_change",
            "cpc_change",
            "num_improvements",
            "num_deteriorations",
            "num_anomalies"
        ]
    ].copy()

    display_df.columns = [
        "Advertisement",
        "Performance Trend",
        "Fatigue Risk Score",
        "Risk Level",
        "CTR Change (%)",
        "CPC Change (%)",
        "Improvements",
        "Deteriorations",
        "Anomalies"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Fatigue Risk Score": st.column_config.ProgressColumn(
            "Fatigue Risk Score",
            help="0 = Fewest detected warning signs | 100 = Highest risk",
            min_value=0,
            max_value=100,
            format="%.1f"
            ),
            
            "CTR Change (%)": st.column_config.NumberColumn(
                "CTR Change (%)",
                format="%+.2f"
            ),
            "CPC Change (%)": st.column_config.NumberColumn(
                "CPC Change (%)",
                format="%+.2f"
            )
        }
    )