from django.core.paginator import Paginator
from django.template.response import TemplateResponse

from home.models import BlogCategory, BlogPage


def search(request):
    search_query = request.GET.get("query", "")
    selected_category = request.GET.get("category", "")

    if search_query:
        qs = BlogPage.objects.live()
        if selected_category:
            qs = qs.filter(category__slug=selected_category)
        search_results = qs.search(search_query)
    else:
        search_results = BlogPage.objects.none()

    paginator = Paginator(search_results, 10)
    page_obj = paginator.get_page(request.GET.get("page"))

    return TemplateResponse(
        request,
        "search/search.html",
        {
            "search_query": search_query,
            "search_results": page_obj,
            "categories": BlogCategory.objects.all(),
            "selected_category": selected_category,
        },
    )
