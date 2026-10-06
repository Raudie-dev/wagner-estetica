from django.db import models

class User_admin(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)
    bloqueado = models.BooleanField(default=False)
    email = models.EmailField(max_length=150, unique=True, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Client(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=30, unique=True, help_text="Número de WhatsApp (ej. 54911...)")
    email = models.EmailField(max_length=150, null=True, blank=True)
    notas = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class Service(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    duracion = models.CharField(max_length=50, blank=True, null=True, help_text="Ej: 60 minutos")
    imagen = models.ImageField(upload_to='servicios/', blank=True, null=True)
    beneficios = models.TextField(blank=True, null=True, help_text="Un beneficio por línea")
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pendiente', 'Pendiente'),
        ('Confirmada', 'Confirmada'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    )

    cliente = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='citas')
    fecha_hora = models.DateTimeField()
    servicio = models.CharField(max_length=200)
    estado = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendiente')
    notas = models.TextField(blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.servicio} - {self.cliente.nombre} ({self.fecha_hora.strftime('%d/%m/%Y %H:%M')})"

class BotResponse(models.Model):
    keyword = models.CharField(max_length=100, unique=True, help_text="Palabra clave o frase que activa esta respuesta (en minúsculas)")
    respuesta = models.TextField(help_text="Mensaje que enviará el bot automáticamente")
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.keyword

class BotSession(models.Model):
    ESTADOS = (
        ('INICIO', 'Inicio'),
        ('ELIGIENDO_SERVICIO', 'Eligiendo Servicio'),
        ('ELIGIENDO_FECHA', 'Eligiendo Fecha'),
        ('ESPERANDO_PAGO', 'Esperando Pago'),
    )
    telefono = models.CharField(max_length=50, unique=True)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='INICIO')
    datos_reserva = models.JSONField(default=dict, blank=True)
    ultima_interaccion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.telefono} - {self.estado}"

class ProfileConfig(models.Model):
    nombre_negocio = models.CharField(max_length=150, default="Clínica Lume")
    direccion = models.CharField(max_length=255, blank=True, null=True)
    horarios = models.TextField(blank=True, null=True)
    mensaje_bienvenida_bot = models.TextField(blank=True, null=True, help_text="Mensaje por defecto que enviará el bot cuando no reconozca un comando. Dejar vacío para desactivar respuesta por defecto.")
    telefono_whatsapp = models.CharField(max_length=20, blank=True, null=True, help_text="Número para el botón flotante de la landing page (ej. 5491166380592)")
    datos_pago_bot = models.TextField(blank=True, null=True, help_text="Instrucciones de pago o CBU que el bot enviará al cliente para confirmar el turno.")
    
    def __str__(self):
        return self.nombre_negocio
