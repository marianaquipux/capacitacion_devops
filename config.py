"""Módulo de configuraciones necesarias para el funcionamiento del API."""

# External libraries
from functools import lru_cache
import os
from typing import Any


@lru_cache()
def get_mongo(
    nombre_var_mongo_host: str,
    nombre_var_mongo_port: str,
    nombre_bd: str,
    mongo_client: Any,
) -> Any:
    """Crea una instancia de base de datos MongoDB.

    Args:
        nombre_var_mongo_host: Nombre de la variable de entorno que corresponde al host
         de la base de datos de Mongo.
        nombre_var_mongo_port: Nombre de la variable de entorno que corresponde al puerto
         de la base de datos Mongo.
        nombre_bd: Nombre de la base de datos de Mongo para la conexión.
        mongo_client: La clase `MongoClient` del paquete `pymongo` utilizada
         para establecer la conexión con MongoDB.

    Returns:
        Instancia de la base de datos MongoDB con la conexión lista para realizar
         peticiones.

    Examples:

        >>> from api_qx.config.qx_config import get_mongo
        >>> from pymongo import MongoClient
        >>>
        >>> mongo_db = get_mongo(
        >>>     nombre_var_mongo_host='NOMBRE_PROYECTO_MONGODB_HOST',
        >>>     nombre_var_mongo_port='NOMBRE_PROYECTO_MONGODB_PORT',
        >>>     nombre_bd='nombre_proyecto',
        >>>     mongo_client=MongoClient
        >>> )

    """
    nombre_var_mongo_host = os.environ.get(nombre_var_mongo_host)
    nombre_var_mongo_port = os.environ.get(nombre_var_mongo_port)

    client = mongo_client(nombre_var_mongo_host, int(nombre_var_mongo_port))
    mongo_db = getattr(client, nombre_bd)

    return mongo_db
