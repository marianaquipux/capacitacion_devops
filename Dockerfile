FROM python:3.12-slim

WORKDIR /opt/python-api/

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código
COPY . .

# Define el punto de entrada para iniciar el servidor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
