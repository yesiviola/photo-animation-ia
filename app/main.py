from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, PlainTextResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.api.image_router import router as image_router
from app.api.animation_router import router as animation_router
from app.api.auth_router import router as auth_router
from app.api.videos_router import router as videos_router
from slowapi.middleware import SlowAPIMiddleware

# Configurar el rate limiter
limiter = Limiter(key_func=get_remote_address)

def create_app() -> FastAPI:
    # Crear la instancia de FastAPI
    app = FastAPI(
        title="Photo Animation IA",
        description="Backend para el proyecto Photo Animation IA",
        version="1.0.0"
    )

    # Configurar el rate limiter y el middleware
    app.state.limiter = limiter
    app.add_middleware(SlowAPIMiddleware)

    # Incluir los routers
    app.include_router(image_router, prefix="/images", tags=["Images"])
    app.include_router(animation_router, prefix="/animation", tags=["Animation"])
    app.include_router(auth_router, prefix="/auth", tags=["Auth"])
    app.include_router(videos_router, prefix="/videos", tags=["Videos"])

    # Manejador global de excepciones HTTP
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"message": exc.detail}
        )

    # Manejador de excepciones para rate-limiting
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return PlainTextResponse("Too many requests", status_code=429)

    # Endpoint de prueba con rate-limiting
    @app.get("/test")
    @limiter.limit("5/minute")
    def test_endpoint(request: Request):
        return {"message": "Hasta 5 requests por minuto"}

    return app

# Crear la aplicación
app = create_app()