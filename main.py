import uvicorn
from fastapi import FastAPI

from api.infrastructure.web.router_registry import RouterRegistry

app = FastAPI(title="Cookflow", description="", version="1.0.0")

RouterRegistry(app)


# Routes
@app.get("/")
async def read_root():
    return {"message": "Bonjour depuis FastAPI"}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
