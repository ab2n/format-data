import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Agrégation des emails par campagne")

# Upload multiple fichiers
uploaded_files = st.file_uploader(
    "Upload des fichiers Excel (chaque fichier = une campagne)", 
    type=["xlsx"], 
    accept_multiple_files=True
)

if uploaded_files:
    st.write(f"{len(uploaded_files)} fichier(s) uploadé(s).")

    # Choisir la colonne contenant les emails (assume que tous les fichiers ont la même colonne)
    col_email = st.text_input("Nom de la colonne contenant les emails dans les fichiers", "Email")

    all_data = []

    for uploaded_file in uploaded_files:
        try:
            df = pd.read_excel(uploaded_file)
            if col_email not in df.columns:
                st.warning(f"Le fichier {uploaded_file.name} n'a pas de colonne '{col_email}'. Ignoré.")
                continue
            # Garder uniquement la colonne email et ajouter le nom du projet
            df_subset = df[[col_email]].copy()
            df_subset.rename(columns={col_email: "Email"}, inplace=True)
            df_subset['Nom projet'] = uploaded_file.name.replace(".xlsx", "")
            all_data.append(df_subset)
        except Exception as e:
            st.error(f"Impossible de lire {uploaded_file.name}: {e}")

    if all_data:
        # Concaténer tous les fichiers dans un seul DataFrame
        df_merged = pd.concat(all_data, ignore_index=True)
        # Supprimer les doublons d'email si besoin
        df_merged.drop_duplicates(subset=["Email"], inplace=True)

        st.write("Aperçu des données agrégées :")
        st.dataframe(df_merged.head())

        # Préparer le fichier Excel en mémoire
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_merged.to_excel(writer, index=False, sheet_name="Emails agrégés")
            writer.save()
        output.seek(0)

        st.success("Fichier final prêt !")
        st.download_button(
            label="Télécharger le fichier agrégé",
            data=output,
            file_name="emails_aggreges.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
