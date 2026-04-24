# YouTube Trending Visualizer

Streamlit dashboard for **200 channel-style records**: subscribers, views, category, and year started — visualized with **Plotly Express** (histogram, donut, box). No external API calls.

## Quick start

```bash
cd visulize-yt-data
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the URL shown (default `http://localhost:8501`). On Windows, prefer `python -m streamlit …` if `streamlit` is not on your PATH.

## Tests

```bash
python -m pytest
```

Coverage is configured in `pytest.ini` for `data/`, `charts.py`, and `app.py`.

## Layout

| Path | Purpose |
|------|---------|
| `app.py` | UI and wiring |
| `charts.py` | Plotly Express figures |
| `data/mock_channels.py` | Reproducible dataset (`seed`) |
| `tests/` | Pytest |

**Stack:** Python 3.10+, Streamlit, Plotly, pandas.

## License

Specify a license before publishing (this repo ships without one by default).
