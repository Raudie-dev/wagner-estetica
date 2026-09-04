from apscheduler.schedulers.background import BackgroundScheduler
from django.utils import timezone
from datetime import timedelta
import requests
import logging

logger = logging.getLogger(__name__)

def enviar_recordatorios():
    from .models import Appointment
    # Buscar citas que sean exactamente mañana
    manana_inicio = timezone.now() + timedelta(days=1)
    manana_fin = manana_inicio + timedelta(hours=1)
    
    citas = Appointment.objects.filter(
        estado='Confirmada', 
        fecha_hora__gte=manana_inicio, 
        fecha_hora__lt=manana_fin
    )
    
    for cita in citas:
        numero = cita.cliente.telefono
        mensaje = f"¡Hola {cita.cliente.nombre}! Te recordamos que tienes una cita de *{cita.servicio}* programada para mañana a las {cita.fecha_hora.strftime('%H:%M')} hs.\n\n¡Te esperamos!"
        
        try:
            requests.post('http://127.0.0.1:3000/send', json={
                'number': numero,
                'message': mensaje
            }, timeout=5)
        except Exception as e:
            logger.error(f"Error enviando recordatorio a {numero}: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    # Ejecutar cada hora para buscar las citas del día siguiente a esa misma hora
    scheduler.add_job(enviar_recordatorios, 'interval', minutes=60)
    scheduler.start()
