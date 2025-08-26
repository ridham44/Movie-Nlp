import streamlit as st

def display_movie_card(movie):
    """
    Display movie card with poster and details.
    """
    col1, col2 = st.columns([1, 3])
    with col1:
        st.image(movie.get("poster_url", "https://via.placeholder.com/200x300?text=No+Poster"), use_column_width=True)
    with col2:
        st.subheader(movie.get("title", "Unknown"))
        st.write(f"⭐ Rating: {movie.get('vote_average', 'N/A')}")
        st.write(f"📅 Release: {movie.get('release_date', 'N/A')}")
        st.write(f"🎭 Genres: {movie.get('genres', 'N/A')}")
        st.markdown("---")
