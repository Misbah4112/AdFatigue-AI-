import streamlit as st


def render_insights(insights):
    """
    Display simple, user-friendly advertisement insights.
    """

    st.markdown("## Smart Performance Insights")

    # ------------------------------------------
    # MAIN STATUS
    # ------------------------------------------

    st.markdown(
        f"### {insights['status']} {insights['headline']}"
    )

    st.info(insights["summary"])

    # ------------------------------------------
    # WHY THIS HAPPENED
    # ------------------------------------------

    st.markdown("#### 📊 What the data tells us")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Click Performance**")
        st.write(insights["ctr_explanation"])

    with col2:
        st.markdown("**Cost Efficiency**")
        st.write(insights["cpc_explanation"])

    # ------------------------------------------
    # ANOMALY EXPLANATION
    # ------------------------------------------

    st.markdown("#### 🔍 Unusual Performance")

    st.write(insights["anomaly_explanation"])

    # ------------------------------------------
    # RECOMMENDED ACTION
    # ------------------------------------------

    st.markdown("#### 💡 Recommended Action")

    if insights["risk_level"] == "High":
        st.error(insights["recommendation"])

    elif insights["risk_level"] == "Medium":
        st.warning(insights["recommendation"])

    else:
        st.success(insights["recommendation"])

    st.caption(
        "Insights are automatically generated from "
        "the existing performance analysis. "
        "Recommendations are suggestions, not guarantees."
    )