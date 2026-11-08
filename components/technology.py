import streamlit as st


def render_technology():

    st.title("Technology & Algorithms")

    st.caption(
        "Understand the technologies powering AdFatigue AI."
    )

    st.info(
        "AdFatigue AI combines machine learning, statistical "
        "change detection, and rule-based analysis to help "
        "advertisers understand their campaign performance."
    )

    # --------------------------------------------------
    # TECHNOLOGY STACK
    # --------------------------------------------------

    st.markdown("## Technology Stack")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🐍 Python")
        st.write(
            "The main programming language used to "
            "process data and run our analysis."
        )

    with col2:
        st.markdown("### 📊 Streamlit")
        st.write(
            "Powers the interactive dashboard, CSV uploads, "
            "advertisement selection, and results display."
        )

    with col3:
        st.markdown("### 📈 Plotly")
        st.write(
            "Creates interactive charts to visualize "
            "advertising performance over time."
        )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🐼 Pandas")
        st.write(
            "Organizes advertising data and calculates "
            "metrics such as CTR, CPC, CPM, and CPA."
        )

    with col2:
        st.markdown("### 🤖 Scikit-learn")
        st.write(
            "Provides Isolation Forest, which identifies "
            "unusual advertising performance observations."
        )

    with col3:
        st.markdown("### 🔍 Ruptures")
        st.write(
            "Provides the PELT algorithm used to "
            "detect changes in CTR patterns."
        )

    st.divider()

    # --------------------------------------------------
    # PELT
    # --------------------------------------------------

    st.markdown("## 1. PELT — Change-Point Detection")

    st.markdown(
        "**PELT** stands for "
        "**Pruned Exact Linear Time**."
    )

    st.write(
        "PELT helps us identify when an advertisement's "
        "click-through rate changes significantly."
    )

    st.markdown("### Example")

    st.markdown(
        """
        Imagine an advertisement with the following CTR:

        - Days 1–20: CTR stays around 3%.
        - Days 21–40: CTR stays around 3%.
        - Days 41–60: CTR drops to around 1%.

        PELT may detect a change around Day 41 because
        the CTR pattern shifted.
        """
    )

    st.success(
        "PELT answers: When did the advertisement's "
        "CTR pattern change?"
    )

    with st.expander("How does PELT work technically?"):

        st.write(
            "PELT divides a time series into segments "
            "and searches for change points that minimize "
            "a cost function plus a penalty."
        )

        st.latex(
            r"\min \left("
            r"\sum_{i=1}^{m+1} C(y_{\tau_{i-1}:\tau_i})"
            r"+\beta m\right)"
        )

        st.markdown(
            """
            **Where:**

            - **C:** Cost of representing a segment.
            - **m:** Number of detected change points.
            - **β:** Penalty for adding change points.

            Our implementation uses the **L2 cost model**,
            which looks for changes in the mean CTR level.

            PELT identifies the change locations. Our
            separate rules classify their direction.
            """
        )

    st.divider()

    # --------------------------------------------------
    # CHANGE CLASSIFICATION
    # --------------------------------------------------

    st.markdown("## 2. Performance Change Classification")

    st.write(
        "After PELT detects a change, our application "
        "compares average CTR and CPC before and after it."
    )

    st.markdown(
        """
        Our classification rules use a **5% relative-change
        threshold**.

        | Classification | Meaning |
        |---|---|
        | 🟢 Improvement | Significant favorable change without a significant unfavorable change |
        | 🔴 Deterioration | Significant unfavorable change without a significant favorable change |
        | 🟡 Mixed Change | Significant favorable and unfavorable changes |
        | ⚪ No Significant Change | Neither metric crosses the threshold |
        """
    )

    st.caption(
        "The comparison uses up to 10 observations "
        "before and after each detected change point."
    )

    st.divider()

    # --------------------------------------------------
    # ISOLATION FOREST
    # --------------------------------------------------

    st.markdown("## 3. Isolation Forest — Anomaly Detection")

    st.write(
        "Isolation Forest is an unsupervised machine "
        "learning algorithm that identifies unusual "
        "observations in advertising data."
    )

    st.markdown("### Features used")

    st.markdown(
        """
        - **CTR:** Click-through rate.
        - **CPC:** Cost per click.
        - **Frequency:** Average ad exposure frequency.
        """
    )

    st.markdown("### Example")

    st.markdown(
        """
        Suppose an advertisement usually has:

        - CTR around 3%.
        - CPC around $1.
        - Frequency around 1.5.

        One day, its CTR falls to 0.5% and CPC rises
        to $5.

        Isolation Forest may flag that observation
        as unusual.
        """
    )

    st.warning(
        "An anomaly is not automatically bad. "
        "It simply means the observation is unusual."
    )

    with st.expander("How does Isolation Forest work technically?"):

        st.write(
            "Isolation Forest creates randomized decision "
            "trees to separate observations."
        )

        st.write(
            "Observations that can be isolated with fewer "
            "splits are more likely to be anomalies."
        )

        st.code(
            """
model = IsolationForest(
    n_estimators=100,
    contamination=0.1,
    random_state=42
)
            """,
            language="python"
        )

        st.caption(
            "Our model uses standardized CTR, CPC, and "
            "frequency values. The contamination setting "
            "controls the expected proportion of anomalies."
        )

    st.divider()

    # --------------------------------------------------
    # BASELINE
    # --------------------------------------------------

    st.markdown("## 4. Baseline Comparison")

    st.write(
        "A baseline is a reference point used to "
        "compare advertisement performance."
    )

    st.info(
        "Our current negative-anomaly rule uses the "
        "average CTR and CPC from the first 15 observations "
        "of each advertisement."
    )

    st.markdown(
        """
        An Isolation Forest anomaly contributes to the
        negative-anomaly count when:

        - CTR is more than 5% below its baseline, **or**
        - CPC is more than 5% above its baseline.

        This is a rule-based interpretation, not an
        additional machine learning prediction.
        """
    )

    st.divider()

    # --------------------------------------------------
    # FATIGUE SCORE
    # --------------------------------------------------

    st.markdown("## 5. Fatigue-Risk Scoring")

    st.write(
        "Our application combines several warning "
        "indicators into a fatigue-risk score."
    )

    st.markdown(
        """
        | Indicator | Maximum Points |
        |---|---:|
        | CTR decline | 40 |
        | CPC increase | 20 |
        | Detected deteriorating change | 20 |
        | Negative anomalies | 20 |
        | **Total** | **100** |
        """
    )

    st.markdown("### Risk levels")

    st.markdown(
        """
        - 🟢 **Low:** Score below 40.
        - 🟡 **Medium:** Score from 40 to below 70.
        - 🔴 **High:** Score of 70 or above.
        """
    )

    st.success(
        "A lower fatigue-risk score means fewer warning "
        "signs were detected by our current rules."
    )

    st.caption(
        "The score is a custom heuristic, not a validated "
        "probability of advertising fatigue."
    )

    st.divider()

    # --------------------------------------------------
    # SYSTEM WORKFLOW
    # --------------------------------------------------

    st.markdown("## 6. How Everything Works Together")

    st.code(
        """
             Upload CSV
                 |
                 v
          Data Preprocessing
                 |
                 v
        Calculate CTR / CPC
                 |
          +------+------+
          |             |
          v             v
         PELT     Isolation Forest
          |             |
          v             v
     Change Points    Anomalies
          |             |
          v             |
    Classify Changes    |
          |             |
          +------+------+
                 |
                 v
          Fatigue Scoring
                 |
                 v
         Performance Results
                 |
                 v
          Smart Insights
                 |
                 v
          User Dashboard
        """,
        language="text"
    )

    st.caption(
        "Smart Insights explains the existing results "
        "using Python rules. It does not use an external LLM."
    )