# Juancito escribe boludeces

Blog personal sobre tecnología, viajes, ferrocarriles y otras cosas.

## Stack

- **Framework:** Django 6.x
- **CMS:** Wagtail 7.x
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Estilos:** Tailwind CSS (CDN)
- **Servidor WSGI:** Gunicorn (producción)
- **Contenedores:** Docker

## Requisitos

- Python 3.11+
- pip

## Instalación y ejecución local

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd my-blog

# 2. Crear y activar entorno virtual
python -m venv env
source env/bin/activate  # Windows: env\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear superusuario (para acceder al admin)
python manage.py createsuperuser

# 6. Correr el servidor de desarrollo
python manage.py runserver
```

## Variables de entorno

Copiá `.env.example` a `.env` y completá los valores:

```bash
cp .env.example .env
```

El archivo `.env.example` documenta todas las variables disponibles. En desarrollo las variables de Django ya vienen hardcodeadas en `mysite/settings/dev.py`, así que esto solo es necesario para producción.

## URLs

| URL | Descripción |
|-----|-------------|
| `http://localhost:8000` | Frontend del blog |
| `http://localhost:8000/admin` | Admin de Wagtail (CMS) |
| `http://localhost:8000/django-admin` | Admin de Django |
| `http://localhost:8000/search` | Búsqueda |
| `http://localhost:8000/contacto` | Formulario de contacto |

## Estructura del proyecto

```
my-blog/
├── home/                    # App principal del blog
│   ├── models.py           # Modelos: HomePage, BlogIndexPage, BlogPage, ContactPage
│   ├── templates/home/     # Templates de cada tipo de página
│   └── migrations/         # Migraciones de base de datos
├── search/                  # Funcionalidad de búsqueda
│   ├── views.py
│   └── templates/search/
├── mysite/                  # Configuración del proyecto
│   ├── settings/
│   │   ├── base.py         # Settings compartidos
│   │   ├── dev.py          # Settings de desarrollo
│   │   └── production.py   # Settings de producción
│   ├── templates/
│   │   ├── base.html       # Template base del que heredan todos
│   │   └── components/     # Header, footer, sidebar, etc.
│   └── static/
│       └── images/         # Logo y otros assets globales
├── .env.example            # Variables de entorno documentadas
├── requirements.txt
└── Dockerfile
```

## Modelos principales

| Modelo | Descripción |
|--------|-------------|
| `BlogCategory` | Snippet de categorías (Viajes, Tecnología, Trenes, Otros) |
| `HomePage` | Página principal del sitio |
| `BlogIndexPage` | Listado de posts con filtros y paginación |
| `BlogPage` | Post individual con StreamField flexible |
| `ContactPage` | Formulario de contacto gestionado desde el admin |

## Comandos útiles

```bash
# Crear nuevas migraciones
python manage.py makemigrations

# Colectar archivos estáticos (producción)
python manage.py collectstatic

# Correr tests
python manage.py test
```
