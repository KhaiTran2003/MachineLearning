import pickle
import streamlit as st
import requests
import pandas as pd

st.header('Hệ Thống Gợi Ý Phim')

# Tải dữ liệu phim và ma trận tương đồng
try:
    movies = pickle.load(open('movie_dict.pkl', 'rb'))
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(f"Không tìm thấy tệp: {e.filename}")
    st.stop()

# Kiểm tra xem movies có phải là DataFrame không và chuyển đổi nếu cần thiết
if isinstance(movies, dict):
    # Chuyển đổi dictionary thành DataFrame
    movies = pd.DataFrame(movies)
elif not isinstance(movies, pd.DataFrame):
    st.error("Dữ liệu phim không phải là một DataFrame.")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Nhập hoặc chọn một bộ phim từ danh sách",
    movie_list
)

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=vi-VN".format(movie_id)
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except requests.RequestException as e:
        st.error(f"Lỗi khi tải poster: {e}")
        return "https://via.placeholder.com/500x750?text=No+Image+Available"

def recommend(movie):
    try:
        index = movies[movies['title'] == movie].index[0]
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
        recommended_movie_names = []
        recommended_movie_posters = []
        for i in distances[1:6]:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movie_posters.append(fetch_poster(movie_id))
            recommended_movie_names.append(movies.iloc[i[0]].title)
        return recommended_movie_names, recommended_movie_posters
    except IndexError:
        st.error(f"Bộ phim '{movie}' không tìm thấy trong tập dữ liệu.")
        return [], []

if st.button('Hiển Thị Gợi Ý'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    if recommended_movie_names:
        cols = st.columns(5)
        for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
            with col:
                st.text(name)
                st.image(poster)
