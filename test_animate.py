import os
from app.services.animate_service import animate_photo

image_path = os.path.join("temp_uploads", "b76e71a5-817e-4860-9d44-68cccb04d30a.jpg")
driving_path = os.path.join("fomm", "assets", "driving.mp4")  # O usa static/driving.mp4 según tu configuración

output = animate_photo(image_path, driving_path)
if output:
    print("Animación completada:", output)
else:
    print("Fallo en la animación.")
