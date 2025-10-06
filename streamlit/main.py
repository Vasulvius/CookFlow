from pages import accueil, ingredients

import streamlit as st

st.set_page_config(page_title="CookFlow", layout="wide")

PAGES = {
    "Accueil": accueil.show,
    "Ingrédients": ingredients.show,
    # "Recettes": recettes.show,
    # "Planning": planning.show,
}

st.sidebar.title("Navigation")
choice = st.sidebar.radio("Aller à", list(PAGES.keys()))

page = PAGES[choice]
page()
