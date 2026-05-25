from django import template

register = template.Library()


@register.inclusion_tag('home/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context: dict) -> dict:
    page = context.get('page')
    if page:
        ancestors = page.get_ancestors(inclusive=True)[1:]
        return {'ancestors': ancestors, 'current': page}
    return {'ancestors': [], 'current': None}
