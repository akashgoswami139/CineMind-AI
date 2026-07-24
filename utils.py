"""
Reusable utility functions shared across pages: TMDB API access (posters,
trailers, live metadata), formatting helpers, and session-state helpers
for the Favorites feature.
"""

import datetime as dt
import io

import pandas as pd
import requests
import streamlit as st

import config


# --------------------------------------------------------------------------
# TMDB API helpers
# --------------------------------------------------------------------------
@st.cache_data(show_spinner=False, ttl=60 * 60 * 24)
def fetch_movie_tmdb_data(movie_id: int) -> dict:
    """Fetch live poster/backdrop/trailer data for a movie from TMDB.

    Falls back gracefully (placeholder poster, no trailer) if the API key
    is missing or the request fails, so the app never crashes without
    network access or credentials.
    """
    result = {
        "poster_url": config.PLACEHOLDER_POSTER,
        "backdrop_url": None,
        "trailer_url": None,
    }

    if not config.TMDB_API_KEY:
        return result

    try:
        resp = requests.get(
            f"{config.TMDB_BASE_URL}/movie/{int(movie_id)}",
            params={"api_key": config.TMDB_API_KEY, "append_to_response": "videos"},
            timeout=6,
        )
        if resp.status_code != 200:
            return result
        data = resp.json()

        if data.get("poster_path"):
            result["poster_url"] = f"{config.TMDB_IMAGE_BASE}/{config.POSTER_SIZE}{data['poster_path']}"
        if data.get("backdrop_path"):
            result["backdrop_url"] = f"{config.TMDB_IMAGE_BASE}/{config.BACKDROP_SIZE}{data['backdrop_path']}"

        videos = data.get("videos", {}).get("results", [])
        trailer = next(
            (v for v in videos if v.get("type") == "Trailer" and v.get("site") == "YouTube"),
            None,
        )
        if trailer:
            result["trailer_url"] = f"https://www.youtube.com/watch?v={trailer['key']}"
    except requests.RequestException:
        pass

    return result


def get_poster(movie_id: int) -> str:
    return fetch_movie_tmdb_data(movie_id)["poster_url"]


def get_trailer(movie_id: int):
    return fetch_movie_tmdb_data(movie_id)["trailer_url"]


# --------------------------------------------------------------------------
# Formatting helpers
# --------------------------------------------------------------------------
def format_currency(value) -> str:
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "N/A"
    if value <= 0:
        return "N/A"
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    if value >= 1_000:
        return f"${value / 1_000:.0f}K"
    return f"${value:,.0f}"


def format_runtime(minutes) -> str:
    try:
        minutes = int(minutes)
    except (TypeError, ValueError):
        return "N/A"
    if minutes <= 0:
        return "N/A"
    h, m = divmod(minutes, 60)
    return f"{h}h {m}m" if h else f"{m}m"


def format_year(release_date) -> str:
    if not release_date or pd.isna(release_date):
        return "N/A"
    try:
        return str(pd.to_datetime(release_date).year)
    except Exception:
        return "N/A"


def format_date(release_date) -> str:
    if not release_date or pd.isna(release_date):
        return "N/A"
    try:
        return pd.to_datetime(release_date).strftime("%B %d, %Y")
    except Exception:
        return str(release_date)


def language_name(code: str) -> str:
    names = {
        "en": "English", "fr": "French", "es": "Spanish", "de": "German",
        "it": "Italian", "ja": "Japanese", "zh": "Chinese", "hi": "Hindi",
        "ko": "Korean", "ru": "Russian", "pt": "Portuguese", "cn": "Chinese",
    }
    return names.get(code, (code or "N/A").upper())


def similarity_pct(score: float) -> str:
    return f"{round(score * 100)}%"


# --------------------------------------------------------------------------
# Session-state helpers (Favorites)
# --------------------------------------------------------------------------
def init_session_state():
    if "favorites" not in st.session_state:
        st.session_state.favorites = {}  # movie_id -> row dict
    if "search_history" not in st.session_state:
        st.session_state.search_history = []


def add_favorite(movie_row: dict):
    st.session_state.favorites[int(movie_row["movie_id"])] = movie_row


def remove_favorite(movie_id: int):
    st.session_state.favorites.pop(int(movie_id), None)


def is_favorite(movie_id: int) -> bool:
    return int(movie_id) in st.session_state.get("favorites", {})


def favorites_to_csv_bytes() -> bytes:
    favs = list(st.session_state.get("favorites", {}).values())
    if not favs:
        df = pd.DataFrame(columns=["title", "genres", "vote_average", "release_date"])
    else:
        df = pd.DataFrame(favs)
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    return buffer.getvalue().encode("utf-8")


def timestamp() -> str:
    return dt.datetime.now().strftime("%Y-%m-%d %H:%M")
