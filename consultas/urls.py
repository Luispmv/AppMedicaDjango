from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('home/', views.home_view, name='home'),
    path('registro/', views.register_view, name='registro'),
    path('dashboard/doctor/', views.dashboard_doctor, name='dashboard_doctor'),
    path('dashboard/paciente/', views.dashboard_paciente, name='dashboard_paciente'),
    path('citas/agendar/doctor/', views.agendar_cita_doctor, name='agendar_cita_doctor'),
    path('historial/<int:id_paciente>/', views.ver_historial, name='ver_historial'),
    path('reportes/crear/', views.generar_reporte, name='generar_reporte'),
    path('medicos/', views.ver_medicos, name='ver_medicos'),
    path('citas/ver/', views.ver_citas, name='ver_citas'),
    path('tratamiento/', views.ver_tratamiento, name='ver_tratamiento'),
    path('logout/', views.logout_view, name='logout'),
]