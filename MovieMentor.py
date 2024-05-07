import pickle
import streamlit as st
import requests
from PIL import Image
import time
from datetime import datetime
from streamlit_lottie import st_lottie
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np
import os
import re

# Function to load the Lottie animation
@st.cache_data()
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Function to fetch movie details
@st.cache_data()
def fetch_movie_details(movie_id, poster_size="w342"):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/{poster_size}/{poster_path}"
    homepage = data['homepage']
    overview = data['overview']
    release_date = data['release_date']
    vote_average = data['vote_average']
    genres = [genre['name'] for genre in data['genres']]
    return full_path, homepage, overview, release_date, vote_average, genres

# Function to recommend movies
@st.cache_data()
def recommend(movie, num_recommendations):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_homepages = []
    recommended_movie_overviews = []
    recommended_movie_release_dates = []
    recommended_movie_ratings = []
    recommended_movie_genres = []
    for i in distances[1:num_recommendations+1]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, homepage, overview, release_date, rating, genres = fetch_movie_details(movie_id)
        recommended_movie_posters.append(poster)
        recommended_movie_homepages.append(homepage)
        recommended_movie_overviews.append(overview)
        recommended_movie_release_dates.append(release_date)
        recommended_movie_ratings.append(rating)
        recommended_movie_genres.append(', '.join(genres))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters, recommended_movie_homepages, recommended_movie_overviews, recommended_movie_release_dates, recommended_movie_ratings, recommended_movie_genres

# Load the movie data and similarity matrix
movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))

# Set the page config
img = Image.open('movies-80.png')
st.set_page_config(page_title='MovieMentor', page_icon=img, layout='wide')

# Load the Lottie animation
lottie_url = "https://lottie.host/746464d7-dc9a-4491-93d7-bb856aad2b46/QDKHgTViiZ.json"
lottie_json = load_lottieurl(lottie_url)

# Apply custom CSS
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700&family=Poppins:wght@400;700&family=Roboto+Slab:wght@400;700&display=swap');

    body {
        background-color: #000000;
        font-family: 'Montserrat', sans-serif;
        color: #fff;
    }
    .movie-recommendation {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        grid-gap: 20px;
    }
    .movie-card {
        display: flex;
        flex-direction: row;
        margin-top: 40px;
        margin-bottom: 20px;
        align-items: center;
        text-align: left;
        background-color: rgba(0, 0, 0, 0.6);
        padding: 10px;
        border-radius: 30px;
        transition: transform 0.4s ease, box-shadow 0.5s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .movie-card:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    .movie-poster {
        width: 300px;
        height: 400px;
        object-fit: cover;
        border-radius: 35px;
        transition: transform 0.4s ease;
    }
    .movie-poster:hover {
        transform: scale(1.1);
    }
    .movie-details-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
        margin-left: 40px;
        width: 100%;
        
    }
    .movie-details-container h1 {
        margin-top: 0;
        font-size: 35px;
        font-weight: bold;
        font-family: 'Roboto Slab', serif;
    }
    .movie-details {
        margin-top: 5px;
        font-size: 14px;
        color: #ccc;
        font-family: 'Montserrat', sans-serif;
        margin-bottom: 25px;
    }
    .movie-details a {
        color: #e50914;
        text-decoration: none;
    }
    .app-title {
        text-align: center;
        margin-bottom: 20px;
        margin-top: 0px;
        grid-gap: 0px;
        padding-top: 0px;
    }
    .app-title h1 {
        font-size: 80px;
        font-weight: 700;
        color: #e50914;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
        font-family: 'Montserrat', sans-serif;
    }
    .app-title h4 {
        font-size: 28px;
        color: #fff;
        font-family: 'Roboto Slab', serif;
    }
    .sub-title {
        text-align: center;
        margin-bottom: 40px;
        margin-top: 0px;
        grid-gap: 0px;
    }
    .sub-title h3 {
        font-size: 36px;
        color: #ccc;
         font-family: 'Roboto Slab', serif;
    }
    .recommendation-button {
        display: block;
        margin: 0 auto;
        padding: 20px 40px;
        font-size: 24px;
        background-color: #e50914;
        color: #fff;
        border: none;
        border-radius: 30px;
        cursor: pointer;
        transition: background-color 0.5s ease, transform 0.5s ease, box-shadow 0.5s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        font-family: 'Poppins', sans-serif;
        text-align: center;
    }
    
    .recommendation-button:hover {
        background-color: #b81d24;
        transform: scale(1.1);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    .loader {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #e50914;
        border-radius: 50%;
        width: 30px;
        height: 30px;
        animation: spin 2s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the app title
st.write(
    f"""
    <div class="app-title">
    <h1>MovieMentor</h1><h4>Movie Recommender Application</h4>
</div>
    """,
    unsafe_allow_html=True
)

# Check if the Lottie animation loaded successfully
if lottie_json:
    st_lottie(lottie_json, height=500, key="animation")
else:
    st.warning("Failed to load the animation.")

st.write(
    f"""
    <div class="sub-title">
        <h3>Discover your next favorite movie 🙂</h3>
    </div>
    """,
    unsafe_allow_html=True
)

# Add the movie selection dropdown
movie_list = pickle.load(open('model/movie_list.pkl', 'rb'))['title'].values
selected_movie = st.selectbox(
    "Enter or Select a movie based on your preferences from the menu below:",
    movie_list
)

# Add the slider to select the number of recommendations
num_recommendations = st.slider("Select the number of movie recommendations (5-20):", 5, 20, 7)

# Add the "Show Recommendation" button
if st.button('Show Recommendation', key='recommendation_button', help='Click to show recommendations', use_container_width=True):
    with st.spinner('Loading recommendations...'):
        recommended_movie_names, recommended_movie_posters, recommended_movie_homepages, recommended_movie_overviews, recommended_movie_release_dates, recommended_movie_ratings, recommended_movie_genres = recommend(selected_movie, num_recommendations)
    with st.container():
        st.write(
            f"""
            <div class="movie-recommendation">
            """,
            unsafe_allow_html=True
        )
        for movie_name, movie_poster, movie_homepage, movie_overview, movie_release_date, movie_rating, movie_genres in zip(recommended_movie_names, recommended_movie_posters, recommended_movie_homepages, recommended_movie_overviews, recommended_movie_release_dates, recommended_movie_ratings, recommended_movie_genres):
            if movie_homepage and re.match(r'^https?://', movie_homepage):
                st.write(
                    f"""
                    <div class="movie-card">
                        <a href="{movie_homepage}" target="_blank"><img class="movie-poster" src="{movie_poster}" alt="{movie_name}"></a>
                        <div class="movie-details-container">
                            <h3>{movie_name}</h3>
                            <div class="movie-details">   
                                <p><b>Release Date:</b> {movie_release_date}</p>
                                <p><b>Rating:</b>  {movie_rating}/10</p>
                                <p><b>Overview:</b> {movie_overview[:100]}...</p>
                                <p><b>Genres:</b> {movie_genres}</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.write(
                    f"""
                    <div class="movie-card">
                        <img class="movie-poster" src="{movie_poster}" alt="{movie_name}">
                        <div class="movie-details-container">
                            <h1>{movie_name}</h1>
                            <div class="movie-details">   
                                <p><b>Release Date:</b> {movie_release_date}</p>
                                <p><b>Rating:</b>  {movie_rating}/10</p>
                                <p><b>Overview:</b> {movie_overview[:100]}...</p>
                                <p><b>Genres:</b> {movie_genres}</p>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        st.write(
            """
            </div>
            """,
            unsafe_allow_html=True
        )

# Generate and display the word cloud
if 'recommended_movie_overviews' in locals():
    all_overviews = ' '.join(recommended_movie_overviews)
    wordcloud = WordCloud(background_color='black', max_words=100, collocations=False).generate(all_overviews)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.set_axis_off()
    st.pyplot(fig)
else:
    st.warning("Please select a movie and click 'Show Recommendation' to generate the word cloud.")

# Add the footer
st.write(
    f"""
    <div style="text-align:center; margin-top: 50px;">
        <br><br>
        <p style='font-size: 20px;'>Made With <span style='color: #e50914;'>&#10084;</span> by <br><code style='font-size: 24px;'><b> Subhransu Priyaranjan Nayak </b></code> </br></p>
        <br><br>
        <p style='font-size: 20px;'>For any inquiries or feedback, please feel free to contact me <a href="https://www.linkedin.com/in/subhransu-p-nayak" target="_blank">Here</a> !</p>
    </div>
    """,
    unsafe_allow_html=True
)