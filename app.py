import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.title("Formatteur de numéros de téléphone FR 🇫🇷")

def format_phone_number(number):
    """
    Formate un numéro de téléphone français en 06.XX.XX.XX.XX
    """
    try:
        # Convertit en string et supprime tout caractère non numérique
        digits = re.sub(r'\D', '', str(number))

        # Cas des numéros sans 0 initial
        if len(digits) == 9:
            digits = '0' + digits
        # Cas très incomplets : on assume 06 au début
        elif len(digits) == 8:
            digits = '06' + digits
        # Si format bizarre, on renvoie tel quel
        elif len(digits) != 10:
            return str(number)

        # Formate avec des points tous les deux chiffres
        return '.'.join([digits[i:i+2] for i in range(0, 10, 2)])
    except:
        return str(number)

st.write("Vous pouvez soit uploader un fichier Excel, soit coller vos numéros directement (1 par ligne).")

# --- Upload fichier Excel ---
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx", "xls"])
numbers_list = []

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.write("Aperçu du fichier uploadé :")
        st.dataframe(df.head())

        # Essaye de récupérer la colonne A
        if "A" in df.columns:
            numbers_list = df["A"].tolist()
        else:
            # Sinon prend la première colonne
            numbers_list = df.iloc[:,0].tolist()
            st.warning("Colonne 'A' non trouvée. La première colonne a été utilisée.")
    except Exception as e:
        st.error(f"Erreur lors de la lecture du fichier Excel : {e}")

# --- Textarea pour coller les numéros ---
text_input = st.text_area("Ou collez vos numéros ici (1 par ligne)")
if text_input:
    numbers_list = text_input.splitlines()

# --- Formattage ---
if numbers_list:
    formatted_numbers = [format_phone_number(n) for n in numbers_list]
    st.write("✅ Numéros formatés :")
    st.text('\n'.join([str(n) for n in formatted_numbers]))

    # --- Bouton pour télécharger le fichier Excel ---
    df_result = pd.DataFrame({"Numéros formatés": formatted_numbers})
    towrite = BytesIO()
    df_result.to_excel(towrite, index=False, engine='openpyxl')
    towrite.seek(0)
    st.download_button(
        label="Télécharger le fichier Excel formaté",
        data=towrite,
        file_name="numeros_formates.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
