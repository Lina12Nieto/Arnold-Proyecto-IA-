from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse

import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


nltk.data.path.append("/app/nltk_data")
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('punkt_tab')

def load_movies():
    df = pd.read_csv('DataSet/netflix_titles.csv')[['show_id', 'title', 'release_year','listed_in','rating', 'description']]

    df.columns = ['id', 'title', 'year', 'category', 'rating', 'description']

    return df.fillna('').to_dict(orient='records')

movies_list = load_movies()

def get_synonyms(word):
    return[lemma.name().lower() for syn in wordnet.synsets(word) for lemma in syn.lemmas()]

app = FastAPI(title = 'Mi aplicación de Peliculas', version  = "1.0.0")

@app.get('/', tags = ['Home'])
def home():
    return HTMLResponse(content = '<h1>Bienvenido a mi aplicación de Peliculas</h1>')

@app.get('/movies', tags = ['Movies'])
def get_movies():
    return movies_list or HTTPException(status_code=500, detail="No se encontraron peliculas")

@app.get('/movies/{id}', tags = ['Movies'])
def get_movie(id: int):
    
    return next((m for m in movies_list if m['id'] == id) , {"detalle":"Pelicula no encontrada"})

@app.get('/chatbot', tags = ['Chatbot'])
def chatbot(query: str):
    query_words = word_tokenize(query.lower())
    
    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words)

    results = [m for m in movies_list if any(s in m['category'].lower() for s in synonyms)]

    return JSONResponse(content = {
        "respuesta": "Aqui tienes algunas peliculas que podrian interesarte" if results else "No se encontraron peliculas",
        "peliculas": results
    })

@app.get('/movies/', tags = ['Movies'])
def get_movies_by_year(category: str):
    return [m for m in movies_list if category.lower() in m['category'].lower] 