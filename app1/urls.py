from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('soporte/', views.soporte, name='soporte'),
    path('contacto/', views.contacto, name='contacto'),
    path('hogar/', views.hogar, name='hogar'),
    path('empresa/', views.empresa, name='empresa'),
]