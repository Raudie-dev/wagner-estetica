from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from .models import User_admin, Client, Appointment, BotResponse, ProfileConfig, Service, BotSession

# Decorador o helper simple para verificar login
def get_logged_user(request):
    user_id = request.session.get('user_admin_id')
    if user_id:
        try:
            return User_admin.objects.get(id=user_id)
        except User_admin.DoesNotExist:
            return None
    return None

def login(request):
    context_user = get_logged_user(request)

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        password = request.POST.get('password', '')

        try:
            user = User_admin.objects.get(nombre=nombre)
            if user.bloqueado:
                messages.error(request, 'Usuario bloqueado')
            elif user.password == password or check_password(password, user.password):
                request.session['user_admin_id'] = user.id
                return redirect('dashboard_citas')
            else:
                messages.error(request, 'Contraseña incorrecta')
        except User_admin.DoesNotExist:
            messages.error(request, 'Usuario no encontrado')

    if context_user:
        return redirect('dashboard_citas')
        
    return render(request, 'login.html', {'user_admin': context_user})


def dashboard_citas(request):
    user = get_logged_user(request)
    if not user: return redirect('login')

    if request.method == 'POST':
        # Crear nueva cita
        cliente_id = request.POST.get('cliente_id')
        fecha_hora = request.POST.get('fecha_hora')
        servicio = request.POST.get('servicio')
        if cliente_id and fecha_hora and servicio:
            cliente = Client.objects.get(id=cliente_id)
            Appointment.objects.create(cliente=cliente, fecha_hora=fecha_hora, servicio=servicio)
            messages.success(request, 'Cita creada exitosamente')
            return redirect('dashboard_citas')

    citas = Appointment.objects.all().order_by('fecha_hora')
    clientes = Client.objects.all()
    servicios_activos = Service.objects.filter(activo=True)
    
    context = {
        'user_admin': user,
        'citas': citas,
        'clientes': clientes,
        'servicios_activos': servicios_activos,
    }
    return render(request, 'dashboard_citas.html', context)


def registro_cliente(request):
    user = get_logged_user(request)
    if not user: return redirect('login')

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        notas = request.POST.get('notas')
        if nombre and telefono:
            Client.objects.create(nombre=nombre, telefono=telefono, email=email, notas=notas)
            messages.success(request, 'Cliente registrado')
            return redirect('registro_cliente')
        else:
            messages.error(request, 'Nombre y teléfono son requeridos')

    clientes = Client.objects.all().order_by('-fecha_registro')
    return render(request, 'registro_cliente.html', {'user_admin': user, 'clientes': clientes})


def configuracion_perfil(request):
    user = get_logged_user(request)
    if not user: return redirect('login')

    config, created = ProfileConfig.objects.get_or_create(id=1)

    if request.method == 'POST':
        config.nombre_negocio = request.POST.get('nombre_negocio', '')
        config.telefono_whatsapp = request.POST.get('telefono_whatsapp', '')
        config.direccion = request.POST.get('direccion', '')
        config.horarios = request.POST.get('horarios', '')
        config.mensaje_bienvenida_bot = request.POST.get('mensaje_bienvenida_bot', '')
        config.datos_pago_bot = request.POST.get('datos_pago_bot', '')
        config.save()
        messages.success(request, 'Perfil actualizado')
        return redirect('configuracion_perfil')

    return render(request, 'perfil.html', {'user_admin': user, 'config': config})


def configuracion_respuestas(request):
    user = get_logged_user(request)
    if not user: return redirect('login')

    config, _ = ProfileConfig.objects.get_or_create(id=1)

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_phone':
            config.telefono_whatsapp = request.POST.get('telefono_whatsapp', '')
            config.save()
            messages.success(request, 'Número de WhatsApp actualizado')
            return redirect('configuracion_respuestas')
            
        elif action == 'add_rule':
            keyword = request.POST.get('keyword', '').lower()
            respuesta = request.POST.get('respuesta', '')
            if keyword and respuesta:
                BotResponse.objects.create(keyword=keyword, respuesta=respuesta)
                messages.success(request, 'Respuesta guardada')
                return redirect('configuracion_respuestas')
                
        elif action == 'delete_rule':
            rule_id = request.POST.get('rule_id')
            if rule_id:
                BotResponse.objects.filter(id=rule_id).delete()
                messages.success(request, 'Respuesta eliminada')
                return redirect('configuracion_respuestas')

    respuestas = BotResponse.objects.all()
    node_api_url = "http://localhost:3000"
    
    return render(request, 'bot.html', {
        'user_admin': user, 
        'respuestas': respuestas,
        'node_api_url': node_api_url,
        'config': config
    })

def gestion_servicios(request):
    user = get_logged_user(request)
    if not user: return redirect('login')

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'add_service':
            nombre = request.POST.get('nombre_servicio', '')
            duracion = request.POST.get('duracion', '')
            descripcion = request.POST.get('descripcion', '')
            beneficios = request.POST.get('beneficios', '')
            
            if nombre:
                servicio = Service(nombre=nombre, duracion=duracion, descripcion=descripcion, beneficios=beneficios, activo=True)
                if 'imagen' in request.FILES:
                    servicio.imagen = request.FILES['imagen']
                servicio.save()
                messages.success(request, 'Servicio agregado exitosamente')
            
        elif action == 'delete_service':
            service_id = request.POST.get('service_id')
            if service_id:
                Service.objects.filter(id=service_id).delete()
                messages.success(request, 'Servicio eliminado')
                
        elif action == 'toggle_service':
            service_id = request.POST.get('service_id')
            if service_id:
                s = Service.objects.filter(id=service_id).first()
                if s:
                    s.activo = not s.activo
                    s.save()
                    messages.success(request, f"Servicio {'activado' if s.activo else 'desactivado'}")

        return redirect('gestion_servicios')

    servicios = Service.objects.all()
    return render(request, 'servicios.html', {
        'user_admin': user, 
        'servicios': servicios,
    })


@csrf_exempt
def whatsapp_webhook(request):
    """
    Recibe los mensajes de WhatsApp desde el gateway (Node.js) y responde
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            remote_jid = data.get('remoteJid', '')
            message_text = data.get('messageText', '').lower()
            
            # Solo contestamos a mensajes directos
            if not (remote_jid.endswith('@s.whatsapp.net') or remote_jid.endswith('@lid')):
                return JsonResponse({'status': 'ignored'})
            
            # Extraer número
            number = remote_jid.split('@')[0]
            
            # Recuperar configuración y servicios
            config = ProfileConfig.objects.first()
            servicios = Service.objects.filter(activo=True)
            
            # Obtener o crear sesión del bot
            from django.utils import timezone
            from datetime import timedelta
            
            session, created = BotSession.objects.get_or_create(telefono=number)
            
            # Si pasó más de 1 hora de inactividad, resetear sesión si no estaba en INICIO
            if not created and session.estado != 'INICIO':
                if timezone.now() - session.ultima_interaccion > timedelta(hours=1):
                    session.estado = 'INICIO'
                    session.datos_reserva = {}
                    session.save()
                    
            matched_reply = None
            
            # COMANDOS GLOBALES DE RESET
            if message_text in ['/cita', '#inicio_bot', 'cancelar', 'salir']:
                session.estado = 'INICIO'
                session.datos_reserva = {}
                session.save()
                
            elif message_text == '#confirmar_web':
                datos_pago = config.datos_pago_bot if config and config.datos_pago_bot else "CBU: 1234567890123456789012\nAlias: wagner.estetica"
                matched_reply = f"¡Hola! Hemos registrado tu solicitud desde la web para *{session.datos_reserva.get('servicio', 'el servicio')}* el *{session.datos_reserva.get('fecha_hora_texto', 'pronto')}*.\n\nPara confirmar tu turno de forma definitiva, necesitamos que realices el pago de apartado. Aquí tienes los datos:\n\n{datos_pago}\n\n*Por favor, envíanos el comprobante de pago por este mismo chat.*\nUna vez que lo envíes, escribe *'listo'* para finalizar."
                session.estado = 'ESPERANDO_PAGO'
                session.save()
                return JsonResponse({'status': 'success', 'reply': matched_reply})
            
            # ==============================
            # MÁQUINA DE ESTADOS
            # ==============================
            if session.estado == 'INICIO':
                if message_text in ['/cita', '#inicio_bot'] or created:
                    session.estado = 'ELIGIENDO_SERVICIO'
                    session.save()
                    
                    if servicios.exists():
                        lista = "\n".join([f"{idx+1}. {s.nombre}" for idx, s in enumerate(servicios)])
                        matched_reply = f"¡Hola! Bienvenido a {config.nombre_negocio if config else 'nuestra estética'}.\n\nPara agendar una cita, por favor responde con el *número* del servicio que deseas:\n\n{lista}"
                    else:
                        matched_reply = "¡Hola! Por el momento no tenemos servicios configurados para agendar automáticamente. Por favor escribe tu consulta y te atenderemos en breve."
                        session.estado = 'INICIO'
                        session.save()
                else:
                    # Buscar en respuestas preconfiguradas si no es un comando de cita
                    responses = BotResponse.objects.filter(activo=True)
                    for bot_res in responses:
                        if bot_res.keyword in message_text:
                            matched_reply = bot_res.respuesta
                            break
                    if not matched_reply and config and config.mensaje_bienvenida_bot:
                        matched_reply = config.mensaje_bienvenida_bot
                        
            elif session.estado == 'ELIGIENDO_SERVICIO':
                # Validar que sea un número válido
                try:
                    opcion = int(message_text.strip())
                    if 1 <= opcion <= servicios.count():
                        servicio_elegido = servicios[opcion-1]
                        session.datos_reserva['servicio'] = servicio_elegido.nombre
                        session.estado = 'ELIGIENDO_FECHA'
                        session.save()
                        
                        horarios_texto = config.horarios if config and config.horarios else "Lunes a Viernes de 9:00 a 18:00"
                        matched_reply = f"Excelente. Has elegido: *{servicio_elegido.nombre}*.\n\nNuestros horarios son:\n{horarios_texto}\n\nPor favor, escribe la fecha y hora en la que deseas tu cita usando este formato exacto:\n*DD/MM/AAAA HH:MM*\n\n(Ejemplo: 25/10/2026 15:30)\n\nSi deseas cancelar, escribe 'cancelar'."
                    else:
                        matched_reply = "Por favor, responde con un número válido de la lista."
                except ValueError:
                    matched_reply = "Por favor, responde solo con el número del servicio (ej. 1, 2, 3)."
                    
            elif session.estado == 'ELIGIENDO_FECHA':
                if message_text.lower() == 'cancelar':
                    session.estado = 'INICIO'
                    session.datos_reserva = {}
                    session.save()
                    matched_reply = "Reserva cancelada. Escribe /cita cuando desees volver a empezar."
                else:
                    import re
                    # Simple regex to validate DD/MM/YYYY HH:MM
                    pattern = r'^\d{2}/\d{2}/\d{4} \d{2}:\d{2}$'
                    if re.match(pattern, message_text.strip()):
                        session.datos_reserva['fecha_hora_texto'] = message_text.strip()
                        session.estado = 'ESPERANDO_PAGO'
                        session.save()
                        
                        datos_pago = config.datos_pago_bot if config and config.datos_pago_bot else "CBU: 1234567890123456789012\nAlias: wagner.estetica"
                        matched_reply = f"¡Perfecto! Hemos pre-agendado tu cita para el *{message_text.strip()}*.\n\nPara confirmar tu turno de forma definitiva, necesitamos que realices el pago de apartado. Aquí tienes los datos:\n\n{datos_pago}\n\n*Por favor, envíanos el comprobante de pago por este mismo chat.*\nUna vez que lo envíes, escribe *'listo'* para finalizar."
                    else:
                        matched_reply = "El formato de fecha no es correcto. Recuerda que debe ser exactamente:\n*DD/MM/AAAA HH:MM*\n\n(Ejemplo: 25/10/2026 15:30)"
                        
            elif session.estado == 'ESPERANDO_PAGO':
                if 'listo' in message_text.lower() or 'pago' in message_text.lower() or 'comprobante' in message_text.lower():
                    # Parsear la fecha para el modelo
                    from datetime import datetime
                    fecha_texto = session.datos_reserva.get('fecha_hora_texto')
                    servicio = session.datos_reserva.get('servicio', 'Servicio Desconocido')
                    
                    try:
                        fecha_dt = datetime.strptime(fecha_texto, '%d/%m/%Y %H:%M')
                    except Exception:
                        fecha_dt = timezone.now() # Fallback
                        
                    # Obtener cliente o crear (se asume que si escribe tiene perfil)
                    cliente, _ = Client.objects.get_or_create(
                        telefono=number,
                        defaults={'nombre': data.get('pushName', 'Cliente')}
                    )
                    
                    Appointment.objects.create(
                        cliente=cliente,
                        fecha_hora=fecha_dt,
                        servicio=servicio,
                        estado='Pendiente', notas=data.get('notas', '')
                )
                    
                    session.estado = 'INICIO'
                    session.datos_reserva = {}
                    session.save()
                    
                    matched_reply = "¡Muchas gracias! Hemos recibido tu confirmación. Un miembro de nuestro equipo revisará el comprobante y te avisaremos si hay algún inconveniente.\n\nTe enviaremos un recordatorio 1 día antes de tu cita. ¡Te esperamos!"
                else:
                    matched_reply = "Recibimos tu mensaje. Recuerda enviarnos el comprobante de pago y escribir *'listo'* para registrar tu cita."
            
            # Actualizar timestamp
            session.save()

            if matched_reply:
                return JsonResponse({'status': 'success', 'reply': matched_reply})

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
    return JsonResponse({'status': 'invalid method'}, status=405)

def api_bot_status(request):
    try:
        response = requests.get('http://127.0.0.1:3000/qr', timeout=5)
        if response.status_code == 200:
            return JsonResponse(response.json())
        return JsonResponse({'error': 'Bad response from gateway'})
    except Exception as e:
        return JsonResponse({'error': str(e)})

@csrf_exempt
def api_bot_unlink(request):
    if request.method == 'POST':
        try:
            # Primero obligamos a desvincular y borrar auth_info
            requests.post('http://127.0.0.1:3000/unlink', timeout=5)
            # Luego pedimos generar un nuevo QR
            response = requests.post('http://127.0.0.1:3000/generate', timeout=15)
            
            if response.status_code == 200:
                return JsonResponse({'status': 'success'})
            return JsonResponse({'error': 'Bad response from gateway'})
        except Exception as e:
            return JsonResponse({'error': str(e)})
    return JsonResponse({'status': 'invalid method'}, status=405)

@csrf_exempt
def api_registrar_cliente(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre = data.get('nombre')
            telefono = data.get('telefono')
            servicio = data.get('servicio', 'Otro / Consulta General')
            fecha = data.get('fecha')
            
            if nombre and telefono:
                cliente, created = Client.objects.get_or_create(
                    telefono=telefono,
                    defaults={'nombre': nombre}
                )
                if not created and cliente.nombre != nombre:
                    cliente.nombre = nombre
                    cliente.save()
                    
                # Crear cita (Appointment)
                from django.utils import timezone
                import datetime
                
                fecha_obj = timezone.now()
                if fecha:
                    try:
                        # expected format from datetime-local is "YYYY-MM-DDTHH:MM"
                        naive_dt = datetime.datetime.strptime(fecha, "%Y-%m-%dT%H:%M")
                        fecha_obj = timezone.make_aware(naive_dt)
                    except ValueError:
                        pass
                
                if fecha:
                    # Verificar disponibilidad (evitar reservas dobles para el mismo servicio en la misma hora)
                    if Appointment.objects.filter(servicio=servicio, fecha_hora=fecha_obj, estado__in=['Pendiente', 'Confirmada']).exists():
                        return JsonResponse({'status': 'error', 'message': 'Ese horario ya está ocupado para este servicio. Por favor, selecciona otro.'})
                
                Appointment.objects.create(
                    cliente=cliente,
                    fecha_hora=fecha_obj,
                    servicio=servicio,
                    estado='Pendiente', notas=data.get('notas', '')
                )
                
                # Configurar la sesión del bot para saltarse los pasos
                from .models import BotSession
                session, _ = BotSession.objects.get_or_create(telefono=telefono)
                session.estado = 'ESPERANDO_PAGO'
                session.datos_reserva['servicio'] = servicio
                session.datos_reserva['fecha_hora_texto'] = fecha_obj.strftime('%d/%m/%Y %H:%M') if fecha else 'A confirmar'
                session.save()
                    
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)

from django.http import HttpResponse
import datetime
from django.utils import timezone

import csv

def exportar_citas(request):
    user = get_logged_user(request)
    if not user: return redirect('login')
    
    start_str = request.GET.get('start')
    end_str = request.GET.get('end')
    
    citas = Appointment.objects.all().order_by('fecha_hora')
    
    if start_str and end_str:
        try:
            start_date = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00'))
            end_date = datetime.datetime.fromisoformat(end_str.replace('Z', '+00:00'))
            citas = citas.filter(fecha_hora__gte=start_date, fecha_hora__lt=end_date)
        except ValueError:
            pass
            
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="citas_lume.csv"'
    response.write(u'\ufeff'.encode('utf8'))
    
    writer = csv.writer(response, delimiter=';')
    writer.writerow(['Fecha y Hora', 'Cliente', 'Teléfono', 'Servicio', 'Estado', 'Notas'])
    
    for cita in citas:
        fecha_str = cita.fecha_hora.strftime("%d/%m/%Y %H:%M") if cita.fecha_hora else ""
        writer.writerow([
            fecha_str,
            cita.cliente.nombre,
            cita.cliente.telefono,
            cita.servicio,
            cita.estado,
            cita.notas
        ])
        
    return response

def actualizar_cita(request, cita_id):
    user = get_logged_user(request)
    if not user: return redirect('login')
    
    if request.method == 'POST':
        cita = get_object_or_404(Appointment, id=cita_id)
        
        notas = request.POST.get('notas')
        estado = request.POST.get('estado')
        
        if notas is not None:
            cita.notas = notas
        if estado:
            cita.estado = estado
            
        cita.save()
        messages.success(request, 'Cita actualizada correctamente.')
        
    return redirect('dashboard_citas')

def logout_view(request):
    request.session.flush()
    return redirect('login')

def configuracion_usuario(request):
    user = get_logged_user(request)
    if not user:
        return redirect('login')
        
    if request.method == 'POST':
        nuevo_nombre = request.POST.get('nombre', '').strip()
        nueva_clave = request.POST.get('password', '').strip()
        
        if nuevo_nombre:
            user.nombre = nuevo_nombre
        if nueva_clave:
            from django.contrib.auth.hashers import make_password
            user.password = make_password(nueva_clave)
            
        user.save()
        messages.success(request, 'Datos de usuario actualizados correctamente.')
        return redirect('configuracion_usuario')
        
    return render(request, 'usuario.html', {'user': user})
