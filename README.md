# 🎬 CineMind AI – Movie Recommendation System

CineMind AI is a modern **content-based movie recommendation system** built using **Python**, **Machine Learning**, and **Streamlit**. It recommends movies based on their similarity by analyzing genres, cast, crew, keywords, and movie overviews, while providing an interactive web interface with analytics, trending movies, favorites, and live TMDB integration.

---

## 🚀 Live Demo



---



## ✨ Features

- 🎯 AI-powered content-based movie recommendations
- 🎬 Live movie posters from TMDB API
- ▶️ Watch official movie trailers
- ❤️ Save and manage favorite movies
- 🔥 Browse trending movies
- 📊 Interactive analytics dashboard
- 📈 Dataset insights and visualizations
- 🎨 Modern responsive Streamlit interface
- ⚡ Fast recommendations using precomputed cosine similarity

---

## 🧠 Recommendation Algorithm

The recommendation engine uses **Content-Based Filtering**.

### Workflow

- Movie metadata preprocessing
- Feature engineering using:
  - Genres
  - Keywords
  - Overview
  - Top Cast
  - Director
- Text vectorization using **CountVectorizer**
- Cosine Similarity computation
- Top-N similar movie recommendations

---


### Data Source

- TMDB 5000 Movie Dataset
- TMDB API

---

## 📂 Project Structure

```text
Movie-Recommender/
│
├── assets/
│   └── style.css
│
├── models/
│   ├── movies.pkl
│   └── similarity.pkl
│
├── pages/
│   ├── 1_Recommend.py
│   ├── 2_Dashboard.py
│   ├── 3_Trending.py
│   ├── 4_Favorites.py
│   ├── 5_Analytics.py
│   └── 6_About.py
│
├── .streamlit/
│   └── secrets.toml
│
├── Home.py
├── components.py
├── config.py
├── recommender.py
├── utils.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/your-username/cinemind-ai.git
```

### Navigate to the project

```bash
cd cinemind-ai
```

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### macOS/Linux

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run Home.py
```

---

## 📊 Application Pages

- 🏠 Home
- 🎬 Recommend Movies
- 📈 Dashboard
- 🔥 Trending Movies
- ❤️ Favorites
- 📊 Analytics
- ℹ️ About

---

## 📦 Dependencies

- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Plotly
- Requests

Install them using:

```bash
pip install -r requirements.txt
```

---

## 🌟 Future Improvements

- User Authentication
- Hybrid Recommendation System
- Collaborative Filtering
- Movie Search with Autocomplete
- Watchlist Persistence
- User Ratings
- Personalized Recommendations
- Cloud Database Integration

---

## 👨‍💻 Author

**Akash Goswami**

- GitHub: https://github.com/akashgoswami139
- LinkedIn: https://www.linkedin.com/in/akashgoswami-/

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

It helps others discover the project and motivates further improvements.