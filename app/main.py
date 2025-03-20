from fastapi import FastAPI
from app.api.image_router import router as image_router
from app.api.animation_router import router as animation_router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Photo Animation IA",
        description="API para animar fotos con IA (First Order Motion Model)",
        version="0.1.0"
    )
    app.include_router(image_router, prefix="/images", tags=["Images"])
    app.include_router(animation_router, prefix="/animation", tags=["Animation"])
    return app

app = create_app()
