"""
CineMind AI -- Home / Landing Page
Entry point of the Streamlit multipage app (streamlit run .py).
"""

import streamlit as st

import components
import config
import recommender
import utils

components.setup_page("Home", icon="🎬")

# --------------------------------------------------------------------------
# Sidebar menu (Streamlit auto-lists the pages/ folder below; we add a
# quick-jump shortcut plus a live snapshot).
# --------------------------------------------------------------------------
with st.sidebar:
    st.page_link("Home.py", label="🏠 Home")
    st.page_link("pages/1_Recommend.py", label="🎬 Recommend")
    st.page_link("pages/2_Dashboard.py", label="📈 Dashboard")
    st.page_link("pages/3_Trending.py", label="🔥 Trending")
    st.page_link("pages/4_Favorites.py", label="❤️ Favorites")
    st.page_link("pages/5_Analytics.py", label="📊 Analytics")
    st.page_link("pages/6_About.py", label="ℹ️ About")
    st.markdown("<hr style='border-color: var(--card-border);'>", unsafe_allow_html=True)
    st.caption(f"❤️ {len(st.session_state.get('favorites', {}))} favorites saved")

movies_df, _ = recommender.load_model()

# --------------------------------------------------------------------------
# Hero section
# --------------------------------------------------------------------------
st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="hero-title">🎬 <span class="gradient-text">AI Movie Recommendation System</span></div>
        <div class="hero-subtitle">{config.APP_TAGLINE}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
search_col, btn_col = st.columns([4, 1])
with search_col:
    selected_movie = st.selectbox(
        "Search a movie you love",
        options=movies_df["title"].sort_values().tolist(),
        index=None,
        placeholder="Start typing a movie title... e.g. Avatar",
        label_visibility="collapsed",
    )
with btn_col:
    go = st.button("✨ Recommend Movies", use_container_width=True, type="primary")

if go:
    if selected_movie:
        st.session_state["preselected_movie"] = selected_movie
        st.switch_page("pages/1_Recommend.py")
    else:
        st.warning("Pick a movie first, then hit Recommend.")

st.write("")

# --------------------------------------------------------------------------
# Poster slider (a curated row of popular posters)
# --------------------------------------------------------------------------
components.section_title("🎞️ Trending Right Now")
top_posters = movies_df.sort_values("popularity", ascending=False).head(10)
poster_cols = st.columns(10)
for i, (_, row) in enumerate(top_posters.iterrows()):
    with poster_cols[i]:
        st.image(utils.get_poster(row["movie_id"]), use_container_width=True)

st.write("")

# --------------------------------------------------------------------------
# Statistics section
# --------------------------------------------------------------------------
components.section_title("⚡ Powered By")
stat_cols = st.columns(6)
stats = [
    (f"{len(movies_df):,}", "Movies"),
    ("Content-Based", "Recommendation"),
    ("Cosine", "Similarity"),
    ("Machine", "Learning"),
    ("Python", "Language"),
    ("Streamlit", "Framework"),
]
for col, (num, label) in zip(stat_cols, stats):
    with col:
        components.stat_card(num, label)

st.write("")
components.section_title("💡 How It Works")
how_cols = st.columns(3)
how_steps = [
    ("1️⃣ Pick a Movie", "Choose any title you enjoyed from our library of 4,800+ films."),
    ("2️⃣ AI Finds Matches", "We compare genres, cast, crew, keywords, and plot using cosine similarity."),
    ("3️⃣ Get Recommendations", "Instantly see the top 6 most similar movies with posters and match scores."),
]
for col, (title, desc) in zip(how_cols, how_steps):
    with col:
        st.markdown(
            f'<div class="glass-card"><h4>{title}</h4><p style="color:var(--text-muted);">{desc}</p></div>',
            unsafe_allow_html=True,
        )

link_cols = st.columns(3)
with link_cols[0]:
    st.link_button("💻 GitHub", "https://github.com/akashgoswami139", use_container_width=True)
with link_cols[1]:
    st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/akashgoswami-/", use_container_width=True)
