from api.infrastructure.web.abstract_router import AbstractRouter


class GeneralRouter(AbstractRouter):
    def __init__(self):
        super().__init__(tags=["General"])

    def _register_routes(self):
        @self.router.get("/")
        async def read_root():
            return {"message": "Bonjour depuis FastAPI"}

        @self.router.get("/health")
        async def health():
            return {"status": "ok"}
