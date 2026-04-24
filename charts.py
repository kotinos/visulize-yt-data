"""Plotly Express figure builders (Streamlit-agnostic)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def _qualitative_palette(name: str) -> list[str]:
    seq = getattr(px.colors.qualitative, name, None)
    if seq is None:
        return list(px.colors.qualitative.D3)
    return list(seq)


def figure_subscriber_histogram(
    df: pd.DataFrame,
    *,
    sequential_scale: str,
    template: str = "plotly_dark",
    bins: int = 28,
) -> go.Figure:
    """Histogram of subscribers with sequential coloring by bin center."""
    subs = df["subscribers"].to_numpy(dtype=np.float64)
    counts, edges = np.histogram(subs, bins=bins)
    centers = (edges[:-1] + edges[1:]) / 2
    hist_df = pd.DataFrame({"subscriber_bin_center": centers, "channel_count": counts})

    fig = px.bar(
        hist_df,
        x="subscriber_bin_center",
        y="channel_count",
        color="subscriber_bin_center",
        color_continuous_scale=sequential_scale,
        labels={
            "subscriber_bin_center": "Subscribers (bin center)",
            "channel_count": "Channels",
            "color": "Subscribers",
        },
        template=template,
    )
    fig.update_layout(
        coloraxis_showscale=True,
        bargap=0.08,
        margin=dict(l=48, r=24, t=56, b=48),
        title=dict(text="Subscriber distribution", x=0.02, xanchor="left"),
    )
    fig.update_xaxes(tickformat=",.0s")
    return fig


def figure_category_donut(
    df: pd.DataFrame,
    *,
    qualitative_palette: str,
    template: str = "plotly_dark",
) -> go.Figure:
    """Donut chart of channel categories."""
    palette = _qualitative_palette(qualitative_palette)
    counts = df.groupby("category", observed=False).size().reset_index(name="count")
    counts = counts.sort_values("count", ascending=False)

    fig = px.pie(
        counts,
        names="category",
        values="count",
        hole=0.38,
        color_discrete_sequence=palette,
        template=template,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(
        margin=dict(l=24, r=24, t=56, b=24),
        title=dict(text="Categories", x=0.02, xanchor="left"),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.25, x=0),
    )
    return fig


def figure_year_started_box(
    df: pd.DataFrame,
    *,
    qualitative_palette: str,
    template: str = "plotly_dark",
) -> go.Figure:
    """Box plot of channel founding years."""
    palette = _qualitative_palette(qualitative_palette)
    work = df.assign(_series="All channels")

    fig = px.box(
        work,
        x="_series",
        y="year_started",
        color="_series",
        color_discrete_sequence=palette,
        points="outliers",
        template=template,
        labels={"year_started": "Year started", "_series": ""},
    )
    fig.update_layout(
        margin=dict(l=48, r=24, t=56, b=48),
        title=dict(text="Year started (spread)", x=0.02, xanchor="left"),
        showlegend=False,
        xaxis=dict(showticklabels=False, title=""),
    )
    return fig
