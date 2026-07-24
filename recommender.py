"""
Content-based recommendation engine.

Loads the pre-computed movies dataframe and cosine-similarity matrix
(models/movies.pkl, models/similarity.pkl -- see build_model.py) and
exposes simple lookup/recommend functions consumed by the Streamlit UI.

The recommendation algorithm itself (CountVectorizer tags + cosine
similarity, top-3 cast + director + genres + keywords + overview) is
unchanged from the original notebook.
"""

import pickle

import pandas as pd
import streamlit as st

import config


@st.cache_resource(show_spinner=False)
def load_model():
    """Load the movies metadata dataframe and similarity matrix once per
    server process (cached as a resource, not re-pickled per session)."""
    with open(config.MOVIES_PKL, "rb") as f:
        movies = pickle.load(f)
    with open(config.SIMILARITY_PKL, "rb") as f:
        similarity = pickle.load(f)
    return movies, similarity


def get_movie_list() -> list:
    movies, _ = load_model()
    return sorted(movies["title"].tolist())


def get_movie_row(title: str) -> dict:
    movies, _ = load_model()
    match = movies[movies["title"] == title]
    if match.empty:
        return {}
    return match.iloc[0].to_dict()


def get_movie_row_by_id(movie_id: int) -> dict:
    movies, _ = load_model()
    match = movies[movies["movie_id"] == int(movie_id)]
    if match.empty:
        return {}
    return match.iloc[0].to_dict()


def recommend(movie_title: str, top_n: int = 6) -> list:
    """Return top_n similar movies as a list of dicts, each augmented with
    a 'similarity' float score (0-1), highest first. Excludes the movie
    itself. Matches the original notebook's `recommend()` logic exactly,
    only adding metadata and similarity score to the return value."""
    movies, similarity = load_model()

    matches = movies.index[movies["title"] == movie_title]
    if len(matches) == 0:
        return []
    index = matches[0]

    distances = sorted(
        list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]
    )

    results = []
    for i, score in distances[1: top_n + 1]:
        row = movies.iloc[i].to_dict()
        row["similarity"] = float(score)
        results.append(row)
    return results


def get_trending(top_n: int = 20) -> pd.DataFrame:
    movies, _ = load_model()
    return movies.sort_values("popularity", ascending=False).head(top_n).reset_index(drop=True)


def get_top_rated(top_n: int = 10, min_votes: int = 500) -> pd.DataFrame:
    movies, _ = load_model()
    eligible = movies[movies["vote_count"] >= min_votes]
    return eligible.sort_values("vote_average", ascending=False).head(top_n).reset_index(drop=True)


def search_titles(query: str, limit: int = 8) -> list:
    if not query:
        return []
    movies, _ = load_model()
    query = query.lower().strip()
    mask = movies["title"].str.lower().str.contains(query, na=False)
    return movies.loc[mask, "title"].head(limit).tolist()
