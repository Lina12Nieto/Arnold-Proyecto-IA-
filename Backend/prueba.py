from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# Configuración de NLTK
nltk.data.path.append("/app/nltk_data")
nltk.download('punkt')
nltk.download('wordnet')

# Cargar las dietas desde el CSV
def load_diets():
    df = pd.read_csv("Dataset/All_Diets.csv")[['Diet_type', 'Recipe_name', 'Cuisine_type', 'Protein(g)', 'Carbs(g)', 'Fat(g)']]
    df.columns = ['Diet_type', 'Recipe_name', 'Cuisine_type', 'Protein', 'Carbs', 'Fat']
    return df.fillna('').to_dict(orient='records')

diets_list = load_diets()

def get_synonyms(word):
    return {lemma.name() for syn in wordnet.synsets(word) for lemma in syn.lemmas()}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo para recibir respuestas del usuario
class UserResponse(BaseModel):
    question_id: int
    answer: str

# Almacenar respuestas del usuario
data_store = {}

# Preguntas secuenciales
questions = [
    "¿Cuál es tu peso en kg?",
    "¿Cuál es tu altura en cm?",
    "¿Cuál es tu edad?",
    "¿Eres hombre o mujer?\n1. Hombre\n2. Mujer)",
    "¿Cuál es tu nivel de actividad física?\n1. Sedentario \n2. Ligero \n3. Moderado \n4. Intenso \n5. Muy intenso ",
    "¿Cuál es tu objetivo?\n1. Mantenimiento\n2. Pérdida de grasa\n3. Ganancia muscular"
]

@app.get("/")
def welcome():
    return {"message": "¡Bienvenido!", "question": questions[0], "question_id": 0}

@app.post("/answer")
def process_answer(user_response: UserResponse):
    answer = user_response.answer.strip()

    # Mapeo de respuestas numéricas
    if user_response.question_id == 3:  # Género
        options = {"1": "hombre", "2": "mujer"}
    elif user_response.question_id == 4:  # Nivel de actividad
        options = {"1": "1.2", "2": "1.375", "3": "1.55", "4": "1.725", "5": "1.9"}
    elif user_response.question_id == 5:  # Objetivo
        options = {"1": "mantenimiento", "2": "pérdida de grasa", "3": "ganancia muscular"}
    else:
        options = {}

    if answer in options:
        answer = options[answer]

    # Guardar la respuesta 
    data_store[user_response.question_id] = answer

    # Enviar siguiente pregunta o calcular resultados
    if user_response.question_id + 1 < len(questions):
        return {"message": "Siguiente pregunta", "question": questions[user_response.question_id + 1], "question_id": user_response.question_id + 1}
    else:
        return calculate_results()

# Función para calcular TMB, GET y macronutrientes
def calculate_results():
    peso = float(data_store[0])
    altura = float(data_store[1])
    edad = int(data_store[2])
    genero = data_store[3]
    actividad = float(data_store[4])
    objetivo = data_store[5]

    # Cálculo de TMB
    if genero.lower() == "hombre":
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) + 5
    else:
        tmb = (10 * peso) + (6.25 * altura) - (5 * edad) - 161
    
    # Cálculo de GET
    get = tmb * actividad
    
    # Déficit y superávit calórico
    caloric_goals = {
        "mantenimiento": get,
        "pérdida de grasa": get - 500,
        "ganancia muscular": get + 500
    }
    calorias_diarias = caloric_goals[objetivo]
    
    # Macronutrientes
    proteina_gkg = {"mantenimiento": 1.6, "pérdida de grasa": 2.2, "ganancia muscular": 2.0}[objetivo]
    proteinas = peso * proteina_gkg
    calorias_proteina = proteinas * 4
    
    grasas_cal = calorias_diarias * 0.25
    grasas = grasas_cal / 9
    
    calorias_carbohidratos = calorias_diarias - (calorias_proteina + grasas_cal)
    carbohidratos = calorias_carbohidratos / 4
    
    return {
        "TMB": tmb,
        "GET": get,
        "Calorías diarias recomendadas": calorias_diarias,
        "Macronutrientes": {
            "Proteínas (g)": proteinas,
            "Grasas (g)": grasas,
            "Carbohidratos (g)": carbohidratos
        }
    }

@app.get("/Chatbot/",tags=["Chatbot"])
def chatbot_diet_response(query: str):

    query_words = word_tokenize(query.lower())

    synonyms = {word for q in query_words for word in get_synonyms(q)} | set(query_words)

    # Buscar dietas relacionadas con la consulta del usuario
    results = [diet for diet in diets_list if any(s in diet['Cuisine_type'].lower() for s in synonyms)]

    if results:
        return JSONResponse(content={"respuesta": "Aquí tienes algunas dietas que podrían interesarte","dietas": results[:2]})
    else:
        return JSONResponse(content={"respuesta": "No encontré dietas relacionadas a tu consulta."})