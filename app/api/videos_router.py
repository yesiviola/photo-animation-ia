import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from s3_utils import upload_to_s3  # Ajusta la ruta del import si hace falta

router = APIRouter()

@router.post("/upload")
async def upload_driving_video(file: UploadFile = File(...)):
    """
    Sube un video personalizado (driving video) en formato .mp4.
    Se guardan 2 copias:
      1) local en temp_uploads
      2) en S3 (si deseas) 
    """
    # Validar la extensión
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension != ".mp4":
        raise HTTPException(status_code=400, detail="Formato de video no permitido. Solo .mp4")

    # Validar tamaño
    MAX_SIZE = 50_000_000  # 50 MB
    file_content = await file.read()
    if len(file_content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="El archivo excede 50MB")

    # Generar nombre único
    unique_id = str(uuid.uuid4())
    local_path = os.path.join("temp_uploads", f"{unique_id}{file_extension}")

    # Guardar local
    with open(local_path, "wb") as f:
        f.write(file_content)

    # Subir a S3 (opcional)
    s3_key = f"videos/{unique_id}{file_extension}"
    s3_url = upload_to_s3(local_path, s3_key)

    # Nota: NO borramos local_path => FOMM podrá usarlo
    # os.remove(local_path)  # <--- la comentamos para conservarlo

    return {
        "message": "Video subido exitosamente",
        "video_id": unique_id,   # ID para usar local
        "local_path": local_path,
        "s3_url": s3_url
    }
