from django.db import models


class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, blank=True, null=True)
    apellido = models.CharField(max_length=50, blank=True, null=True)
    correo = models.EmailField(unique=True, max_length=100, blank=True, null=True)
    tipo_usuario = models.CharField(
        max_length=10,
        choices=[('doctor', 'Doctor'), ('paciente', 'Paciente')],
        blank=True,
        null=True
    )
    contrasena = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'usuarios'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.tipo_usuario})"


class Doctores(models.Model):
    id_doctor = models.OneToOneField(Usuarios, on_delete=models.CASCADE, db_column='id_doctor', primary_key=True)
    especialidad = models.CharField(max_length=100, blank=True, null=True)
    horario_disponible = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'doctores'
        verbose_name_plural = 'Doctores'

    def __str__(self):
        return f"Dr. {self.id_doctor.nombre} {self.id_doctor.apellido} - {self.especialidad}"


class Pacientes(models.Model):
    id_paciente = models.OneToOneField(Usuarios, on_delete=models.CASCADE, db_column='id_paciente', primary_key=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tel_contacto = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        db_table = 'pacientes'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f"{self.id_paciente.nombre} {self.id_paciente.apellido}"


class Citas(models.Model):
    id_cita = models.AutoField(primary_key=True)
    id_doctor = models.ForeignKey(Doctores, on_delete=models.CASCADE, db_column='id_doctor', blank=True, null=True)
    id_paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, db_column='id_paciente', blank=True, null=True)
    fecha_hora = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=10,
        choices=[('pendiente', 'Pendiente'), ('confirmada', 'Confirmada'), ('cancelada', 'Cancelada')],
        default='pendiente'
    )

    class Meta:
        db_table = 'citas'
        verbose_name_plural = 'Citas'

    def __str__(self):
        return f"Cita de {self.id_paciente} con {self.id_doctor} el {self.fecha_hora}"


class HistorialMedico(models.Model):
    id_historial = models.AutoField(primary_key=True)
    id_paciente = models.ForeignKey(Pacientes, on_delete=models.CASCADE, db_column='id_paciente', blank=True, null=True)
    diagnostico = models.TextField(blank=True, null=True)
    tratamiento = models.TextField(blank=True, null=True)
    fecha = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'historial_medico'
        verbose_name_plural = 'Historiales Médicos'

    def __str__(self):
        return f"Historial de {self.id_paciente} - {self.fecha}"


class Reportes(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    id_doctor = models.ForeignKey(Doctores, on_delete=models.CASCADE, db_column='id_doctor', blank=True, null=True)
    contenido = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reportes'
        verbose_name_plural = 'Reportes'

    def __str__(self):
        return f"Reporte del Dr. {self.id_doctor} - {self.fecha_creacion}"


class Session(models.Model):
    user_id = models.IntegerField()
    session_token = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    class Meta:
        verbose_name_plural = 'Sessions'

    def __str__(self):
        return f"Session for User {self.user_id}"