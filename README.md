# Python API Dockerized

Este proyecto contiene una API escrita en Python que se ejecuta utilizando Uvicorn
dentro de un contenedor Docker. A continuación, se proporciona una guía para la configuración,
construcción y ejecución de la API.

## Pasos para Desplegar el Proyecto

Construir y Levantar los Servicios: En el directorio donde tienes el archivo `docker-compose.yml`, ejecuta el siguiente comando para construir las imágenes y levantar los servicios:

docker compose up --build

Este comando:

- Construirá la imagen del servicio `python-api` usando el Dockerfile en el directorio actual.
- Descargaría la imagen de MongoDB y la ejecutaría.
- Levantará ambos servicios y los conectará a través de la red `mongodb-net`.

Verificar que los Contenedores Están Corriendo: Puedes verificar el estado de los contenedores con:

docker ps

Debes ver dos contenedores: `python-api` y `mongodb` en ejecución.

Acceder a la API: Una vez que los servicios estén arriba, puedes acceder a la API FastAPI en el navegador o mediante curl en la siguiente URL:

http://localhost:8000


Si deseas ver los logs de un servicio específico, como `python-api`:

docker compose logs python-api

Detener y Eliminar los Contenedores: Para detener los contenedores sin eliminar los volúmenes, ejecuta:

docker compose down

Si también deseas eliminar los volúmenes asociados:

docker compose down --volumes



### Endpoints

#### 1. Redirección a la documentación

- **Endpoint**: `/`
- **Descripción**: Redirige a la documentación de la API.
- **Uso con `curl`**:

  ```bash
  curl http://localhost:8000/
  ```

  Redirigirá a `http://localhost:8000/docs/`, donde puedes ver la documentación generada
  automáticamente por FastAPI.

#### 2. Ordenar una lista

- **Endpoint**: `/lista-ordenada`
- **Descripción**: Ordena una lista de números y devuelve la lista ordenada junto
 con la hora actual del sistema.
- **Parámetro**: `lista-no-ordenada` (en formato JSON)
- **Uso con `curl`**:

  ```bash
    curl "http://localhost:8000/lista-ordenada?lista-no-ordenada=1,2,3"
  ```

  **Respuesta Ejemplo**:

  ```json
  {
    "hora_sistema": "2024-09-06 12:34:56",
    "lista_ordenada": [2, 2, 4, 5, 7, 7]
  }
  ```

#### 3. Verificar estado

- **Endpoint**: `/healthcheck`
- **Descripción**: Verifica el estado de la API.
- **Uso con `curl`**:

  ```bash
  curl http://localhost:8000/healthcheck
  ```

  **Respuesta Ejemplo**:

  ```text
  OK
  ```

#### 4. Lista no ordenada

  ```bash
  curl "http://localhost:8000/guardar-lista-no-ordenada?lista-no-ordenada=%5B5,4,7,2,7,2%5D"
  ```


# Configurar y levantar los contenedores manualmente sin un archivo docker-compose.yml

# Crear la red mongodb-net
docker network create mongodb-net

# Iniciar MongoDB
  ```bash
  docker run -d --name mongodb --network mongodb-net -p 27017:27017 mongo:latest
  ```

# Iniciar el contenedor de Python con Uvicorn

```bash
docker build -t python-api:v1.1.0 .

docker run -d --name python-api --network mongodb-net -p 8000:8000 -e MONGODB_HOST=mongodb -e MONGODB_PORT=27017 python-api:v1.1.0
```