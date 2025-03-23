import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from s3_utils import upload_to_s3

router = APIRouter()

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Validar la extensión del archivo
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no permitido.")

    # Validar el tamaño del archivo
    MAX_SIZE = 5_000_000  # 5 MB
    file_content = await file.read()
    if len(file_content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="El archivo excede los 5MB.")

    # Genera un nombre único para el archivo
    unique_id = str(uuid.uuid4())
    temp_path = os.path.join("temp_uploads", f"{unique_id}{file_extension}")

    # Guardar el archivo temporalmente en el servidor
    with open(temp_path, "wb") as f:
        f.write(file_content)

    # Subir el archivo a S3
    s3_key = f"images/{unique_id}{file_extension}"
    url = upload_to_s3(temp_path, s3_key)

    # Eliminar el archivo temporal
    os.remove(temp_path)

    # Retornar la respuesta
    return {
        "message": "Imagen subida exitosamente",
        "image_id": unique_id,
        "s3_url": url
    }