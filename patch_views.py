import re

with open('app2/views.py', 'r', encoding='utf-8') as f:
    content = f.read()

new_func = """import csv

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
    response.write(u'\\ufeff'.encode('utf8'))
    
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
        
    return response"""

old_start = content.find('def exportar_citas(request):')
old_end = content.find('def actualizar_cita(', old_start)

if old_start != -1 and old_end != -1:
    before = content[:old_start]
    after = content[old_end:]
    with open('app2/views.py', 'w', encoding='utf-8') as f:
        f.write(before + new_func + '\n\n' + after)
    print('Done replacing.')
else:
    print('Could not find boundaries.')
