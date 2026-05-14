from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter

import os

# --- FORCE LE DOSSIER DE TRAVAIL ---
os.chdir(os.path.dirname(os.path.abspath(__file__)))
def split_pdf(pdf_path, splits):
    """
    Découpe un PDF en plusieurs fichiers.

    Paramètres
    ----------
    pdf_path : str
        Chemin du PDF source

    splits : list of tuples
        Format :
        [
            (page_debut, page_fin),
            (page_debut, page_fin),
            ...
        ]

        ATTENTION :
        Les pages commencent à 1.
        page_fin incluse.

    Exemple :
        [
            (1, 10),
            (11, 25),
            (26, 40)
        ]
    """

    # Lecture du PDF
    reader = PdfReader(pdf_path)

    # Dossier de sortie
    output_dir = Path("cardiologie_pdf")
    output_dir.mkdir(exist_ok=True)

    # Création des PDFs
    for i, (start, end) in enumerate(splits, start=1):

        writer = PdfWriter()

        # Conversion vers index Python
        start_idx = start - 1
        end_idx = end

        # Ajout des pages
        for page_num in range(start_idx, end_idx):

            if page_num < len(reader.pages):
                writer.add_page(reader.pages[page_num])

        # Nom du fichier
        output_file = output_dir / f"Syllab cardio_{i}.pdf"

        # Sauvegarde
        with open(output_file, "wb") as f:
            writer.write(f)

        print(f"Créé : {output_file}")


# ==================================================
# EXEMPLE D'UTILISATION
# ==================================================

if __name__ == "__main__":

    split_pdf(
        pdf_path="syllabus cardio.pdf",

        splits=[

            (9, 14),     # cardio_1.pdf
            (15, 22),    # cardio_2.pdf
            (23, 40), 
            (41, 64),
            (65, 94),
            (95, 122),
            (123, 132),
            (133, 144),
            (145, 156),
            (157, 162),
            (163, 168),
            (169, 176),
            (177, 184),
            (185, 192),
            (193, 203)
            
            
            

        ]
    )