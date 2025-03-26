import os
import subprocess
import uuid

def animate_photo(image_path: str, driving_path: str = None) -> str:
    """
    Aplica FOMM (First Order Motion Model) usando el script demo.py.
    Retorna la ruta del archivo de video resultante (mp4).

    Args:
        image_path (str): Ruta de la imagen de origen.
        driving_path (str, optional): Ruta del video de animación (driving video). 
                                      Si no se proporciona, se usa un video fijo por defecto.
    """
    # Ruta al script principal de FOMM
    fomm_script = os.path.join("fomm", "demo.py")
    # Archivo de configuración para el modelo "vox"
    config_file = os.path.join("fomm", "config", "vox-256.yaml")
    # Ruta al checkpoint pre-entrenado
    checkpoint_path = os.path.join("models", "vox-cpk.pth.tar")
    # Nombre único para el archivo de salida
    output_name = f"animated_{uuid.uuid4()}.mp4"
    output_path = os.path.join("temp_uploads", output_name)

    # Si no se proporciona un driving_path, usar el video fijo por defecto
    if not driving_path:
        driving_path = os.path.join("fomm", "assets", "driving.mp4")

    # Construir el comando con el argumento correcto "--result_video"
    command = [
        "python", fomm_script,
        "--config", config_file,
        "--driving_video", driving_path,
        "--source_image", image_path,
        "--checkpoint", checkpoint_path,
        "--result_video", output_path,
        "--relative",
        "--adapt_scale"
    ]

    try:
        # Ejecutar el comando y capturar la salida para depurar
        result = subprocess.run(command, check=True, capture_output=True, text=True)
        print("FOMM output:", result.stdout)
    except subprocess.CalledProcessError as e:
        # Imprimir el error para depuración y retornar None para indicar fallo
        print("Error corriendo FOMM:", e.stderr)
        return None

    return output_path
