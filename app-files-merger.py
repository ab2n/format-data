import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Agrégation des informations par campagne")

st.markdown("""
Upload tes fichiers Excel (chaque fichier = une campagne).  
Tu pourras choisir la colonne contenant les informations importantes (ex: Email).  
Le script va créer un fichier final avec deux colonnes :  
- `Nom projet` (nom du fichier)  
- `Info` (la colonne choisie)
""")

# Upload multiple fichiers
uploaded_files = st.file_uploader(
    "Upload des fichiers Excel", 
    type=["xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"{len(uploaded_files)} fichier(s) uploadé(s).")

    # Lecture du premier fichier pour permettre de choisir la colonne
    try:
        first_df = pd.read_excel(uploaded_files[0])
        col_to_use = st.selectbox(
            "Choisis la colonne contenant les informations importantes", 
            first_df.columns
        )
    except Exception as e:
        st.error(f"Impossible de lire le premier fichier : {e}")
        st.stop()

    if st.button("Créer le fichier agrégé"):
        all_data = []

        for uploaded_file in uploaded_files:
            try:
                df = pd.read_excel(uploaded_file)
                if col_to_use not in df.columns:
                    st.warning(f"Le fichier {uploaded_file.name} n'a pas de colonne '{col_to_use}'. Ignoré.")
                    continue

                # Créer un DataFrame avec seulement la colonne d'intérêt et le nom du projet
                df_subset = df[[col_to_use]].copy()
                df_subset.rename(columns={col_to_use: "Info"}, inplace=True)
                df_subset['Nom projet'] = uploaded_file.name.replace(".xlsx", "")
                all_data.append(df_subset)

            except Exception as e:
                st.error(f"Impossible de lire {uploaded_file.name}: {e}")

        if all_data:
            # Concaténer tous les fichiers
            df_merged = pd.concat(all_data, ignore_index=True)

            # Optionnel : supprimer les doublons
            df_merged.drop_duplicates(subset=["Info"], inplace=True)

            st.write("Aperçu des données agrégées :")
            st.dataframe(df_merged.head())

            # Préparer le fichier Excel en mémoire
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df_merged.to_excel(writer, index=False, sheet_name="Agrégé")
            output.seek(0)

            st.success("Fichier final prêt !")
            st.download_button(
                label="Télécharger le fichier agrégé",
                data=output,
                file_name="campagnes_agregees.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

