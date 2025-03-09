# Productos Microservice

## Descripción

Este proyecto es un microservicio para la gestión de productos. Utiliza Python, Flask, RabbitMQ y PostgreSQL. El microservicio se encarga de recibir mensajes de productos a través de RabbitMQ y procesarlos para almacenarlos en una base de datos PostgreSQL.

## Requisitos

- Docker
- Docker Compose

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
   git clone <URL_DEL_REPOSITORIO>
   cd <NOMBRE_DEL_REPOSITORIO>
   ```

2. Construye y levanta los contenedores de Docker:

   ```sh
   docker-compose up --build
   ```

## Uso

El microservicio estará disponible en `http://localhost:5000`. Asegúrate de que RabbitMQ y PostgreSQL estén corriendo y configurados correctamente.

### Endpoints

- **GET** `/health`: Verifica el estado del microservicio.

## Estructura del Proyecto

- `productos/`: Contiene el código fuente del microservicio.
  - `src/`: Código fuente principal.
    - `infrastructure/`: Código relacionado con la infraestructura, como consumidores de RabbitMQ.
    - `adapter/`: Adaptadores para interactuar con otras capas.
    - `mapper/`: Mapeadores para transformar datos.
    - `application/`: Lógica de aplicación y casos de uso.
- `docker-compose.yml`: Configuración de Docker Compose.
- `Dockerfile`: Configuración del contenedor Docker para el microservicio.

## Desarrollo

### Ejecutar Pruebas

Para ejecutar las pruebas, usa el siguiente comando:

```sh
pipenv run pytest
```

### Contribuir

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube tus cambios (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

---