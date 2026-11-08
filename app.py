from pathlib import Path

import pandas as pd
import streamlit as st

from src.pipeline import run_pipeline
from src.insights import generate_ad_insights

from components.metrics import render_metrics

from components.charts import (
    create_ctr_chart,
    create_cpc_chart,
    create_frequency_chart
)

from components.tables import render_risk_table
from components.sidebar import render_sidebar
from components.insights import render_insights

# NEW COMPONENTS
from components.technology import render_technology
from components.user_guide import render_user_guide


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AdFatigue AI | Performance Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# LOAD CSS
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

css_path = BASE_DIR / "assets" / "styles.css"

if css_path.exists():

    with open(css_path, encoding="utf-8") as css_file:

        st.markdown(
            f"<style>{css_file.read()}</style>",
            unsafe_allow_html=True
        )


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("AdFatigue AI")

st.caption(
    "Advertising Performance Intelligence | "
    "Machine Learning-Powered Analysis"
)


# --------------------------------------------------
# CREATE TABS
# --------------------------------------------------

tab_dashboard, tab_technology, tab_guide = st.tabs(
    [
        "📊 Dashboard",
        "🧠 Technology & Algorithms",
        "📖 User Guide"
    ]
)


# --------------------------------------------------
# TECHNOLOGY TAB
# --------------------------------------------------

with tab_technology:

    render_technology()


# --------------------------------------------------
# USER GUIDE TAB
# --------------------------------------------------

with tab_guide:

    render_user_guide()


# --------------------------------------------------
# DASHBOARD TAB
# --------------------------------------------------

with tab_dashboard:

    # ----------------------------------------------
    # UPLOAD DATA
    # ----------------------------------------------

    st.sidebar.markdown("### Upload Advertising Data")

    uploaded_file = st.sidebar.file_uploader(
        "Upload your advertising performance report",
        type=["csv"],
        help="Upload a CSV containing daily advertising metrics."
    )

    if uploaded_file is None:

        st.markdown(
            "## Advertising Performance Dashboard"
        )

        st.info(
            "Upload your advertising performance CSV "
            "using the sidebar to begin analysis."
        )

    else:

        # ------------------------------------------
        # READ CSV
        # ------------------------------------------

        try:
            raw_df = pd.read_csv(uploaded_file)

        except Exception as error:
            st.error(
                f"Unable to read the uploaded CSV: {error}"
            )
            st.stop()

        # ------------------------------------------
        # VALIDATE COLUMNS
        # ------------------------------------------

        required_columns = {
            "date",
            "ad_id",
            "impressions",
            "clicks",
            "spend",
            "conversions",
            "frequency"
        }

        missing_columns = (
            required_columns - set(raw_df.columns)
        )

        if missing_columns:

            st.error(
                "Your uploaded CSV is missing these columns: "
                + ", ".join(sorted(missing_columns))
            )

            st.stop()

        # ------------------------------------------
        # RUN ML PIPELINE
        # ------------------------------------------

        try:

            (
                processed_df,
                results_df,
                change_points,
                change_analysis
            ) = run_pipeline(raw_df)

        except Exception as error:

            st.error(
                f"Analysis failed: {error}"
            )

            st.stop()

        # ------------------------------------------
        # SIDEBAR
        # ------------------------------------------

        selected_ad = render_sidebar(results_df)

        # ------------------------------------------
        # DASHBOARD HEADER
        # ------------------------------------------

        st.markdown(
            "## Advertisement Performance Dashboard"
        )

        st.caption(
            "Monitor advertising performance, "
            "detect unusual behavior, and identify "
            "potential advertising fatigue."
        )

        st.divider()

        # ------------------------------------------
        # OVERVIEW METRICS
        # ------------------------------------------

        render_metrics(
            results_df,
            processed_df
        )

        st.write("")

        # ------------------------------------------
        # RISK LEADERBOARD
        # ------------------------------------------

        render_risk_table(results_df)

        st.divider()

        # ------------------------------------------
        # INDIVIDUAL AD ANALYSIS
        # ------------------------------------------

        st.markdown(
            "## Advertisement Analysis"
        )

        ad_data = processed_df[
            processed_df["ad_id"] == selected_ad
        ].copy()

        ad_results = results_df[
            results_df["ad_id"] == selected_ad
        ].iloc[0]

        selected_changes = change_analysis.get(
            selected_ad,
            []
        )

        # ------------------------------------------
        # PERFORMANCE SUMMARY
        # ------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Fatigue Risk (0 = Best, 100 = Worst)",
                f"{ad_results['fatigue_score']:.1f}/100",
                help=(
                    "Lower scores mean fewer detected "
                    "fatigue warning signs. A score of "
                    "0 does not guarantee zero risk."
                )
            )

        with col2:

            st.metric(
                "Performance Trend",
                ad_results["performance_trend"]
            )

        with col3:

            st.metric(
                "Risk Level",
                ad_results["risk_level"]
            )

        # ------------------------------------------
        # SMART INSIGHTS
        # ------------------------------------------

        st.divider()

        insights = generate_ad_insights(
            ad_results
        )

        render_insights(insights)

        # ------------------------------------------
        # PERFORMANCE CHARTS
        # ------------------------------------------

        st.divider()

        st.markdown(
            "### Performance Trends"
        )

        st.plotly_chart(
            create_ctr_chart(
                ad_data,
                selected_changes
            ),
            use_container_width=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.plotly_chart(
                create_cpc_chart(ad_data),
                use_container_width=True
            )

        with col2:

            st.plotly_chart(
                create_frequency_chart(ad_data),
                use_container_width=True
            )

        # ------------------------------------------
        # CHANGE ANALYSIS
        # ------------------------------------------

        st.divider()

        st.markdown(
            "### Detected Performance Changes"
        )

        if selected_changes:

            change_df = pd.DataFrame(
                selected_changes
            )

            sorted_ad_data = ad_data.sort_values(
                "date"
            ).reset_index(drop=True)

            change_df["date"] = change_df[
                "change_point"
            ].apply(
                lambda point: sorted_ad_data[
                    "date"
                ].iloc[point]
            )

            change_df["date"] = pd.to_datetime(
                change_df["date"]
            ).dt.strftime("%d %b %Y")

            change_df = change_df[
                [
                    "date",
                    "classification",
                    "ctr_change_pct",
                    "cpc_change_pct"
                ]
            ]

            change_df.columns = [
                "Date",
                "Classification",
                "CTR Change (%)",
                "CPC Change (%)"
            ]

            st.dataframe(
                change_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No significant CTR change points "
                "detected for this advertisement."
            )

        # ------------------------------------------
        # ANOMALY ANALYSIS
        # ------------------------------------------

        st.divider()

        st.markdown(
            "### Anomaly Detection"
        )

        anomalies = ad_data[
            ad_data["anomaly"] == -1
        ].copy()

        anomalies["date"] = pd.to_datetime(
            anomalies["date"]
        ).dt.strftime("%d %b %Y")

        st.caption(
            f"Isolation Forest detected "
            f"{len(anomalies)} unusual observations "
            f"for {selected_ad}."
        )

        if not anomalies.empty:

            st.dataframe(
                anomalies[
                    [
                        "date",
                        "ctr",
                        "cpc",
                        "frequency",
                        "anomaly_score"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

        else:

            st.success(
                "No unusual observations detected."
            )

        # ------------------------------------------
        # EXPORT RESULTS
        # ------------------------------------------

        st.divider()

        st.markdown(
            "### Export Analysis"
        )

        csv_data = results_df.to_csv(
            index=False
        )

        st.download_button(
            label="Download Performance Analysis",
            data=csv_data,
            file_name="adfatigue_analysis.csv",
            mime="text/csv"
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AdFatigue AI • Advertising Performance Intelligence "
    "• PELT + Isolation Forest"
)