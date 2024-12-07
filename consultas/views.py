from django.shortcuts import render, redirect
import secrets
from datetime import datetime, timedelta
from .models import Usuarios, Session
from django.utils import timezone
# import hashlib


# Create your views here.
from django.db import connection

# views.py

def limpiar_sesiones_expiradas():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sesiones WHERE expiracion < NOW()")

# def home_view(request):
#     return render(request, 'consultas/home.html')
def home_view(request):
    limpiar_sesiones_expiradas()
    id_usuario = validar_sesion(request)
    if id_usuario:
        # Usuario autenticado, renderiza la página principal.
        return render(request, 'home.html', {'id_usuario': id_usuario})
    else:
        # Redirige al inicio de sesión si no hay sesión válida.
        return redirect('login')


# def login_view(request):
#     if request.method == 'POST':
#         correo = request.POST['correo']
#         contrasena = request.POST['contrasena']
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT * FROM usuarios WHERE correo = %s AND contrasena = %s", [correo, contrasena])
#             usuario = cursor.fetchone()
#         if usuario:
#             request.session['usuario_id'] = usuario[0]
#             request.session['tipo_usuario'] = usuario[4]
#             return redirect('home')
#         else:
#             return render(request, 'login.html', {'error': 'Credenciales inválidas'})
#     return render(request, 'login.html')





# def login_view(request):
#     if request.method == 'POST':
#         correo = request.POST['correo']
#         contrasena = request.POST['contrasena']  # Esto es texto plano, ten en cuenta la seguridad.

#         # Verificar las credenciales en la tabla `usuarios`.
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT id_usuario FROM usuarios WHERE correo = %s AND contrasena = %s", [correo, contrasena])
#             usuario = cursor.fetchone()

#         if usuario:
#             # Generar un token único para la sesión
#             token_sesion = secrets.token_hex(32)
#             expiracion = datetime.now() + timedelta(days=1)  # La sesión dura 1 día

#             # Crear la sesión en la tabla `sesiones`
#             with connection.cursor() as cursor:
#                 cursor.execute(
#                     """
#                     INSERT INTO sesiones (id_usuario, token_sesion, expiracion) 
#                     VALUES (%s, %s, %s)
#                     """,
#                     [usuario[0], token_sesion, expiracion]
#                 )

#             # Almacenar el token de sesión en la sesión del cliente
#             request.session['token_sesion'] = token_sesion
#             return redirect('home')
#         else:
#             return render(request, 'login.html', {'error': 'Credenciales inválidas'})

#     return render(request, 'login.html')


def login_view(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        contrasena = request.POST.get('contrasena')

        # Verificar que el usuario existe y la contraseña es correcta
        user = Usuarios.objects.filter(correo=correo).first()
        if user and contrasena == user.contrasena:  # Comparar la contraseña ingresada con la de la base de datos
            # Generar un token de sesión único
            token_sesion = secrets.token_hex(32)
            expires_at = datetime.now() + timedelta(days=1)  # Expira en 1 día

            # Crear la sesión en la base de datos
            Session.objects.create(
                user_id=user.id_usuario,
                session_token=token_sesion,
                expires_at=expires_at
            )

            # Establecer el token de sesión en una cookie
            response = redirect('home')  # Redirige a la página de inicio
            response.set_cookie('session_token', token_sesion, max_age=86400)  # La cookie expira en 1 día
            return response
        else:
            error = "Correo o contraseña incorrectos."
            return render(request, 'consultas/login.html', {'error': error})

    return render(request, 'consultas/login.html')


# def validar_sesion(request):
#     token_sesion = request.session.get('token_sesion')
#     if token_sesion:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 SELECT id_usuario FROM sesiones 
#                 WHERE token_sesion = %s AND expiracion > NOW()
#                 """,
#                 [token_sesion]
#             )
#             sesion = cursor.fetchone()
#         if sesion:
#             return sesion[0]  # Devuelve el ID del usuario si la sesión es válida.
#     return None  # Retorna `None` si no hay sesión válida.
def validar_sesion(request):
    session_token = request.COOKIES.get('session_token')  # Obtener el token de sesión de la cookie

    if session_token:
        session = Session.objects.filter(session_token=session_token).first()
        if session and session.expires_at > timezone.now():
            # Sesión válida
            return session.user_id  # Devolver el ID del usuario autenticado
    return None  # Usuario no autenticado



def register_view(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        correo = request.POST['correo']
        contrasena = request.POST['contrasena']
        tipo_usuario = request.POST['tipo_usuario']
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO usuarios (nombre, apellido, correo, tipo_usuario, contrasena)
                VALUES (%s, %s, %s, %s, %s)
            """, [nombre, apellido, correo, tipo_usuario, contrasena])
        return redirect('login')
    return render(request, 'register.html')


def agendar_cita(request):
    if request.method == 'POST':
        id_doctor = request.POST['id_doctor']
        id_paciente = request.POST['id_paciente']
        fecha_hora = request.POST['fecha_hora']
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO citas (id_doctor, id_paciente, fecha_hora, estado)
                VALUES (%s, %s, %s, 'agendada')
            """, [id_doctor, id_paciente, fecha_hora])
        return redirect('home')
    return render(request, 'agendar_cita.html')


def ver_historial(request, id_paciente):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM historial_medico WHERE id_paciente = %s", [id_paciente])
        historial = cursor.fetchall()
    return render(request, 'ver_historial.html', {'historial': historial})


def generar_reporte(request):
    if request.method == 'POST':
        id_doctor = request.session['usuario_id']
        contenido = request.POST['contenido']
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO reportes (id_doctor, contenido, fecha_creacion)
                VALUES (%s, %s, NOW())
            """, [id_doctor, contenido])
        return redirect('home')
    return render(request, 'generar_reporte.html')


# def logout_view(request):
#     # Elimina la sesión actual
#     request.session.flush()
#     return redirect('login')

# def logout_view(request):
#     token_sesion = request.session.get('token_sesion')
#     if token_sesion:
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 "DELETE FROM sesiones WHERE token_sesion = %s",
#                 [token_sesion]
#             )
#         request.session.flush()  # Limpia toda la sesión del cliente
#     return redirect('login')  # Redirige al inicio de sesión

def logout_view(request):
    session_token = request.COOKIES.get('session_token')
    if session_token:
        # Eliminar la sesión de la base de datos
        Session.objects.filter(session_token=session_token).delete()

    # Redirigir al usuario al login
    response = redirect('login')
    response.delete_cookie('session_token')  # Eliminar la cookie del navegador
    return response
