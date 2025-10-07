import asyncio

from src.infrastructure import get_settings
from src.infrastructure.api_clients.unit_api_client import UnitAPIClient

import streamlit as st

settings = get_settings()
unit_api_client = UnitAPIClient(base_url=f"http://{settings.host}:{settings.port}")


def show():
    st.title("Unités 📏")
    st.write("Gérez les unités de mesure et leurs conversions.")

    # Create tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📋 Voir", "➕ Ajouter", "✏️ Modifier", "🗑️ Supprimer", "🔄 Convertir"])

    with tab1:
        _show_units()

    with tab2:
        _add_unit()

    with tab3:
        _edit_unit()

    with tab4:
        _delete_unit()

    with tab5:
        _convert_units()


def _show_units():
    """Affiche toutes les unités."""
    try:
        units = asyncio.run(unit_api_client.get_units())

        if st.button("🔄 Actualiser", key="refresh_units"):
            st.rerun()

        if not units:
            st.info("Aucune unité trouvée.")
            return

        st.write(f"**Nombre d'unités:** {len(units)}")

        # Grouper par type
        volume_units = [u for u in units if u.unit_type == "volume"]
        weight_units = [u for u in units if u.unit_type == "weight"]
        quantity_units = [u for u in units if u.unit_type == "quantity"]

        if volume_units:
            st.subheader("🧪 Volume")
            for unit in volume_units:
                col1, col2 = st.columns([3, 1])
                with col1:
                    base_text = " (unité de base)" if unit.is_base_unit else ""
                    st.write(f"**{unit.name}** ({unit.symbol}){base_text}")
                    st.caption(f"Facteur: {unit.base_conversion_factor}")

        if weight_units:
            st.subheader("⚖️ Poids")
            for unit in weight_units:
                col1, col2 = st.columns([3, 1])
                with col1:
                    base_text = " (unité de base)" if unit.is_base_unit else ""
                    st.write(f"**{unit.name}** ({unit.symbol}){base_text}")
                    st.caption(f"Facteur: {unit.base_conversion_factor}")

        if quantity_units:
            st.subheader("🔢 Quantité")
            for unit in quantity_units:
                col1, col2 = st.columns([3, 1])
                with col1:
                    base_text = " (unité de base)" if unit.is_base_unit else ""
                    st.write(f"**{unit.name}** ({unit.symbol}){base_text}")
                    st.caption(f"Facteur: {unit.base_conversion_factor}")

    except Exception as e:
        st.error(f"Erreur lors de la récupération des unités: {e}")


def _add_unit():
    """Ajoute une nouvelle unité."""
    st.subheader("Ajouter une nouvelle unité")

    with st.form("add_unit_form"):
        name = st.text_input("Nom de l'unité", placeholder="ex: Litre")
        symbol = st.text_input("Symbole", placeholder="ex: l")
        unit_type = st.selectbox("Type d'unité", ["volume", "weight", "quantity"])
        base_conversion_factor = st.number_input("Facteur de conversion", min_value=0.0, step=0.001, value=1.0)
        is_base_unit = st.checkbox("Unité de base pour ce type")

        submitted = st.form_submit_button("Ajouter l'unité")

        if submitted:
            if not name or not symbol:
                st.error("Veuillez remplir tous les champs obligatoires.")
                return

            try:
                _ = asyncio.run(unit_api_client.create_unit(name, symbol, unit_type, base_conversion_factor, is_base_unit))
                st.success(f"Unité '{name}' ajoutée avec succès!")
                st.balloons()
            except Exception as e:
                st.error(f"Erreur lors de l'ajout: {e}")


def _edit_unit():
    """Modifie une unité existante."""
    st.subheader("Modifier une unité")
    st.info("Fonctionnalité à venir...")


def _delete_unit():
    """Supprime une unité existante."""
    st.subheader("Supprimer une unité")
    st.info("Fonctionnalité à venir...")


def _convert_units():
    """Interface de conversion d'unités."""
    st.subheader("Convertir les unités")

    try:
        units = asyncio.run(unit_api_client.get_units())
        unit_symbols = [u.symbol for u in units]

        with st.form("convert_form"):
            value = st.number_input("Valeur à convertir", min_value=0.0, step=0.1, value=1.0)
            from_unit = st.selectbox("De l'unité", unit_symbols)
            to_unit = st.selectbox("Vers l'unité", unit_symbols)

            submitted = st.form_submit_button("Convertir")

            if submitted:
                try:
                    result = asyncio.run(unit_api_client.convert_units(value, from_unit, to_unit))
                    st.success(f"{result['original_value']} {result['from_unit']} = {result['converted_value']:.3f} {result['to_unit']}")
                except Exception as e:
                    st.error(f"Erreur lors de la conversion: {e}")

    except Exception as e:
        st.error(f"Erreur lors du chargement des unités: {e}")
