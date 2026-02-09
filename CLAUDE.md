# CLAUDE.md - Guía de Desarrollo

## Descripción del Proyecto

Blog personal "Juancito escribe boludeces" construido con Wagtail CMS y Django. El blog cubrirá temas de tecnología, viajes, ferrocarriles y otros intereses personales.

## Stack Tecnológico

- **Framework:** Django 6.x
- **CMS:** Wagtail 7.3rc1
- **Base de datos:** SQLite (desarrollo) / PostgreSQL (producción)
- **Servidor WSGI:** Gunicorn (producción)
- **Contenedores:** Docker

## Estructura del Proyecto

```
my-blog/
├── home/                    # App principal del blog
│   ├── models.py           # Modelos de páginas (HomePage)
│   ├── templates/home/     # Templates de la app
│   └── static/css/         # Estilos específicos
├── search/                  # Funcionalidad de búsqueda
│   ├── views.py            # Vista de búsqueda con paginación
│   └── templates/search/   # Template de resultados
├── mysite/                  # Configuración del proyecto
│   ├── settings/           # Settings por entorno (base, dev, production)
│   ├── templates/          # Templates base (base.html, 404, 500)
│   ├── static/             # Assets estáticos globales
│   └── urls.py             # Rutas principales
├── manage.py
├── requirements.txt
└── Dockerfile
```

## Comandos Útiles

```bash
# Activar entorno virtual
source env/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Correr migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Servidor de desarrollo
python manage.py runserver

# Crear nuevas migraciones
python manage.py makemigrations

# Colectar archivos estáticos
python manage.py collectstatic
```

## URLs Importantes

- **Frontend:** http://localhost:8000
- **Admin Wagtail:** http://localhost:8000/admin
- **Admin Django:** http://localhost:8000/django-admin
- **Búsqueda:** http://localhost:8000/search

## Modelo de Datos Actual

### HomePage (home/models.py)
- Modelo básico que hereda de `wagtail.models.Page`
- Sin campos personalizados definidos aún

## Estructura Deseada del Blog

### Header
- Logo
- Nombre: "Juancito escribe boludeces"
- Navegación: Home, Viajes, Tecnología, Hablemos de Trenes, Buscador, Contacto

### Main Content
- Resumen de publicaciones con foto y link
- Espacio para videos de YouTube
- Sidebar de publicidad (derecha)

### Footer
- Links importantes
- Redes sociales
- Copyright
- Contacto

## Modelos a Implementar

1. **BlogIndexPage** - Página índice que lista todos los posts
2. **BlogPage** - Página individual de post con:
   - Título
   - Fecha de publicación
   - Autor
   - Imagen destacada
   - Contenido (StreamField para flexibilidad)
   - Categoría (Viajes, Tecnología, Trenes, Otros)
   - Tags
   - Excerpt/resumen

3. **CategoryPage** - Página de categoría que filtra posts

4. **ContactPage** - Formulario de contacto (usando wagtail.contrib.forms)

## Convenciones de Código

- **Idioma del código:** Inglés (nombres de clases, variables, funciones)
- **Idioma del contenido:** Español
- **Templates:** Usar herencia de base.html
- **Estilos:** Planificar integración con Bootstrap
- **Migraciones:** Crear migraciones descriptivas

## Consideraciones de Wagtail

- Los modelos de página heredan de `wagtail.models.Page`
- Usar `StreamField` para contenido flexible (texto, imágenes, videos)
- Usar `FieldPanel`, `MultiFieldPanel` para organizar el admin
- Las imágenes se manejan con `wagtail.images.models.Image`
- Los documentos con `wagtail.documents.models.Document`

## Testing

El proyecto usa `WagtailPageTestCase` para tests de páginas.
Correr tests: `python manage.py test`

## Próximos Pasos Sugeridos

1. [ ] Crear modelo BlogPage con campos básicos
2. [ ] Crear modelo BlogIndexPage para listar posts
3. [ ] Implementar categorías (Viajes, Tecnología, Trenes)
4. [ ] Diseñar templates con Tailwind CSS
5. [ ] Integrar embeds de YouTube
6. [ ] Crear formulario de contacto
7. [ ] Implementar sidebar de publicidad
8. [ ] Agregar footer con redes sociales
9. [ ] Configurar búsqueda para indexar posts
10. [ ] Optimizar para SEO
