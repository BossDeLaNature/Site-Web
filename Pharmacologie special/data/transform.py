import json
import pandas as pd
from pathlib import Path


def excel_to_json(input_excel_path, output_json_path=None):
    """
    Convertit un fichier Excel contenant des médicaments en JSON structuré.

    Colonnes attendues dans le fichier Excel :
    - nom_medicament
    - type_medicament
    - indication_1, indication_2, ...
    - contre_indication_1, contre_indication_2, ...
    - interaction_1, interaction_2, ...
    - effet_indesirable_1, effet_indesirable_2, ...
    - precaution_1, precaution_2, ...

    Exemple :
    nom_medicament | type_medicament | indication_1 | indication_2 | ...
    """

    # Lecture du fichier Excel
    df = pd.read_excel(input_excel_path)

    medicaments = []

    for _, row in df.iterrows():

        def extract_fields(prefix):
            """
            Extrait toutes les colonnes commençant par un préfixe.
            Exemple : indication_1, indication_2, ...
            """
            values = []

            for col in df.columns:
                if col.startswith(prefix):
                    value = row[col]

                    if pd.notna(value) and str(value).strip() != "":
                        values.append(str(value).strip())

            return values
        medicament = {
            "nom_medicament": row.get("Nom du médicament", ""),
            "type_medicament": (
                str(row["Type du médicament"]).strip()
                if pd.notna(row.get("Type du médicament"))
                else ""
                ),
            "indications": extract_fields("Indication_"),
            "contre_indications": extract_fields("Contre_indication_"),
            "interactions": extract_fields("Interaction_"),
            "effets_indesirables": extract_fields("Effet_indésirable_"),
            "precautions": extract_fields("Précaution_")
        }

        medicaments.append(medicament)

    # Sauvegarde JSON
    if output_json_path is None:
        output_json_path = Path(input_excel_path).with_suffix(".json")

    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(medicaments, f, ensure_ascii=False, indent=4)

    print(f"JSON sauvegardé dans : {output_json_path}")


# Exemple d'utilisation
if __name__ == "__main__":
    excel_to_json("medicaments.xlsx")



def save_sorted_lists_separately(json_path, output_dir=None):
    """
    Lit le fichier médicaments.json et crée plusieurs fichiers JSON :
    - types_medicaments.json
    - indications.json
    - contre_indications.json
    - interactions.json
    - effets_indesirables.json
    - precautions.json
    """

    # Chargement du JSON principal
    with open(json_path, "r", encoding="utf-8") as f:
        medicaments = json.load(f)

    # Dossier de sortie
    if output_dir is None:
        output_dir = Path(json_path).parent

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sets pour éviter les doublons
    data = {
        "type_medicament": set(),
        "indications": set(),
        "contre_indications": set(),
        "interactions": set(),
        "effets_indesirables": set(),
        "precautions": set()
    }

    # Extraction des données
    for med in medicaments:

        # Type médicament
        type_med = med.get("type_medicament")
        print(type_med)
        if type_med and str(type_med).strip():
            data["type_medicament"].add(str(type_med).strip())

        # Indications
        for item in med.get("indications", []):
            if item and str(item).strip():
                data["indications"].add(str(item).strip())

        # Contre-indications
        for item in med.get("contre_indications", []):
            if item and str(item).strip():
                data["contre_indications"].add(str(item).strip())

        # Interactions
        for item in med.get("interactions", []):
            if item and str(item).strip():
                data["interactions"].add(str(item).strip())

        # Effets indésirables
        for item in med.get("effets_indesirables", []):
            if item and str(item).strip():
                data["effets_indesirables"].add(str(item).strip())

        # Précautions
        for item in med.get("precautions", []):
            if item and str(item).strip():
                data["precautions"].add(str(item).strip())

    # Sauvegarde des fichiers séparés
    for filename, values in data.items():

        sorted_values = sorted(values, key=lambda x: x.lower())

        file_path = output_dir / f"{filename}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(sorted_values, f, ensure_ascii=False, indent=4)

        print(f"Créé : {file_path}")


# Exemple d'utilisation
if __name__ == "__main__":

    save_sorted_lists_separately(
        json_path="medicaments.json"
    )





