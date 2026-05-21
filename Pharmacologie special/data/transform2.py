import json
import pandas as pd
from pathlib import Path
import os

# ==================================================
# CONFIGURATION DOSSIER
# ==================================================

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# ==================================================
# EXCEL -> JSON MALADIES
# ==================================================

def excel_maladies_to_json(input_excel_path, output_json_path=None):
    """
    Convertit un Excel Maladies.xlsx en JSON structuré.

    Colonnes attendues :
    - Pathologie
    - Chapitre
    - 1ere intention_1, 1ere intention_2, ...
    - 2eme intention_1, 2eme intention_2, ...
    """

    # ==========================================
    # Lecture Excel
    # ==========================================
    df = pd.read_excel(input_excel_path)

    maladies = []

    # ==========================================
    # Parcours lignes
    # ==========================================
    for _, row in df.iterrows():

        # --------------------------------------
        # Extraction colonnes multiples
        # --------------------------------------
        def extract_fields(prefix):

            values = []

            for col in df.columns:

                if col.startswith(prefix):

                    value = row[col]

                    if pd.notna(value) and str(value).strip() != "":

                        values.append(
                            str(value).strip()
                        )

            return values

        # --------------------------------------
        # Objet maladie
        # --------------------------------------
        maladie = {

            "Maladies": (
                str(row.get("Pathologie", "")).strip()
            ),

            "Chapitre": (
                str(row.get("Chapitre", "")).strip()
            ),

            "1ere intention_i": extract_fields(
                "1ere intention_"
            ),

            "2eme intention_i": extract_fields(
                "2eme intention_"
            )
        }

        maladies.append(maladie)

    # ==========================================
    # Sauvegarde JSON
    # ==========================================
    if output_json_path is None:

        output_json_path = Path(
            input_excel_path
        ).with_suffix(".json")

    with open(output_json_path, "w", encoding="utf-8") as f:

        json.dump(
            maladies,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"JSON sauvegardé : {output_json_path}")


# ==================================================
# EXTRACTION LISTES TRIÉES
# ==================================================

def save_sorted_maladies_lists(
    json_path,
    output_dir=None
):
    """
    Génère :
    - pathologies.json
    - chapitres.json
    - premiere_intention.json
    - deuxieme_intention.json
    """

    # ==========================================
    # Chargement JSON
    # ==========================================
    with open(json_path, "r", encoding="utf-8") as f:

        maladies = json.load(f)

    # ==========================================
    # Dossier sortie
    # ==========================================
    if output_dir is None:

        output_dir = Path(json_path).parent

    output_dir = Path(output_dir)

    output_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    # ==========================================
    # Structures
    # ==========================================
    data = {

        "pathologies": set(),

        "chapitres": set(),

        "1ere intention_i": set(),

        "2eme intention_i": set()
    }

    # ==========================================
    # Extraction données
    # ==========================================
    for maladie in maladies:

        # --------------------------------------
        # Pathologie
        # --------------------------------------
        pathologie = maladie.get("pathologie")

        if pathologie and str(pathologie).strip():

            data["pathologies"].add(
                str(pathologie).strip()
            )

        # --------------------------------------
        # Chapitre
        # --------------------------------------
        chapitre = maladie.get("chapitre")

        if chapitre and str(chapitre).strip():

            data["chapitres"].add(
                str(chapitre).strip()
            )

        # --------------------------------------
        # Première intention
        # --------------------------------------
        for item in maladie.get(
            "1ere intention_i",
            []
        ):

            if item and str(item).strip():

                data["1ere intention_i"].add(
                    str(item).strip()
                )

        # --------------------------------------
        # Deuxième intention
        # --------------------------------------
        for item in maladie.get(
            "2eme intention_i",
            []
        ):

            if item and str(item).strip():

                data["2eme intention_i"].add(
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

    # ------------------------------------------
    # Création maladies.json
    # ------------------------------------------
    excel_maladies_to_json(
        input_excel_path="Maladies.xlsx"
    )

    # ------------------------------------------
    # Création fichiers séparés
    # ------------------------------------------
    save_sorted_maladies_lists(
        json_path="Maladies.json"
    )