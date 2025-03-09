# Experimiento de Arquitectura 1

## Descripción

Este proyecto tiene como finalidad la experimentación de los atributos de calidad de Latencia para dos componentes con alto impacto dentro del ecosistema de Compañía Comercializadora de productos:

- Productos
- BFF web

## Requisitos

- Docker
- Docker Compose
- Python
- Flask
- RabbitMQ
- Postgresql

## Configuración del Entorno

### Variables de Entorno

Asegúrate de configurar las siguientes variables de entorno en tu archivo `docker-compose.yml`:

- `DB_USER`: Usuario de la base de datos PostgreSQL.
- `DB_PASSWORD`: Contraseña de la base de datos PostgreSQL.
- `DB_HOST`: Host de la base de datos PostgreSQL.
- `DB_PORT`: Puerto de la base de datos PostgreSQL.
- `DB_NAME`: Nombre de la base de datos PostgreSQL.
- `RABBITMQ_USER`: Usuario de RabbitMQ.
- `RABBITMQ_PASSWORD`: Contraseña de RabbitMQ.
- `RABBITMQ_HOST`: Host de RabbitMQ.
- `RABBITMQ_PORT`: Puerto de RabbitMQ.
- `PRODUCTS_ROUTING_KEY`: Clave de enrutamiento para la cola de productos en RabbitMQ.

## Instalación

1. Clona el repositorio:

   ```sh
   git clone git@github.com:edwinsilva-miso/grupo12_experimento1.git
   cd grupo12_experimento1
   ```

2. Construye y levanta los contenedores de Docker:

   ```sh
   docker-compose up --build
   ```

## Uso

El microservicio estará disponible en `http://localhost:5000`. Asegúrate de que RabbitMQ y PostgreSQL estén corriendo y configurados correctamente.

## Estructura del Proyecto

- `productos/`: Contiene el código fuente del microservicio.
  - `src/`: Código fuente principal.
    - `infrastructure/`: Código relacionado con la infraestructura, como consumidores de RabbitMQ.
    - `adapter/`: Adaptadores para interactuar con otras capas.
    - `mapper/`: Mapeadores para transformar datos.
    - `application/`: Lógica de aplicación y casos de uso.
- `docker-compose.yml`: Configuración de Docker Compose.
- `Dockerfile`: Configuración del contenedor Docker para el microservicio.

```
.
├── ccp_web_bff
│   ├── Dockerfile
│   ├── Pipfile
│   ├── __init__.py
│   └── src
│       ├── __init__.py
│       ├── blueprints
│       │   ├── __init__.py
│       │   └── products_blueprint.py
│       ├── commands
│       │   ├── __init__.py
│       │   └── process_file.py
│       ├── main.py
│       └── producers
│           ├── __init__.py
│           └── products_load_producer.py
├── docker-compose.yml
├── generador_prueba
│   ├── __init__.py
│   └── test_generator.py
└── productos
    ├── Dockerfile
    ├── Pipfile
    ├── __init__.py
    └── src
        ├── __init__.py
        ├── application
        │   ├── __init__.py
        │   ├── create_multiple_products.py
        │   ├── create_product.py
        │   ├── delete_product.py
        │   ├── get_all_products.py
        │   ├── get_product_by_id.py
        │   └── update_product.py
        ├── domain
        │   ├── __init__.py
        │   ├── entities
        │   │   ├── __init__.py
        │   │   └── product_dto.py
        │   └── repositories
        │       ├── __init__.py
        │       └── product_repository.py
        ├── infrastructure
        │   ├── __init__.py
        │   ├── adapter
        │   │   ├── __init__.py
        │   │   └── product_adapter.py
        │   ├── consumer
        │   │   ├── __init__.py
        │   │   └── products_load_consumer.py
        │   ├── dao
        │   │   ├── __init__.py
        │   │   └── product_dao.py
        │   ├── database
        │   │   ├── __init__.py
        │   │   └── declarative_base.py
        │   ├── mapper
        │   │   ├── __init__.py
        │   │   └── product_mapper.py
        │   └── model
        │       ├── __init__.py
        │       └── product_model.py
        ├── interface
        │   ├── __init__.py
        │   └── product_blueprint.py
        └── main.py

```

## Ejecutar proyecto

### Infraestructura requerida

```bash
$ docker-compose up -d rabbitmq db
```

### BFF

```bash
$ pipenv install
$ pipenv run python -m src.main
```

### Productos

```bash
$ pipenv install
$ pipenv run python -m src.main
```


## Ejecución

- Generar archivos de prueba

```bash
$ cd generador_prueba
$ python test_generator.py
```
Esto generará los archivos:

```
├── generador_prueba
│   ├── __init__.py
│   ├── products_10mb.csv
│   ├── products_1mb.csv
│   ├── products_2mb.csv
│   ├── products_5mb.csv
│   └── test_generator.py

```

- Ejecución del BFF de carga de productos

```bash
curl --location 'http://localhost:5001/bff/products/upload' \
--form 'file=@"${FILEPATH}/products.csv"'
```

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---