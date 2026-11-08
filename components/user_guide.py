import streamlit as st


def render_user_guide():

    st.title("User Guide")

    st.caption(
        "Everything you need to know about using AdFatigue AI."
    )

    # --------------------------------------------------
    # INTRODUCTION
    # --------------------------------------------------

    st.markdown("## What is AdFatigue AI?")

    st.write(
        "AdFatigue AI is an advertising performance "
        "analysis application that helps businesses "
        "identify improving advertisements, declining "
        "performance, unusual observations, and "
        "potential advertising fatigue."
    )

    st.info(
        "The goal is to help advertisers understand "
        "which advertisements may need attention "
        "without requiring technical knowledge."
    )

    st.divider()

    # --------------------------------------------------
    # GETTING STARTED
    # --------------------------------------------------

    st.markdown("## Getting Started")

    st.markdown(
        """
        **Step 1 — Prepare your data**

        Export your advertising performance data
        into a CSV file.

        **Step 2 — Upload your CSV**

        Use the file uploader in the left sidebar.

        **Step 3 — Review the overview**

        Check which advertisements are improving,
        deteriorating, or showing high fatigue risk.

        **Step 4 — Select an advertisement**

        Use the advertisement selector in the sidebar.

        **Step 5 — Read Smart Performance Insights**

        Understand what changed and what actions
        you might consider.

        **Step 6 — Explore detailed analytics**

        Review charts, detected changes, and anomalies.

        **Step 7 — Export results**

        Download the performance analysis as a CSV.
        """
    )

    st.divider()

    # --------------------------------------------------
    # CSV FORMAT
    # --------------------------------------------------

    st.markdown("## Required CSV Format")

    st.write(
        "Your uploaded CSV must contain the following columns:"
    )

    st.markdown(
        """
        | Column | Description |
        |---|---|
        | date | Date of the advertising observation |
        | ad_id | Unique advertisement identifier |
        | impressions | Number of times the ad was displayed |
        | clicks | Number of clicks received |
        | spend | Amount spent on advertising |
        | conversions | Number of recorded conversions |
        | frequency | Average number of times the ad was shown per person |
        """
    )

    st.markdown("### Example CSV")

    st.code(
        """date,ad_id,impressions,clicks,spend,conversions,frequency
2026-08-01,AD_001,10000,300,300,15,1.2
2026-08-02,AD_001,11000,320,330,18,1.3
2026-08-03,AD_001,12000,290,350,12,1.4""",
        language="csv"
    )

    st.caption(
        "Each row represents one advertisement's "
        "performance for a particular date. "
        "The current application expects daily data."
    )

    st.divider()

    # --------------------------------------------------
    # METRIC DEFINITIONS
    # --------------------------------------------------

    st.markdown("## Understanding Advertising Metrics")

    with st.expander("CTR — Click-Through Rate", expanded=True):

        st.write(
            "CTR measures the percentage of impressions "
            "that resulted in clicks."
        )

        st.latex(
            r"CTR = \frac{Clicks}{Impressions} \times 100"
        )

        st.markdown(
            "**Example:** 300 clicks from 10,000 impressions "
            "gives a CTR of 3%."
        )

        st.success(
            "A higher CTR generally indicates stronger "
            "click engagement."
        )

    with st.expander("CPC — Cost Per Click"):

        st.write(
            "CPC tells you how much you pay, on average, "
            "for each click."
        )

        st.latex(
            r"CPC = \frac{Ad\ Spend}{Clicks}"
        )

        st.markdown(
            "**Example:** $300 spent on 300 clicks "
            "gives a CPC of $1."
        )

        st.success(
            "A lower CPC generally means cheaper clicks."
        )

    with st.expander("CPM — Cost Per 1,000 Impressions"):

        st.write(
            "CPM measures how much you spend "
            "for every 1,000 impressions."
        )

        st.latex(
            r"CPM = \frac{Ad\ Spend}{Impressions}"
            r"\times 1000"
        )

    with st.expander("CPA — Cost Per Acquisition"):

        st.write(
            "CPA measures the average advertising cost "
            "per recorded conversion."
        )

        st.latex(
            r"CPA = \frac{Ad\ Spend}{Conversions}"
        )

        st.caption(
            "The meaning of a conversion depends "
            "on how it is defined in your advertising data."
        )

    with st.expander("Frequency"):

        st.write(
            "Frequency measures how often, on average, "
            "people have seen an advertisement."
        )

        st.markdown(
            "**Example:** A frequency of 3 means "
            "the advertisement was shown approximately "
            "three times per reached person."
        )

        st.warning(
            "High frequency can be a warning sign, "
            "but it does not automatically prove ad fatigue."
        )

    st.divider()

    # --------------------------------------------------
    # RESULTS
    # --------------------------------------------------

    st.markdown("## Understanding Your Results")

    st.markdown("### Performance Trend")

    st.markdown(
        """
        | Status | Meaning |
        |---|---|
        | 🟢 Improving | The latest classified change indicates improvement |
        | 🔴 Deteriorating | The latest classified change indicates deterioration |
        | 🟡 Mixed | The latest classified change has both favorable and unfavorable signals |
        | 🔵 Stable | No qualifying latest change was detected |
        """
    )

    st.caption(
        "The trend classification is based on detected "
        "change points. Stable does not guarantee that "
        "performance is good."
    )

    st.markdown("### CTR Change (%)")

    st.write(
        "Compares average CTR in the first 15 observations "
        "with the last 15 observations."
    )

    st.markdown(
        """
        - **+40%:** CTR increased by 40% relative to its starting average.
        - **-40%:** CTR decreased by 40% relative to its starting average.
        """
    )

    st.markdown("### CPC Change (%)")

    st.write(
        "Compares average CPC in the first 15 observations "
        "with the last 15 observations."
    )

    st.markdown(
        """
        - **-30%:** Clicks became 30% cheaper.
        - **+150%:** Clicks became 150% more expensive.
        """
    )

    st.info(
        "Percentage changes can exceed 100%. "
        "For example, CPC rising from $1 to $3 "
        "is a 200% increase."
    )

    st.markdown("### Fatigue-Risk Score")

    st.write(
        "A score from 0 to 100 summarizing the warning "
        "indicators found by our current rules."
    )

    st.markdown(
        """
        - 🟢 **0–39.99:** Low risk.
        - 🟡 **40–69.99:** Medium risk.
        - 🔴 **70–100:** High risk.
        """
    )

    st.success(
        "Lower is better. A score of 0 means no fatigue "
        "warning points were assigned by our rules."
    )

    st.markdown("### Improvements and Deteriorations")

    st.write(
        "These columns count the change points classified "
        "as improvements or deteriorations."
    )

    st.warning(
        "An Improvements value of 3 means three detected "
        "changes were classified as improvements. "
        "It does not mean performance improved by 3%."
    )

    st.markdown("### Anomalies")

    st.write(
        "Anomalies are unusual performance observations "
        "detected by Isolation Forest."
    )

    st.markdown(
        """
        An anomaly could represent:

        - An unusually strong performance day.
        - An unusually weak performance day.
        - An unusual combination of advertising metrics.
        """
    )

    st.caption(
        "The anomaly count includes both favorable "
        "and unfavorable unusual observations."
    )

    st.markdown("### Anomaly Score")

    st.write(
        "A model-generated measure of how unusual "
        "an observation is."
    )

    st.write(
        "In our implementation, higher values indicate "
        "more unusual observations. It is not a percentage "
        "or a measure of how bad the advertisement is."
    )

    st.markdown("### Detected Change Points")

    st.write(
        "These are dates where PELT identified "
        "changes in the CTR pattern."
    )

    st.markdown(
        """
        - **Improvement:** Favorable performance change.
        - **Deterioration:** Unfavorable performance change.
        - **Mixed Change:** Both favorable and unfavorable signals.
        - **No Significant Change:** Changes did not cross the classification threshold.
        """
    )

    st.divider()

    # --------------------------------------------------
    # INSIGHTS
    # --------------------------------------------------

    st.markdown("## Smart Performance Insights")

    st.write(
        "The Smart Insights section translates technical "
        "results into simple explanations."
    )

    st.markdown(
        """
        It explains:

        1. What is happening with the advertisement.
        2. How CTR and CPC have changed.
        3. How many unusual observations were detected.
        4. What actions an advertiser could consider.
        """
    )

    st.info(
        "These explanations are generated using Python "
        "rules applied to existing results. "
        "They are not responses from a generative AI model."
    )

    st.divider()

    # --------------------------------------------------
    # LIMITATIONS
    # --------------------------------------------------

    st.markdown("## Important Limitations")

    st.markdown(
        """
        - AdFatigue AI identifies warning patterns; it
          cannot prove that ad fatigue caused them.
        - A low risk score does not guarantee future success.
        - Unusual observations are not always negative.
        - Results depend on data quality and the available
          observation history.
        - The fatigue-risk score uses custom rules and
          has not been validated as a probability.
        - The current system does not directly measure
          revenue, ROAS, or profitability.
        """
    )

    st.warning(
        "Use these results to support advertising decisions, "
        "not as the only reason to pause, scale, or "
        "replace an advertisement."
    )

    st.divider()

    st.caption(
        "AdFatigue AI • Advertising Performance Intelligence"
    )