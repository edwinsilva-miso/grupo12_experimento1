import csv
import json
import os
import threading
import uuid
import logging

import redis
from werkzeug.utils import secure_filename

from ..producers.products_load_producer import ProductsLoadProducer

logging.basicConfig(
    level=logging.DEBUG,  # Set logging level to DEBUG (captures everything)
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date and time format
)

logger = logging.getLogger(__name__)

logging = logging.getLogger(__name__)

UPLOAD_PATH = os.getenv('TEMP_UPLOAD_FOLDER')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
MAX_ROWS_PER_CHUNK = int(os.getenv('MAX_ROWS_PER_CHUNK'))
MAX_CHUNKS_SIZE = int(os.getenv('MAX_CHUNKS_SIZE'))

redis_client = redis.Redis(host='localhost', port=6379)


class ProcessFile:

    def __init__(self):
        self.producer = ProductsLoadProducer()

    def execute(self, file):
        # Crear directorio de carga si no existe
        os.makedirs(UPLOAD_PATH, exist_ok=True)
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_PATH, filename)
        file.save(file_path)

        process_id = str(uuid.uuid4())
        threading.Thread(target=self.process_csv_file, args=(file_path, process_id)).start()

        return {"message": "File successfully uploaded and processed", "process_id": process_id}

    def process_csv_file(self, file_path, process_id):
        logging.debug("Begining processing file")
        try:
            # Primero, determinamos el encabezado y estructura del archivo
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                sample = csvfile.read(1024)
                dialect = csv.Sniffer().sniff(sample)
                csvfile.seek(0)

                # Leer encabezados
                reader = csv.reader(csvfile, dialect)
                headers = next(reader)

                # Contar número total de filas para el seguimiento del progreso
                csvfile.seek(0)
                row_count = sum(1 for _ in reader)
                # Restar el encabezado
                row_count -= 1

            # Inicializar el estado en Redis
            redis_client.hset(f"process:{process_id}", "total_rows", row_count)
            redis_client.hset(f"process:{process_id}", "processed_rows", 0)
            redis_client.hset(f"process:{process_id}", "status", "processing")
            redis_client.hset(f"process:{process_id}", "filename", os.path.basename(file_path))

            # Guardar los encabezados para uso posterior
            redis_client.hset(f"process:{process_id}", "headers", json.dumps(headers))

            # Leer el archivo y procesar en bloques
            with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, dialect)
                chunk_index = 0
                chunk_data = []
                current_size = 0
                row_index = 0

                for row in reader:
                    # Añadir fila al chunk actual
                    chunk_data.append(row)

                    # Calcular el tamaño del chunk aproximado en bytes
                    row_size = sum(len(str(cell)) for cell in row)
                    current_size += row_size
                    row_index += 1

                    logging.debug(f'Fila {row_index} - Tamaño total: {row_size} - Tamaño actual: {current_size}')

                    if (len(chunk_data) >= MAX_ROWS_PER_CHUNK or
                        current_size >= MAX_CHUNKS_SIZE or
                        row_index == row_count):

                        # Producir el bloque
                        message = {
                            "process_id": process_id,
                            "products": chunk_data,
                            "row_count": len(chunk_data),
                            "total_rows": row_count,
                            "start_row": row_index - len(chunk_data)
                        }
                        logging.debug("Producing message")
                        self.producer.produce(message)

                        # Actualizar el estado en Redis
                        logging.debug(f"process:{process_id}", "processed_rows", row_index)
                        redis_client.hset(f"process:{process_id}", "processed_rows", row_index)

                        # Limpiar el chunk
                        chunk_data = []
                        current_size = 0
                        chunk_index += 1

            # Actualizar el estado en Redis
            redis_client.hset(f"process:{process_id}", "status", 'completed')
            logging.debug("Processing completed")
        except Exception as e:
            # Registrar error
            logging.error(str(e))
            redis_client.hset(f"process:{process_id}", "status", f"error: {str(e)}")
            # Limpiar archivos
            try:
                os.remove(file_path)
            except:
                pass

    def get_status(self, process_id):
        if not redis_client.exists(f"process:{process_id}"):
            return {"error": "Proceso no encontrado"}, 404

        status = redis_client.hget(f"process:{process_id}", "status").decode('utf-8')
        total_rows = int(redis_client.hget(f"process:{process_id}", "total_rows"))
        processed_rows = int(redis_client.hget(f"process:{process_id}", "processed_rows"))
        filename = redis_client.hget(f"process:{process_id}", "filename").decode('utf-8')

        # Calcular progreso
        progress = (processed_rows / total_rows) * 100 if total_rows > 0 else 0

        # Si el procesamiento está completo, preparar resultados
        if status == "completed":
            # Obtener resumen del procesamiento
            summary = json.loads(redis_client.get(f"process:{process_id}:summary") or '{}')

            # Devolver datos procesados
            return {
                "status": status,
                "progress": 100,
                "filename": filename,
                "total_rows": total_rows,
                "processed_rows": processed_rows,
                "summary": summary
            }, 200

        # Si sigue en proceso o hubo error
        return {
            "status": status,
            "progress": progress,
            "filename": filename,
            "total_rows": total_rows,
            "processed_rows": processed_rows
        }, 200