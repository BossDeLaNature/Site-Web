# -*- coding: utf-8 -*-
"""
Created on Sun May 10 22:10:31 2026

@author: moito
"""

import re
import pandas as pd
from pathlib import Path


def extract_qcm_from_txt(txt_path):
    """
    Extrait les QCM depuis un fichier texte.
    Retourne une liste de dictionnaires.
    """

    # =========================
    # Lecture fichier
    # =========================
    with open(txt_path, "r", encoding="utf-8") as f:
        text = f.read()

    # =========================
    # Suppression en-têtes
    # =========================
    lines = text.splitlines()

    cleaned_lines = []

    for line in lines:

        line = line.strip()

        if not line:
            continue

        if (
            line.upper() == "CARDIO"
            or "Chapitre" in line
        ):
            continue

        cleaned_lines.append(line)

    text = " ".join(cleaned_lines)

    # =========================
    # Force retour ligne avant réponses
    # =========================
    text = re.sub(
        r"(\d+\.\s*(?:Vrai|Faux))",
        r"\n\1",
        text,
        flags=re.IGNORECASE
    )

    # =========================
    # Extraction réponses
    # =========================
    reponses = {}

    for match in re.finditer(
        r"(\d+)\.\s*(Vrai|Faux)",
        text,
        flags=re.IGNORECASE
    ):

        numero = int(match.group(1))
        reponse = match.group(2).capitalize()

        reponses[numero] = reponse

    # =========================
    # Suppression réponses
    # =========================
    questions_text = re.sub(
        r"\d+\.\s*(?:Vrai|Faux)",
        "",
        text,
        flags=re.IGNORECASE
    )

    # =========================
    # Extraction propositions
    # =========================
    questions = {}

    matches = list(re.finditer(r"(\d+)\.\s", questions_text))

    for i, match in enumerate(matches):

        numero = int(match.group(1))

        start = match.end()

        if i < len(matches) - 1:
            end = matches[i + 1].start()
        else:
            end = len(questions_text)

        proposition = questions_text[start:end].strip()

        proposition = re.sub(r"\s+", " ", proposition)

        questions[numero] = proposition

    # =========================
    # Construction résultats
    # =========================
    rows = []

    for numero in sorted(questions.keys()):

        rows.append({
            "numero": numero,
            "proposition": questions[numero],
            "reponse": reponses.get(numero, "")
        })

    return rows


def merge_txt_pages_to_excel(
    input_folder="cardiologie_txt/cardio_1",
    output_excel="cardio_1.xlsx"
):
    """
    Lit tous les page_i.txt d'un dossier
    et fusionne tout dans un seul Excel.
    """

    input_folder = Path(input_folder)

    # Tri page_1, page_2, ...
    txt_files = sorted(
        input_folder.glob("page_*.txt"),
        key=lambda x: int(x.stem.split("_")[1])
    )

    all_rows = []

    # =========================
    # Parcours des pages
    # =========================
    for txt_file in txt_files:

        print(f"Lecture : {txt_file.name}")

        rows = extract_qcm_from_txt(txt_file)

        all_rows.extend(rows)

    # =========================
    # DataFrame final
    # =========================
    df = pd.DataFrame(all_rows)

    # =========================
    # Export Excel
    # =========================
    df.to_excel(output_excel, index=False)

    print(f"\nExcel créé : {output_excel}")


# ==================================
# UTILISATION
# ==================================

if __name__ == "__main__":
    for i in range(15):
        a = str(i+1)
        merge_txt_pages_to_excel(
            input_folder="cardiologie_txt/cardio_"+a,
            output_excel="cardio_"+a+".xlsx"
        )