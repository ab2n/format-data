import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Fusion de fichiers Excel en un seul fichier")

# Upload multiple fichiers
uploaded_files = st.file_uploader("Upload des fichiers Excel", type=["xlsx"], accept_multiple_files=True)

if uploaded_files:
    st.write(f"{len(uploaded_files)} fichier(s) uploadé(s).")

    # Préparer un fichier Excel en mémoire
    output = BytesIO()

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        for uploaded_file in uploaded_files:
            # Lire chaque fichier Excel
            try:
                df = pd.read_excel(uploaded_file)
                # Nommer la feuille avec le nom du fichier sans extension
                sheet_name = uploaded_file.name.replace(".xlsx", "")
                # Écrire dans le fichier final
                df.to_excel(writer, index=False, sheet_name=sheet_name[:31])  # max 31 chars pour nom feuille
            except Exception as e:
                st.error(f"Impossible de lire {uploaded_file.name}: {e}")

        writer.save()
        output.seek(0)

    st.success("Fichiers fusionnés avec succès !")
    st.download_button(
        label="Télécharger le fichier fusionné",
        data=output,
        file_name="fichier_fusionné.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
