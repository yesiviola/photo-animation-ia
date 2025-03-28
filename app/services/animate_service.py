import os
import subprocess
import uuid
import warnings
import imageio.v2 as imageio   # type: ignore


warnings.filterwarnings("ignore", category=DeprecationWarning, module="imageio")

def animate_photo(image_path: str, driving_path: str = None) -> str:
    """
    Aplica FOMM (First Order Motion Model) usando el script demo.py.
    Retorna la ruta del archivo de video resultante (mp4) o None en caso de error.

    Args:
        image_path (str): Ruta de la imagen de origen.
        driving_path (str, optional): Ruta del video de animación.
            Si no se proporciona, se usa un video fijo por defecto.

    Returns:
        str: Ruta del video generado o None si ocurrió un error.
    """
    # Ruta al script principal de FOMM
    fomm_script = os.path.join("fomm", "demo.py")
    
    # Archivo de configuración para el modelo "vox"
    config_file = os.path.join("fomm", "config", "vox-256.yaml")
    
    # Ruta del checkpoint del modelo
    checkpoint_path = os.path.join("models", "vox-cpk.pth.tar")
    
    # Nombre único para el archivo de salida y ruta completa en "temp_uploads"
    output_name = f"animated_{uuid.uuid4()}.mp4"
    output_path = os.path.join("temp_uploads", output_name)
    
    # Si no se proporciona un driving_path, usar video fijo
    if not driving_path:
        driving_path = os.path.join("fomm", "assets", "driving.mp4")
    
    # Armar el comando; se agrega "--cpu" para forzar modo CPU
    command = [
        "python", fomm_script,
        "--config", config_file,
        "--driving_video", driving_path,
        "--source_image", image_path,
        "--checkpoint", checkpoint_path,
        "--relative",
        "--adapt_scale",
        "--cpu"
    ]
    
    try:
        # Ejecutar el comando y capturar el error en caso de fallo
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        # Imprimir el error completo para depuración
        print("Error corriendo FOMM:")
        print(e.stderr.decode())
        return None

    # Por defecto, demo.py guarda la salida en "result.mp4"
    result_file = "result.mp4"
    if os.path.exists(result_file):
        try:
            # Renombrar result.mp4 al nombre único generado
            os.rename(result_file, output_path)
        except Exception as e:
            print(f"Error renombrando el video de salida: {e}")
            return None
        return output_path
    else:
        print("No se encontró el archivo result.mp4 generado por FOMM")
        return None
