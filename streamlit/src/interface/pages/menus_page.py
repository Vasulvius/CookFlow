import asyncio
from datetime import date

from src.infrastructure import get_settings
from src.infrastructure.api_clients.menu_api_client import MenuAPIClient
from src.infrastructure.api_clients.recipe_api_client import RecipeAPIClient

import streamlit as st

settings = get_settings()
menu_api_client = MenuAPIClient(base_url=f"http://{settings.host}:{settings.port}")
recipe_api_client = RecipeAPIClient(base_url=f"http://{settings.host}:{settings.port}")


def show():
    st.title("Menus 📅")
    st.write("Here you can add, edit or delete menus.")

    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View", "➕ Add", "✏️ Edit", "🗑️ Delete"])

    with tab1:
        _show_menus()

    with tab2:
        _add_menu()

    with tab3:
        _edit_menu()

    with tab4:
        _delete_menu()


def _show_menus():
    """Display all menus."""
    try:
        menus = asyncio.run(menu_api_client.get_menus())

        # Manual refresh button
        if st.button("🔄 Refresh", key="refresh_menus"):
            st.rerun()

        if not menus:
            st.info("No menus found.")
            return

        st.write(f"**Number of menus:** {len(menus)}")

        # Display in a cleaner format
        for i, menu in enumerate(menus, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.subheader(f"{i}. {menu.name}")
                    st.write(f"**Description:** {menu.description}")
                    st.write(f"**Date:** {menu.scheduled_at}")
                    st.write(f"**Meal type:** {menu.meal_type}")
                    st.write(f"**Number of recipes:** {len(menu.recipe_ids)}")
                    st.caption(f"ID: {menu.id}")
                with col2:
                    st.write("")  # Space for alignment

                st.divider()

    except Exception as e:
        st.error(f"Error retrieving menus: {e}")


def _add_menu():
    """Add a new menu."""
    st.subheader("Add a new menu")

    try:
        # Get available recipes for selection
        recipes = asyncio.run(recipe_api_client.get_recipes())
        recipe_options = {f"{recipe.name}": str(recipe.id) for recipe in recipes}

        with st.form("add_menu_form"):
            name = st.text_input("Menu name", placeholder="e.g. Sunday Lunch")
            description = st.text_area("Description", placeholder="e.g. Family meal for Sunday")
            scheduled_date = st.date_input("Scheduled date", value=date.today())
            meal_type = st.selectbox("Meal type", ["breakfast", "lunch", "dinner"])

            selected_recipes = []
            if recipe_options:
                selected_recipes = st.multiselect(
                    "Select recipes for this menu", options=list(recipe_options.keys()), help="You can select multiple recipes"
                )

            submitted = st.form_submit_button("Add menu")

            if submitted:
                if not name:
                    st.error("Please fill in all required fields.")
                    return

                try:
                    # Convert selected recipe names to IDs
                    recipe_ids = [recipe_options[recipe_name] for recipe_name in selected_recipes]

                    _ = asyncio.run(
                        menu_api_client.create_menu(
                            name=name,
                            description=description,
                            scheduled_at=scheduled_date.isoformat(),
                            meal_type=meal_type,
                            recipe_ids=recipe_ids,
                        )
                    )
                    st.success(f"Menu '{name}' added successfully!")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error adding menu: {e}")

    except Exception as e:
        st.error(f"Error loading recipes: {e}")


def _edit_menu():
    """Edit an existing menu."""
    st.subheader("Edit a menu")

    try:
        menus = asyncio.run(menu_api_client.get_menus())
        recipes = asyncio.run(recipe_api_client.get_recipes())
        recipe_options = {f"{recipe.name}": str(recipe.id) for recipe in recipes}

        if not menus:
            st.info("No menus available for editing.")
            return

        # Menu selection for editing
        menu_options = {f"{menu.name} - {menu.scheduled_at} ({menu.meal_type})": menu for menu in menus}
        selected_key = st.selectbox("Choose a menu to edit", list(menu_options.keys()))

        if selected_key:
            selected_menu = menu_options[selected_key]

            with st.form("edit_menu_form"):
                name = st.text_input("Name", value=selected_menu.name)
                description = st.text_area("Description", value=selected_menu.description)
                scheduled_date = st.date_input("Scheduled date", value=date.fromisoformat(selected_menu.scheduled_at))
                meal_type = st.selectbox(
                    "Meal type", ["breakfast", "lunch", "dinner"], index=["breakfast", "lunch", "dinner"].index(selected_menu.meal_type)
                )

                # Pre-select current recipes
                current_recipe_names = []
                if recipe_options:
                    current_recipe_names = [name for name, id_ in recipe_options.items() if id_ in selected_menu.recipe_ids]

                selected_recipes = st.multiselect(
                    "Select recipes for this menu",
                    options=list(recipe_options.keys()),
                    default=current_recipe_names,
                    help="You can select multiple recipes",
                )

                submitted = st.form_submit_button("Update menu")

                if submitted:
                    if not name or not description:
                        st.error("Please fill in all required fields.")
                        return

                    try:
                        # Convert selected recipe names to IDs
                        recipe_ids = [recipe_options[recipe_name] for recipe_name in selected_recipes]

                        _ = asyncio.run(
                            menu_api_client.update_menu(
                                menu_id=selected_menu.id,
                                name=name,
                                description=description,
                                scheduled_at=scheduled_date.isoformat(),
                                meal_type=meal_type,
                                recipe_ids=recipe_ids,
                            )
                        )
                        st.success(f"Menu '{name}' updated successfully!")
                    except Exception as e:
                        st.error(f"Error updating menu: {e}")

    except Exception as e:
        st.error(f"Error retrieving data: {e}")


def _delete_menu():
    """Delete a menu."""
    st.subheader("Delete a menu")
    st.warning("⚠️ This action is irreversible!")

    try:
        menus = asyncio.run(menu_api_client.get_menus())

        if not menus:
            st.info("No menus available for deletion.")
            return

        # Menu selection for deletion
        menu_options = {f"{menu.name} - {menu.scheduled_at} ({menu.meal_type})": menu for menu in menus}
        selected_key = st.selectbox("Choose a menu to delete", list(menu_options.keys()))

        if selected_key:
            selected_menu = menu_options[selected_key]

            st.write(f"**Selected menu:** {selected_menu.name}")
            st.write(f"**Description:** {selected_menu.description}")
            st.write(f"**Date:** {selected_menu.scheduled_at}")
            st.write(f"**Meal type:** {selected_menu.meal_type}")
            st.write(f"**Number of recipes:** {len(selected_menu.recipe_ids)}")

            # Deletion confirmation
            confirm = st.checkbox("I confirm I want to delete this menu")

            if st.button("🗑️ Delete", type="primary", disabled=not confirm):
                try:
                    success = asyncio.run(menu_api_client.delete_menu(selected_menu.id))
                    if success:
                        st.success(f"Menu '{selected_menu.name}' deleted successfully!")
                    else:
                        st.error("Error during deletion.")
                except Exception as e:
                    st.error(f"Error deleting menu: {e}")

    except Exception as e:
        st.error(f"Error retrieving menus: {e}")
