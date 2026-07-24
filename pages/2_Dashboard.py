"""CineMind AI -- Dashboard Page."""

import pandas as pd
import plotly.express as px
import streamlit as st

import components
import config
import recommender

components.setup_page("Dashboard", icon="📈")

st.markdown(
    '<div class="hero-title" style="font-size:2.2rem;">📈 <span class="gradient-text">Dashboard</span></div>',
    unsafe_allow_html=True,
)
st.caption("A quick snapshot of the entire TMDB 5000 catalog.")
st.write("")

movies_df, similarity = recommender.load_model()

# --------------------------------------------------------------------------
# Key metrics
# --------------------------------------------------------------------------
cols = st.columns(5)
with cols[0]:
    components.stat_card(f"{len(movies_df):,}", "Total Movies")
with cols[1]:
    components.stat_card(f"{movies_df['vote_average'].mean():.2f}", "Avg. Rating")
with cols[2]:
    components.stat_card(f"{movies_df['runtime'].mean():.0f} min", "Avg. Runtime")
with cols[3]:
    components.stat_card(f"{movies_df['original_language'].nunique()}", "Languages")
with cols[4]:
    components.stat_card(f"{similarity.shape[0]:,} × {similarity.shape[1]:,}", "Similarity Matrix")

st.write("")

c1, c2 = st.columns(2)
with c1:
    components.section_title("🏆 Top Rated Movies")
    top_rated = recommender.get_top_rated(top_n=8)
    fig = px.bar(
        top_rated.sort_values("vote_average"),
        x="vote_average", y="title", orientation="h",
        color="vote_average", color_continuous_scale=[config.COLORS["primary"], config.COLORS["accent"]],
        template=config.PLOTLY_TEMPLATE, labels={"vote_average": "Rating", "title": ""},
    )
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, height=380)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    components.section_title("🔥 Most Popular Movies")
    trending = recommender.get_trending(top_n=8)
    fig2 = px.bar(
        trending.sort_values("popularity"),
        x="popularity", y="title", orientation="h",
        color="popularity", color_continuous_scale=[config.COLORS["accent"], config.COLORS["primary_soft"]],
        template=config.PLOTLY_TEMPLATE, labels={"popularity": "Popularity", "title": ""},
    )
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False, height=380)
    st.plotly_chart(fig2, use_container_width=True)

st.write("")
components.section_title("📅 Movies Released Per Year")
years = pd.to_datetime(movies_df["release_date"], errors="coerce").dt.year.dropna().astype(int)
year_counts = years.value_counts().sort_index()
fig3 = px.area(
    x=year_counts.index, y=year_counts.values,
    template=config.PLOTLY_TEMPLATE, labels={"x": "Year", "y": "Movies Released"},
)
fig3.update_traces(line_color=config.COLORS["primary"], fillcolor="rgba(99,102,241,0.25)")
fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=340)
st.plotly_chart(fig3, use_container_width=True)

link_cols = st.columns(3)
with link_cols[0]:
    st.link_button("💻 GitHub", "https://github.com/akashgoswami139", use_container_width=True)
with link_cols[1]:
    st.link_button("💼 LinkedIn", "https://www.linkedin.com/in/akashgoswami-/", use_container_width=True)
