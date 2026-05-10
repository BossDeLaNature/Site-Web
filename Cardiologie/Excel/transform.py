# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:06:47 2024

@author: moito
"""

import pandas as pd
from json import loads, dumps
import json
from unidecode import unidecode

## Respiratoire

# Charger le fichier Excel
df = pd.read_excel('respiratoire.xlsx')
df['Justification'] = df['Justification'].apply(unidecode)
df['Question'] = df['Question'].apply(unidecode)
df['Proposition'] = df['Proposition'].apply(unidecode)

# Convertir en JSON
json_data = df.to_json(orient="records",indent=4)

parsed = loads(json_data)

test = dumps(parsed, indent=4, separators=(',', ': '))
test2 = loads(test)



# Sauvegarder en fichier JSON
with open('respiratoire.json', 'w') as json_file:
    json.dump(test2, json_file,indent=6)


## Renale

# Charger le fichier Excel
df = pd.read_excel('renale.xlsx')
df['Justification'] = df['Justification'].apply(unidecode)
df['Question'] = df['Question'].apply(unidecode)
df['Proposition'] = df['Proposition'].apply(unidecode)

# Convertir en JSON
json_data = df.to_json(orient="records",indent=4)

parsed = loads(json_data)

test = dumps(parsed, indent=4, separators=(',', ': '))
test2 = loads(test)



# Sauvegarder en fichier JSON
with open('renale.json', 'w') as json_file:
    json.dump(test2, json_file,indent=6)


## Cardiaque

# Charger le fichier Excel
df = pd.read_excel('cardiaque.xlsx')
df['Justification'] = df['Justification'].apply(unidecode)
df['Question'] = df['Question'].apply(unidecode)
df['Proposition'] = df['Proposition'].apply(unidecode)

# Convertir en JSON
json_data = df.to_json(orient="records",indent=4)

parsed = loads(json_data)

test = dumps(parsed, indent=4, separators=(',', ': '))
test2 = loads(test)



# Sauvegarder en fichier JSON
with open('cardiaque.json', 'w') as json_file:
    json.dump(test2, json_file,indent=6)


## Endocrinien

# Charger le fichier Excel
df = pd.read_excel('endocrinien.xlsx')
df['Justification'] = df['Justification'].apply(unidecode)
df['Question'] = df['Question'].apply(unidecode)
df['Proposition'] = df['Proposition'].apply(unidecode)

# Convertir en JSON
json_data = df.to_json(orient="records",indent=4)

parsed = loads(json_data)

test = dumps(parsed, indent=4, separators=(',', ': '))
test2 = loads(test)



# Sauvegarder en fichier JSON
with open('endocrinien.json', 'w') as json_file:
    json.dump(test2, json_file,indent=6)


## digestif

# Charger le fichier Excel
df = pd.read_excel('digestif.xlsx')
df['Justification'] = df['Justification'].apply(unidecode)
df['Question'] = df['Question'].apply(unidecode)
df['Proposition'] = df['Proposition'].apply(unidecode)

# Convertir en JSON
json_data = df.to_json(orient="records",indent=4)

parsed = loads(json_data)

test = dumps(parsed, indent=4, separators=(',', ': '))
test2 = loads(test)



# Sauvegarder en fichier JSON
with open('digestif.json', 'w') as json_file:
    json.dump(test2, json_file,indent=6)


##juin2024



# Charger le fichier Excel
df = pd.read_excel('juin2024.xlsx')
df['Justification'] = df['Justification'].apply(unidecode)
df['Question'] = df['Question'].apply(unidecode)
df['Proposition'] = df['Proposition'].apply(unidecode)

# Convertir en JSON
json_data = df.to_json(orient="records",indent=4)

parsed = loads(json_data)

test = dumps(parsed, indent=4, separators=(',', ': '))
test2 = loads(test)



# Sauvegarder en fichier JSON
with open('juin2024.json', 'w') as json_file:
    json.dump(test2, json_file,indent=6)