# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:06:47 2024

@author: moito
"""

import pandas as pd
import json
from unidecode import unidecode
# Charger le fichier Excel
df = pd.read_excel('Question-Chapitre-II.xlsx')
df['Justification'] = df['Justification'].apply(unidecode)
df['Question'] = df['Question'].apply(unidecode)
df['Proposition'] = df['Proposition'].apply(unidecode)

# Convertir en JSON
json_data = df.to_json(orient="records")

# Sauvegarder en fichier JSON
with open('Question-Chapitre-II.json', 'w') as json_file:
    json.dump(json_data, json_file)