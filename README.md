# CookFlow

CookFlow is a REST API for managing cooking recipes. It provides endpoints to create, read, update, and delete recipes using FastAPI.

## Features

- Full CRUD operations for recipes
- Data models powered by SQLModel
- Database management with SQLAlchemy Async
- Flexible configuration via environment variables
- Unit and integration testing with Pytest

## Prerequisites

- Python 3.13 or higher
- [Poetry](https://python-poetry.org/) or another dependency manager
- SQLite database (default) or PostgreSQL

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/cookflow.git
   cd cookflow
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment variables:
   Copy the `.env.example` file to `.env` and modify it as needed:
   ```bash
   cp .env.example .env
   ```

## Usage

1. Start the FastAPI server:
   ```bash
   python main.py
   ```

2. Access the interactive API documentation:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Testing

1. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Run the tests:
   ```bash
   pytest
   ```

## Project Structure

```
CookFlow/
├── src/
│   ├── config/          # Application configuration
│   ├── entities/        # Data models
│   ├── infrastructure/  # Routers and database management
│   ├── repositories/    # CRUD operations
│   └── main.py          # Application entry point
├── tests/               # Unit and integration tests
├── .env.example         # Example configuration
├── pyproject.toml       # Project configuration
└── README.md            # Documentation
```

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.