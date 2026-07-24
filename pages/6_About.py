"""CineMind AI -- About Page."""

import streamlit as st

import components

components.setup_page("About", icon="ℹ️")

st.markdown(
    '<div class="hero-title" style="font-size:2.2rem;">ℹ️ <span class="gradient-text">About This Project</span></div>',
    unsafe_allow_html=True,
)
st.write("")

st.markdown(
    """
    <div class="glass-card">
    <p style="font-size:1.05rem; color:var(--text-muted);">
    <b>CineMind AI</b> is a content-based movie recommendation system built
    on the TMDB 5000 dataset. It analyzes each movie's overview, genres,
    keywords, top cast, and director to compute similarity between films
    -- then recommends titles most similar to whatever you already love.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")
c1, c2 = st.columns(2)

with c1:
    components.section_title("📦 Dataset")
    st.markdown(
        """
        <div class="glass-card">
        <ul>
            <li><b>TMDB 5000 Movies</b> -- metadata, budgets, genres, ratings</li>
            <li><b>TMDB 5000 Credits</b> -- cast and crew information</li>
            <li>~4,800 movies after cleaning and merging</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    components.section_title("🧠 Algorithm")
    st.markdown(
        """
        <div class="glass-card">
        <ul>
            <li><b>Content-Based Filtering</b> -- no user ratings required</li>
            <li><b>Feature Engineering</b> -- overview + genres + keywords + top-3 cast + director combined into a single "tags" string</li>
            <li><b>NLP</b> -- stemming + <code>CountVectorizer</code> (English stop-words, 6,000 max features)</li>
            <li><b>Cosine Similarity</b> -- measures the angle between movie vectors to rank closest matches</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with c2:
    components.section_title("🛠️ Tech Stack")
    st.markdown(
        """
        <div class="glass-card">
        <ul>
            <li>Python 3</li>
            <li>Pandas &amp; NumPy</li>
            <li>Scikit-learn</li>
            <li>Streamlit</li>
            <li>Plotly</li>
            <li>Requests</li>
            <li>TMDB API</li>
        </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")
    components.section_title("🚀 How Recommendations Work")
    st.markdown(
        """
        <div class="glass-card">
        <ol>
            <li>Select a movie you enjoyed</li>
            <li>Its "tags" vector is compared against every other movie</li>
            <li>The 6 movies with the highest cosine similarity score are returned</li>
            <li>Results are displayed with posters, ratings, and a match percentage</li>
        </ol>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.write("")
components.section_title("👤 Connect")
link_cols = st.columns(3)
with link_cols[0]:
    st.link_button("💻 GitHub", "https://github.com/akashgoswami139", use_container_width=True)
with link_cols[1]:
    st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/akashgoswami-/", use_container_width=True)
