"""Reproducible synthetic channel dataset for demos and tests."""

from __future__ import annotations

from typing import Final

import numpy as np
import pandas as pd

CATEGORIES: Final[tuple[str, ...]] = (
    "Gaming",
    "Music",
    "Entertainment",
    "Education",
    "Howto & Style",
    "Sports",
    "Science & Tech",
    "News",
    "Kids",
    "Comedy",
    "Film & Animation",
    "People & Blogs",
    "Autos & Vehicles",
    "Travel",
    "Other",
)

_CATEGORY_WEIGHTS: Final[np.ndarray] = np.array(
    [0.18, 0.14, 0.12, 0.10, 0.08, 0.07, 0.07, 0.05, 0.05, 0.04, 0.03, 0.03, 0.02, 0.01, 0.01],
    dtype=np.float64,
)


def generate_channel_dataset(
    n: int = 200,
    *,
    seed: int | None = 42,
    year_min: int = 2005,
    year_max: int = 2024,
) -> pd.DataFrame:
    """
    Build a dataframe of top-style YouTube channel records.

    Columns: channel_name, subscribers, video_views, category, year_started
    """
    if n < 1:
        raise ValueError("n must be at least 1")
    if year_min > year_max:
        raise ValueError("year_min must be <= year_max")

    rng = np.random.default_rng(seed)

    # Subscriber counts (roughly log-normal, millions-ish)
    log_subs = rng.normal(loc=np.log(2_000_000), scale=1.35, size=n)
    subscribers = np.clip(np.exp(log_subs), 50_000, 250_000_000).astype(np.int64)

    # Views correlated with subscribers + noise
    view_multiplier = rng.lognormal(mean=2.8, sigma=0.45, size=n)
    video_views = np.clip(
        (subscribers * view_multiplier * rng.uniform(5, 80, size=n)).astype(np.int64),
        subscribers,
        50_000_000_000,
    )

    category_idx = rng.choice(len(CATEGORIES), size=n, p=_CATEGORY_WEIGHTS)
    category = np.array([CATEGORIES[i] for i in category_idx], dtype=object)

    year_started = rng.integers(low=year_min, high=year_max + 1, size=n, dtype=np.int64)

    channel_name = np.array([f"Channel {i + 1:03d}" for i in range(n)], dtype=object)

    df = pd.DataFrame(
        {
            "channel_name": channel_name,
            "subscribers": subscribers,
            "video_views": video_views,
            "category": pd.Categorical(category, categories=list(CATEGORIES)),
            "year_started": year_started,
        }
    )

    return df
