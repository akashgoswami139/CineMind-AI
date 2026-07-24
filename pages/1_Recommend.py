"""CineMind AI -- Recommendation Page."""

import time

import streamlit as st

import components
import recommender

components.setup_page("Recommend", icon="🎬")

st.markdown(
    '<div class="hero-title" style="font-size:2.2rem;">🎬 Find Your Next '
    '<span class="gradient-text">Favorite Movie</span></div>',
    unsafe_allow_html=True,
)
st.caption("Pick a movie you already love -- our AI will find 6 similar titles instantly.")
st.write("")

all_titles = recommender.get_movie_list()
default_index = None
if st.session_state.get("preselected_movie") in all_titles:
    default_index = all_titles.index(st.session_state.pop("preselected_movie"))

col_search, col_btn = st.columns([4, 1])
with col_search:
    movie = st.selectbox(
        "Choose a movie",
        options=all_titles,
        index=default_index,
        placeholder="Type to search... e.g. The Dark Knight",
        label_visibility="collapsed",
    )
with col_btn:
    recommend_clicked = st.button("🔮 Recommend", type="primary", use_container_width=True)

if recommend_clicked and not movie:
    st.warning("Please select a movie first.")

if recommend_clicked and movie:
    progress = st.progress(0, text="Analyzing your movie's DNA...")
    stages = [
        (25, "Extracting genres & keywords..."),
        (55, "Comparing cast & crew..."),
        (80, "Computing cosine similarity..."),
        (100, "Finalizing recommendations..."),
    ]
    for pct, msg in stages:
        time.sleep(0.15)
        progress.progress(pct, text=msg)
    time.sleep(0.1)
    progress.empty()

    st.session_state["last_recommend_source"] = movie
    st.session_state["last_recommendations"] = recommender.recommend(movie, top_n=6)

source_movie = st.session_state.get("last_recommend_source")
results = st.session_state.get("last_recommendations")

if source_movie and results:
    components.section_title(f'🎯 Because you liked "{source_movie}"')

    with st.expander(f"📋 About {source_movie}", expanded=False):
        components.render_movie_details(recommender.get_movie_row(source_movie))

    st.write("")
    components.render_movie_grid(results, key_prefix="rec", columns=3, show_similarity=True)
elif not recommend_clicked:
    st.info("👆 Select a movie above and click **Recommend** to get started.")

link_cols = st.columns(3)
with link_cols[0]:
    st.link_button("💻 GitHub", "https://github.com/akashgoswami139", use_container_width=True)
with link_cols[1]:
    st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/akashgoswami-/", use_container_width=True)
