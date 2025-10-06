# 🍳 CookFlow

[![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.118+-green.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.50+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![uv](https://img.shields.io/badge/uv-workspace-blue.svg)](https://docs.astral.sh/uv/)

CookFlow is a modern cooking recipe management system with a REST API backend and a Streamlit frontend. Built with FastAPI and SQLModel, it provides an intuitive interface to manage recipes, ingredients, and meal planning.

## ✨ Features

- 🔧 **Full CRUD operations** for recipes, ingredients, and menus
- 📊 **Robust data models** with SQLModel
- 🗄️ **Async database management** with SQLAlchemy
- ⚙️ **Flexible configuration** via environment variables
- 📚 **Interactive API documentation** with Swagger UI
- 🖥️ **User-friendly web interface** with Streamlit
- 🚀 **Optimized performance** with async FastAPI
- 🔍 **Automatic data validation**
- 📅 **Meal planning system** with menu management
- 🛒 **Shopping list generation** (planned)

## 📋 Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- SQLite database (default)

## 🚀 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/cookflow.git
   cd cookflow
   ```

2. **Install uv (if not already installed):**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Install dependencies:**
   ```bash
   uv sync
   ```

## ⚙️ Configuration

1. **Copy configuration file:**
   ```bash
   cp .env.example .env
   ```

2. **Modify environment variables in `.env`:**
   ```env
   DATABASE_URL=sqlite+aiosqlite:///./cookflow.db
   APP_NAME="CookFlow API"
   APP_VERSION="0.1.0"
   DEBUG=true
   HOST=127.0.0.1
   PORT=8000
   ```

## 🎯 Usage

### Quick Start

Use the provided launch script to start both server and frontend:
```bash
./launch.sh
```

This will start:
- FastAPI server at [http://127.0.0.1:8000](http://127.0.0.1:8000)
- Streamlit interface at [http://127.0.0.1:8501](http://127.0.0.1:8501)

### Manual Start

#### Start the API server
```bash
uv run --package cookflow-server server/main.py
```

#### Start the Streamlit frontend
```bash
uv run --package cookflow-streamlit streamlit run streamlit/main.py
```

### Access Documentation

- **Streamlit Interface:** [http://127.0.0.1:8501](http://127.0.0.1:8501)
- **API Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Redoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### API Usage Examples

#### Create a new ingredient
```bash
curl -X POST "http://127.0.0.1:8000/ingredients/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Tomato",
       "description": "Fresh red tomato"
     }'
```

#### Get all ingredients
```bash
curl -X GET "http://127.0.0.1:8000/ingredients/"
```

#### Create a new recipe
```bash
curl -X POST "http://127.0.0.1:8000/recipes/" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Pasta Carbonara",
       "description": "Traditional Italian pasta dish"
     }'
```

## 📁 Project Structure

```
CookFlow/
├── 📁 server/                     # FastAPI backend
│   ├── 📄 main.py                 # Server entry point
│   └── 📄 pyproject.toml          # Server dependencies
├── 📁 streamlit/                  # Streamlit frontend
│   ├── 📁 src/
│   │   ├── 📁 domain/
│   │   │   └── 📁 entities/       # Data models
│   │   │       ├── ingredient.py
│   │   │       ├── recipe.py
│   │   │       ├── menu.py
│   │   │       └── recipe_ingredient.py
│   │   ├── 📁 infrastructure/
│   │   │   ├── 📁 api_clients/    # API clients
│   │   │   └── settings.py        # Configuration
│   │   └── 📁 interface/
│   │       └── 📁 pages/          # Streamlit pages
│   │           └── ingredients_page.py
│   ├── 📄 main.py                 # Frontend entry point
│   └── 📄 pyproject.toml          # Frontend dependencies
├── 📄 .env.example                # Configuration example
├── 📄 .gitignore                  # Git ignored files
├── 📄 pyproject.toml              # Workspace configuration
├── 📄 launch.sh                   # Launch script
├── 📄 LICENSE                     # MIT License
├── 📄 TODO.md                     # Development roadmap
└── 📄 README.md                   # Documentation
```

## 🚧 Current Status

### ✅ Implemented Features
- [x] Separate backend and frontend workspaces
- [x] Ingredients CRUD API and UI
- [x] Menus CRUD API
- [x] Recipe-ingredient relationship system

### 🔄 In Progress
- [ ] Recipe visual CRUD interface
- [ ] Menu visual CRUD interface  
- [ ] Shopping list generation from menus
- [ ] Data seeding system

### 📋 Planned Features
- [ ] Meal planning interface
- [ ] Unit and integration testing
- [ ] User authentication
- [ ] Recipe import/export
- [ ] Nutritional information

## 🛠️ Development

### Database Management

The application uses SQLite by default. Database file is created automatically at first run.

## 📝 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

<div align="center">
  <p>Made with ❤️ for cooking and coding enthusiasts</p>
</div>