from src.interface.pages import (
    accueil,
    ingredients_page,
    menus_page,
    recipes_page,
    unit_page,
)

import streamlit as st


def main():

    st.set_page_config(page_title="CookFlow", layout="wide")

    PAGES = {
        "Accueil": accueil.show,
        "Ingrédients": ingredients_page.show,
        "Recettes": recipes_page.show,
        "Menus": menus_page.show,
        "Unités": unit_page.show,
    }

    st.sidebar.title("Navigation")
    choice = st.sidebar.radio("Aller à", list(PAGES.keys()))

    page = PAGES[choice]
    page()


if __name__ == "__main__":
    main()
