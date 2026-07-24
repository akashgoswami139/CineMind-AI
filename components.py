"""
Reusable UI components shared across every page: page setup, sidebar
branding, footer, movie card grid, and small stat widgets.
"""

import streamlit as st

import config
import utils


def setup_page(title: str, icon: str = "🎬"):
    st.set_page_config(
        page_title=f"{title} · {config.APP_NAME}",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded",
    )
    utils.init_session_state()
    _inject_css()
    _render_sidebar_branding()


def _inject_css():
    try:
        with open(config.STYLE_CSS, "r", encoding="utf-8") as f:
            css = f.read()
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Stylesheet not found -- run the app from the project root.")


def _render_sidebar_branding():
    with st.sidebar:
        st.markdown(
            f"""
            <div style="text-align:center; padding: 6px 0 18px 0;">
                <div style="font-size:2.4rem; line-height:1;">🎬</div>
                <div style="font-family:'Poppins',sans-serif; font-weight:800;
                            font-size:1.3rem; margin-top:4px;"
                     class="gradient-text">{config.APP_NAME}</div>
                <div style="color:var(--text-muted); font-size:0.75rem;">Movie AI</div>
            </div>
            <hr style="border-color: var(--card-border); margin-bottom: 18px;">
            """,
            unsafe_allow_html=True,
        )




def section_title(text: str):
    st.markdown(
        f'<div class="section-title"><div class="bar"></div>{text}</div>',
        unsafe_allow_html=True,
    )


def stat_card(number: str, label: str):
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">{number}</div>
            <div class="stat-label">{label}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def genre_badges(genres, limit=3):
    genres = genres or []
    return "".join(f'<span class="badge badge-genre">{g}</span>' for g in genres[:limit])


def render_movie_card(row: dict, key_prefix: str, show_similarity: bool = False):
    """Render a single movie card with poster, badges, and action buttons."""
    poster = utils.get_poster(row["movie_id"])
    year = utils.format_year(row.get("release_date"))
    rating = row.get("vote_average", 0) or 0
    movie_id = int(row["movie_id"])

    st.markdown('<div class="movie-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="movie-poster-wrap"><img src="{poster}" /></div>',
        unsafe_allow_html=True,
    )
    st.markdown(f'<div class="movie-title" title="{row["title"]}">{row["title"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="movie-meta">{year} &middot; {utils.language_name(row.get("original_language"))}</div>', unsafe_allow_html=True)

    badges = f'<span class="badge badge-rating">⭐ {rating:.1f}</span>'
    if show_similarity and "similarity" in row:
        badges += f'<span class="badge badge-similarity">🎯 {utils.similarity_pct(row["similarity"])} match</span>'
    badges += genre_badges(row.get("genres"))
    st.markdown(badges, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        with st.popover("📋 Details", use_container_width=True):
            render_movie_details(row)
    with c2:
        trailer_url = utils.get_trailer(movie_id)
        if trailer_url:
            st.link_button("▶ Trailer", trailer_url, use_container_width=True)
        else:
            st.button("▶ Trailer", key=f"{key_prefix}_no_trailer_{movie_id}", disabled=True, use_container_width=True)

    fav = utils.is_favorite(movie_id)
    fav_label = "💔 Remove Favorite" if fav else "❤️ Add Favorite"
    if st.button(fav_label, key=f"{key_prefix}_fav_{movie_id}", use_container_width=True):
        if fav:
            utils.remove_favorite(movie_id)
        else:
            utils.add_favorite(row)
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def render_movie_details(row: dict):
    st.markdown(f"#### {row['title']}")
    if row.get("tagline"):
        st.caption(f"_{row['tagline']}_")
    st.write(row.get("overview", "No overview available."))
    st.divider()
    d1, d2 = st.columns(2)
    with d1:
        st.markdown(f"**Genres:** {', '.join(row.get('genres') or []) or 'N/A'}")
        st.markdown(f"**Runtime:** {utils.format_runtime(row.get('runtime'))}")
        st.markdown(f"**Release Date:** {utils.format_date(row.get('release_date'))}")
        st.markdown(f"**Vote Average:** {row.get('vote_average', 'N/A')} / 10")
        st.markdown(f"**Vote Count:** {int(row.get('vote_count') or 0):,}")
    with d2:
        st.markdown(f"**Popularity:** {round(row.get('popularity') or 0, 1)}")
        st.markdown(f"**Original Language:** {utils.language_name(row.get('original_language'))}")
        st.markdown(f"**Director:** {', '.join(row.get('director') or []) or 'N/A'}")
        st.markdown(f"**Budget:** {utils.format_currency(row.get('budget'))}")
        st.markdown(f"**Revenue:** {utils.format_currency(row.get('revenue'))}")
    companies = row.get("production_companies") or []
    if companies:
        st.markdown(f"**Production Companies:** {', '.join(companies[:5])}")
    cast = row.get("cast") or []
    if cast:
        st.markdown(f"**Cast:** {', '.join(cast)}")


def render_movie_grid(rows, key_prefix: str, columns: int = 4, show_similarity: bool = False):
    cols = st.columns(columns)
    for i, row in enumerate(rows):
        with cols[i % columns]:
            render_movie_card(row, key_prefix=f"{key_prefix}_{i}", show_similarity=show_similarity)
