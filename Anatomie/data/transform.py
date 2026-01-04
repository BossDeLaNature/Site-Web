import pandas as pd
import json

# Lecture Excel
df = pd.read_excel("Reconnaissance.xlsx")

df["image"] = "media/Reconnaissance/"+df["image"].astype(int).astype(str)+".png"

# Colonnes de base
base_cols = ["titre", "image", "ordre"]

# Détection automatique des colonnes réponses
reponse_cols = sorted([c for c in df.columns if c.startswith("reponse_")])
explication_cols = sorted([c for c in df.columns if c.startswith("explication_")])

questions = []

for _, row in df.iterrows():
    reponses = []
    numero = 1

    for r_col, e_col in zip(reponse_cols, explication_cols):
        if pd.notna(row[r_col]):  # on ignore les réponses vides
            reponses.append({
                "numero": numero,
                "correct": row[r_col],
                "explication": row[e_col] if pd.notna(row[e_col]) else ""
            })
            numero += 1

    questions.append({
        "titre": row["titre"],
        "image": row["image"] if pd.notna(row["image"]) else "",
        "ordre": bool(row["ordre"]),
        "reponses": reponses
    })

# Sauvegarde JSON
with open("Reconnaissance.json", "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)
    
    

with open("Reconnaissance.json", "r", encoding="utf-8") as f:
    questions = json.load(f)

reponses_uniques = set()

for q in questions:
    for r in q["reponses"]:
        texte = r["correct"].strip()
        if texte:
            reponses_uniques.add(texte)

# Tri alphabétique
reponses_list = sorted(reponses_uniques)

with open("databaseReconnaissance.json", "w", encoding="utf-8") as f:
    json.dump(reponses_list, f, ensure_ascii=False, indent=2)