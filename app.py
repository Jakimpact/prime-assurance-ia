import pandas as pd
import pickle
import streamlit as st

modalities = {
    "age": [18, 100],
    "sex": ["male", "female"],
    "bmi": [15.00, 70.00],
    "height": [0.70, 2.50],
    "weight": [30.0, 200.0],
    "children": [0, 20],
    "smoker": ["yes", "no"],
    "region": ["northwest", "northeast", "southwest", "southeast"],
    }

bmi_scale = [
    {"category": "Underweight", "range": [float("-inf"), 18.499]},
    {"category": "Healthy weight", "range": [18.5, 24.999]},
    {"category": "Overweight", "range": [25, 29.999]},
    {"category": "Obesity class I", "range": [30, 34.999]},
    {"category": "Obesity class II", "range": [35, 39.999]},
    {"category": "Obesity class III", "range": [40, float("inf")]},
    ]

data = pd.read_csv("project/csv/dataset_cleaned.csv")

with open("project/modele.pkl", "rb") as file:
    model = pickle.load(file)
file.close()

form = {}

st.title("Prédiction de primes d'assurance grâce à l'IA")


with st.form("Nouvel assuré"):

    st.header("Estimation des charges du nouvel assuré :")

    form["age"] = st.number_input(
        "Age :",
        min_value=modalities["age"][0],
        max_value=modalities["age"][1],
        value=None,
        step=1,
    )

    form["sex"] = st.selectbox(
        "Genre :",
        modalities["sex"],
        index=None
    )

    form["bmi"] = st.number_input(
        "IMC :",
        min_value=modalities["bmi"][0],
        max_value=modalities["bmi"][1],
        value=None,
        step=0.01,
    )

    st.write("Si vous ne connaissez pas votre IMC, veuillez remplir votre taille et votre poids.")

    height = st.number_input(
        "Taille (en m) :",
        min_value=modalities["height"][0],
        max_value=modalities["height"][1],
        value=None,
        step=0.01,
    )

    weight = st.number_input(
        "Poids (en kg) :",
        min_value=modalities["weight"][0],
        max_value=modalities["weight"][1],
        value=None,
        step=0.1,
    )

    form["children"] = st.number_input(
        "Nombre d'enfants :",
        min_value=modalities["children"][0],
        max_value=modalities["children"][1],
        value=None,
        step=1
    )

    form["smoker"] = st.selectbox(
        "Fumeur :",
        modalities["smoker"],
        index=None
    )

    form["region"] = st.selectbox(
        "Region :",
        modalities["region"],
        index=None
    )

    submitted = st.form_submit_button("Valider")

    if submitted:

        for answer in form:
            stop = False

            if form[answer] == None:

                if answer == "bmi":
                    if (height and weight) != None:
                        form[answer] = weight / (height*2)
                        continue

                st.error(f"Missing answer for : {answer}")
                stop = True

            if stop:
                break

        if not stop:

            for group in bmi_scale:

                if form["bmi"] >= group["range"][0] and form["bmi"] <= group["range"][1]:
                    form["bmi"] = group["category"]
                    break
                
            df = pd.DataFrame(form, index=[0])
            charges = model.predict(df)[0]

            st.divider()
            st.write("Montant des charges : $", str(charges))