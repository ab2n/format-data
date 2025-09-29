import streamlit as st
import pandas as pd
import re
from io import BytesIO

st.title("Formatteur de numéros de téléphone FR 🇫🇷")

def format_phone_number(number):
    # Supprime tout ce qui n'est pas un chiffre
    digits = re.sub(r'\D', '', str(number))
    # Assure que ça commence par 0 et 10 chiffres
    if len(digits) == 9 and digits[0] != "0":
        digits = "0" + digits
    elif len(digits) == 8:  # Cas très mauvais
        digits = "06" + digits  # par défaut on met 06
    elif len(digits) != 10:
        return number  # si format trop bizarre, on laisse tel quel
    # Formate avec points
    return '.'.join([digits[i:i+2] for i in range(0, 10, 2)])

st.write("Vous pouvez soit uploader un fichier Excel, soit coller vos numéros ci-dessous (1 par ligne).")

# --- Upload fichier ---
uploaded_file = st.file_uploader("Choisissez un fichier Excel", type=["xlsx", "xls"])
numbers_list = []

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("Aperçu du fichier uploadé :")
    st.dataframe(df.head())
    if "A" in df.columns:
        numbers_list = df["A"].tolist()
    else:
        st.warning("Aucune colonne 'A' trouvée. Veuillez vous assurer que vos numéros sont dans la colonne A.")

# --- Textarea pour coller les numéros ---
text_input = st.text_area("Ou collez vos numéros ici (1 par ligne)")
if text_input:
    numbers_list = text_input.splitlines()

if numbers_list:
    formatted_numbers = [format_phone_number(n) for n in numbers_list]
    st.write("✅ Numéros formatés :")
    st.text('\n'.join(formatted_numbers))
    
    # --- Télécharger le résultat ---
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
