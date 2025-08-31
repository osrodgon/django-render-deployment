# API de Libros con Django REST Framework

Este proyecto es una API RESTful para gestionar libros y categorías, construida con Python, Django y Django REST Framework. Está diseñada para conectarse a una base de datos PostgreSQL y está completamente containerizada con Docker, facilitando su despliegue en plataformas como Render.

## ✨ Características

- **API RESTful**: Endpoints para operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre libros y categorías.
- **Framework Robusto**: Construido sobre Django y Django REST Framework.
- **Base de Datos PostgreSQL**: Configurado para una base de datos relacional potente.
- **Containerización**: Listo para producción con un `Dockerfile` optimizado.
- **Configuración Flexible**: Utiliza variables de entorno para la configuración de la base de datos y secretos.
- **CORS Habilitado**: Preparado para integrarse con frontends de diferentes orígenes.

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python, Django, Django REST Framework
- **Base de Datos**: PostgreSQL
- **Containerización**: Docker
- **Dependencias Clave**:
  - `psycopg2-binary`: Adaptador de PostgreSQL para Python.
  - `djangorestframework`: Toolkit para construir APIs web.
  - `django-cors-headers`: Para manejar cabeceras CORS.
  - `python-dotenv`: Para gestionar variables de entorno.

## 🚀 Cómo Empezar

Sigue estos pasos para configurar y ejecutar el proyecto en un entorno de desarrollo local o para despliegue.

### Prerrequisitos

- Docker
- Una base de datos PostgreSQL accesible (local o remota).

### ⚙️ Configuración

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd django-render-deployment
    ```

2.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto. Puedes copiar el contenido de `.env.example` y ajustarlo a tu configuración.

    ```bash
    cp .env.example .env
    ```

    Abre el archivo `.env` y edita las variables.

    ```ini
    # .env

    # Clave secreta de Django. ¡Cámbiala por una nueva para producción!
    # Puedes generar una aquí: https://djecrety.ir/
    SECRET_KEY='django-insecure-tu-clave-aqui'

    # Modo Debug. Cambiar a False en producción.
    DEBUG=True

    # Configuración de la base de datos PostgreSQL
    DB_NAME=booksdb
    DB_USER=admin
    DB_PASSWORD=tu_contraseña_segura # Usa la misma que en compose.yml
    DB_HOST=db # Para Docker Compose. Cambia a 'localhost' para ejecución local.
    DB_PORT=5432
    ```

3.  **Crea un script de despliegue (Opcional, recomendado para Render):**
    Los servicios de hosting como Render pueden usar un script para construir y lanzar la aplicación. Crea un archivo `build.sh` en la raíz del proyecto.

    ```bash
    touch build.sh
    chmod +x build.sh
    ```

    Añade el siguiente contenido a `build.sh`. Este script instalará las dependencias, aplicará las migraciones y recolectará los archivos estáticos.

    ```sh
    #!/usr/bin/env bash
    # exit on error
    set -o errexit

    pip install -r requirements.txt

    python manage.py collectstatic --no-input
    python manage.py migrate
    ```

### 🐳 Ejecución con Docker Compose

Usar Docker Compose simplifica la gestión de los contenedores de la aplicación y la base de datos.

1.  **Crea un archivo `compose.yml` en la raíz del proyecto:**

    ```bash
    touch compose.yml
    ```

    Añade el siguiente contenido. Este archivo define los servicios de la aplicación (`web`) y la base de datos (`db`).

    ```yaml
    version: '3.8'

    services:
      db:
        image: postgres:13
        volumes:
          - postgres_data:/var/lib/postgresql/data/
        environment:
          - POSTGRES_DB=${DB_NAME}
          - POSTGRES_USER=${DB_USER}
          - POSTGRES_PASSWORD=${DB_PASSWORD}

      web:
        build: .
        command: >
          sh -c "python manage.py migrate &&
                 python manage.py runserver 0.0.0.0:8010"
        volumes:
          - .:/app
        ports:
          - "8010:8010"
        env_file: .env
        environment:
          - DB_HOST=db
        depends_on:
          - db

    volumes:
      postgres_data:
    ```

2.  **Levanta los servicios:**
    Este comando construirá las imágenes, creará los contenedores y los iniciará. También aplicará las migraciones de la base de datos automáticamente al arrancar el servicio `web`.

    ```bash
    docker compose up --build
    ```

    - La API estará disponible en `http://localhost:8010`.
    - La base de datos PostgreSQL estará accesible en el puerto `5432` de tu `localhost`.

3.  **Para detener los servicios:**
    Presiona `Ctrl+C` en la terminal donde se están ejecutando, o ejecuta el siguiente comando desde otra terminal en la raíz del proyecto:
    ```bash
    docker compose down
    ```

## 🔌 Endpoints de la API (Inferidos)

Los endpoints exactos se definen en los archivos `urls.py` de las aplicaciones. Basado en la estructura, los endpoints probables para las operaciones CRUD son:

| Método | Ruta               | Descripción                     |
| :----- | :----------------- | :------------------------------ |
| `GET`    | `/api/books/`      | Obtiene una lista de libros.    |
| `GET`    | `/api/books/:id/`  | Obtiene un libro por su ID.     |
| `POST`   | `/api/books/`      | Crea un nuevo libro.            |
| `PUT`    | `/api/books/:id/`  | Actualiza un libro existente.   |
| `DELETE` | `/api/books/:id/`  | Elimina un libro.               |

Y de forma similar para las categorías:

| Método | Ruta                  | Descripción                        |
| :----- | :-------------------- | :--------------------------------- |
| `GET`    | `/api/categories/`    | Obtiene una lista de categorías.   |
| `GET`    | `/api/categories/:id/`| Obtiene una categoría por su ID.   |
| `POST`   | `/api/categories/`    | Crea una nueva categoría.          |
| `PUT`    | `/api/categories/:id/`| Actualiza una categoría existente. |
| `DELETE` | `/api/categories/:id/`| Elimina una categoría.             |

## 🗃️ Estructura del Proyecto

```
.
├── books/                # App de Django para la lógica de libros
├── categories/           # App de Django para la lógica de categorías
├── book_system/
│   ├── settings.py       # Configuración del proyecto Django
│   ├── urls.py           # Rutas principales del proyecto
│   └── ...
├── .env.example          # Ejemplo de variables de entorno
├── build.sh              # Script de construcción para despliegue
├── Dockerfile            # Instrucciones para construir la imagen de Docker
├── manage.py             # Utilidad de línea de comandos de Django
└── requirements.txt      # Dependencias de Python
```
