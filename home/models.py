from django.db import models

from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.blocks import CharBlock, RichTextBlock, TextBlock, BlockQuoteBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


# =============================================================================
# Snippets
# =============================================================================

@register_snippet
class BlogCategory(models.Model):
    """Categorías para clasificar los posts del blog."""
    name = models.CharField(max_length=100, verbose_name="Nombre")
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, verbose_name="Descripción")
    color = models.CharField(
        max_length=7,
        default="#3B82F6",
        help_text="Color en formato hex (ej: #3B82F6)"
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
        FieldPanel('color'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"


# =============================================================================
# Tags
# =============================================================================

class BlogPageTag(TaggedItemBase):
    """Relación entre BlogPage y Tags."""
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


# =============================================================================
# Pages
# =============================================================================

class HomePage(Page):
    """Página principal del sitio."""
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('body'),
    ]


class BlogIndexPage(Page):
    """Página índice que lista todos los posts del blog."""
    intro = RichTextField(blank=True, verbose_name="Introducción")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    # Solo puede contener BlogPages como hijos
    subpage_types = ['home.BlogPage']

    # Solo puede estar bajo HomePage
    parent_page_types = ['home.HomePage']

    def get_context(self, request):
        context = super().get_context(request)

        # Obtener posts publicados, ordenados por fecha
        posts = BlogPage.objects.live().descendant_of(self).order_by('-date')

        # Filtro por categoría
        category_slug = request.GET.get('category')
        if category_slug:
            posts = posts.filter(category__slug=category_slug)

        # Filtro por tag
        tag = request.GET.get('tag')
        if tag:
            posts = posts.filter(tags__name=tag)

        # Paginación
        from django.core.paginator import Paginator
        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        context['posts'] = posts
        context['categories'] = BlogCategory.objects.all()

        return context


class BlogPage(Page):
    """Página individual de un post del blog."""

    # Campos principales
    subtitle = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Subtítulo"
    )
    date = models.DateField(verbose_name="Fecha de publicación")
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Imagen destacada"
    )
    excerpt = models.TextField(
        max_length=500,
        verbose_name="Resumen",
        help_text="Resumen corto para mostrar en listados (máx. 500 caracteres)"
    )
    reading_time = models.PositiveIntegerField(
        default=5,
        verbose_name="Tiempo de lectura",
        help_text="Tiempo estimado de lectura en minutos"
    )

    # Categoría y tags
    category = models.ForeignKey(
        'home.BlogCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name="Categoría"
    )
    tags = ClusterTaggableManager(
        through=BlogPageTag,
        blank=True,
        verbose_name="Tags"
    )

    # Contenido flexible con StreamField
    body = StreamField([
        ('heading', CharBlock(
            classname="title",
            help_text="Título de sección",
            label="Título"
        )),
        ('paragraph', RichTextBlock(label="Párrafo")),
        ('image', ImageChooserBlock(label="Imagen")),
        ('quote', BlockQuoteBlock(label="Cita")),
        ('code', TextBlock(
            help_text="Bloque de código",
            label="Código"
        )),
        ('video', EmbedBlock(
            help_text="Pega la URL de YouTube o Vimeo",
            label="Video"
        )),
    ], use_json_field=True, verbose_name="Contenido")

    # Paneles del admin
    content_panels = Page.content_panels + [
        FieldPanel('subtitle'),
        MultiFieldPanel([
            FieldPanel('date'),
            FieldPanel('reading_time'),
        ], heading="Información"),
        FieldPanel('featured_image'),
        FieldPanel('excerpt'),
        MultiFieldPanel([
            FieldPanel('category'),
            FieldPanel('tags'),
        ], heading="Clasificación"),
        FieldPanel('body'),
    ]

    # Configuración de búsqueda
    search_fields = Page.search_fields + [
        index.SearchField('subtitle'),
        index.SearchField('excerpt'),
        index.SearchField('body'),
        index.FilterField('category'),
        index.FilterField('date'),
        index.RelatedFields('tags', [
            index.SearchField('name'),
        ]),
    ]

    # Solo puede estar bajo BlogIndexPage
    parent_page_types = ['home.BlogIndexPage']

    # No puede tener páginas hijas
    subpage_types = []

    class Meta:
        verbose_name = "Post del Blog"
        verbose_name_plural = "Posts del Blog"


# =============================================================================
# Contact Form
# =============================================================================

class FormField(AbstractFormField):
    """Campo individual del formulario de contacto."""
    page = ParentalKey(
        'ContactPage',
        on_delete=models.CASCADE,
        related_name='form_fields'
    )


class ContactPage(AbstractEmailForm):
    """Página de contacto con formulario gestionado desde el admin de Wagtail."""
    intro = RichTextField(blank=True, verbose_name="Introducción")
    thank_you_text = RichTextField(blank=True, verbose_name="Texto de agradecimiento")

    content_panels = AbstractEmailForm.content_panels + [
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Campos del formulario"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldPanel('to_address'),
            FieldPanel('from_address'),
            FieldPanel('subject'),
        ], heading="Configuración de Email"),
    ]

    parent_page_types = ['home.HomePage']
    subpage_types = []

    def serve(self, request, *args, **kwargs):
        if request.method == 'POST' and request.POST.get('website'):
            return self.render_landing_page(request, None, *args, **kwargs)
        return super().serve(request, *args, **kwargs)

    class Meta:
        verbose_name = "Página de Contacto"
