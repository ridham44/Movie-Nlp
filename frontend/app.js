const API_URL = 'http://127.0.0.1:5000/recommend';
const FALLBACK_POSTER = 'Default.png';

document.getElementById('goBtn').addEventListener('click', () => {
    const type = window.searchType; // ✅ switch selection
    const query = document.getElementById('userInput').value.trim();

    if (!query) {
        alert('⚠️ Please enter something!');
        return;
    }

    fetchMovies(type, query);
});

async function fetchMovies(type, query) {
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type, query }),
        });

        if (!response.ok) throw new Error('API request failed');

        const data = await response.json();

        // Show mood separately
        const moodRow = document.getElementById('moodRow');
        if (data.mood) {
            moodRow.innerHTML = `<h3 style="color:cyan; text-align:center;">🎭 Detected Mood: ${data.mood}</h3>`;
        } else {
            moodRow.innerHTML = '';
        }

        displayMovies(data.movies);
    } catch (error) {
        console.error('🚨 Error calling API:', error);
        document.getElementById('movieGrid').innerHTML = `<p style="color:red;">⚠️ Failed to load movies.</p>`;
    }
}
function displayMovies(movies) {
  const container = document.getElementById("movieGrid");

  // ✅ Keep only the first row (mood row) and clear the rest
  const moodRow = container.firstElementChild;  
  container.innerHTML = "";  
  if (moodRow) container.appendChild(moodRow);

  if (!movies || movies.length === 0) {
    container.innerHTML += "<p>No movies found.</p>";
    return;
  }

  movies.forEach(movie => {
    const card = document.createElement("div");
    card.classList.add("movie-card");

    let poster = movie.poster_url;
    if (!poster || poster.trim() === "" || poster === "N/A") {
      poster = FALLBACK_POSTER;
    }

    card.innerHTML = `
      <img src="${poster}" alt="${movie.title || 'Poster'}"
           onerror="this.onerror=null; this.src='${FALLBACK_POSTER}';">
      <h3 class="movie-title">${movie.title || 'N/A'}</h3>

      <div class="movie-info">
        <div class="info-line">
          <div class="emoji">📅</div>
          <div class="text">${movie.release_date || 'N/A'}</div>
        </div>

        <div class="info-line">
          <div class="emoji">🎭</div>
          <div class="text">${movie.genres || 'N/A'}</div>
        </div>

        <div class="info-line">
          <div class="emoji">⭐</div>
          <div class="text">${movie.overview ?? 'N/A'}</div>
        </div>
      </div>
    `;

    container.appendChild(card);
  });
}
