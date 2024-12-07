from django.urls import path
from . import views  # Importa las vistas de la app consultas


urlpatterns = [

    path('home/', views.home_view, name='home'),

    # Página principal: login
    path('', views.login_view, name='login'),

    # Registro de usuarios
    path('registro/', views.register_view, name='registro'),

    # Agendar citas
    path('citas/agendar/', views.agendar_cita, name='agendar_cita'),

    # Historial médico
    path('historial/<int:id_paciente>/', views.ver_historial, name='ver_historial'),

    # Generar reportes por doctores
    path('reportes/crear/', views.generar_reporte, name='generar_reporte'),

    #logout
    path('logout/', views.logout_view, name='logout'),

]
