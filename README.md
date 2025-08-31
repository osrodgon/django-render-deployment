# API de Libros con Django, MySQL y Docker

Este proyecto es una API RESTful para la gestión de libros y categorías, construida con Python, Django y Django REST Framework. El entorno está completamente containerizado con Docker y Docker Compose para facilitar su configuración, desarrollo y despliegue.

## ✨ Características

- **API RESTful**: Endpoints para operaciones CRUD (Crear, Leer, Actualizar, Eliminar) sobre libros y categorías.
- **Framework Robusto**: Construido sobre Django y Django REST Framework.
- **Base de Datos MySQL**: Orquestada a través de Docker Compose.
- **Entorno Containerizado**: Configuración de desarrollo lista para usar con un solo comando.
- **Persistencia de Datos**: Utiliza un volumen de Docker para que los datos de la base de datos no se pierdan al reiniciar los contenedores.
- **Frontend de Ejemplo**: Incluye un pequeño dashboard con Streamlit para interactuar con la API.

## 🛠️ Tecnologías Utilizadas

- **Backend**: Python, Django, Django REST Framework
- **Base de Datos**: MySQL
- **Containerización**: Docker, Docker Compose
- **Frontend (Ejemplo)**: Streamlit
- **Dependencias Clave**:
  - `mysqlclient`: Adaptador de MySQL para Python.
  - `python-dotenv`: Para gestionar variables de entorno.
  - `django-cors-headers`: Para manejar cabeceras CORS.

## 🚀 Cómo Empezar

Sigue estos pasos para levantar el proyecto completo en tu máquina local.

### Prerrequisitos

Asegúrate de tener instaladas las siguientes herramientas en tu sistema:
- Docker
- Docker Compose

### ⚙️ Configuración

1.  **Clona el repositorio:**
    ```bash
    git clone <URL_DEL_REPOSITORIO>
    cd django-render-deployment
    ```

2.  **Configura las variables de entorno:**
    Crea un archivo `.env` en la raíz del proyecto. Este archivo centraliza toda la configuración sensible.

    ```bash
    touch .env
    ```

    Añade el siguiente contenido al archivo `.env`. Estos valores serán utilizados por Docker Compose para configurar tanto la base de datos como la aplicación Django.

    ```ini
    # .env

    # Clave secreta de Django. ¡Cámbiala por una nueva para producción!
    # Puedes generar una aquí: https://djecrety.ir/
    SECRET_KEY='django-insecure-tu-clave-secreta-aqui'

    # Modo Debug. Cambiar a False en producción.
    DEBUG=True

    # Configuración de la base de datos MySQL
    # Estos valores son usados por los servicios 'db' y 'web' en compose.yaml
    DB_NAME=booksdb
    DB_USER=admin
    DB_PASSWORD=tu_contraseña_segura
    DB_ROOT_PASSWORD=tu_contraseña_root_muy_segura # Contraseña para el usuario root de MySQL
    DB_HOST=db # ¡Importante! Este debe ser el nombre del servicio de la DB en compose.yaml
    DB_PORT=3306
    ```

### 🐳 Ejecución con Docker Compose

El proyecto incluye un fichero `compose.yaml` para orquestar los servicios. El contenido de este fichero es crucial para un funcionamiento correcto.

1.  **Asegura el contenido del fichero `compose.yaml`:**
    El siguiente contenido es la versión recomendada, ya que automatiza las migraciones y configura correctamente la red entre contenedores.

    ```yaml
    # compose.yaml
    version: '3.8'

    services:
      db:
        image: mysql:8.0
        command: '--default-authentication-plugin=mysql_native_password'
        volumes:
          - mysql_data:/var/lib/mysql
        environment:
          MYSQL_DATABASE: ${DB_NAME}
          MYSQL_USER: ${DB_USER}
          MYSQL_PASSWORD: ${DB_PASSWORD}
          MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
        ports:
          - "3306:3306" # Mapeo estándar para facilitar la conexión
        restart: always

      web:
        build: .
        # Espera a la DB, ejecuta migraciones y luego inicia el servidor
        command: >
          sh -c "sleep 10 && python manage.py migrate &&
                 python manage.py runserver 0.0.0.0:8010"
        volumes:
          - .:/app
        ports:
          - "8010:8010" # El puerto interno es 8010, se expone como 8010
        env_file: .env # Simplificado a un solo fichero .env
        environment:
          - DB_HOST=db # El host es el nombre del servicio de la base de datos
          - DB_PORT=3306
        depends_on:
          - db
        restart: always

    volumes:
      mysql_data:
    ```

2.  **Levanta los servicios:**
    Este comando construirá las imágenes, creará los contenedores y los iniciará en segundo plano (`-d`). El servicio `web` esperará 10 segundos para que la base de datos se inicie, aplicará las migraciones y luego arrancará el servidor.

    ```bash
    docker compose -f compose.yaml up --build -d
    ```

    - La **API de Django** estará disponible en `http://localhost:8010`.
    - La **base de datos MySQL** estará expuesta en el puerto `3306` de tu máquina local.

3.  **Verifica que los contenedores están en ejecución:**
    ```bash
    docker compose -f compose.yaml ps
    ```

4.  **Para detener los servicios:**
    Este comando detendrá y eliminará los contenedores. El volumen de la base de datos (`mysql_data`) no se eliminará, por lo que tus datos persistirán.
    ```bash
    docker compose -f compose.yaml down
    ```

## 🔌 Endpoints de la API

La API está versionada y la base de las rutas es `/v1/`.

### Libros (`/v1/libros/`)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/v1/libros/` | Obtiene una lista de todos los libros. |
| `POST` | `/v1/libros/crear` | Crea un nuevo libro. |
| `GET` | `/v1/libros/<id>` | Obtiene un libro específico por su ID. |
| `PUT` | `/v1/libros/<id>` | Actualiza un libro existente. |
| `DELETE` | `/v1/libros/<id>` | Elimina un libro por su ID. |

### Categorías (`/v1/categorias/`)

| Método | Ruta | Descripción |
| :--- | :--- | :--- |
| `GET` | `/v1/categorias/` | Obtiene una lista de todas las categorías. |
| `POST` | `/v1/categorias/crear` | Crea una nueva categoría. |
| `GET` | `/v1/categorias/<id>` | Obtiene una categoría específica por su ID. |
| `PUT` | `/v1/categorias/<id>` | Actualiza una categoría existente. |
| `DELETE` | `/v1/categorias/<id>` | Elimina una categoría por su ID. |

### Ejemplo de uso con `curl`

**Crear una categoría:**
```bash
curl -X POST -H "Content-Type: application/json" -d '{"nombre_categoria": "Ciencia Ficción"}' http://localhost:8010/v1/categorias/crear
```

**Crear un libro (asumiendo que la categoría con ID 1 existe):**
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"titulo": "Dune", "autor": "Frank Herbert", "isbn": "9780441013593", "fecha_publicacion": "1965-08-01", "categorias": [1]}' \
http://localhost:8010/v1/libros/crear
```

**Obtener todos los libros:**
```bash
curl http://localhost:8010/v1/libros/
```

##  frontend con Streamlit

El proyecto incluye un archivo `app.py` con una interfaz simple creada con Streamlit para interactuar con la API.

1.  **Asegúrate de que los contenedores de Docker estén en ejecución.**

2.  **Instala las dependencias necesarias en tu entorno local (fuera de Docker):**
    ```bash
    pip install streamlit requests
    ```

3.  **Ejecuta la aplicación de Streamlit:**
    *Nota: El código en `app.py` puede necesitar que ajustes la URL de la API de `http://127.0.0.1:8000` a `http://localhost:8010` para que funcione correctamente con la configuración de Docker Compose.*

    ```bash
    streamlit run app.py
    ```

## 🗃️ Estructura del Proyecto

```
.
├── book_system/          # Directorio principal del proyecto Django
│   ├── settings.py       # Configuración del proyecto
│   └── urls.py           # URLs principales
├── books/                # App de Django para la lógica de libros
├── categories/           # App de Django para la lógica de categorías
├── .env                  # (No versionado) Variables de entorno
├── .env.example          # Ejemplo de variables de entorno
├── app.py                # Frontend de ejemplo con Streamlit
├── compose.yml           # Orquestación de servicios con Docker Compose
├── Dockerfile            # Instrucciones para construir la imagen de la app
├── manage.py             # Utilidad de línea de comandos de Django
└── requirements.txt      # Dependencias de Python
```