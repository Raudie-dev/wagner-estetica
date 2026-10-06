import os
import django
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proyecto.settings')
django.setup()

from app2.models import Service, ProfileConfig

# Actualizar nombre del negocio en ProfileConfig
config = ProfileConfig.objects.first()
if config:
    config.nombre_negocio = "Clínica Lume"
    config.save()
else:
    ProfileConfig.objects.create(nombre_negocio="Clínica Lume")

servicios_iniciales = [
    {
        "nombre": "Dermatología Médica & Clínica",
        "duracion": "45 minutos",
        "descripcion": "Consulta médica especializada para el diagnóstico, prevención y tratamiento integral de afecciones de la piel, acné, rosácea, lesiones pigmentarias y salud cutánea.",
        "beneficios": "Evaluación por médicos dermatólogos certificados\nDiagnóstico dermatológico personalizado\nTratamiento específico de acné, manchas y afecciones\nPlan clínico preventivo y de seguimiento",
        "imagen_path": "wagner-img/service_facial_glow.jpg"
    },
    {
        "nombre": "Dermocosmiatría & Rituales Faciales",
        "duracion": "60 minutos",
        "descripcion": "Protocolos dermo-cosmiátricos de vanguardia para renovar la textura, exfoliar profundamente e hidratar la piel mediante sueros concentrados de alta tecnología y peelings médicos.",
        "beneficios": "Limpieza profunda de poros e hidratación intensa\nRenovación epidermal y luminosidad instantánea\nTratamiento no invasivo de alta tolerancia\nAplicación de activos biocosméticos de última generación",
        "imagen_path": "wagner-img/service_bbglow.jpg"
    },
    {
        "nombre": "Odontología Estética & Diseño de Sonrisa",
        "duracion": "60 minutos",
        "descripcion": "Tratamientos odontológicos de precisión dedicados a la estética y salud dental: blanqueamiento profesional, limpieza ultrasónica, carillas y armonización de la sonrisa.",
        "beneficios": "Blanqueamiento dental seguro y de alta eficacia\nArmonización de la sonrisa con la estética facial\nDiagnóstico odontológico integral\nCuidado preventivo y restauración estética",
        "imagen_path": "wagner-img/service_hifu.jpg"
    },
    {
        "nombre": "Medicina Estética & Armonización Facial",
        "duracion": "60-90 minutos",
        "descripcion": "Procedimientos médicos mínimamente invasivos para suavizar líneas de expresión, restaurar volúmenes faciales y rejuvenecer la piel con toxina botulínica, ácido hialurónico y HIFU.",
        "beneficios": "Restauración de volúmenes y contornos faciales\nPrevención y supresión de arrugas de expresión\nBioestimulación tisular con efecto lifting natural\nResultados sutiles, armónicos y sin cirugía",
        "imagen_path": "wagner-img/service_peptonas.jpg"
    },
    {
        "nombre": "Depilación Definitiva Láser",
        "duracion": "30-60 minutos",
        "descripcion": "Sistema de depilación láser de diodo con tecnología de enfriamiento continuo. Rápido, inofensivo, indoloro e ideal para la eliminación progresiva y definitiva del vello.",
        "beneficios": "Eliminación permanente del vello no deseado\nSistema indoloro apto para todo tipo de piel\nTratamiento rápido y seguro con enfriamiento constante\nSolución definitiva a la foliculitis y vellos encarnados",
        "imagen_path": "wagner-img/service_laser.jpg"
    }
]

# Desactivar servicios anteriores
Service.objects.all().update(activo=False)

media_servicios_dir = os.path.join('media', 'servicios')
os.makedirs(media_servicios_dir, exist_ok=True)

for data in servicios_iniciales:
    src_path = os.path.join('assets', data['imagen_path'])
    dst_filename = os.path.basename(data['imagen_path'])
    dst_path = os.path.join(media_servicios_dir, dst_filename)
    
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)

    service, created = Service.objects.update_or_create(
        nombre=data['nombre'],
        defaults={
            "duracion": data['duracion'],
            "descripcion": data['descripcion'],
            "beneficios": data['beneficios'],
            "imagen": f"servicios/{dst_filename}" if os.path.exists(src_path) else None,
            "activo": True
        }
    )

print("Servicios sembrados exitosamente para Clínica Lume.")
