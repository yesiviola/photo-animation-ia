import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from s3_utils import upload_to_s3

router = APIRouter()

# Asegurarse de que exista el directorio temporal
UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # Validar la extensión del archivo
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in [".jpg", ".jpeg", ".png"]:
        raise HTTPException(status_code=400, detail="Formato de imagen no permitido.")

    # Validar el tamaño del archivo (5 MB máximo)
    MAX_SIZE = 5_000_000
    file_content = await file.read()
    if len(file_content) > MAX_SIZE:
        raise HTTPException(status_code=400, detail="El archivo excede los 5MB.")

    # Generar un nombre único para el archivo
    unique_id = str(uuid.uuid4())
    temp_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}{file_extension}")

    # Guardar el archivo temporalmente en el servidor
    try:
        with open(temp_path, "wb") as f:
            f.write(file_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al guardar el archivo: {e}")

    # Subir el archivo a S3
    s3_key = f"images/{unique_id}{file_extension}"
    try:
        url = upload_to_s3(temp_path, s3_key)
    except Exception as e:
        # En caso de error, se elimina el archivo temporal
        if os.path.exists(temp_path):
            os.remove(temp_path)
        raise HTTPException(status_code=500, detail=f"Error al subir a S3: {e}")

    # Eliminar el archivo temporal
    if os.path.exists(temp_path):
        os.remove(temp_path)

    # Retornar la respuesta
    return {
        "message": "Imagen subida exitosamente",
        "image_id": unique_id,
        "s3_url": url
    }
