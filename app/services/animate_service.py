import os
import subprocess
import uuid

def animate_photo(image_path: str) -> str:
    """
    Aplica FOMM (First Order Motion Model) usando el script demo.py.
    Retorna la ruta del archivo de video resultante (mp4).
    """

    # 1. Ruta al script principal de FOMM
    fomm_script = os.path.join("fomm", "demo.py")

    # 2. Config file. Para el modelo "vox", es:
    config_file = os.path.join("fomm", "config", "vox-256.yaml")
    
    checkpoint_path = os.path.join("models", "vox-cpk.pth.tar")

    output_name = f"animated_{uuid.uuid4()}.mp4"
    output_path = os.path.join("temp_uploads", output_name)

    driving_video_path = os.path.join("fomm", "assets", "driving_cropped.mp4")


    # 6. Comando para ejecutar FOMM vía demo.py
    #    Revisa que: 
    #       --config  -> config yaml
    #       --driving_video -> tu driving video
    #       --source_image  -> tu foto
    #       --checkpoint -> tu checkpoint .pth.tar
    #       --output -> adónde guarda result.mp4 (en este caso output_path)
    #       --relative (opcional) y --adapt_scale (opcional) para mejorar la animación.
    command = [
        "python", fomm_script,
        "--config", config_file,
        "--driving_video", driving_video_path,
        "--source_image", image_path,
        "--checkpoint", checkpoint_path,
        "--output", output_path,
        "--relative",
        "--adapt_scale"
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error corriendo FOMM: {e}")
        return None

    return output_path
