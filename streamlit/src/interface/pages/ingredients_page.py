import asyncio

from src.infrastructure import get_settings
from src.infrastructure.api_clients.ingredient_api_client import IngredientAPIClient

import streamlit as st

settings = get_settings()
ingredient_api_client = IngredientAPIClient(base_url=f"http://{settings.host}:{settings.port}")


def show():
    st.title("Ingrédients 🥗")
    st.write("Ici tu peux ajouter, modifier ou supprimer des ingrédients.")

    # Créer les onglets
    tab1, tab2, tab3, tab4 = st.tabs(["📋 Voir", "➕ Ajouter", "✏️ Modifier", "🗑️ Supprimer"])

    with tab1:
        _show_ingredients()

    with tab2:
        _add_ingredient()

    with tab3:
        _edit_ingredient()

    with tab4:
        _delete_ingredient()


def _show_ingredients():
    """Afficher tous les ingrédients."""
    try:
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())

        if not ingredients:
            st.info("Aucun ingrédient trouvé.")
            return

        st.write(f"**Nombre d'ingrédients :** {len(ingredients)}")

        # Bouton de rafraîchissement manuel
        if st.button("🔄 Rafraîchir", key="refresh_ingredients"):
            st.rerun()

        # Afficher dans un format plus propre
        for i, ingredient in enumerate(ingredients, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{i}. {ingredient.name}")
                    st.write(f"**Description :** {ingredient.description}")
                    st.caption(f"ID: {ingredient.id}")
                with col2:
                    st.write("")  # Espace pour alignement

                st.divider()

    except Exception as e:
        st.error(f"Erreur lors de la récupération des ingrédients: {e}")


def _add_ingredient():
    """Ajouter un nouvel ingrédient."""
    st.subheader("Ajouter un nouvel ingrédient")

    with st.form("add_ingredient_form"):
        name = st.text_input("Nom de l'ingrédient", placeholder="Ex: Tomate")
        description = st.text_area("Description", placeholder="Ex: Légume rouge riche en vitamines")

        submitted = st.form_submit_button("Ajouter l'ingrédient")

        if submitted:
            if not name or not description:
                st.error("Veuillez remplir tous les champs.")
                return

            try:
                # Ici vous devrez implémenter la méthode create_ingredient dans votre client API
                _ = asyncio.run(ingredient_api_client.create_ingredient(name, description))
                st.success(f"Ingrédient '{name}' ajouté avec succès!")
                st.balloons()
            except Exception as e:
                st.error(f"Erreur lors de l'ajout: {e}")


def _edit_ingredient():
    """Modifier un ingrédient existant."""
    st.subheader("Modifier un ingrédient")

    try:
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())

        if not ingredients:
            st.info("Aucun ingrédient disponible pour modification.")
            return

        # Sélection de l'ingrédient à modifier
        ingredient_options = {f"{ing.name} ({ing.id})": ing for ing in ingredients}
        selected_key = st.selectbox("Choisir un ingrédient à modifier", list(ingredient_options.keys()))

        if selected_key:
            selected_ingredient = ingredient_options[selected_key]

            with st.form("edit_ingredient_form"):
                name = st.text_input("Nom", value=selected_ingredient.name)
                description = st.text_area("Description", value=selected_ingredient.description)

                submitted = st.form_submit_button("Modifier l'ingrédient")

                if submitted:
                    if not name or not description:
                        st.error("Veuillez remplir tous les champs.")
                        return

                    try:
                        # Ici vous devrez implémenter la méthode update_ingredient dans votre client API
                        _ = asyncio.run(ingredient_api_client.update_ingredient(selected_ingredient.id, name, description))
                        st.success(f"Ingrédient '{name}' modifié avec succès!")
                    except Exception as e:
                        st.error(f"Erreur lors de la modification: {e}")

    except Exception as e:
        st.error(f"Erreur lors de la récupération des ingrédients: {e}")


def _delete_ingredient():
    """Supprimer un ingrédient."""
    st.subheader("Supprimer un ingrédient")
    st.warning("⚠️ Cette action est irréversible!")

    try:
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())

        if not ingredients:
            st.info("Aucun ingrédient disponible pour suppression.")
            return

        # Sélection de l'ingrédient à supprimer
        ingredient_options = {f"{ing.name} - {ing.description[:50]}...": ing for ing in ingredients}
        selected_key = st.selectbox("Choisir un ingrédient à supprimer", list(ingredient_options.keys()))

        if selected_key:
            selected_ingredient = ingredient_options[selected_key]

            st.write(f"**Ingrédient sélectionné :** {selected_ingredient.name}")
            st.write(f"**Description :** {selected_ingredient.description}")

            # Confirmation de suppression
            confirm = st.checkbox("Je confirme vouloir supprimer cet ingrédient")

            if st.button("🗑️ Supprimer", type="primary", disabled=not confirm):
                try:
                    # Ici vous devrez implémenter la méthode delete_ingredient dans votre client API
                    success = asyncio.run(ingredient_api_client.delete_ingredient(selected_ingredient.id))
                    if success:
                        st.success(f"Ingrédient '{selected_ingredient.name}' supprimé avec succès!")
                    else:
                        st.error("Erreur lors de la suppression.")
                except Exception as e:
                    st.error(f"Erreur lors de la suppression: {e}")

    except Exception as e:
        st.error(f"Erreur lors de la récupération des ingrédients: {e}")
