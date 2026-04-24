"""Integration smoke: app module imports (exercises top-level Streamlit wiring)."""

from __future__ import annotations


def test_app_module_loads() -> None:
    import app as yt_app

    assert hasattr(yt_app, "main")
    assert callable(yt_app.main)


def test_load_channel_frame_returns_two_hundred_rows() -> None:
    import app as yt_app

    df = yt_app.load_channel_frame(99)
    assert len(df) == 200
    assert set(df.columns) >= {"subscribers", "video_views", "category", "year_started"}
