# Usa la imagen slim para reducir el tamaño
FROM python:3.12-slim

# Establece el directorio de trabajo
WORKDIR /opt/python-api/

# Copia solo el archivo de dependencias, no el código fuente completo
COPY requirements.txt .

# Instala las dependencias del proyecto para aprovechar caché
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Define el punto de entrada para iniciar el servidor
ENTRYPOINT ["uvicorn", "main:app"]
CMD ["--host", "0.0.0.0", "--port", "8000"]