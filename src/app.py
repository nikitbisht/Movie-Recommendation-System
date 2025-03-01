import pickle
import streamlit as st
import requests
similarity = pickle.load(open('model\Similarity.pkl','rb'))
df = pickle.load(open('model\movies.pkl','rb'))

def fetch_poster(movie_name,movie_id):
    url = f"https://www.omdbapi.com/?t={movie_name}&apikey=e5e9da27"
    response = requests.get(url)
    data = response.json()
    return data['Poster']


def recommend(movie):
    if movie not in df['title'].values:
        print(f"❌ Error: '{movie}' not found in dataset!")
        return [], []  # Return empty lists to prevent crashing

    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_movi_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recomeded_movie = []
    recommended_movie_poster = []

    for i in top_movi_list:
        movie_id = df.iloc[i[0]].id
        movie_name = df.iloc[i[0]].title
        recommended_movie_poster.append(fetch_poster(movie_name,movie_id))
        recomeded_movie.append(df.iloc[i[0]].title)
    return recomeded_movie , recommended_movie_poster





movies_list = df['title'].values

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Search a Movie',movies_list
)

if st.button('Submit'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])