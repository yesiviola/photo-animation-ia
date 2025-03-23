import boto3
import os


s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

def upload_to_s3(file_path: str, key: str) -> str:
    """
    Sube el archivo 'file_path' a 'key' en S3.
    Retorna la URL pública si el bucket es público.
    """
    bucket_name = os.getenv('AWS_S3_BUCKET')
    s3.upload_file(file_path, bucket_name, key)
    return f"https://{bucket_name}.s3.amazonaws.com/{key}"
