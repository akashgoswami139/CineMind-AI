"""
Central configuration for the Movie Recommender app.
Holds theme tokens, file paths, and TMDB API settings.
"""

import os
from pathlib import Path

# --------------------------------------------------------------------------
# Paths
# --------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
MODELS_DIR = BASE_DIR / "models"

MOVIES_PKL = MODELS_DIR / "movies.pkl"
SIMILARITY_PKL = MODELS_DIR / "similarity.pkl"
STYLE_CSS = ASSETS_DIR / "style.css"

# --------------------------------------------------------------------------
# TMDB API
# --------------------------------------------------------------------------
# Preferred: set via environment variable or .streamlit/secrets.toml.
# Falls back to the key below so the app works out of the box.
DEFAULT_TMDB_API_KEY = "8a4a4ec78cb4d519f1962e230ebcee86"


def _get_tmdb_key() -> str:
    try:
        import streamlit as st
        if "TMDB_API_KEY" in st.secrets:
            return st.secrets["TMDB_API_KEY"]
    except Exception:
        pass
    return os.environ.get("TMDB_API_KEY", DEFAULT_TMDB_API_KEY)


TMDB_API_KEY = _get_tmdb_key()
TMDB_BASE_URL = "https://api.themoviedb.org/3"
TMDB_IMAGE_BASE = "https://image.tmdb.org/t/p"
POSTER_SIZE = "w500"
BACKDROP_SIZE = "w1280"

PLACEHOLDER_POSTER = "https://placehold.co/500x750/18181B/A1A1AA?text=No+Poster"

# --------------------------------------------------------------------------
# Theme tokens (kept in sync with assets/style.css)
# --------------------------------------------------------------------------
COLORS = {
    "background": "#09090B",
    "surface": "#0F0F12",
    "card": "#18181B",
    "card_border": "rgba(255, 255, 255, 0.08)",
    "primary": "#6366F1",
    "primary_soft": "#818CF8",
    "accent": "#06B6D4",
    "success": "#10B981",
    "danger": "#EF4444",
    "warning": "#F59E0B",
    "text_primary": "#FAFAFA",
    "text_secondary": "#A1A1AA",
    "text_muted": "#71717A",
}

PLOTLY_TEMPLATE = "plotly_dark"
PLOTLY_COLORWAY = [
    COLORS["primary"], COLORS["accent"], COLORS["success"],
    COLORS["warning"], COLORS["danger"], COLORS["primary_soft"],
]

APP_NAME = "CineMind AI"
APP_TAGLINE = "Discover movies you'll love using Machine Learning."

NAV_LINKS = {
    "github": "https://github.com/akashgoswami139",
    "linkedin": "https://www.linkedin.com/in/akashgoswami-/",
    "portfolio": "https://your-portfolio.example.com",
}
