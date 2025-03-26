import os
import uuid
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import FileResponse
from app.services.animate_service import animate_photo
from app.api.auth_router import get_current_user
from slowapi import Limiter
from slowapi.util import get_remote_address
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Animation
from s3_utils import upload_to_s3

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/animate")
@limiter.limit("2/minute")  # 2 solicitudes por minuto
async def animate_image(
    request: Request,
    image_id: str,
    driving_video_id: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Aplica IA para animar la imagen cuyo id se pasa como parámetro.
    driving_video_id es el video subido con /videos/upload (conservado localmente).
    Si no se provee, se usa un driving.mp4 fijo en /static/driving.mp4.
    """
    # Buscar la imagen en temp_uploads probando distintas extensiones
    possible_extensions = [".jpg", ".jpeg", ".png"]
    image_path = None
    for ext in possible_extensions:
        temp_path = os.path.join("temp_uploads", f"{image_id}{ext}")
        if os.path.exists(temp_path):
            image_path = temp_path
            break

    if image_path is None:
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    # Determinar la ruta del driving video
    if driving_video_id:
        driving_video_path = os.path.join("temp_uploads", f"{driving_video_id}.mp4")
        if not os.path.exists(driving_video_path):
            raise HTTPException(
                status_code=404, 
                detail=f"Video personalizado con ID {driving_video_id} no encontrado"
            )
    else:
        # Usar un video fijo
        driving_video_path = os.path.join("static", "driving.mp4")
        if not os.path.exists(driving_video_path):
            raise HTTPException(status_code=404, detail="Video fijo no encontrado")

    # Llamar a la función de animación
    output_video_path = animate_photo(image_path, driving_video_path)
    if not output_video_path:
        raise HTTPException(status_code=500, detail="Error en la animación")
    
    # Subir el video final a S3
    s3_key = f"animations/{uuid.uuid4()}.mp4"
    s3_url = upload_to_s3(output_video_path, s3_key)

    # Guardar el registro en la base de datos
    new_anim = Animation(
        user_id=current_user.id,
        s3_url=s3_url
    )
    db.add(new_anim)
    db.commit()
    db.refresh(new_anim)

    return {
        "message": "Animación generada exitosamente☺️",
        "animation_file": output_video_path,
        "s3_url": s3_url
    }

@router.get("/download")
def download_video(
    file_path: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Retorna el video animado en formato Mp4.
    Solo usuarios autenticados pueden acceder a este endpoint.
    file_path es la ruta local donde se generó el video.
    """
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado.")
    return FileResponse(file_path, media_type="video/mp4", filename="animated.mp4")
