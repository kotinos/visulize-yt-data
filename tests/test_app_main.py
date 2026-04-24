"""Exercise app dashboard with a mocked Streamlit surface."""

from __future__ import annotations

from unittest.mock import MagicMock

import streamlit

import app


def _context_manager() -> MagicMock:
    cm = MagicMock()
    cm.__enter__.return_value = cm
    cm.__exit__.return_value = None
    return cm


def test_render_dashboard_calls_plotly_three_times() -> None:
    s = MagicMock()

    s.number_input.return_value = 11
    s.selectbox.side_effect = ["Turbo", "Pastel"]

    side = MagicMock()
    side.__enter__.return_value = None
    side.__exit__.return_value = None
    s.sidebar = side

    s.columns.return_value = (_context_manager(), _context_manager(), _context_manager(), _context_manager())

    tab_a, tab_b, tab_c = _context_manager(), _context_manager(), _context_manager()
    s.tabs.return_value = (tab_a, tab_b, tab_c)

    app._render_dashboard(s)

    assert s.plotly_chart.call_count == 3


def test_main_delegates_to_render_dashboard(monkeypatch) -> None:
    spy = MagicMock()
    monkeypatch.setattr(app, "_render_dashboard", spy)
    app.main()
    spy.assert_called_once_with(streamlit)
