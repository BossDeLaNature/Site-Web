import pandas as pd
import time
import os
import sys
from google import genai
from google.genai import types

# --- CONFIGURATION DU DOSSIER ---
# Force Python à travailler dans le dossier du script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# --- PARAMÈTRES ---
API_KEY = "AIzaSyDaPdKhaD7XCvAfHGv_2F0IPsuj7UQkXjA"
EXCEL_ENTREE = "cardio_4.xlsx"
EXCEL_SORTIE = "justifications_finales.xlsx"
PDF_FILE = "Syllab cardio_4.pdf"
MODEL_ID = "gemini-2.0-flash-lite"
BATCH_SIZE = 15  # On réduit un peu la taille pour être plus discret

client = genai.Client(api_key=API_KEY)

def process_cardio():
    try:
        # 1. Chargement des données
        if os.path.exists(EXCEL_SORTIE):
            print(f"Reprise du travail à partir de {EXCEL_SORTIE}...")
            df = pd.read_excel(EXCEL_SORTIE)
        else:
            print(f"Chargement de {EXCEL_ENTREE}...")
            df = pd.read_excel(EXCEL_ENTREE)
        
        total_lignes = len(df)

        # 2. Upload du syllabus
        print(f"Analyse du syllabus : {PDF_FILE}...")
        uploaded_file = client.files.upload(file=PDF_FILE)
        
        while uploaded_file.state.name == "PROCESSING":
            time.sleep(2)
            uploaded_file = client.files.get(name=uploaded_file.name)

        print("\n" + "="*40)
        print(" DEBUT DU TRAITEMENT DES QUESTIONS ")
        print("="*40 + "\n")

        # 3. Boucle par lots
        i = 0
        while i < total_lignes:
            batch_indices = df.index[i : i + BATCH_SIZE]
            
            # On vérifie si tout le lot est déjà rempli
            if df.loc[batch_indices, 'Justification'].notna().all():
                i += BATCH_SIZE
                continue

            # Construction du prompt
            prompt = "Justifie ces propositions en 1 phrase courte selon le syllabus. " \
                     "Pas de 'Vrai' ou 'Faux'. Format strict : " \
                     "ID:[numéro] | JUSTIF:[justification] | PAGE:[page]\n\n"
            
            for idx in batch_indices:
                prop = df.at[idx, 'Proposition']
                prompt += f"ID:{idx} | Prop: {prop}\n"

            try:
                # Requête
                response = client.models.generate_content(
                    model=MODEL_ID,
                    contents=[
                        types.Content(
                            role="user",
                            parts=[
                                types.Part.from_uri(file_uri=uploaded_file.uri, mime_type="application/pdf"),
                                types.Part.from_text(text=prompt),
                            ]
                        )
                    ]
                )

                # Parsing des réponses
                lignes_reponse = response.text.strip().split('\n')
                count_success = 0
                for ligne in lignes_reponse:
                    if "|" in ligne and "ID:" in ligne:
                        try:
                            parts = ligne.split('|')
                            row_id = int(parts[0].split(':')[1].strip())
                            justif_text = parts[1].split(':')[1].strip()
                            page_num = parts[2].split(':')[1].strip()
                            
                            df.at[row_id, 'Justification'] = justif_text
                            df.at[row_id, 'Page'] = page_num
                            count_success += 1
                        except:
                            continue

                # Affichage de l'avancement
                avancement = ((i + BATCH_SIZE) / total_lignes) * 100
                avancement = min(avancement, 100.0)
                print(f"Progression : [{i + BATCH_SIZE}/{total_lignes}] - {avancement:.1f}% TERMINE ✅")
                
                # Sauvegarde intermédiaire
                df.to_excel(EXCEL_SORTIE, index=False)
                
                # Passage au lot suivant
                i += BATCH_SIZE
                time.sleep(15) # Petite pause normale

            except Exception as e:
                if "429" in str(e):
                    print(f"\n[!] QUOTA ATTEINT. Pause forcée de 60 secondes pour respirer...")
                    time.sleep(60) # On attend que le quota se libère
                    # On ne change pas 'i', donc il va retenter le même lot
                else:
                    print(f"\n[!] Erreur inattendue : {e}")
                    time.sleep(10)
                    i += BATCH_SIZE # On passe au suivant si c'est une erreur de contenu

        print("\n" + "="*40)
        print(" TRAVAIL TERMINE AVEC SUCCES ! ")
        print(f" Fichier : {EXCEL_SORTIE}")
        print("="*40)

    except Exception as e:
        print(f"Erreur critique : {e}")

if __name__ == "__main__":
    process_cardio()