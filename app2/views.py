from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

from .models import User_admin, Client, Appointment, BotResponse, ProfileConfig

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
    
    context = {
        'user_admin': user,
        'citas': citas,
        'clientes': clientes,
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
        config.direccion = request.POST.get('direccion', '')
        config.horarios = request.POST.get('horarios', '')
        config.mensaje_bienvenida_bot = request.POST.get('mensaje_bienvenida_bot', '')
        config.save()
        messages.success(request, 'Perfil actualizado')
        return redirect('configuracion_perfil')

    return render(request, 'perfil.html', {'user_admin': user, 'config': config})


def configuracion_respuestas(request):
    user = get_logged_user(request)
    if not user: return redirect('login')

    config = ProfileConfig.objects.first()

    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_phone':
            if config:
                config.telefono_whatsapp = request.POST.get('telefono_whatsapp', '')
                config.save()
            messages.success(request, 'Número de WhatsApp actualizado')
            return redirect('configuracion_respuestas')
            
        else:
            # action implicitly is add_rule if not update_phone but let's check
            keyword = request.POST.get('keyword', '').lower()
            respuesta = request.POST.get('respuesta', '')
            if keyword and respuesta:
                BotResponse.objects.create(keyword=keyword, respuesta=respuesta)
                messages.success(request, 'Respuesta guardada')
                return redirect('configuracion_respuestas')

    respuestas = BotResponse.objects.all()
    node_api_url = "http://localhost:3000"
    
    return render(request, 'bot.html', {
        'user_admin': user, 
        'respuestas': respuestas,
        'node_api_url': node_api_url,
        'config': config
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
            if not remote_jid.endswith('@s.whatsapp.net'):
                return JsonResponse({'status': 'ignored'})
            
            # Buscar una respuesta configurada
            responses = BotResponse.objects.filter(activo=True)
            matched_reply = None
            
            for bot_res in responses:
                if bot_res.keyword in message_text:
                    matched_reply = bot_res.respuesta
                    break
            
            if not matched_reply:
                config = ProfileConfig.objects.first()
                if config and config.mensaje_bienvenida_bot:
                    matched_reply = config.mensaje_bienvenida_bot

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
            if nombre and telefono:
                cliente, created = Client.objects.get_or_create(
                    telefono=telefono,
                    defaults={'nombre': nombre}
                )
                if not created and cliente.nombre != nombre:
                    cliente.nombre = nombre
                    cliente.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'Missing fields'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'invalid method'}, status=405)