import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

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

with open("modele.pkl", "rb") as file:
    model = pickle.load(file)
file.close()

st.title("Prédiction de la prime d'assurance d'Assur'Aimant")
data = pd.read_csv("datasetClean.csv")

form = {}

st.sidebar.image("assuraimant.png", width=275)
menu = st.sidebar.radio("Menu",["Accueil","Prédiction d'assurance"])


if menu == "Accueil":
    st.header("Statistiques des données")
    if st.checkbox("Stats"):
        st.table(data.describe())
    if st.header("Graphique de corrélation"):
        fig,ax = plt.subplots(figsize=(10,5))
        sns.heatmap(data.corr(),annot=True,cmap="coolwarm")
        st.pyplot(fig)
    
    st.title("Affichage des graphiques de données")
    graph = st.selectbox("Types de graphiques :",["Diagramme de points","Diagramme de barres","Histogramme"])
    if graph == "Diagramme de points":
        value = st.slider("Filtrer les données selon l'age",18,65)
        data = data.loc[data["age"]<=value]
        fig,ax = plt.subplots(figsize=(10,5))
        sns.scatterplot(data=data , x="bmi", y="charges",hue="smoker").set(title="Charges en fonction de l'IMC")
        st.pyplot(fig)
    if graph == "Diagramme de barres":
        fig,ax = plt.subplots(figsize=(5,3))
        sns.barplot(x="smoker",y="charges",data=data).set(title="Moyenne des charges pour les fumeurs et non fumeurs")
        st.pyplot(fig)
    if graph == "Histogramme":
        fig,ax = plt.subplots(figsize=(5,3))
        sns.histplot(data=data, x="bmi", kde=True, color="darkgreen").set(title="Répartition des individus selon l'IMC")
        st.pyplot(fig)

if menu == "Prédiction d'assurance":
    with st.form("Nouvel assuré"):
        st.header("Estimation des charges du nouvel assuré:")
        form["age"] = st.number_input(
            "Age:",
            min_value=modalities["age"][0],
            max_value=modalities["age"][1],
            value=None,
            step=1,
        )
        form["sex"] = st.selectbox(
            "Sexe:",
            modalities["sex"],
            index=None
        )
        form["bmi"] = st.number_input(
            "IMC:",
            min_value=modalities["bmi"][0],
            max_value=modalities["bmi"][1],
            value=None,
            step=0.01,
        )

        st.write("Si vous ne connaissez pas votre IMC, veuillez remplir votre taille et votre poids.")

        height = st.number_input(
            "Taille (en m):",
            min_value=modalities["height"][0],
            max_value=modalities["height"][1],
            value=None,
            step=0.01,
        )
        weight = st.number_input(
            "Poids (en kg):",
            min_value=modalities["weight"][0],
            max_value=modalities["weight"][1],
            value=None,
            step=0.1,
        )
        form["children"] = st.number_input(
            "Nombre d'enfants:",
            min_value=modalities["children"][0],
            max_value=modalities["children"][1],
            value=None,
            step=1
        )
        form["smoker"] = st.selectbox(
            "Fumeur:",
            modalities["smoker"],
            index=None
        )
        form["region"] = st.selectbox(
            "Region:",
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

