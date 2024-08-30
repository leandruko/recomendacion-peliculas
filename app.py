import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
import streamlit as st
import gc
import psutil

# Función para limitar el uso de memoria ya que mi pc no tiene mucha ram
def limit_memory(max_mem_percent=80):
    max_mem = psutil.virtual_memory().total * (max_mem_percent / 100)
    if psutil.virtual_memory().used > max_mem:
        gc.collect()
        raise MemoryError(f"El uso de memoria excedió el {max_mem_percent}% del total disponible")

# Cargar los datos  de manera mas optima
@st.cache_data
def load_data(nrows=100000):
    ratings = pd.read_csv('ratings.csv', nrows=nrows, dtype={'userId': 'int32', 'movieId': 'int32', 'rating': 'float32'})
    movies = pd.read_csv('movies.csv', dtype={'movieId': 'int32', 'title': 'str', 'genres': 'str'})
    return ratings, movies

# Crear una matriz de películas-usuarios más eficiente
def create_matrix(df, n_movies=1000, n_users=1000):
    top_movies = df['movieId'].value_counts().nlargest(n_movies).index
    top_users = df['userId'].value_counts().nlargest(n_users).index
    
    df_filtered = df[df['movieId'].isin(top_movies) & df['userId'].isin(top_users)]
    
    user_mapper = dict(zip(np.unique(df_filtered["userId"]), list(range(len(top_users)))))
    movie_mapper = dict(zip(np.unique(df_filtered["movieId"]), list(range(len(top_movies)))))
    
    user_inv_mapper = {v: k for k, v in user_mapper.items()}
    movie_inv_mapper = {v: k for k, v in movie_mapper.items()}
    
    user_index = [user_mapper[i] for i in df_filtered['userId']]
    movie_index = [movie_mapper[i] for i in df_filtered['movieId']]
    
    X = csr_matrix((df_filtered["rating"], (movie_index, user_index)), shape=(len(top_movies), len(top_users)))
    
    return X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper

def find_similar_movies(movie_id, X, k, metric='cosine'):
    limit_memory()  # Verificar uso de memoria
    neighbour_ids = []
    movie_ind = movie_mapper.get(movie_id)
    if movie_ind is None:
        return []
    movie_vec = X[movie_ind]
    if metric == 'cosine':
        similarities = cosine_similarity(movie_vec, X).flatten()
    else:
        raise ValueError("Metric not understood")
    
    similar_indices = np.argsort(similarities)[::-1][1:k+1]
    similar_items = [(movie_inv_mapper[i], similarities[i]) for i in similar_indices if i in movie_inv_mapper]
    return similar_items

def get_movie_recommendations(movie_id, n_recommendations):
    limit_memory()  # Verificar uso de memoria
    similar_movies = find_similar_movies(movie_id, X, n_recommendations)
    recommended_movie_ids = [movie_id for movie_id, _ in similar_movies]
    recommended_movies = movies[movies['movieId'].isin(recommended_movie_ids)]
    return recommended_movies[['title', 'genres']]

# Cargar datos
ratings, movies = load_data()

# Crear matriz
X, user_mapper, movie_mapper, user_inv_mapper, movie_inv_mapper = create_matrix(ratings)

# Interfaz 
st.title('Sistema de Recomendación de Películas')

movie_list = movies['title'].tolist()
selected_movie = st.selectbox('Selecciona una película:', movie_list)

if st.button('Obtener Recomendaciones'):
    try:
        selected_movie_id = movies[movies['title'] == selected_movie]['movieId'].values[0]
        recommendations = get_movie_recommendations(selected_movie_id, 5)
        st.write(f"Recomendaciones basadas en '{selected_movie}':")
        st.table(recommendations)
    except MemoryError:
        st.error("Se ha excedido el límite de memoria. Por favor, intenta con menos datos o aumenta el límite de memoria.")
    except Exception as e:
        st.error(f"Ocurrió un error: {str(e)}")

# Para ejecutar: streamlit run app.py
