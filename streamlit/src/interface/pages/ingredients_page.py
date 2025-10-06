import asyncio

from src.infrastructure import get_settings
from src.infrastructure.api_clients.ingredient_api_client import IngredientAPIClient

import streamlit as st

settings = get_settings()
ingredient_api_client = IngredientAPIClient(base_url=f"http://{settings.host}:{settings.port}")


def show():
    st.title("Ingrédients 🥗")
    st.write("Ici tu peux ajouter, modifier ou supprimer des ingrédients.")

    try:
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())
        st.write(f"Nombre d'ingrédients: {len(ingredients)}")
        for ingredient in ingredients:
            st.header(f"{ingredient.name}")
            st.write(f"  - ID : {ingredient.id}")
            st.write(f"  - Description : {ingredient.description}")
    except Exception as e:
        st.error(f"Erreur lors de la récupération des ingrédients: {e}")
