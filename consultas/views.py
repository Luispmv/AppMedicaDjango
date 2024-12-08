from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Usuarios, Session, Citas, Doctores, Pacientes, HistorialMedico, Reportes
import secrets

# Limpia las sesiones expiradas de la base de datos
def limpiar_sesiones_expiradas():
    Session.objects.filter(expires_at__lt=timezone.now()).delete()

# Valida la sesión actual del usuario
def validar_sesion(request):
    session_token = request.COOKIES.get('session_token')
    if session_token:
        session = Session.objects.filter(session_token=session_token).first()
        if session and session.expires_at > timezone.now():
            return session.user_id
    return None

# Vista principal después del login
def home_view(request):
    limpiar_sesiones_expiradas()
    id_usuario = validar_sesion(request)
    if id_usuario:
        return render(request, 'home.html', {'id_usuario': id_usuario})
    return redirect('login')

# Vista de login
def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')
        user = Usuarios.objects.filter(correo=correo).first()
        if user and user.contrasena == contrasena:
            token = secrets.token_hex(32)
            expires_at = timezone.now() + timedelta(days=1)
            Session.objects.create(user_id=user.id_usuario, session_token=token, expires_at=expires_at)
            response = redirect('dashboard_doctor' if user.tipo_usuario == 'doctor' else 'dashboard_paciente')
            response.set_cookie('session_token', token, max_age=86400)
            return response
        return render(request, 'consultas/login.html', {'error': 'Correo o contraseña incorrectos'})
    return render(request, 'consultas/login.html')

# Vista de registro
def register_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        tipo_usuario = request.POST['tipo_usuario']
        Usuarios.objects.create(nombre=nombre, apellido=apellido, correo=correo, contrasena=contrasena, tipo_usuario=tipo_usuario)
        return redirect('login')
    return render(request, 'register.html')

# Dashboard para doctores
def dashboard_doctor(request):
    id_usuario = validar_sesion(request)
    if not id_usuario:
        return redirect('login')
    return render(request, 'consultas/dashboard_doctor.html', {'id_usuario': id_usuario})

# Dashboard para pacientes
def dashboard_paciente(request):
    id_usuario = validar_sesion(request)
    if not id_usuario:
        return redirect('login')
    citas = Citas.objects.filter(id_paciente=id_usuario)
    return render(request, 'consultas/dashboard_paciente.html', {'id_usuario': id_usuario, 'citas': citas})

# Agendar cita (doctor)
def agendar_cita_doctor(request):
    id_doctor = validar_sesion(request)
    if not id_doctor:
        return redirect('login')
    if request.method == 'POST':
        correo_paciente = request.POST.get('correo_paciente')
        fecha_hora = request.POST.get('fecha_hora')
        paciente = get_object_or_404(Usuarios, correo=correo_paciente, tipo_usuario='paciente')
        Citas.objects.create(id_doctor_id=id_doctor, id_paciente_id=paciente.id_usuario, fecha_hora=fecha_hora, estado='agendada')
        return redirect('dashboard_doctor')
    return render(request, 'consultas/agendar_cita_doctor.html')

# Ver historial médico
def ver_historial(request, id_paciente):
    historial = HistorialMedico.objects.filter(id_paciente=id_paciente)
    return render(request, 'consultas/ver_historial.html', {'historial': historial})

# Generar reporte
def generar_reporte(request):
    id_usuario = validar_sesion(request)
    if not id_usuario:
        return redirect('login')
    if request.method == 'POST':
        contenido = request.POST.get('contenido')
        Reportes.objects.create(id_doctor_id=id_usuario, contenido=contenido, fecha_creacion=timezone.now())
        return redirect('dashboard_doctor')
    return render(request, 'consultas/generar_reporte.html')

# Cerrar sesión
def logout_view(request):
    session_token = request.COOKIES.get('session_token')
    if session_token:
        Session.objects.filter(session_token=session_token).delete()
    response = redirect('login')
    response.delete_cookie('session_token')
    return response

# Ver médicos
def ver_medicos(request):
    medicos = Doctores.objects.all()
    return render(request, 'consultas/ver_medicos.html', {'medicos': medicos})

# Ver citas (paciente)
def ver_citas(request):
    id_usuario = validar_sesion(request)
    if not id_usuario:
        return redirect('login')
    citas = Citas.objects.filter(id_paciente=id_usuario)
    return render(request, 'consultas/ver_citas.html', {'citas': citas})

# Ver tratamiento
def ver_tratamiento(request):
    tratamiento = [
        {'descripcion': 'Tomar una tableta de paracetamol cada 8 horas por 5 días.'},
        {'descripcion': 'Aplicar una crema tópica en la zona afectada dos veces al día.'}
    ]
    return render(request, 'consultas/ver_tratamiento.html', {'tratamiento': tratamiento})