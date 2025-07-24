import streamlit as st
import pandas as pd
import os

# Cargar preguntas desde archivo CSV
FILE_PREGUNTAS = "Cuestionario_Ansiedad_Matematica_ESP.csv"
df_preguntas = pd.read_csv(FILE_PREGUNTAS, encoding="latin1")

st.title("Formulario de Cuestionario de Ansiedad Matemática")

with st.form("formulario_ansiedad"):
    respuestas = {}

    # Preguntas Q1 a Q31: opciones de 1 a 5
    for i in range(31):
        row = df_preguntas.iloc[i]
        codigo = row["ítem"]
        texto = row["Pregunta"]
        respuestas[codigo] = st.radio(f"{codigo}. {texto}", options=[1, 2, 3, 4, 5], key=codigo)

    # Q32 - Edad
    respuestas["Q32"] = st.number_input("Q32. ¿Cuál es tu edad?", min_value=5, max_value=100, step=1)

    # Q33 - Género (M o F)
    texto_q33 = df_preguntas[df_preguntas["ítem"] == "Q33"]["Pregunta"].values[0]
    respuestas["Q33"] = st.selectbox(f"Q33. {texto_q33}", options=["M", "F"])

    # Q34 a Q42 - Usar textos del archivo
    for i in range(33, 42):
        item = f"Q{i+1}"
        texto = df_preguntas[df_preguntas["ítem"] == item]["Pregunta"].values[0]

        if item == "Q35" or item in ["Q38", "Q39", "Q40"]:
            respuestas[item] = st.text_input(f"{item}. {texto}", max_chars=9)
        elif item == "Q36":
            respuestas[item] = st.selectbox(f"{item}. {texto}", options=list(range(24)))
        elif item == "Q37":
            respuestas[item] = st.number_input(f"{item}. {texto}", step=1, format="%d")
       # Q41 y Q42 - Target: entrada libre (número o letra mayúscula)
    for item in ["Q41", "Q42"]:
        texto = df_preguntas[df_preguntas["ítem"] == item]["Pregunta"].values[0]
        entrada = st.text_input(f"{item}. {texto} (Escribe un número entero o una letra mayúscula)", key=item)

        if entrada and not entrada.strip().isdigit() and not (entrada.strip().isalpha() and entrada.strip().isupper()):
            st.warning(f"{item}: Debes escribir solo un número o una letra mayúscula.")
        
        respuestas[item] = entrada.strip()

    # Botón para enviar
    enviado = st.form_submit_button("Enviar respuestas")

# Guardar respuestas si se envió el formulario
if enviado:
    df_nuevo = pd.DataFrame([respuestas])
    archivo_respuestas = "respuestas.csv"

    if os.path.exists(archivo_respuestas):
        df_existente = pd.read_csv(archivo_respuestas)
        df_final = pd.concat([df_existente, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    df_final.to_csv(archivo_respuestas, index=False)
    st.success("✅ Tus respuestas han sido registradas correctamente.")
