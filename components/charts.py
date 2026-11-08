import plotly.graph_objects as go


CHART_LAYOUT = {
    "template": "plotly_dark",
    "paper_bgcolor": "#111827",
    "plot_bgcolor": "#111827",
    "hovermode": "x unified",
    "margin": dict(l=20, r=20, t=60, b=20)
}


def create_ctr_chart(ad_data, change_analysis):

    ad_data = ad_data.sort_values("date").reset_index(drop=True)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ad_data["date"],
            y=ad_data["ctr"],
            mode="lines",
            name="CTR",
            line=dict(
                color="#38BDF8",
                width=3
            )
        )
    )

    colors = {
        "Improvement": "#22C55E",
        "Deterioration": "#EF4444",
        "Mixed Change": "#FACC15",
        "No Significant Change": "#94A3B8",
        "Insufficient Data": "#64748B"
    }

    for change in change_analysis:

        point = change["change_point"]
        classification = change["classification"]

        if point >= len(ad_data):
            continue

        change_date = ad_data["date"].iloc[point]

        color = colors.get(
            classification,
            "#94A3B8"
        )

        fig.add_vline(
            x=change_date,
            line_dash="dash",
            line_color=color,
            line_width=2
        )

        fig.add_trace(
            go.Scatter(
                x=[change_date],
                y=[ad_data["ctr"].iloc[point]],
                mode="markers",
                name=classification,
                marker=dict(
                    color=color,
                    size=10
                ),
                hovertemplate=(
                    f"{classification}<br>"
                    "Date: %{x}<br>"
                    "CTR: %{y:.2f}%<extra></extra>"
                )
            )
        )

    fig.update_layout(
        title="CTR Performance & Change Detection",
        xaxis_title="Date",
        yaxis_title="CTR (%)",
        height=400,
        **CHART_LAYOUT
    )

    return fig


def create_cpc_chart(ad_data):

    ad_data = ad_data.sort_values("date")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ad_data["date"],
            y=ad_data["cpc"],
            mode="lines",
            name="CPC",
            line=dict(
                color="#A78BFA",
                width=3
            ),
            fill="tozeroy",
            fillcolor="rgba(167,139,250,0.08)"
        )
    )

    fig.update_layout(
        title="Cost Per Click",
        xaxis_title="Date",
        yaxis_title="CPC ($)",
        height=350,
        **CHART_LAYOUT
    )

    return fig


def create_frequency_chart(ad_data):

    ad_data = ad_data.sort_values("date")

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=ad_data["date"],
            y=ad_data["frequency"],
            mode="lines",
            name="Frequency",
            line=dict(
                color="#FBBF24",
                width=3
            )
        )
    )

    fig.update_layout(
        title="Ad Frequency",
        xaxis_title="Date",
        yaxis_title="Frequency",
        height=350,
        **CHART_LAYOUT
    )

    return fig