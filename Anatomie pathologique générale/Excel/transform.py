# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:06:47 2024

@author: moito
"""

import pandas as pd
from json import loads, dumps
import json
# Charger le fichier Excel
df = pd.read_excel('Secret.xlsx')

df = df.fillna("")

df["Proposition"] = df["Proposition"].str.replace("•0","")
df["Proposition"] = df["Proposition"].str.replace("•O "," ")
df["Proposition"] = df["Proposition"].str.replace("•"," ")
df["Proposition"] = df["Proposition"].str.replace("O "," ")

df["Reponse"] = df["Reponse"]==1.0

df["image"] = "media/"+df["image"].astype(str)+".png"

# Convertir en JSON
json_data = df.to_json(orient="records",indent=4)

parsed = loads(json_data)

test = dumps(parsed, indent=4, separators=(',', ': '))
test2 = loads(test)



# Sauvegarder en fichier JSON

    
with open("Secret.json", "w", encoding="utf-8") as f:
    json.dump(test2, f, ensure_ascii=False, indent=2)