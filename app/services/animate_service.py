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
    #Ruta al script principal de FOMM
    fomm_script = os.path.join("fomm", "demo.py")

    #Config file. Para el modelo "vox", es:
    config_file = os.path.join("fomm", "config", "vox-256.yaml")
    
    #Ruta del checkpoint del modelo
    checkpoint_path = os.path.join("models", "vox-cpk.pth.tar")

    #Nombre único para el archivo de salida
    output_name = f"animated_{uuid.uuid4()}.mp4"
    output_path = os.path.join("temp_uploads", output_name)

    #Ruta del video de animación (driving video)
    # Si no se proporciona un driving_path, se usa un video fijo por defecto
    if not driving_path:
        driving_path = os.path.join("fomm", "assets", "driving.mp4")

    #Comando para ejecutar FOMM vía demo.py
    command = [
        "python", fomm_script,
        "--config", config_file,
        "--driving_video", driving_path,
        "--source_image", image_path,
        "--checkpoint", checkpoint_path,
        "--output", output_path,
        "--relative",
        "--adapt_scale"
    ]

    try:
        # Ejecutar el comando
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error corriendo FOMM: {e}")
        return None

    return output_path