import json
import pandas as pd
from pathlib import Path
import os

# ==================================================
# CONFIGURATION DOSSIER
# ==================================================

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# ==================================================
# EXCEL -> JSON PRINCIPAL
# ==================================================

def excel_to_json(input_excel_path, output_json_path=None):

    # Lecture Excel
    df = pd.read_excel(input_excel_path)

    medicaments = []

    for _, row in df.iterrows():

        # ==========================================
        # Extraction colonnes multiples
        # ==========================================
        def extract_fields(prefix):

            values = []

            for col in df.columns:

                if col.startswith(prefix):

                    value = row[col]

                    if pd.notna(value) and str(value).strip() != "":
                        values.append(str(value).strip())

            return values

        # ==========================================
        # Objet médicament
        # ==========================================
        medicament = {

            "nom_medicament": (
                str(row.get("Nom du médicament", "")).strip()
            ),

            "type_medicament": (
                str(row["Type du médicament"]).strip()
                if pd.notna(row.get("Type du médicament"))
                else ""
            ),

            "classe_medicament": (
                str(row["Classe_médicament"]).strip()
                if pd.notna(row.get("Classe_médicament"))
                else ""
            ),

            "classe_medicament_2": (
                str(row["Classe_médicament_2"]).strip()
                if pd.notna(row.get("Classe_médicament_2"))
                else ""
            ),

            "indications": extract_fields("Indication_"),

            "contre_indications": extract_fields("Contre_indication_"),

            "interactions": extract_fields("Interaction_"),

            "effets_indesirables": extract_fields("Effet_indésirable_"),

            "precautions": extract_fields("Précaution_")
        }

        medicaments.append(medicament)

    # ==========================================
    # Sauvegarde JSON
    # ==========================================
    if output_json_path is None:
        output_json_path = Path(input_excel_path).with_suffix(".json")

    with open(output_json_path, "w", encoding="utf-8") as f:

        json.dump(
            medicaments,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"JSON sauvegardé : {output_json_path}")


# ==================================================
# EXTRACTION LISTES TRIÉES
# ==================================================

def save_sorted_lists_separately(json_path, output_dir=None):

    # ==========================================
    # Chargement JSON
    # ==========================================
    with open(json_path, "r", encoding="utf-8") as f:

        medicaments = json.load(f)

    # ==========================================
    # Dossier sortie
    # ==========================================
    if output_dir is None:
        output_dir = Path(json_path).parent

    output_dir = Path(output_dir)

    output_dir.mkdir(parents=True, exist_ok=True)

    # ==========================================
    # Structures
    # ==========================================
    data = {

        "type_medicament": set(),

        "classe_medicament": set(),

        "classe_medicament_2": set(),

        "indications": set(),

        "contre_indications": set(),

        "interactions": set(),

        "effets_indesirables": set(),

        "precautions": set()
    }

    # ==========================================
    # Extraction données
    # ==========================================
    for med in medicaments:

        # --------------------------------------
        # Type médicament
        # --------------------------------------
        type_med = med.get("type_medicament")

        if type_med and str(type_med).strip():

            data["type_medicament"].add(
                str(type_med).strip()
            )

        # --------------------------------------
        # Classe médicament
        # --------------------------------------
        classe_med = med.get("classe_medicament")

        if classe_med and str(classe_med).strip():

            data["classe_medicament"].add(
                str(classe_med).strip()
            )

        # --------------------------------------
        # Classe médicament 2
        # --------------------------------------
        classe_med_2 = med.get("classe_medicament_2")

        if classe_med_2 and str(classe_med_2).strip():

            data["classe_medicament_2"].add(
                str(classe_med_2).strip()
            )

        # --------------------------------------
        # Indications
        # --------------------------------------
        for item in med.get("indications", []):

            if item and str(item).strip():

                data["indications"].add(
                    str(item).strip()
                )

        # --------------------------------------
        # Contre indications
        # --------------------------------------
        for item in med.get("contre_indications", []):

            if item and str(item).strip():

                data["contre_indications"].add(
                    str(item).strip()
                )

        # --------------------------------------
        # Interactions
        # --------------------------------------
        for item in med.get("interactions", []):

            if item and str(item).strip():

                data["interactions"].add(
                    str(item).strip()
                )

        # --------------------------------------
        # Effets indésirables
        # --------------------------------------
        for item in med.get("effets_indesirables", []):

            if item and str(item).strip():

                data["effets_indesirables"].add(
                    str(item).strip()
                )

        # --------------------------------------
        # Précautions
        # --------------------------------------
        for item in med.get("precautions", []):

            if item and str(item).strip():

                data["precautions"].add(
                    str(item).strip()
                )

    # ==========================================
    # Sauvegarde JSON séparés
    # ==========================================
    for filename, values in data.items():

        sorted_values = sorted(
            values,
            key=lambda x: x.lower()
        )

        file_path = output_dir / f"{filename}.json"

        with open(file_path, "w", encoding="utf-8") as f:

            json.dump(
                sorted_values,
                f,
                ensure_ascii=False,
                indent=4
            )

        print(f"Créé : {file_path}")


# ==================================================
# UTILISATION
# ==================================================

if __name__ == "__main__":

    # Création medicaments.json
    excel_to_json(
        input_excel_path="medicaments.xlsx"
    )

    # Création fichiers séparés
    save_sorted_lists_separately(
        json_path="medicaments.json"
    )