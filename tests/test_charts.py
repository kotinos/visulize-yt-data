"""Tests for Plotly figure builders."""

import pandas as pd
import plotly.graph_objects as go

from charts import (
    figure_category_donut,
    figure_subscriber_histogram,
    figure_year_started_box,
)
from data.mock_channels import generate_channel_dataset


def _sample_df() -> pd.DataFrame:
    return generate_channel_dataset(120, seed=3)


def test_histogram_returns_bar_figure_with_expected_trace() -> None:
    df = _sample_df()
    fig = figure_subscriber_histogram(df, sequential_scale="Plasma")
    assert isinstance(fig, go.Figure)
    assert fig.data[0].type == "bar"


def test_donut_returns_pie_trace() -> None:
    df = _sample_df()
    fig = figure_category_donut(df, qualitative_palette="Bold")
    assert isinstance(fig, go.Figure)
    assert fig.data[0].type == "pie"
    assert fig.data[0].hole is not None
    assert fig.data[0].hole > 0


def test_box_returns_box_trace() -> None:
    df = _sample_df()
    fig = figure_year_started_box(df, qualitative_palette="D3")
    assert isinstance(fig, go.Figure)
    assert fig.data[0].type == "box"


def test_unknown_palette_falls_back_without_error() -> None:
    df = _sample_df()
    fig = figure_category_donut(df, qualitative_palette="NonexistentPaletteName")
    assert isinstance(fig, go.Figure)
    assert fig.data[0].type == "pie"
