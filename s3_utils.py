import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def upload_to_s3(file_path: str, key: str) -> str:
    """
    Sube el archivo 'file_path' a S3 en la clave 'key'.
    Retorna la URL pública (si el bucket es público).
    """
    bucket_name = os.getenv('AWS_S3_BUCKET')
    s3.upload_file(file_path, bucket_name, key)
    return f"https://{bucket_name}.s3.amazonaws.com/{key}"

def download_from_s3(key: str, file_path: str):
    """
    Descarga el archivo de S3 especificado por 'key' y lo guarda en 'file_path'.
    """
    bucket_name = os.getenv('AWS_S3_BUCKET')
    s3.download_file(bucket_name, key, file_path)
