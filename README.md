# Python API Dockerized

Este proyecto contiene una API escrita en Python que se ejecuta utilizando Uvicorn
dentro de un contenedor Docker. A continuación, se proporciona una guía para la configuración,
construcción y ejecución de la API.

## Configuración

1. **Clonar el repositorio**

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. **Construir la imagen Docker**

   En la raíz del proyecto, ejecuta el siguiente comando para construir la imagen Docker:

   ```bash
   docker build -t python-api:v1.0.0 .
   ```

3. **Ejecutar el contenedor**

   Una vez que la imagen se haya construido correctamente, puedes ejecutar el contenedor con el
   siguiente comando:

   ```bash
   docker run -p 8000:8000 python-api:v1.0.0
   ```

   Esto mapeará el puerto 8000 del contenedor al puerto 8000 de tu máquina local,
   permitiéndote acceder a la API a través de `http://localhost:8000`.

## Uso

Para ejecutar la API, inicia el contenedor Docker como se describe en la sección de ejecución.
Luego, puedes interactuar con la API usando herramientas como `curl`, `Postman`, o cualquier cliente HTTP.

### Ejemplos de Endpoints

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
  curl "http://localhost:8000/lista-ordenada?lista-no-ordenada=[5,4,7,2,7,2]"
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