import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Prédiction de la prime d'assurance d'Assur'Aimant")

st.image("assuraimant.png", width=500)

data = pd.read_csv("datasetClean.csv")


def build_model(df):
    X = df.iloc[:,:-1]
    Y = df.iloc[:,-1]

    st.markdown()


menu = st.sidebar.radio("Menu",["Accueil","Prédiction d'assurance"])

if menu == "Accueil":
    st.header("Affichage des premières données")
    if st.checkbox("Afficher"):
        st.table(data.head(10))
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
        sns.scatterplot(data=data , x="bmi", y="charges",hue="smoker")
        st.pyplot(fig)
    if graph == "Diagramme de barres":
        fig,ax = plt.subplots(figsize=(5,3))
        sns.barplot(x="smoker",y="charges",data=data)
        st.pyplot(fig)
    if graph == "Histogramme":
        fig,ax = plt.subplots(figsize=(5,3))
        sns.displot(data,x="smoker",y="charges")
        st.pyplot(fig)

if menu == "Prédiction d'assurance":
    st.header("Prédiction des charges d'un nouvel assuré")
    with st.form("Nouvel assuré"):
        st.write("Nouvel assuré")
        value_1 = st.text_input("Age:")
        value_2 = st.text_input("IMC:")
        value_2 = st.selectbox("Sexe:",["Homme","Femme"])
        value_2 = st.selectbox("Nombre d'enfants:",["0","1","2","3","4","5","6"])
        value_2 = st.selectbox("Fumeur:",["Oui","Non"])
        value_2 = st.selectbox("Région:",["Northwest","Southwest","Northeast","Southeast"])

        submitted = st.form_submit_button("Valider")
        if submitted:
            st.write("valeur 1", value_1, "valeur 2", value_2)

