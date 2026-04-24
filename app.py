"""YouTube Trending Visualizer — Streamlit + Plotly Express."""

from __future__ import annotations

from typing import Any

import pandas as pd
import streamlit as st

from charts import (
    figure_category_donut,
    figure_subscriber_histogram,
    figure_year_started_box,
)
from data.mock_channels import generate_channel_dataset

SEQUENTIAL_SCALES: tuple[str, ...] = (
    "Viridis",
    "Plasma",
    "Inferno",
    "Magma",
    "Cividis",
    "Turbo",
    "Blues",
    "Purples",
    "Tealgrn",
)

QUALITATIVE_PALETTES: tuple[str, ...] = (
    "D3",
    "Plotly",
    "Bold",
    "Safe",
    "Pastel",
    "Light24",
    "Set3",
    "Dark24",
    "Alphabet",
)


@st.cache_data(show_spinner=False)
def load_channel_frame(seed: int) -> pd.DataFrame:
    """Cached dataset for a given RNG seed."""
    return generate_channel_dataset(200, seed=seed)


def _render_dashboard(streamlit: Any) -> None:
    """Render the full page using the given Streamlit module (injectable for tests)."""
    streamlit.set_page_config(
        page_title="YouTube Trending Visualizer",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    streamlit.markdown(
        """
        <style>
        .block-container { padding-top: 1.25rem; padding-bottom: 2rem; }
        div[data-testid="stMetricValue"] { font-size: 1.65rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    streamlit.title("YouTube Trending Visualizer")
    streamlit.caption(
        "200 channels — subscribers, categories, and founding years. Adjust seed and colors in the sidebar."
    )

    with streamlit.sidebar:
        streamlit.subheader("Data")
        seed = streamlit.number_input("Random seed", min_value=0, max_value=10_000, value=42, step=1)
        streamlit.divider()
        streamlit.subheader("Color themes")
        streamlit.caption("Sequential scales color the **subscriber histogram** by bin magnitude.")
        sequential = streamlit.selectbox("Histogram colormap", SEQUENTIAL_SCALES, index=0)
        streamlit.caption("Qualitative palettes drive **category** and **year** charts.")
        qualitative = streamlit.selectbox("Category & box palette", QUALITATIVE_PALETTES, index=0)

    df = load_channel_frame(int(seed))

    c1, c2, c3, c4 = streamlit.columns(4)
    with c1:
        streamlit.metric("Channels", f"{len(df):,}")
    with c2:
        streamlit.metric("Median subscribers", f"{df['subscribers'].median():,.0f}")
    with c3:
        streamlit.metric("Median views", f"{df['video_views'].median():,.0f}")
    with c4:
        streamlit.metric("Categories", f"{df['category'].nunique()}")

    streamlit.divider()

    top, mid, bot = streamlit.tabs(["Subscriber histogram", "Categories", "Year started"])

    with top:
        fig_hist = figure_subscriber_histogram(df, sequential_scale=sequential)
        streamlit.plotly_chart(fig_hist, use_container_width=True)

    with mid:
        fig_pie = figure_category_donut(df, qualitative_palette=qualitative)
        streamlit.plotly_chart(fig_pie, use_container_width=True)

    with bot:
        fig_box = figure_year_started_box(df, qualitative_palette=qualitative)
        streamlit.plotly_chart(fig_box, use_container_width=True)


def main() -> None:
    _render_dashboard(st)


if __name__ == "__main__":
    main()
