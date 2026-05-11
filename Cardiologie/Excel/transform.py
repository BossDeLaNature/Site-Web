from pathlib import Path
from PyPDF2 import PdfReader


def extract_text_from_all_pdfs(
    input_folder="cardiologie_pdf",
    output_folder="cardiologie_txt"
):
    """
    Extrait le texte brut page par page
    pour TOUS les PDFs du dossier.

    Structure créée :

    cardiologie_txt/
    ├── cardio_1/
    │   ├── page_1.txt
    │   ├── page_2.txt
    │   └── ...
    │
    ├── cardio_2/
    │   ├── page_1.txt
    │   └── ...
    """

    input_folder = Path(input_folder)
    output_folder = Path(output_folder)

    output_folder.mkdir(exist_ok=True)

    # Tous les PDFs
    pdf_files = sorted(input_folder.glob("*.pdf"))

    if not pdf_files:
        print("Aucun PDF trouvé.")
        return

    # Parcours des PDFs
    for pdf_file in pdf_files:

        print(f"\nTraitement : {pdf_file.name}")

        # Lecture PDF
        reader = PdfReader(pdf_file)

        # Sous-dossier du PDF
        pdf_output_dir = output_folder / pdf_file.stem
        pdf_output_dir.mkdir(exist_ok=True)

        # Parcours des pages
        for i, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text is None:
                text = ""

            # Fichier texte
            output_file = pdf_output_dir / f"page_{i}.txt"

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(text)

            print(f"Créé : {output_file}")


# ==========================================
# UTILISATION
# ==========================================

if __name__ == "__main__":

    extract_text_from_all_pdfs()