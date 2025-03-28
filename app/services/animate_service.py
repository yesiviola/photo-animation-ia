import os
import subprocess
import uuid
# Importamos imageio.v2 para mantener el comportamiento actual y eliminar la advertencia de deprecation
import imageio.v2 as imageio

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
    
    # Ruta del checkpoint del modelo
    checkpoint_path = os.path.join("models", "vox-cpk.pth.tar")

    # Nombre único para el archivo de salida
    output_name = f"animated_{uuid.uuid4()}.mp4"
    output_path = os.path.join("temp_uploads", output_name)

    # Si no se proporciona un driving_path, se usa un video fijo por defecto
    if not driving_path:
        driving_path = os.path.join("fomm", "assets", "driving.mp4")

    # Comando para ejecutar FOMM vía demo.py
    command = [
        "python", fomm_script,
        "--config", config_file,
        "--driving_video", driving_path,
        "--source_image", image_path,
        "--checkpoint", checkpoint_path,
        "--result_video", output_path,  # Usamos --result_video en lugar de --output
        "--relative",
        "--adapt_scale",
        "--cpu"  # Se añade para forzar la ejecución en CPU
    ]

    try:
        # Ejecutar el comando y comprobar que se ejecuta correctamente
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        # Imprimir el error para depuración y retornar None para indicar fallo
        print(f"Error corriendo FOMM: {e}")
        return None

    return output_path
