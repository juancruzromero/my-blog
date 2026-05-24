# CLAUDE.md

Blog personal "Juancito escribe boludeces" — Django 6.x + Wagtail 7.x, SQLite en desarrollo, PostgreSQL en producción.

## Arranque rápido

```bash
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

URLs: frontend `localhost:8000` · Wagtail admin `/admin` · Django admin `/django-admin`

## Convenciones

- **Código en inglés**, contenido en español
- **PEP 8** estricto + type hints + f-strings; imports explícitos ordenados: stdlib → Django/Wagtail → terceros → locales
- Templates heredan de `base.html`; estilos con Tailwind CSS (CDN)
- Migraciones con nombre descriptivo (`makemigrations <app> --name <descripcion>`)

## Wagtail

Docs: https://docs.wagtail.org/en/stable/

- Siempre definir `parent_page_types` y `subpage_types` en cada modelo de página
- Lógica de contexto en `get_context()`, no en vistas separadas
- Formularios via `wagtail.contrib.forms` (ya instalado)

## Pendiente

- Formulario de contacto: crear página en el admin con slug `contacto`
- Búsqueda: mejorar para filtrar solo `BlogPage` y agregar filtro por categoría
- SEO: sitemap, robots.txt, Open Graph, JSON-LD
