import streamlit as st


def render_sidebar(results_df):

    with st.sidebar:

        st.markdown("# ◈ AdFatigue AI")

        st.caption("AD PERFORMANCE INTELLIGENCE")

        st.divider()

        st.markdown("### Advertisement Selection")

        ad_ids = results_df["ad_id"].tolist()

        selected_ad = st.selectbox(
            "Select Advertisement",
            options=ad_ids
        )

        st.divider()

        st.markdown("### About")

        st.caption(
            "AI-powered advertising performance analysis "
            "using change-point detection and anomaly detection."
        )

        st.caption("Built with Python, Scikit-learn & Streamlit")

    return selected_ad