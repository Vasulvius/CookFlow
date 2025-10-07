import asyncio

from src.infrastructure import get_settings
from src.infrastructure.api_clients.ingredient_api_client import IngredientAPIClient

import streamlit as st

settings = get_settings()
ingredient_api_client = IngredientAPIClient(base_url=f"http://{settings.host}:{settings.port}")


def show():
    st.title("Ingredients 🥗")
    st.write("Here you can add, edit, or delete ingredients.")

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View", "➕ Add", "✏️ Edit", "🗑️ Delete"])

    with tab1:
        _show_ingredients()

    with tab2:
        _add_ingredient()

    with tab3:
        _edit_ingredient()

    with tab4:
        _delete_ingredient()


def _show_ingredients():
    """Display all ingredients."""
    try:
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())

        # Manual refresh button
        if st.button("🔄 Refresh", key="refresh_ingredients"):
            st.rerun()

        if not ingredients:
            st.info("No ingredients found.")
            return

        st.write(f"**Number of ingredients:** {len(ingredients)}")

        # Display in a cleaner format
        for i, ingredient in enumerate(ingredients, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{i}. {ingredient.name}")
                    st.write(f"**Description:** {ingredient.description}")
                    st.caption(f"ID: {ingredient.id}")
                with col2:
                    st.write("")  # Space for alignment

                st.divider()

    except Exception as e:
        st.error(f"Error while fetching ingredients: {e}")


def _add_ingredient():
    """Add a new ingredient."""
    st.subheader("Add a new ingredient")

    with st.form("add_ingredient_form"):
        name = st.text_input("Ingredient name", placeholder="Ex: Tomato")
        description = st.text_area("Description", placeholder="Ex: Red vegetable rich in vitamins")

        submitted = st.form_submit_button("Add ingredient")

        if submitted:
            if not name or not description:
                st.error("Please fill in all fields.")
                return

            try:
                # Here you need to implement the create_ingredient method in your API client
                _ = asyncio.run(ingredient_api_client.create_ingredient(name, description))
                st.success(f"Ingredient '{name}' added successfully!")
                st.balloons()
            except Exception as e:
                st.error(f"Error while adding: {e}")


def _edit_ingredient():
    """Edit an existing ingredient."""
    st.subheader("Edit an ingredient")

    try:
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())

        if not ingredients:
            st.info("No ingredients available for editing.")
            return

        # Select the ingredient to edit
        ingredient_options = {f"{ing.name} ({ing.id})": ing for ing in ingredients}
        selected_key = st.selectbox("Choose an ingredient to edit", list(ingredient_options.keys()))

        if selected_key:
            selected_ingredient = ingredient_options[selected_key]

            with st.form("edit_ingredient_form"):
                name = st.text_input("Name", value=selected_ingredient.name)
                description = st.text_area("Description", value=selected_ingredient.description)

                submitted = st.form_submit_button("Edit ingredient")

                if submitted:
                    if not name or not description:
                        st.error("Please fill in all fields.")
                        return

                    try:
                        # Here you need to implement the update_ingredient method in your API client
                        _ = asyncio.run(ingredient_api_client.update_ingredient(selected_ingredient.id, name, description))
                        st.success(f"Ingredient '{name}' updated successfully!")
                    except Exception as e:
                        st.error(f"Error while editing: {e}")

    except Exception as e:
        st.error(f"Error while fetching ingredients: {e}")


def _delete_ingredient():
    """Delete an ingredient."""
    st.subheader("Delete an ingredient")
    st.warning("⚠️ This action is irreversible!")

    try:
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())

        if not ingredients:
            st.info("No ingredients available for deletion.")
            return

        # Select the ingredient to delete
        ingredient_options = {f"{ing.name} - {ing.description[:50]}...": ing for ing in ingredients}
        selected_key = st.selectbox("Choose an ingredient to delete", list(ingredient_options.keys()))

        if selected_key:
            selected_ingredient = ingredient_options[selected_key]

            st.write(f"**Selected ingredient:** {selected_ingredient.name}")
            st.write(f"**Description:** {selected_ingredient.description}")

            # Deletion confirmation
            confirm = st.checkbox("I confirm I want to delete this ingredient")

            if st.button("🗑️ Delete", type="primary", disabled=not confirm):
                try:
                    # Here you need to implement the delete_ingredient method in your API client
                    success = asyncio.run(ingredient_api_client.delete_ingredient(selected_ingredient.id))
                    if success:
                        st.success(f"Ingredient '{selected_ingredient.name}' deleted successfully!")
                    else:
                        st.error("Error while deleting.")
                except Exception as e:
                    st.error(f"Error while deleting: {e}")

    except Exception as e:
        st.error(f"Error while fetching ingredients: {e}")
