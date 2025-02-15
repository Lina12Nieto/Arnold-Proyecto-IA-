"""
Imagina que esta API es una biblioteca de películas:
La función load_movies() es como un bibliotecario que carga el catálogo de
libros  cuando se abre la biblioteca.
La función get_movies() muestra todo el catálogo cuando alguien lo pide.
La función get_movie(id) es como si alguien preguntara por un libro específico por su código de identificación.
La función chatbot (query) es un asistente que busca libros según palabras clave y sinónimo.
La función get_movies_by_category (category) ayuda a encontrar películas según su género (acción, comedia, etc.).

"""

# Importamos las herramientas necesarias para contruir nuestra API
from fastapi import FastAPI, HTTPException # FastAPI nos ayuda a crear a API, HTTPException maneja errores
from fastapi.responses import HTMLResponse, JSONResponse # HTMLResponse para páginas web, JSONResponse para respuestas en formato JSON.
import pandas as pd # Pandas nos ayuda a trabajar con datos en formato de tabla como si fuera un Excel
import nltk # NLTK es una librería para procesar texto y analizar palabras
from nltk.tokenize import word_tokenize # Se usa para dividir un texto en palabras individuales
from nltk.corpus import wordnet # Se usa para buscar sinónimos de palabras

# Iniciamos la ruta donde NLTK buscará los datos descargados en nuestro computador.
# nltk.data.path.append("/tmp")

# Descargamos las herramientas necesarias de NLTK para el análisis de palabras.

nltk.download('punkt') # Paquete para dividir frases en palabras
nltk.download('wordnet') # Paquete para encontrar sinónimos de palabras en inglés

# Funcón para cargar las dietas desde un archivo CSV

def load_diets():
    # Leemos el archivo que contiene información de dietas y seleccionamos las columnas más importantes
    df = pd.read_csv("Dataset/All_Diets.csv")[['Diet_type', 'Recipe_name', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)', 'Extraction_day', 'Extraction_time']]

    # Renombramos las columnas para que sean más fáciles de entender
    df.columns = ['Diet_type', 'Recipe_name', 'Cuisine_type', 'Protein', 'Carbs', 'Fat', 'Extraction_day', 'Extraction_time']

    # Llenamos los espacios vacíos con texto vacío y convertimos los datos en una lista de diccionario
    return df.fillna('').to_dict(orient='records')

# Cargamos las dietas al iniciar la API para no leer el archivo cada vez que algien pregunte por ellas.
diets_list = load_diets()

# Función para encontrar sinónios de una palabra

def get_synnyms(word):
    # Usamos WordNet para obtener distintas palabras que significan los mismo
    return{lemma.name() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}

# Creamos la aplicación FastAPI, que será el motor de nuestra API
# Esto iniciliza la API y le da un título y una versión
app = FastAPI(title="Diet API", version="1.0.0")

# Ruta de inicio: Cuando alguien entra a la API sin especificar nada, verá un mensaje de bienvenida

@app.get("/", tags=["Home"])
def home():
    return HTMLResponse(content="<h1>Bienvenido a la API de Dieta</h1>")

# Obteniendo la lista de películas
# Creamos una ruta para obtener todas las dietas disponibles

@app.get("/diets", tags=["Diets"])
def get_diets():
    return diets_list or HTTPException(status_code=500, detail="No se encontraron dietas")

# Ruta para obtener una película específica por su ID
@app.get("/diets/{id}", tags=["Diets"])
def get_diet(id: str):
    return next(m for m in diets_list if m['id'] == id), {"detalle": "Dieta no encontrada"}

# Ruta del chatbot que responde con dietas según palabras clave de la consulta

@app.get("/chatbot", tags=["Chatbot"])
def chatbot(query: str):
    # Dividimos la consulta en palabras clave, para entender mejor la intención del usuario
    query_words = word_tokenize(query.lower())

    # Buscamos sinónimos de las palabras clave para mejorar la búsqueda
    synonyms = {word for q in query_words for word in get_synnyms(q)} | set(query_words)

    # Filtramos la lista de dietas buscando coincidencias en el tipo de la cocina
    results = [m for m in diets_list if any(s in m['Cuisine_type'].lower() for s in synonyms)]

    # Si encontramos películas, enviamos la lista; si no, mostramos un mensaje que no se encontraron dietas

    return JSONResponse(content={
        "respuesta": "Aquí tienes algunas dietas que podrían interesarte" if results else "No encontré dietas de esa cocina",
        "dietas": results
    })

# Ruta para obtener dietas por tipo de cocina
@app.get("/diets/by_cuisine_type/", tags=["Diets"])
def get_diets_by_cuisine(cuisine: str):
    # Filtramos la lista de dietas según la cocina especificada
    return [m for m in diets_list if cuisine.lower() in m['Cuisine_type'].lower()]