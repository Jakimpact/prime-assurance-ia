import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import scipy.stats as st

# Charger le csv dans une variable data
data = pd.read_csv('dataset.csv')
# data.head()
# print(data.dtypes)

# On vérifie s'il y a des valeurs nulles dans le jeu de données
print(data.isnull().sum())

# On va s'intéresser aux doublons
a = data.loc[data[['bmi', 'age', 'charges']].duplicated(keep=False),:]
print(a)

# On supprime les doublons
data.drop_duplicates(subset=['bmi', 'age', 'charges'], inplace=True, ignore_index=True)

# On cherche ensuite à trouver les outliers
print(data.describe())

i = data.loc[data['charges']==63770.428010,:].index[0] # récupération de l'index où les charges sont à plus de 60k
print(i)

