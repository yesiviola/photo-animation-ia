from fastapi import APIRouter, HTTPException
import os
from app.services.animate_service import animate_photo

router = APIRouter()

@router.post("/animate")
async def animate_image(image_id: str):
    """
    Aplica IA para animar la imagen cuyo id se pasa como parámetro.
    """
    #ruta donde la imagen se guardó
    image_path = os.path.join("temp_uploads", f"{image_id}.jpg")  # asumiendo JPG
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Imagen no encontrada")

    # Llamamos al servicio de animación
    output_video_path = animate_photo(image_path)

    if not output_video_path:
        raise HTTPException(status_code=500, detail="Error en la animación")

    return {
        "message": "Animación generada exitosamente",
        "animation_file": output_video_path
    }
