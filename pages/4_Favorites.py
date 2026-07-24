"""CineMind AI -- Favorites Page."""

import streamlit as st

import components
import utils

components.setup_page("Favorites", icon="❤️")

st.markdown(
    '<div class="hero-title" style="font-size:2.2rem;">❤️ <span class="gradient-text">Your Favorites</span></div>',
    unsafe_allow_html=True,
)
st.caption("Movies you've saved during this session. Download the list anytime as CSV.")
st.write("")

favorites = list(st.session_state.get("favorites", {}).values())

top_row = st.columns([3, 1])
with top_row[0]:
    st.write(f"**{len(favorites)}** movie(s) saved.")
with top_row[1]:
    st.download_button(
        "⬇️ Download CSV",
        data=utils.favorites_to_csv_bytes(),
        file_name="my_favorite_movies.csv",
        mime="text/csv",
        use_container_width=True,
        disabled=len(favorites) == 0,
    )

st.write("")

if not favorites:
    st.info("You haven't added any favorites yet. Head to **Recommend** or **Trending** and tap ❤️ on a movie card.")
else:
    components.render_movie_grid(favorites, key_prefix="fav", columns=4)

link_cols = st.columns(3)
with link_cols[0]:
    st.link_button("💻 GitHub", "https://github.com/akashgoswami139", use_container_width=True)
with link_cols[1]:
    st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/akashgoswami-/", use_container_width=True)
