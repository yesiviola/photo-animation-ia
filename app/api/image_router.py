from fastapi import APIRouter, File, UploadFile
import os
import uuid

router = APIRouter()

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Sube una imagen y la guarda en el servidor con un nombre único.
    """
    file_extension = os.path.splitext(file.filename)[1]
    unique_id = str(uuid.uuid4())
    file_name = f"{unique_id}{file_extension}"
    file_path = os.path.join(UPLOAD_FOLDER, file_name)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Imagen subida exitosamente",
        "image_id": unique_id,
        "file_path": file_path
    }
