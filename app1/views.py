from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

from .models import Blog
from django.contrib.auth.models import User

from app2.models import ProfileConfig

# Create your views here.
def index(request):
    config = ProfileConfig.objects.first()
    return render(request, 'index.html', {'config': config})


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