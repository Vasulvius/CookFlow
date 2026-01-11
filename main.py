import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from api.infrastructure.web.router_registry import RouterRegistry

load_dotenv()

app = FastAPI(title="Cookflow", description="", version="1.0.0")

RouterRegistry(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
