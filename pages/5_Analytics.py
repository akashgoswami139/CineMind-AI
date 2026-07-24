"""CineMind AI -- Analytics Page."""

import pandas as pd
import plotly.express as px
import streamlit as st

import components
import config
import recommender

components.setup_page("Analytics", icon="📊")

st.markdown(
    '<div class="hero-title" style="font-size:2.2rem;">📊 <span class="gradient-text">Analytics</span></div>',
    unsafe_allow_html=True,
)
st.caption("Explore patterns across the entire TMDB 5000 dataset.")
st.write("")

movies_df, _ = recommender.load_model()

# --------------------------------------------------------------------------
# Filters
# --------------------------------------------------------------------------
with st.expander("🔍 Filters", expanded=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        all_genres = sorted({g for genres in movies_df["genres"] for g in genres})
        genre_filter = st.multiselect("Genre", all_genres)
    with f2:
        years = pd.to_datetime(movies_df["release_date"], errors="coerce").dt.year.dropna()
        year_range = st.slider(
            "Release Year", int(years.min()), int(years.max()),
            (int(years.min()), int(years.max())),
        )
    with f3:
        min_rating = st.slider("Minimum Rating", 0.0, 10.0, 0.0, 0.5)

df = movies_df.copy()
df["year"] = pd.to_datetime(df["release_date"], errors="coerce").dt.year
df = df[df["year"].between(*year_range, inclusive="both") | df["year"].isna()]
df = df[df["vote_average"] >= min_rating]
if genre_filter:
    df = df[df["genres"].apply(lambda g: any(x in g for x in genre_filter))]

st.caption(f"Showing analytics for **{len(df):,}** movies matching your filters.")
st.write("")

c1, c2 = st.columns(2)
with c1:
    components.section_title("🎭 Top Genres")
    genre_counts = pd.Series([g for genres in df["genres"] for g in genres]).value_counts().head(12)
    fig = px.bar(
        x=genre_counts.values, y=genre_counts.index, orientation="h",
        template=config.PLOTLY_TEMPLATE, labels={"x": "Movies", "y": ""},
        color=genre_counts.values, color_continuous_scale=[config.COLORS["primary"], config.COLORS["accent"]],
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, height=420)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    components.section_title("🌐 Movie Languages")
    lang_counts = df["original_language"].value_counts().head(10)
    fig2 = px.pie(
        values=lang_counts.values, names=lang_counts.index, hole=0.55,
        template=config.PLOTLY_TEMPLATE, color_discrete_sequence=config.PLOTLY_COLORWAY,
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=420)
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)
with c3:
    components.section_title("📈 Popularity Distribution")
    fig3 = px.histogram(
        df, x="popularity", nbins=40, template=config.PLOTLY_TEMPLATE,
        color_discrete_sequence=[config.COLORS["primary"]],
    )
    fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380)
    st.plotly_chart(fig3, use_container_width=True)

with c4:
    components.section_title("🗳️ Vote Distribution")
    fig4 = px.histogram(
        df, x="vote_average", nbins=30, template=config.PLOTLY_TEMPLATE,
        color_discrete_sequence=[config.COLORS["accent"]],
    )
    fig4.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380)
    st.plotly_chart(fig4, use_container_width=True)

components.section_title("📅 Movies by Year")
year_counts = df["year"].dropna().astype(int).value_counts().sort_index()
fig5 = px.line(
    x=year_counts.index, y=year_counts.values, markers=True,
    template=config.PLOTLY_TEMPLATE, labels={"x": "Year", "y": "Movies Released"},
)
fig5.update_traces(line_color=config.COLORS["primary_soft"])
fig5.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=360)
st.plotly_chart(fig5, use_container_width=True)

components.section_title("🏆 Top Rated Movies (Filtered)")
top_rated = df[df["vote_count"] >= 100].sort_values("vote_average", ascending=False).head(10)
fig6 = px.bar(
    top_rated.sort_values("vote_average"), x="vote_average", y="title", orientation="h",
    template=config.PLOTLY_TEMPLATE, labels={"vote_average": "Rating", "title": ""},
    color="vote_average", color_continuous_scale=[config.COLORS["success"], config.COLORS["accent"]],
)
fig6.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, height=420)
st.plotly_chart(fig6, use_container_width=True)

link_cols = st.columns(3)
with link_cols[0]:
    st.link_button("💻 GitHub", "https://github.com/akashgoswami139", use_container_width=True)
with link_cols[1]:
    st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/akashgoswami-/", use_container_width=True)
