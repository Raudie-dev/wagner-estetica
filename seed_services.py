import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from app2.models import Service

servicios_iniciales = [
    {
        "nombre": "Ritual Facial Glow",
        "duracion": "60 minutos",
        "descripcion": "Un tratamiento facial diseñado a medida para devolverle la luz a tu rostro. Utilizamos activos botánicos de alta pureza y tecnología no invasiva para limpiar profundamente, extraer impurezas, exfoliar y nutrir la piel desde adentro.",
        "beneficios": "Piel visiblemente más luminosa e hidratada\nReducción de poros dilatados y puntos negros\nEstimulación de la producción natural de colágeno\nRelajación profunda con masaje facial de drenaje linfático",
        "imagen_path": "wagner-img/service_facial_glow.jpg"
    },
    {
        "nombre": "Escultura Corporal",
        "duracion": "50 minutos",
        "descripcion": "Tratamiento intensivo para moldear tu figura de manera natural y sin cirugía. Combinamos masajes reductores manuales, drenaje linfático y aparatología de última generación para atacar la adiposidad localizada.",
        "beneficios": "Reducción de medidas desde la primera sesión\nMejora visible en la apariencia de la celulitis\nEfecto tensor en la piel flácida\nEstimulación de la circulación y eliminación de toxinas",
        "imagen_path": "wagner-img/service_body_sculpt.jpg"
    },
    {
        "nombre": "BBGlow Perfección",
        "duracion": "90 minutos",
        "descripcion": "El famoso tratamiento coreano 'efecto piel de porcelana'. Mediante la técnica de microneedling introducimos sueros con color y vitaminas en la epidermis, logrando un tono unificado como si llevaras una base de maquillaje semipermanente perfecta.",
        "beneficios": "Camufla manchas, ojeras y rojeces\nAporta un brillo natural y saludable extremo\nHidratación profunda con ácido hialurónico\nTratamiento indoloro con resultados que duran meses",
        "imagen_path": "wagner-img/service_bbglow.jpg"
    },
    {
        "nombre": "HIFU 7D Lifting",
        "duracion": "75 minutos",
        "descripcion": "La alternativa número uno al lifting quirúrgico. El Ultrasonido Focalizado de Alta Intensidad (HIFU 7D) penetra en las capas más profundas de la piel para tensar el músculo y generar colágeno nuevo de forma masiva.",
        "beneficios": "Efecto lifting en rostro, cuello y escote\nRedefinición del óvalo facial y eliminación de papada\nResultados progresivos que mejoran mes a mes\nSin agujas, sin cortes y sin tiempo de recuperación",
        "imagen_path": "wagner-img/service_hifu.jpg"
    },
    {
        "nombre": "Glúteos Peptonas",
        "duracion": "45 minutos",
        "descripcion": "El tratamiento estrella para aumentar y reafirmar los glúteos. Las peptonas son nutrientes celulares que actúan directamente sobre el músculo, promoviendo su desarrollo natural de forma rápida, segura e indolora.",
        "beneficios": "Aumento de volumen muscular natural y duradero\nElevación y firmeza visible (efecto push-up)\nMejora la textura de la piel en la zona\nTratamiento 100% biológico, sin riesgos de rechazo",
        "imagen_path": "wagner-img/service_peptonas.jpg"
    },
    {
        "nombre": "Depilación Láser Soprano",
        "duracion": "30-60 minutos",
        "descripcion": "Despídete del vello no deseado con la tecnología láser más avanzada, segura y cómoda del mercado. Eficaz en todo tipo de pieles e indolora gracias a su sistema de enfriamiento continuo.",
        "beneficios": "Eliminación del vello de forma definitiva\nSoluciona problemas de foliculitis (vellos encarnados)\nPiel mucho más suave y clara\nSesiones rápidas, seguras y sin dolor",
        "imagen_path": "wagner-img/service_laser.jpg"
    }
]

# We won't copy the images to the media folder just yet, we can just leave the ImageField empty and fall back to the static path if it's empty, or copy them to media.
# For simplicity, let's copy the static images to media so we don't have to change the logic later if the user uploads new ones.
import shutil

media_servicios_dir = os.path.join('media', 'servicios')
os.makedirs(media_servicios_dir, exist_ok=True)

for data in servicios_iniciales:
    # Check if it already exists
    if not Service.objects.filter(nombre=data['nombre']).exists():
        src_path = os.path.join('static', data['imagen_path'])
        dst_filename = os.path.basename(data['imagen_path'])
        dst_path = os.path.join(media_servicios_dir, dst_filename)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, dst_path)
            
        Service.objects.create(
            nombre=data['nombre'],
            duracion=data['duracion'],
            descripcion=data['descripcion'],
            beneficios=data['beneficios'],
            imagen=f"servicios/{dst_filename}" if os.path.exists(src_path) else None,
            activo=True
        )

print("Servicios sembrados exitosamente.")
