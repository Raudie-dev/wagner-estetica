from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard_citas, name='dashboard_citas'),
    path('clientes/', views.registro_cliente, name='registro_cliente'),
    path('perfil/', views.configuracion_perfil, name='configuracion_perfil'),
    path('bot/', views.configuracion_respuestas, name='configuracion_respuestas'),
    path('servicios/', views.gestion_servicios, name='gestion_servicios'),
    path('exportar-citas/', views.exportar_citas, name='exportar_citas'),
    path('citas/<int:cita_id>/actualizar/', views.actualizar_cita, name='actualizar_cita'),
    path('api/whatsapp/webhook/', views.whatsapp_webhook, name='whatsapp_webhook'),
    path('api/whatsapp/status/', views.api_bot_status, name='api_bot_status'),
    path('api/whatsapp/unlink/', views.api_bot_unlink, name='api_bot_unlink'),
    path('api/clientes/registrar/', views.api_registrar_cliente, name='api_registrar_cliente'),
]