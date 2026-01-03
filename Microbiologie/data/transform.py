import pandas as pd
import json

# Charger le fichier Excel
df = pd.read_excel("Parasitologie.xlsx")

# Nettoyage : remplacer les NaN par des chaînes vides
df = df.fillna("")

parasites = []

for _, row in df.iterrows():
    parasites.append({
        "Espece": row["Espèce"],
        "Maladie": row["Maladie"],
        "Repartition": row["Répartition (Lieu)"],
        "Reservoir": row["Réservoir"],
        "Caracteristiques": row["Caractéristiques"],
        "Localisation": row["Localisation"],
        "Cycle_type": row["Cycle (monoxène ou dixène)"],
        "Cycle_homme": row["Cycle chez l'homme"],
        "Cycle_vecteur": row["Cycle chez le vecteur (mettre / si pas de cycle)"],
        "Mode_contamination": row["Mode de contamination"],
        "Manifestations_cliniques": row["Manifestations cliniques"],
        "Diagnostic": row["Diagnostique"],
        "Traitement": row["Traitement/Prophylaxie"],
        "Image": row["Image"]
    })

# Sauvegarde en JSON
with open("parasitologie.json", "w", encoding="utf-8") as f:
    json.dump(parasites, f, ensure_ascii=False, indent=2)



import pandas as pd
import json
import os

# Charger Excel
df = pd.read_excel("Parasitologie.xlsx")
df = df.fillna("")

# Dossier de sortie
OUTPUT_DIR = "databases_parasitologie"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping colonnes Excel -> noms de fichiers JSON
columns_map = {
    "Espèce": "Espece",
    "Maladie": "Maladie",
    "Répartition (Lieu)": "Repartition",
    "Réservoir": "Reservoir",
    "Caractéristiques": "Caracteristiques",
    "Localisation": "Localisation",
    "Cycle (monoxène ou dixène)": "Cycle_type",
    "Cycle chez l'homme": "Cycle_homme",
    "Cycle chez le vecteur (mettre / si pas de cycle)": "Cycle_vecteur",
    "Mode de contamination": "Mode_contamination",
    "Manifestations cliniques": "Manifestations_cliniques",
    "Diagnostique": "Diagnostic",
    "Traitement/Prophylaxie": "Traitement",
    "Image": "Image"
}

for excel_col, json_name in columns_map.items():
    valeurs_uniques = set()

    for value in df[excel_col]:
        value = value.strip()
        if value and value != "/":
            valeurs_uniques.add(value)

    # Tri alphabétique
    data = sorted(valeurs_uniques)

    # Sauvegarde
    with open(f"{OUTPUT_DIR}/{json_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Toutes les bases JSON ont été générées.")




#################################################################################################


# Charger le fichier Excel
df = pd.read_excel("Mycologie.xlsx")

# Nettoyage : remplacer les NaN par des chaînes vides
df = df.fillna("")

parasites = []

for _, row in df.iterrows():
    parasites.append({
        "Espece": row["Espèce"],
        "Maladie": row["Maladie"],
        "Caracteristiques": row["Caractéristiques"],
        "Manifestations_cliniques": row["Manifestations cliniques"],
        "Diagnostic": row["Diagnostique"],
        "Traitement": row["Traitement/Prophylaxie"],
        "Image": row["Image"]
    })

# Sauvegarde en JSON
with open("mycologie.json", "w", encoding="utf-8") as f:
    json.dump(parasites, f, ensure_ascii=False, indent=2)



import pandas as pd
import json
import os

# Charger Excel
df = pd.read_excel("Mycologie.xlsx")
df = df.fillna("")

# Dossier de sortie
OUTPUT_DIR = "databases_mycologie"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Mapping colonnes Excel -> noms de fichiers JSON
columns_map = {
    "Espèce": "Espece",
    "Maladie": "Maladie",
    "Caractéristiques": "Caracteristiques",
    "Manifestations cliniques": "Manifestations_cliniques",
    "Diagnostique": "Diagnostic",
    "Traitement/Prophylaxie": "Traitement",
    "Image": "Image"
}

for excel_col, json_name in columns_map.items():
    valeurs_uniques = set()

    for value in df[excel_col]:
        value = value.strip()
        if value and value != "/":
            valeurs_uniques.add(value)

    # Tri alphabétique
    data = sorted(valeurs_uniques)

    # Sauvegarde
    with open(f"{OUTPUT_DIR}/{json_name}.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ Toutes les bases JSON ont été générées.")






















