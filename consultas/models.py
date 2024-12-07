from django.db import models


class Citas(models.Model):
    id_cita = models.AutoField(primary_key=True)
    id_doctor = models.ForeignKey('Doctores', models.DO_NOTHING, db_column='id_doctor', blank=True, null=True)
    id_paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='id_paciente', blank=True, null=True)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'citas'


class Doctores(models.Model):
    id_doctor = models.OneToOneField('Usuarios', models.DO_NOTHING, db_column='id_doctor', primary_key=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    horario_disponible = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'doctores'


class HistorialMedico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey('Pacientes', models.DO_NOTHING, db_column='id_paciente', blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'historial_medico'


class Pacientes(models.Model):
    id_paciente = models.OneToOneField('Usuarios', models.DO_NOTHING, db_column='id_paciente', primary_key=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tel_contacto = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pacientes'


class Reportes(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    id_doctor = models.ForeignKey(Doctores, models.DO_NOTHING, db_column='id_doctor', blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reportes'


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    correo = models.CharField(unique=True, max_length=100, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=10, blank=True, null=True)
    contrasena = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuarios'

class Session(models.Model):
    user_id = models.IntegerField()
    session_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"Session for User {self.user_id}"