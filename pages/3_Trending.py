"""CineMind AI -- Trending Page."""

import streamlit as st

import components
import recommender

components.setup_page("Trending", icon="🔥")

st.markdown(
    '<div class="hero-title" style="font-size:2.2rem;">🔥 <span class="gradient-text">Trending Now</span></div>',
    unsafe_allow_html=True,
)
st.caption("The 20 most popular movies in the TMDB 5000 catalog, ranked by popularity score.")
st.write("")

sort_by = st.radio(
    "Sort by", ["Popularity", "Rating", "Release Date"], horizontal=True, label_visibility="collapsed"
)

trending = recommender.get_trending(top_n=20)
if sort_by == "Rating":
    trending = trending.sort_values("vote_average", ascending=False).reset_index(drop=True)
elif sort_by == "Release Date":
    trending = trending.sort_values("release_date", ascending=False).reset_index(drop=True)

st.write("")
rows = trending.to_dict("records")
components.render_movie_grid(rows, key_prefix="trend", columns=4)

link_cols = st.columns(3)
with link_cols[0]:
    st.link_button("💻 GitHub", "https://github.com/akashgoswami139", use_container_width=True)
with link_cols[1]:
    st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/akashgoswami-/", use_container_width=True)
