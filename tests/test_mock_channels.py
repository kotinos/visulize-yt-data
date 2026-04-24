"""Tests for mock channel dataset generation."""

import pandas as pd
import pytest

from data.mock_channels import generate_channel_dataset


def test_generate_returns_requested_row_count() -> None:
    df = generate_channel_dataset(200, seed=1)
    assert len(df) == 200


def test_generate_columns_and_dtypes() -> None:
    df = generate_channel_dataset(50, seed=0)
    expected = {"channel_name", "subscribers", "video_views", "category", "year_started"}
    assert set(df.columns) == expected
    assert pd.api.types.is_integer_dtype(df["subscribers"])
    assert pd.api.types.is_integer_dtype(df["video_views"])
    assert isinstance(df["category"].dtype, pd.CategoricalDtype)
    assert pd.api.types.is_integer_dtype(df["year_started"])


def test_determinism_with_seed() -> None:
    a = generate_channel_dataset(200, seed=123)
    b = generate_channel_dataset(200, seed=123)
    pd.testing.assert_frame_equal(a.reset_index(drop=True), b.reset_index(drop=True))


def test_different_seeds_produce_different_data() -> None:
    a = generate_channel_dataset(200, seed=1)
    b = generate_channel_dataset(200, seed=2)
    assert not a.equals(b)


def test_subscribers_and_views_positive() -> None:
    df = generate_channel_dataset(200, seed=7)
    assert (df["subscribers"] > 0).all()
    assert (df["video_views"] > 0).all()
    assert (df["video_views"] >= df["subscribers"]).all()


def test_year_started_within_default_bounds() -> None:
    df = generate_channel_dataset(500, seed=99)
    assert (df["year_started"] >= 2005).all()
    assert (df["year_started"] <= 2024).all()


def test_custom_year_bounds_respected() -> None:
    df = generate_channel_dataset(100, seed=0, year_min=2010, year_max=2015)
    assert (df["year_started"] >= 2010).all()
    assert (df["year_started"] <= 2015).all()


def test_n_must_be_positive() -> None:
    with pytest.raises(ValueError, match="at least 1"):
        generate_channel_dataset(0)


def test_year_min_max_validation() -> None:
    with pytest.raises(ValueError, match="year_min"):
        generate_channel_dataset(10, year_min=2020, year_max=2010)
