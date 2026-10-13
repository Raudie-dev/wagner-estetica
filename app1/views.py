from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Blog
from django.contrib.auth.models import User

from app2.models import ProfileConfig, Service, ServiceCategory, ensure_service_categoria_column

def _service_category_order(service):
    cat = (getattr(service, 'categoria', None) or '').lower()
    order_map = {
        'dermocosmiatria': 0,
        'medicina-estetica': 1,
        'odontologia': 2,
        'depilacion': 3,
    }
    if cat in order_map:
        return order_map[cat]
    nombre = (service.nombre or '').lower()
    if 'dermocosmiatr' in nombre:
        return 0
    if 'medicina' in nombre or 'armoniza' in nombre:
        return 1
    if 'odontolog' in nombre:
        return 2
    if 'depila' in nombre or 'láser' in nombre or 'laser' in nombre:
        return 3
    return 4


# Create your views here.
def index(request):
    ensure_service_categoria_column()
    config = ProfileConfig.objects.first()
    servicios_qs = list(Service.objects.filter(activo=True))
    for s in servicios_qs:
        if s.nombre and 'definitiva' in s.nombre.lower():
            s.nombre = (
                s.nombre.replace('Depilación Definitiva Láser', 'Depilación Láser')
                .replace('Depilación Definitiva', 'Depilación Láser')
                .replace('depilación definitiva', 'depilación láser')
            )
            s.save(update_fields=['nombre'])
    servicios = sorted(servicios_qs, key=_service_category_order)
    categorias_servicios = list(ServiceCategory.objects.all())
    return render(request, 'index.html', {
        'config': config,
        'servicios': servicios,
        'categorias_servicios': categorias_servicios,
    })


def blog(request):
    """Lista pública de blogs con búsqueda, filtro por autor y paginación."""
    q = request.GET.get('q', '').strip()
    author = request.GET.get('author', '').strip()
    page = request.GET.get('page', 1)

    posts = Blog.objects.filter(published=True).filter(
        Q(published_at__lte=timezone.now()) | Q(published_at__isnull=True)
    )

    if q:
        posts = posts.filter(
            Q(title__icontains=q) | Q(content__icontains=q) | Q(excerpt__icontains=q)
        )

    if author:
        # allow filtering by username or id
        if author.isdigit():
            posts = posts.filter(author__id=int(author))
        else:
            posts = posts.filter(author__username=author)

    posts = posts.order_by('-published_at', '-created_at')

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(page)

    # authors for sidebar filter
    authors = User.objects.filter(blogs__published=True).distinct()

    popular_posts = Blog.objects.filter(published=True).filter(
        Q(published_at__lte=timezone.now()) | Q(published_at__isnull=True)
    ).order_by('-published_at')[:3]

    context = {
        'posts': page_obj.object_list,
        'page_obj': page_obj,
        'paginator': paginator,
        'q': q,
        'author_filter': author,
        'authors': authors,
        'popular_posts': popular_posts,
    }
    return render(request, 'blog.html', context)


def blog_detail(request, slug):
    qs = Blog.objects.filter(published=True).filter(
        Q(published_at__lte=timezone.now()) | Q(published_at__isnull=True)
    )
    post = get_object_or_404(qs, slug=slug)
    return render(request, 'blog_detail.html', {'post': post})


def soporte(request):
    return render(request, 'soporte.html')


def contacto(request):
    return render(request, 'contacto.html')


def hogar(request):
    return render(request, 'hogar.html')


def empresa(request):
    return render(request, 'empresas.html')