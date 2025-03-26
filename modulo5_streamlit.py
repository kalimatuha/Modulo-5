import random
import json
import streamlit as st

# Cargar el dataset de preguntas desde un archivo JSON
try:
    with open('modulo5.json', 'r', encoding='utf-8') as f:  # Ruta relativa al JSON
        trivia_data = json.load(f)
except FileNotFoundError:
    st.error("Error: No se encontró el archivo 'modulo5.json'. Asegúrate de que está en el mismo directorio que este script.")
    st.stop()
except json.JSONDecodeError:
    st.error("Error: El archivo 'modulo5.json' tiene un formato inválido.")
    st.stop()

# Verificar la estructura del JSON cargado
if not isinstance(trivia_data, list) or any('tag' not in category or 'qa' not in category for category in trivia_data):
    st.error("Error: El archivo JSON debe ser una lista de categorías con 'tag' y 'qa'. Revisa el formato.")
    st.stop()

# Título de la aplicación
st.title("Trivial Jedi")
st.write("Te haré preguntas de diferentes categorías. Responde correctamente y usa el botón 'Siguiente' para continuar.")

# Estado inicial del juego (usando Streamlit's session state)
if 'score' not in st.session_state:
    st.session_state.score = 0
    st.session_state.total_questions = 0
    st.session_state.question_item = None
    st.session_state.category = None
    st.session_state.answered = False  # Nuevo estado para controlar si la pregunta fue respondida

# Función para cargar una nueva pregunta
def load_question():
    st.session_state.category = random.choice(trivia_data)
    st.session_state.question_item = random.choice(st.session_state.category['qa'])
    st.session_state.answered = False  # Resetear estado al cargar nueva pregunta

# Si no hay pregunta cargada, cargar una
if st.session_state.question_item is None:
    load_question()

# Mostrar la categoría y pregunta
category = st.session_state.category
question_item = st.session_state.question_item
st.subheader(f"Categoría: {category['tag'].capitalize()}")
st.write(f"Pregunta: {question_item['pattern']}")

# Mostrar las opciones como botones
options = question_item['options']
correct_answer = question_item['correct'].lower()

# Streamlit crea un widget para las opciones
user_choice = st.radio("Selecciona una opción:", options, key="options")

# Botón para responder
if st.button("Responder") and not st.session_state.answered:
    st.session_state.answered = True  # Marcar como respondida
    st.session_state.total_questions += 1
    if user_choice.lower().startswith(correct_answer):  # Compara la respuesta
        st.success("¡Correcto! 🎉")
        st.session_state.score += 1
    else:
        st.error(f"Incorrecto. La respuesta correcta era: {correct_answer.upper()} 😢")

    st.write(f"Puntuación: {st.session_state.score}/{st.session_state.total_questions}")

# Botón para pasar a la siguiente pregunta
if st.session_state.answered:
    if st.button("Siguiente"):
        load_question()
