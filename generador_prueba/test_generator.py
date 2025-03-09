import csv
import random
import os


def generate_product_name():
    """Genera un nombre de producto aleatorio"""
    adjectives = ['Premium', 'Deluxe', 'Super', 'Ultra', 'Mega', 'Pro', 'Elite', 'Classic', 'Vintage', 'Smart',
                  'Eco', 'Tech', 'Modern', 'Digital', 'Advanced', 'Portable', 'Wireless', 'Compact', 'Professional']

    nouns = ['Laptop', 'Phone', 'Camera', 'Tablet', 'Watch', 'Speaker', 'Headphones', 'Monitor', 'Keyboard',
             'Mouse', 'Charger', 'Adapter', 'Cable', 'Drive', 'Router', 'Scanner', 'Printer', 'Microphone',
             'Drone', 'Console', 'Controller', 'Projector', 'Server', 'Device', 'Machine', 'System', 'Tool']

    brands = ['TechX', 'DigiMart', 'FutureTech', 'SmartWave', 'ElectroPro', 'NovaTech', 'GigaBytes', 'InfoSphere',
              'ByteWorks', 'MegaComp', 'CyberTech', 'DataFlow', 'CoreTech', 'NetVision', 'PrimeWare', 'AlphaByte']

    models = ['X1', 'V2', 'Pro', 'Plus', 'Max', 'Ultra', 'Lite', 'Mini', 'Nano', 'Z9', 'A7', 'S5', 'M3',
              'G10', 'T500', 'R700', '2000', '3000', '5000', 'Elite', 'Premium', 'Standard']

    # Generación aleatoria con formato variado
    name_format = random.choice([
        f"{random.choice(brands)} {random.choice(adjectives)} {random.choice(nouns)} {random.choice(models)}",
        f"{random.choice(adjectives)} {random.choice(nouns)} {random.choice(models)} by {random.choice(brands)}",
        f"{random.choice(brands)} {random.choice(nouns)} {random.choice(models)}",
        f"{random.choice(adjectives)} {random.choice(nouns)}"
    ])

    return name_format


def generate_price():
    """Genera un precio aleatorio en formato decimal"""
    # Generar precio entre $10 y $2000
    price = round(random.uniform(10.0, 2000.0), 2)
    return price


def generate_csv_file(filename, target_size_mb):
    """
    Genera un archivo CSV con nombres y precios hasta alcanzar el tamaño objetivo.

    Args:
        filename (str): Nombre del archivo a generar
        target_size_mb (int): Tamaño objetivo en MB
    """
    target_size_bytes = target_size_mb * 1024 * 1024

    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['name', 'price'])  # Encabezados

        current_size = 0
        rows_written = 0

        # Escribir filas hasta alcanzar el tamaño aproximado
        while current_size < target_size_bytes:
            name = generate_product_name()
            price = generate_price()
            writer.writerow([name, price])

            # Actualizar tamaño aproximado (añadiendo longitud de la fila + salto de línea)
            row_size = len(name) + len(str(price)) + 2  # +2 para la coma y el salto de línea
            current_size += row_size
            rows_written += 1

            # Mostrar progreso cada 10,000 filas
            if rows_written % 10000 == 0:
                print(f"Progreso {filename}: {current_size / target_size_bytes * 100:.1f}% ({rows_written:,} filas)")

    # Obtener tamaño real del archivo
    actual_size_mb = os.path.getsize(filename) / (1024 * 1024)
    print(f"Archivo generado: {filename}")
    print(f"Tamaño: {actual_size_mb:.2f} MB")
    print(f"Filas generadas: {rows_written:,}")
    print("-" * 40)


def main():
    # Configuración de archivos a generar
    files_to_generate = [
        {"filename": "products_1mb.csv", "size_mb": 1},
        {"filename": "products_2mb.csv", "size_mb": 2},
        {"filename": "products_5mb.csv", "size_mb": 5},
        {"filename": "products_10mb.csv", "size_mb": 10}
    ]

    print("Iniciando generación de archivos CSV de prueba")
    print("=" * 40)

    # Generar cada archivo
    for file_config in files_to_generate:
        generate_csv_file(file_config["filename"], file_config["size_mb"])

    print("Generación de archivos completada")


if __name__ == "__main__":
    main()