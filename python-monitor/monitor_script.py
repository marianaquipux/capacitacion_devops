"""Módulo con funcionalidades para monitorear el el API 'python_api'."""

# External libraries
import logging
import os
import requests
import time

log_dir = '/opt/python-monitor/logs'
logging.basicConfig(
    filename=os.path.join(log_dir, 'api-monitor.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def monitorear_api():
    check_interval = int(os.getenv('CHECK_INTERVAL'))
    target_host = os.getenv('TARGET_CONTAINER_HOST')
    target_port = os.getenv('TARGET_CONTAINER_PORT')
    
    url = f"http://{target_host}:{target_port}/healthcheck"

    try:
        while True:
            response = requests.get(url)

            if response.status_code == 200 and response.text == '"OK"':
                logging.info(f"Healthcheck OK: {response.text}")
            else:
                logging.error(f"Healthcheck fallo con estado {response.status_code} y respuesta: {response.text}")

            time.sleep(check_interval)

    except requests.exceptions.RequestException as e:
        logging.error(f"Error consultando {url}: {e}")

if __name__ == "__main__":
    monitorear_api()
