# -*- coding: utf-8 -*-
"""
Created on Thu May 14 15:39:32 2026

@author: moito


"""


import os
import sys

# 1. On force la mise à jour silencieuse au démarrage
os.system(f"{sys.executable} -m pip install --upgrade google-generativeai")

import google.generativeai as genai

# 2. CONFIGURATION CRUCIALE : On force la version "v1" ou "v1beta" 
# C'est ici que ton erreur 404 se règle
genai.configure(api_key="TON_API_KEY", transport='rest') 

# 3. Test de présence du modèle 1.5 Flash
try:
    model = genai.GenerativeModel('gemini-1.5-flash')
    print("Succès : Le modèle 1.5 Flash est reconnu !")
except Exception as e:
    print(f"Le modèle n'est toujours pas vu. Erreur : {e}")
    
    
import google.generativeai as genai
import pandas as pd
import time
from google.api_core import exceptions

# 1. Configuration
# Remplace par ta clé API récupérée sur https://aistudio.google.com/
API_KEY = "AIzaSyCeEnP0xahNmrZd0QzUH4CxhclDjnpf8dU"
genai.configure(api_key=API_KEY)

# 2. Upload du Syllabus (une seule fois)
print("Téléchargement du syllabus sur les serveurs Google...")
path_to_pdf = "syllabus cardio.pdf" # Assure-toi que le nom est correct

import google.generativeai as genai

# ... après ta configuration API ...


import google.generativeai as genai
from google.generativeai import types

# ... après genai.configure ...

print("Tentative d'upload...")
try:
    # On passe par le module spécifique 'files' au cas où l'alias global bug
    cardio_file = genai.get_model("models/gemini-1.5-flash") # Test connexion
    cardio_file = genai.upload_file(path="syllabus cardio.pdf", display_name="Syllabus")
    print("Upload réussi !")
except AttributeError:
    print("Erreur : La version installée de google-generativeai est trop vieille.")
    print("Version actuelle détectée :", genai.__version__)
    
# Utilise cette syntaxe si genai.upload_file() bloque encore :
cardio_file = genai.upload_file(path="syllabus cardio.pdf")

# Attendre que le fichier soit prêt (parfois nécessaire pour les gros PDF)
while cardio_file.state.name == "PROCESSING":
    print(".", end="")
    time.sleep(2)
    cardio_file = genai.get_file(cardio_file.name)

print("\nSyllabus prêt !")

# 3. Chargement du fichier Excel
df = pd.read_excel("cardio_4.xlsx")

# 4. Configuration du modèle
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# 5. Boucle de traitement
for index, row in df.iterrows():
    # On vérifie si la ligne est déjà traitée pour pouvoir reprendre après une coupure
    if pd.notna(row.get('Justification')): 
        continue
    
    proposition = row['Proposition']
    reponse_qcm = "VRAI" if row['Reponse'] else "FAUX"
    
    prompt = f"""
    En te basant uniquement sur le document fourni, trouve la justification de la proposition suivante.
    Proposition : "{proposition}"
    Réponse dans le QCM : {reponse_qcm}
    
    Format de réponse souhaité :
    JUSTIF: [Copie-colle ici le passage exact du texte qui confirme ou infirme la proposition]
    PAGE: [Numéro de la page où se trouve l'info]
    """

    success = False
    while not success:
        try:
            # Envoi de la requête avec le lien vers le fichier + le prompt
            response = model.generate_content([cardio_file, prompt])
            res_text = response.text
            
            # Extraction des données (Split basique)
            if "JUSTIF:" in res_text and "PAGE:" in res_text:
                justif = res_text.split("JUSTIF:")[1].split("PAGE:")[0].strip()
                page = res_text.split("PAGE:")[1].strip()
                
                df.at[index, 'Justification'] = justif
                df.at[index, 'Reference'] = page
                print(f"[{index+1}/575] OK")
            else:
                print(f"[{index+1}/575] Format de réponse incorrect, passage à la suivante.")
            
            success = True # On sort de la boucle while
            
        except exceptions.ResourceExhausted:
            # Si on atteint la limite de l'API (Rate Limit)
            print("Limite atteinte (429), pause de 30 secondes...")
            time.sleep(30)
        except Exception as e:
            print(f"Erreur à la ligne {index}: {e}")
            time.sleep(5)
            break

    # Sauvegarde automatique toutes les 10 lignes pour ne rien perdre
    if index % 10 == 0:
        df.to_excel("cardio_4_sauvegarde.xlsx", index=False)

# 6. Sauvegarde finale
df.to_excel("cardio_4_finalise.xlsx", index=False)
print("Travail terminé ! Fichier : cardio_4_finalise.xlsx")