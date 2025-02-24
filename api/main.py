from fastapi import FastAPI
from src.controllers.ingredient_controller import router as ingredient_router
from src.database import engine
from src.entity.ingredient import SQLModel

app = FastAPI()

# Créer les tables si elles n'existent pas


def create_tables():
    SQLModel.metadata.create_all(engine)


create_tables()

# Inclure les routes
app.include_router(ingredient_router, prefix="/ingredients",
                   tags=["Ingredients"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
