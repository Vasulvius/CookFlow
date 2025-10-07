import asyncio

from src.infrastructure import get_settings
from src.infrastructure.api_clients.ingredient_api_client import IngredientAPIClient
from src.infrastructure.api_clients.recipe_api_client import RecipeAPIClient
from src.infrastructure.api_clients.recipe_ingredient_api_client import (
    RecipeIngredientAPIClient,
)

import streamlit as st

settings = get_settings()
recipe_api_client = RecipeAPIClient(base_url=f"http://{settings.host}:{settings.port}")
ingredient_api_client = IngredientAPIClient(base_url=f"http://{settings.host}:{settings.port}")
recipe_ingredient_api_client = RecipeIngredientAPIClient(base_url=f"http://{settings.host}:{settings.port}")


def show():
    st.title("Recipes 🍳")
    st.write("Here you can add, edit or delete recipes with their ingredients.")

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View", "➕ Add", "✏️ Edit", "🗑️ Delete"])

    with tab1:
        _show_recipes()

    with tab2:
        _add_recipe()

    with tab3:
        _edit_recipe()

    with tab4:
        _delete_recipe()


async def _get_recipe_with_ingredients(recipe):
    """Helper function to get recipe with its ingredients."""
    recipe_ingredients = await recipe_ingredient_api_client.get_recipe_ingredients_by_recipe_id(recipe.id)
    recipe.ingredients = recipe_ingredients
    return recipe


def _show_recipes():
    """Display all recipes with their ingredients."""
    try:
        recipes = asyncio.run(recipe_api_client.get_recipes())

        # Manual refresh button
        if st.button("🔄 Refresh", key="refresh_recipes"):
            st.rerun()

        if not recipes:
            st.info("No recipes found.")
            return

        st.write(f"**Number of recipes:** {len(recipes)}")

        # Display in a cleaner format
        for i, recipe in enumerate(recipes, 1):
            # Get ingredients for this recipe
            recipe_with_ingredients = asyncio.run(_get_recipe_with_ingredients(recipe))

            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{i}. {recipe_with_ingredients.name}")
                    st.write(f"**Description:** {recipe_with_ingredients.description}")

                    # Display ingredients
                    if recipe_with_ingredients.ingredients:
                        st.write("**Ingredients:**")
                        for ri in recipe_with_ingredients.ingredients:
                            # Get ingredient details
                            try:
                                ingredients = asyncio.run(ingredient_api_client.get_ingredients())
                                ingredient = next((ing for ing in ingredients if ing.id == ri.ingredient_id), None)
                                if ingredient:
                                    st.write(f"• {ingredient.name}: {ri.quantity} {ri.unit}")
                            except Exception:
                                st.write(f"• Ingredient ID {ri.ingredient_id}: {ri.quantity} {ri.unit}")
                    else:
                        st.write("**Ingredients:** None")

                    st.caption(f"ID: {recipe_with_ingredients.id}")
                with col2:
                    st.write("")  # Space for alignment

                st.divider()

    except Exception as e:
        st.error(f"Error retrieving recipes: {e}")


def _add_recipe():
    """Add a new recipe with ingredients."""
    st.subheader("Add a new recipe")

    try:
        # Get available ingredients
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())
        ingredient_options = {f"{ing.name}": ing for ing in ingredients}

        with st.form("add_recipe_form"):
            name = st.text_input("Recipe name", placeholder="e.g. Pasta Carbonara")
            description = st.text_area("Description", placeholder="e.g. Traditional Italian pasta dish with eggs and bacon")

            st.subheader("Ingredients")

            # Dynamic ingredient selection
            if "recipe_ingredients" not in st.session_state:
                st.session_state.recipe_ingredients = []

            # Add ingredient section
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            with col1:
                selected_ingredient = st.selectbox("Select ingredient", [""] + list(ingredient_options.keys()), key="new_ingredient")
            with col2:
                quantity = st.number_input("Quantity", min_value=0.0, step=0.1, key="new_quantity")
            with col3:
                unit = st.text_input("Unit", placeholder="g, ml, pcs", key="new_unit")
            with col4:
                if st.form_submit_button("Add Ingredient", use_container_width=True):
                    if selected_ingredient and quantity > 0 and unit:
                        ingredient = ingredient_options[selected_ingredient]
                        st.session_state.recipe_ingredients.append({"ingredient": ingredient, "quantity": quantity, "unit": unit})
                        st.rerun()

            # Display current ingredients
            if st.session_state.recipe_ingredients:
                st.write("**Selected Ingredients:**")
                for i, ri in enumerate(st.session_state.recipe_ingredients):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.write(f"• {ri['ingredient'].name}: {ri['quantity']} {ri['unit']}")
                    with col2:
                        if st.form_submit_button("Remove", key=f"remove_{i}", use_container_width=True):
                            st.session_state.recipe_ingredients.pop(i)
                            st.rerun()

            submitted = st.form_submit_button("Add recipe")

            if submitted:
                if not name:
                    st.error("Please fill in all required fields.")
                    return

                try:
                    # Create the recipe first
                    created_recipe = asyncio.run(recipe_api_client.create_recipe(name, description))

                    # Add ingredients to the recipe
                    for ri in st.session_state.recipe_ingredients:
                        asyncio.run(
                            recipe_ingredient_api_client.create_recipe_ingredient(
                                recipe_id=created_recipe.id, ingredient_id=ri["ingredient"].id, quantity=ri["quantity"], unit=ri["unit"]
                            )
                        )

                    st.success(f"Recipe '{name}' added successfully with {len(st.session_state.recipe_ingredients)} ingredients!")
                    st.session_state.recipe_ingredients = []  # Clear the ingredients
                    st.balloons()
                except Exception as e:
                    st.error(f"Error adding recipe: {e}")

    except Exception as e:
        st.error(f"Error loading ingredients: {e}")


def _edit_recipe():
    """Edit an existing recipe and its ingredients."""
    st.subheader("Edit a recipe")

    try:
        recipes = asyncio.run(recipe_api_client.get_recipes())
        ingredients = asyncio.run(ingredient_api_client.get_ingredients())
        ingredient_options = {f"{ing.name}": ing for ing in ingredients}

        if not recipes:
            st.info("No recipes available for editing.")
            return

        # Recipe selection for editing
        recipe_options = {f"{recipe.name} ({recipe.id})": recipe for recipe in recipes}
        selected_key = st.selectbox("Choose a recipe to edit", list(recipe_options.keys()))

        if selected_key:
            selected_recipe = recipe_options[selected_key]

            # Get current recipe ingredients
            current_recipe_ingredients = asyncio.run(recipe_ingredient_api_client.get_recipe_ingredients_by_recipe_id(selected_recipe.id))

            # Initialize session state for editing
            if "edit_recipe_ingredients" not in st.session_state:
                st.session_state.edit_recipe_ingredients = []
                # Load current ingredients
                for ri in current_recipe_ingredients:
                    ingredient = next((ing for ing in ingredients if ing.id == ri.ingredient_id), None)
                    if ingredient:
                        st.session_state.edit_recipe_ingredients.append(
                            {"id": ri.id, "ingredient": ingredient, "quantity": ri.quantity, "unit": ri.unit}
                        )

            with st.form("edit_recipe_form"):
                name = st.text_input("Name", value=selected_recipe.name)
                description = st.text_area("Description", value=selected_recipe.description)

                st.subheader("Ingredients")

                # Add new ingredient section
                col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                with col1:
                    new_ingredient = st.selectbox("Add ingredient", [""] + list(ingredient_options.keys()), key="edit_new_ingredient")
                with col2:
                    new_quantity = st.number_input("Quantity", min_value=0.0, step=0.1, key="edit_new_quantity")
                with col3:
                    new_unit = st.text_input("Unit", placeholder="g, ml, pcs", key="edit_new_unit")
                with col4:
                    if st.form_submit_button("Add", use_container_width=True):
                        if new_ingredient and new_quantity > 0 and new_unit:
                            ingredient = ingredient_options[new_ingredient]
                            st.session_state.edit_recipe_ingredients.append(
                                {"id": None, "ingredient": ingredient, "quantity": new_quantity, "unit": new_unit}  # New ingredient
                            )
                            st.rerun()

                # Display and edit current ingredients
                if st.session_state.edit_recipe_ingredients:
                    st.write("**Current Ingredients:**")
                    for i, ri in enumerate(st.session_state.edit_recipe_ingredients):
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
                        with col1:
                            st.write(f"{ri['ingredient'].name}")
                        with col2:
                            new_qty = st.number_input("Qty", value=ri["quantity"], min_value=0.0, step=0.1, key=f"edit_qty_{i}")
                            st.session_state.edit_recipe_ingredients[i]["quantity"] = new_qty
                        with col3:
                            new_unit = st.text_input("Unit", value=ri["unit"], key=f"edit_unit_{i}")
                            st.session_state.edit_recipe_ingredients[i]["unit"] = new_unit
                        with col4:
                            if st.form_submit_button("Remove", key=f"edit_remove_{i}", use_container_width=True):
                                st.session_state.edit_recipe_ingredients.pop(i)
                                st.rerun()

                submitted = st.form_submit_button("Update recipe")

                if submitted:
                    if not name or not description:
                        st.error("Please fill in all required fields.")
                        return

                    try:
                        # Update the recipe
                        _ = asyncio.run(recipe_api_client.update_recipe(selected_recipe.id, name, description))

                        # Delete all existing recipe ingredients
                        asyncio.run(recipe_ingredient_api_client.delete_all_for_recipe(selected_recipe.id))

                        # Add all ingredients (updated and new)
                        for ri in st.session_state.edit_recipe_ingredients:
                            asyncio.run(
                                recipe_ingredient_api_client.create_recipe_ingredient(
                                    recipe_id=selected_recipe.id,
                                    ingredient_id=ri["ingredient"].id,
                                    quantity=ri["quantity"],
                                    unit=ri["unit"],
                                )
                            )

                        st.success(f"Recipe '{name}' updated successfully!")
                        st.session_state.edit_recipe_ingredients = []  # Clear the session state
                    except Exception as e:
                        st.error(f"Error updating recipe: {e}")

    except Exception as e:
        st.error(f"Error retrieving data: {e}")


def _delete_recipe():
    """Delete a recipe and its ingredients."""
    st.subheader("Delete a recipe")
    st.warning("⚠️ This action is irreversible!")

    try:
        recipes = asyncio.run(recipe_api_client.get_recipes())

        if not recipes:
            st.info("No recipes available for deletion.")
            return

        # Recipe selection for deletion
        recipe_options = {f"{recipe.name} - {recipe.description[:50]}...": recipe for recipe in recipes}
        selected_key = st.selectbox("Choose a recipe to delete", list(recipe_options.keys()))

        if selected_key:
            selected_recipe = recipe_options[selected_key]

            st.write(f"**Selected recipe:** {selected_recipe.name}")
            st.write(f"**Description:** {selected_recipe.description}")

            # Show ingredients that will be deleted
            recipe_ingredients = asyncio.run(recipe_ingredient_api_client.get_recipe_ingredients_by_recipe_id(selected_recipe.id))
            if recipe_ingredients:
                st.write(f"**This will also delete {len(recipe_ingredients)} associated ingredients.**")

            # Deletion confirmation
            confirm = st.checkbox("I confirm I want to delete this recipe and all its ingredients")

            if st.button("🗑️ Delete", type="primary", disabled=not confirm):
                try:
                    # Delete recipe ingredients first
                    asyncio.run(recipe_ingredient_api_client.delete_all_for_recipe(selected_recipe.id))

                    # Then delete the recipe
                    success = asyncio.run(recipe_api_client.delete_recipe(selected_recipe.id))
                    if success:
                        st.success(f"Recipe '{selected_recipe.name}' and its ingredients deleted successfully!")
                    else:
                        st.error("Error during deletion.")
                except Exception as e:
                    st.error(f"Error deleting recipe: {e}")

    except Exception as e:
        st.error(f"Error retrieving recipes: {e}")
