import pickle
import streamlit as st
import httpx
similarity = pickle.load(open('model\Similarity.pkl','rb'))
df = pickle.load(open('model\movies.pkl','rb'))

# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a45bb52f0053a49487d63049745b0619&language=en-US"
    
#     with httpx.Client(timeout=100) as client:
#         response = client.get(url)
#         data = response.json()
    
#     st.write(data)  # Print JSON response in Streamlit
#     return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"


def recommend(movie):
    if movie not in df['title'].values:
        print(f"❌ Error: '{movie}' not found in dataset!")
        return [], []  # Return empty lists to prevent crashing

    movie_index = df[df['title'] == movie].index[0]
    distances = similarity[movie_index]
    top_movi_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recomeded_movie = []
    # recommended_movie_poster = []

    for i in top_movi_list:
        movie_id = df.iloc[i[0]].id
        # recommended_movie_poster.append(fetch_poster(movie_id))
        recomeded_movie.append(df.iloc[i[0]].title)
    return recomeded_movie





movies_list = df['title'].values

st.title("Movie Recommender System")

movie_name = st.selectbox(
    'Search a Movie',movies_list
)

if st.button('Submit'):
    names = recommend(movie_name)
    for name in names:
        st.subheader(name)