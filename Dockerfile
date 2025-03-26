# 1. Usar una imagen base de Python
FROM python:3.9-slim-buster

# 2. Instalar utilidades del sistema necesarias para compilar dlib (cmake, g++, etc.)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        make \
        cmake \
        libopenblas-dev \
        libx11-6 \
        libgtk2.0-dev \
        pkg-config \
        && rm -rf /var/lib/apt/lists/*

# 3. Crear un directorio de trabajo dentro del contenedor
WORKDIR /app


# 4. Copiar el archivo de requerimientos
COPY requirements.txt .

# 5. Instalar dependencias con pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar la carpeta "fomm" y "static"
COPY fomm/ fomm/
COPY static/ static/

# 6. Copiar el resto del código (excluyendo .env)
COPY . .

# 7. Exponer el puerto 8000 (donde corre FastAPI por defecto)
EXPOSE 8000

# 8. Comando por defecto para correr la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]