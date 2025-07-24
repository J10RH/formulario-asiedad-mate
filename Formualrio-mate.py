import streamlit as st
import pandas as pd
import os

# Cargar preguntas desde archivo CSV
FILE_PREGUNTAS = "Cuestionario_Ansiedad_Matematica_ESP.csv"
df_preguntas = pd.read_csv(FILE_PREGUNTAS, encoding="latin1")

st.title("Formulario de Cuestionario de Ansiedad Matemática")

with st.form("formulario_ansiedad"):
    respuestas = {}
    
    # Preguntas Q1 a Q31: escala 1-5
    for i in range(31):
        row = df_preguntas.iloc[i]
        pregunta = row["Pregunta"]
        codigo = row["ítem"]
        respuesta = st.radio(f"{codigo}. {pregunta}", options=[1, 2, 3, 4, 5], key=codigo)
        respuestas[codigo] = respuesta

    # Q32 - Edad (texto numérico)
    respuestas["Q32"] = st.number_input("Q32. ¿Cuál es tu edad?", min_value=5, max_value=100, step=1)

    # Q33 - Sexo (M o F)
    respuestas["Q33"] = st.selectbox("Q33. Sexo", options=["M", "F"])

    # Q34 - No está especificada, opcionalmente se puede omitir o definir

    # Q35 - Palabra de máx 9 letras
    respuestas["Q35"] = st.text_input("Q35. Escribe una palabra (máx. 9 letras)", max_chars=9)

    # Q36 - Elegir hora (0 a 23 h)
    respuestas["Q36"] = st.selectbox("Q36. Selecciona una hora del día", options=list(range(24)))

    # Q37 - Número entero
    respuestas["Q37"] = st.number_input("Q37. Escribe un número entero", step=1, format="%d")

    # Q38 a Q40 - Palabras máx 9 letras
    for q in ["Q38", "Q39", "Q40"]:
        respuestas[q] = st.text_input(f"{q}. Escribe una palabra (máx. 9 letras)", max_chars=9)

    # Q41 y Q42 - Elegir entre número (0 a 20) o letra A/B/C/D/F
    for q in ["Q41", "Q42"]:
        tipo_dato = st.radio(f"{q}. ¿Qué tipo de dato deseas ingresar?", ["Número", "Letra"], key=q+"_tipo")
        if tipo_dato == "Número":
            respuestas[q] = st.number_input(f"{q} (Número entre 0 y 20)", min_value=0, max_value=20, step=1, key=q+"_num")
        else:
            respuestas[q] = st.selectbox(f"{q} (Letra)", options=["A", "B", "C", "D", "F"], key=q+"_letra")

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
