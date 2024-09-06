# External libraries
from datetime import datetime

from fastapi import FastAPI, Query
from starlette.responses import RedirectResponse

app = FastAPI()

@app.get('/')
def raiz():
    return RedirectResponse(url='/docs/')


@app.get('/lista-ordenada')
def lista_ordenada(
    lista_no_ordenada: str = Query(..., alias='lista-no-ordenada')
) -> dict:
    """
    Ordena una lista de números y devuelve la lista ordenada junto con la hora actual del sistema.

    Args:
        lista_no_ordenada: Lista de números enteros no ordenada en formato JSON.

    Returns:
        La hora actual del sistema en formato 'YYYY-MM-DD HH:MM:SS' y la
        lista de números ordenada de menor a mayor.

    """
    return {
        'hora_sistema': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'lista_ordenada': sorted(lista_no_ordenada)
    }

@app.get('/healthcheck')
def healthcheck() -> str:
    """
    Verifica el estado de la API.

    Returns:
        Cadena que indica que la API está funcionando correctamente.
    """
    return 'OK'
