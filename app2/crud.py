from app1.models import Blog, Category
from django.utils.dateparse import parse_date
from datetime import datetime


def _parse_published_at(fecha):
    if not fecha:
        return None
    # try parsing YYYY-MM-DD or ISO formats
    d = parse_date(fecha)
    if d:
        return datetime.combine(d, datetime.min.time())
    try:
        return datetime.fromisoformat(fecha)
    except Exception:
        return None


def crear_post(title, published_at_str=None, published=True, excerpt=None, content='', featured_image=None, author=None, categories=None):
    """Crear una publicación (Blog) con campos adicionales.
    - `excerpt`, `content`, `featured_image`, `author` son opcionales.
    """
    published_at = _parse_published_at(published_at_str)
    post = Blog(title=title, excerpt=excerpt or '', content=content or '', published=bool(published), published_at=published_at)
    if author:
        post.author = author
    if featured_image:
        post.featured_image = featured_image
    post.save()
    # assign categories if provided (accept list of ids or slugs or names)
    if categories:
        # if categories are numeric ids
        if all(str(c).isdigit() for c in categories):
            post.categories.set(Category.objects.filter(id__in=[int(c) for c in categories]))
        else:
            # try by slug or name
            objs = Category.objects.filter(slug__in=[str(c) for c in categories])
            # if not found by slug, try name
            if objs.count() == 0:
                objs = Category.objects.filter(name__in=[str(c) for c in categories])
            post.categories.set(objs)
    return post


def obtener_posts():
    return Blog.objects.all()


def eliminar_post(post_id):
    Blog.objects.filter(id=post_id).delete()


def actualizar_post(post_id, title=None, published_at_str=None, published=None, excerpt=None, content=None, featured_image=None, categories=None):
    post = Blog.objects.get(id=post_id)
    if title is not None:
        post.title = title
    if published_at_str is not None:
        parsed = _parse_published_at(published_at_str)
        post.published_at = parsed
    if published is not None:
        post.published = bool(published)
    if excerpt is not None:
        post.excerpt = excerpt
    if content is not None:
        post.content = content
    if featured_image is not None:
        post.featured_image = featured_image
    post.save()
    # update categories if passed
    if categories is not None:
        if all(str(c).isdigit() for c in categories):
            post.categories.set(Category.objects.filter(id__in=[int(c) for c in categories]))
        else:
            objs = Category.objects.filter(slug__in=[str(c) for c in categories])
            if objs.count() == 0:
                objs = Category.objects.filter(name__in=[str(c) for c in categories])
            post.categories.set(objs)
    return post
    

def crear_categoria(name):
    cat, _ = Category.objects.get_or_create(name=name)
    return cat


def obtener_categorias():
    return Category.objects.all()
    post.save()
    return post


# Wrappers para compatibilidad con código existente que usaba los nombres antiguos
def crear_prueba(nombre, fecha, socio=True):
    return crear_post(title=nombre, published_at_str=fecha, published=socio)


def obtener_pruebas():
    return obtener_posts()


def eliminar_prueba(prueba_id):
    return eliminar_post(prueba_id)


def actualizar_prueba(prueba_id, nombre=None, fecha=None, socio=None):
    return actualizar_post(prueba_id, title=nombre, published_at_str=fecha, published=socio)