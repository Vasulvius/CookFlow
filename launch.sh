# !/usr/bin/env python3

# Detecter si le venv est activé et l'activer si ce n'est pas le cas
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -f ".venv/bin/activate" ]; then
        source .venv/bin/activate
        uv sync
    else
        echo "Le venv n'existe pas. Veuillez d'abord créer un environnement virtuel."
        exit 1
    fi
fi

# Lancer le serveur FastAPI
uv run --package cookflow-server server/main.py

# Lancer streamlit
uv run --package cookflow-streamlit streamlit run streamlit/main.py --client.showSidebarNavigation False