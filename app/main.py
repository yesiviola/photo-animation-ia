# app/main.py

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from app.api.image_router     import router as image_router
from app.api.animation_router import router as animation_router
from app.api.auth_router      import router as auth_router
from app.api.videos_router    import router as videos_router
from app.database             import init_db

# Configuramos el rate-limiter de slowapi
limiter = Limiter(key_func=get_remote_address)

def create_app() -> FastAPI:
    app = FastAPI(
        title="Photo Animation IA",
        description="Backend para el proyecto Photo Animation IA",
        version="1.0.0"
    )

    # Inicializa la base de datos
    init_db()

    # ✨ CORS abierto durante desarrollo para descartar bloqueos
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],     
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate-limiting middleware (SlowAPI)
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Montamos los routers
    app.include_router(image_router,      prefix="/images",    tags=["Images"])
    app.include_router(animation_router,  prefix="/animation", tags=["Animation"])
    app.include_router(auth_router,       prefix="/auth",      tags=["Auth"])
    app.include_router(videos_router,     prefix="/videos",    tags=["Videos"])

    # Endpoint de prueba
    @app.get("/test")
    @limiter.limit("5/minute")
    def test_endpoint(request: Request):
        return {"message": "Hasta 5 requests por minuto"}

    return app

# Creamos la app
app = create_app()
