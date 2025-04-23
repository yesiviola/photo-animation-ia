import os
import subprocess
import uuid
import imageio.v2 as imageio  # Usamos imageio.v2 para mantener el comportamiento actual

def animate_photo(image_path: str, driving_path: str = None) -> str:
    """
    Aplica FOMM (First Order Motion Model) usando el script demo.py.
    Retorna la ruta del archivo de video resultante (mp4).

    Args:
        image_path (str): Ruta de la imagen de origen.
        driving_path (str, optional): Ruta del video de animación (driving video). 
                                      Si no se proporciona, se usa un video fijo por defecto.
    """
    # --- Configuración de rutas ---
    # Ruta al script principal de FOMM.
    # Asumimos que se ejecuta desde la raíz del backend.
    fomm_script = os.path.join("fomm", "demo.py")
    
    # Archivo de configuración para el modelo "vox".
    config_file = os.path.join("fomm", "config", "vox-256.yaml")
    
    # Ruta del checkpoint del modelo.
    checkpoint_path = os.path.join("models", "vox-cpk.pth.tar")
    
    # Nombre único para el archivo de salida.
    output_name = f"animated_{uuid.uuid4()}.mp4"
    output_path = os.path.join("temp_uploads", output_name)
    
    # --- Video fijo para animación ---
    # Si no se proporciona un driving_path, se usa un video fijo.
    if not driving_path:
        # Opción A: Usar el video en la carpeta "fomm/assets"
        driving_path = os.path.join("fomm", "assets", "driving.mp4")
        # Opción B: Si prefieres usar "static/driving.mp4", comenta la línea anterior
        # y descomenta la siguiente línea:
        # driving_path = os.path.join("static", "driving.mp4")
    
    # --- Logs de depuración ---
    print("[DEBUG] Iniciando animación:")
    print(f" - Imagen de origen: {image_path}")
    print(f" - Video de conducción: {driving_path}")
    print(f" - Script: {fomm_script}")
    print(f" - Config file: {config_file}")
    print(f" - Checkpoint: {checkpoint_path}")
    print(f" - Archivo de salida: {output_path}")
    
    # --- Construir el comando para ejecutar el script ---
    command = [
        "python", fomm_script,
        "--config", config_file,
        "--driving_video", driving_path,
        "--source_image", image_path,
        "--checkpoint", checkpoint_path,
        "--result_video", output_path,  # Usamos --result_video para especificar el archivo de salida
        "--relative",
        "--adapt_scale",
        "--cpu"  # Forza la ejecución en CPU
    ]
    
    print(f"[DEBUG] Ejecutando comando: {' '.join(command)}")
    
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error corriendo FOMM: {e}")
        return None
    
    print(f"[DEBUG] Animación completada, video generado en: {output_path}")
    return output_path
