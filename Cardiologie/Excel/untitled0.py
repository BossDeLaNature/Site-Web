# -*- coding: utf-8 -*-
"""
Created on Mon May 11 13:03:55 2026

@author: moito
"""

import pandas as pd
from json import loads, dumps
import json
# Charger le fichier Excel

import os
import sys

# --- CONFIGURATION DU DOSSIER ---
# Force Python à travailler dans le dossier du script
os.chdir(os.path.dirname(os.path.abspath(__file__)))
Cardio = "cardio_"




for i in range(15):
    a = str(i+1)
    df = pd.read_excel(Cardio+a+".xlsx")

    df = df.fillna("")


    df["Reponse"] = df["Reponse"]==1.0

    df["image"] = "media/"+df["image"].astype(str)+".png"

    # Convertir en JSON
    json_data = df.to_json(orient="records",indent=4)

    parsed = loads(json_data)

    test = dumps(parsed, indent=4, separators=(',', ': '))
    test2 = loads(test)



    # Sauvegarder en fichier JSON

        
    with open(Cardio+a+".json", "w", encoding="utf-8") as f:
        json.dump(test2, f, ensure_ascii=False, indent=2)
