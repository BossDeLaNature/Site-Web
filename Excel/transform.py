# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:06:47 2024

@author: moito
"""

import pandas as pd
import json

# Charger le fichier Excel
df = pd.read_excel('Question-Chapitre-II.xlsx')

# Convertir en JSON
json_data = df.to_json(orient='records',indent=2)

# Sauvegarder en fichier JSON
with open('Question-Chapitre-II.json', 'w', encoding='utf-8') as json_file:
    json.dump(json_data, json_file)