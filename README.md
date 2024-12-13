# Python API Dockerized

Este proyecto contiene una API escrita en Python que se ejecuta utilizando Uvicorn
dentro de un contenedor Docker. A continuación, se proporciona una guía para la configuración,
construcción y ejecución de la API.

## Pasos para Desplegar el Proyecto

Construir y Levantar los Servicios: En el directorio donde tienes el archivo `docker-compose.yml`, ejecuta el siguiente comando para construir las imágenes y levantar todos los servicios:

docker compose --profile back up -d --build

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
    curl "http://localhost:8000/lista-ordenada?lista-no-ordenada=1,6,3"
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

- **Endpoint**: `/guardar-lista-no-ordenada`
- **Descripción**: Guarda una lista no ordenada en MongoDB junto con la hora del sistema y un identificador único.
- **Uso con `curl`**:

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


# Configuración de Volúmenes en Docker Compose

Este proyecto utiliza Docker Compose para levantar los servicios de `python-api` y `mongodb`. Aquí se explican los volúmenes configurados para ambos servicios.

## Volumen en `python-api`

El servicio `python-api` monta un archivo de logs desde el sistema de archivos del host hacia el contenedor.

### Detalles del volumen:
- **Fuente (host)**: `./volumes/logs/info.log`
  - Esta ruta corresponde a un archivo en el sistema de archivos del host donde se almacenarán los logs generados por el contenedor `python-api`.
- **Destino (contenedor)**: `/opt/python-api/logs/info.log`
  - Dentro del contenedor, el archivo de logs se almacena en la ruta `/opt/python-api/logs/info.log`.

### Propósito:
Este volumen es un **bind mount**, lo que significa que cualquier cambio en el archivo `info.log` del host se reflejará en el contenedor, y viceversa. Se usa para almacenar los logs generados por la API en un archivo persistente en el host.

```yaml
volumes:
  - ./volumes/logs/info.log:/opt/python-api/logs/info.log

## Volumen en `mongodb`

El servicio `mongodb` utiliza un **volumen nombrado** para almacenar de forma persistente los datos de la base de datos, incluso si el contenedor se detiene o elimina.

### Detalles del volumen:
- **Volumen nombrado**: `mongodb-data`
  - Este volumen es gestionado por Docker. Se crea y administra automáticamente por Docker en el host. Al ser un volumen nombrado, Docker determina la ubicación donde se guardan los datos.
- **Destino en el contenedor**: `/data/db`
  - MongoDB guarda los datos de la base de datos en el directorio `/data/db` dentro del contenedor. Esta es la ruta por defecto para MongoDB.

### Propósito:
El volumen nombrado `mongodb-data` asegura que los datos de la base de datos de MongoDB se almacenen de manera persistente fuera del ciclo de vida del contenedor. Esto significa que los datos no se perderán si el contenedor se detiene o elimina, ya que permanecen almacenados en el volumen del host.

```yaml

volumes:
  - mongodb-data:/data/db
  

# Proyecto de Monitoreo de API con Docker

Este proyecto tiene como objetivo crear un sistema de monitoreo de un contenedor que expone un API con un endpoint `/healthcheck`. El contenedor de monitoreo realiza solicitudes periódicas al endpoint y registra los resultados en un archivo de log. A continuación, se explica cómo ejecutar el proyecto y configurar los diferentes aspectos.

## Requisitos

- Docker y Docker Compose instalados.
- Acceso a un contenedor que expone un API con el endpoint `/healthcheck` (por ejemplo, `python-api`).
- El contenedor de monitoreo estará configurado para verificar el estado de este API periódicamente.

## Pasos para Ejecutar el Proyecto

### 1. Configurar las Variables de Entorno

Antes de ejecutar los contenedores, es necesario configurar las variables de entorno que controlan el contenedor de monitoreo.
Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```bash
TARGET_CONTAINER_HOST=python-api
TARGET_CONTAINER_PORT=8000
CHECK_INTERVAL=5
TZ=America/Bogota
```

- `TARGET_CONTAINER_HOST`: Nombre o IP del contenedor a monitorear (por ejemplo, `python-api`).
- `TARGET_CONTAINER_PORT`: Puerto del contenedor a monitorear (por ejemplo, `8000`).
- `CHECK_INTERVAL`: Tiempo en segundos entre cada solicitud de monitoreo (por ejemplo, `5`).
- `TZ`: Zona horaria para el contenedor de monitoreo (por ejemplo, `America/Bogota`).

> **Nota**: No olvides agregar el archivo `.env` al archivo `.gitignore` para evitar exponer información sensible.

### 2. Configuración del Archivo Docker Compose

El archivo `docker-compose.yml` define la infraestructura del proyecto, con dos contenedores: el contenedor de monitoreo (`api-monitor`) y el contenedor objetivo (`python-api`).

- **Contenedor `python-api`**: Este contenedor expone el API con el endpoint `/healthcheck`.
- **Contenedor `api-monitor`**: Este contenedor ejecuta el script de monitoreo que realiza las solicitudes al endpoint `/healthcheck` del contenedor `python-api`.
- **Volumen de Logs**: Se monta un volumen bind en `./volumes/logs/api-monitor.log` para almacenar los logs del monitoreo de manera persistente.

### 3. Crear los Archivos del Contenedor de Monitoreo

#### 3.1. Dockerfile para el Servicio `api-monitor`

Dentro de la carpeta `api-monitor`, crea un archivo `Dockerfile.monitor` que definirá cómo construir el contenedor de monitoreo:

```Dockerfile
FROM python:3.12-slim

# Crear directorios necesarios
RUN mkdir -p /opt/monitor/logs

# Copiar el script de monitoreo
COPY monitor_script.py /opt/monitor/monitor_script.py

# Instalar las librerías necesarias
RUN pip install requests

# Establecer el punto de entrada
ENTRYPOINT ["python", "/opt/monitor/monitor_script.py"]
```

#### 3.2. Script de Monitoreo (`monitor_script.py`)

Crea el script `monitor_script.py` dentro de la carpeta `api-monitor` que realiza las solicitudes al endpoint `/healthcheck`:

Este script realiza solicitudes al endpoint `/healthcheck` y registra los resultados en un archivo de log. Si la respuesta es válida (código 200 y contiene "OK"), registra un mensaje de información. Si la solicitud falla, registra un mensaje de error.

### 4. Ejecutar los Servicios con Docker Compose

Para iniciar todos los servicios definidos en `docker-compose.yml`, ejecuta el siguiente comando:

```bash
docker-compose --profile back up -d --build
```

Este comando construye las imágenes necesarias y ejecuta los contenedores. El contenedor `api-monitor` comenzará a realizar solicitudes periódicas al contenedor `python-api` y almacenará los logs en `./volumes/logs/api-monitor.log`.

### 5. Verificar el Archivo de Logs

El archivo `./volumes/logs/api-monitor.log` debe irse llenando con los resultados de las solicitudes al endpoint `/healthcheck`. Un ejemplo de salida en el log sería:

```text
2024-09-26 12:30:00,123 - INFO - Se hizo la solicitud al endpoint http://python-api:8000/healthcheck y devolvió OK
2024-09-26 12:30:05,456 - ERROR - Se hizo la solicitud al endpoint http://python-api:8000/healthcheck y devolvió error: Código de estado: 500, Respuesta: Internal Server Error
```

## Documentación del Proyecto

- **Variables de entorno**: El archivo `.env` define las variables necesarias para configurar el contenedor de monitoreo. Recuerda que este archivo debe ser añadido al `.gitignore`.
- **Volúmenes**: Se usa un volumen bind para almacenar los logs de monitoreo en el archivo `volumes/logs/api-monitor.log`, lo que permite que los logs persistan incluso después de reiniciar los contenedores.
- **Política de reinicio**: El contenedor `api-monitor` tiene la política de reinicio `always`, lo que garantiza que el contenedor se reinicie automáticamente si se detiene o falla.
- **Red**: Ambos contenedores están conectados a la misma red (`monitor_network`), lo que permite que se comuniquen entre sí.
