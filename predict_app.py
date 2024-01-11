import numpy as np
import pandas as pd
import pickle
import streamlit as st

modalities = {
    "age": [18, 100],
    "sex": ["male", "female"],
    "bmi": [15.00, 70.00],
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

with open("model.pkl", "rb") as file:
    model = pickle.load(file)
file.close()
    
answers = {}

st.title("Predictive tool for insurance premium")
st.divider()
st.header("Respond to each section to get an estimation")

answers["age"] = st.number_input(
    "age:",
    min_value=modalities["age"][0],
    max_value=modalities["age"][1],
    value=None,
    step=1,
)

answers["sex"] = st.selectbox(
    "Sex of the person:",
    modalities["sex"],
    index=None
)

# Amélioration -> proposer taille et poids pour calcul bmi
answers["bmi"] = st.number_input(
    "bmi:",
    min_value=modalities["bmi"][0],
    max_value=modalities["bmi"][1],
    value=None,
    step=0.01,
)

answers["children"] = st.number_input(
    "Number of children:",
    min_value=modalities["children"][0],
    max_value=modalities["children"][1],
    value=None,
    step=1
)

answers["smoker"] = st.selectbox(
    "Smoker:",
    modalities["smoker"],
    index=None
)

answers["region"] = st.selectbox(
    "Region:",
    modalities["region"],
    index=None
)

if st.button("Predict", type="primary"):

    for answer in answers:
        stop = False
        if answers[answer] == None:
            st.error(f"Missing answer for : {answer}")
            stop = True
        if stop:
            break

    if not stop:

        for group in bmi_scale:
            if answers["bmi"] >= group["range"][0] and answers["bmi"] <= group["range"][1]:
                answers["bmi"] = group["category"]
                break
            
        df = pd.DataFrame(answers, index=[0])
        charges = model.predict(df)[0]

        st.divider()
        st.header("Estimation of the charges for this person:")
        st.write("$", str(charges))