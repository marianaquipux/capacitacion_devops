"""Módulo de FastAPI para operaciones básicas y verificación del estado de la API."""

# External libraries
from datetime import datetime

from fastapi import FastAPI, Query
from starlette.responses import RedirectResponse
from pymongo import MongoClient
import uuid

import json

# Own libraries
from config import get_mongo

app = FastAPI()


@app.get('/')
def raiz():
    """Redirige la solicitud de la raíz ('/') a la documentación de la API.

    Returns:
        RedirectResponse: Una respuesta de redirección a '/docs/'.

    """
    return RedirectResponse(url='/docs/')

@app.get('/lista-ordenada')
def lista_ordenada(
    lista_no_ordenada: str = Query(..., alias='lista-no-ordenada')
) -> dict:
    """Ordena una lista de números y devuelve la lista ordenada junto con la hora
     actual del sistema.

    Args:
        lista_no_ordenada: Lista de números enteros no ordenada en formato JSON.

    Returns:
        La hora actual del sistema en formato 'YYYY-MM-DD HH:MM:SS' y la
        lista de números ordenada de menor a mayor.

    """
    lista_no_ordenada = [int(x) for x in lista_no_ordenada]
    return {
        'hora_sistema': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'lista_ordenada': sorted(lista_no_ordenada)
    }

@app.get('/healthcheck')
def healthcheck() -> str:
    """Verifica el estado de la API.

    Returns:
        Cadena que indica que la API está funcionando correctamente.

    """
    return 'OK'


@app.get('/guardar-lista-no-ordenada')
def guardar_lista_no_ordenada(
    lista_no_ordenada: str = Query(..., alias='lista-no-ordenada')
) -> dict:
    """Guarda una lista no ordenada en MongoDB junto con la hora del sistema y un
     identificador único.

    Args:
        lista_no_ordenada: Lista de números enteros no ordenada en formato JSON.

    Returns:
        Mensaje con el identificador único del registro guardado.

    """
    mongo_db = get_mongo(
        nombre_var_mongo_host='MONGODB_HOST',
        nombre_var_mongo_port='MONGODB_PORT',
        nombre_bd='python_app',
        mongo_client=MongoClient
    )
    coleccion = mongo_db['listas_no_ordenadas']

    id_unico = str(uuid.uuid4())

    documento = {
        'id': id_unico,
        'lista_no_ordenada': lista_no_ordenada,
        'hora_sistema': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    coleccion.insert_one(documento)

    return {'msg': f'La lista ordenada fue guardada con el id: {id_unico}'}
