# Generated by Django 5.1.4 on 2024-12-07 06:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Citas',
            fields=[
                ('id_cita', models.AutoField(primary_key=True, serialize=False)),
                ('fecha_hora', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(blank=True, max_length=10, null=True)),
            ],
            options={
                'db_table': 'citas',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id_usuario', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('apellido', models.CharField(blank=True, max_length=50, null=True)),
                ('correo', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('tipo_usuario', models.CharField(blank=True, max_length=10, null=True)),
                ('contrasena', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'usuarios',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='HistorialMedico',
            fields=[
                ('id_historial', models.AutoField(primary_key=True, serialize=False)),
                ('diagnostico', models.TextField(blank=True, null=True)),
                ('tratamiento', models.TextField(blank=True, null=True)),
                ('fecha', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'historial_medico',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Reportes',
            fields=[
                ('id_reporte', models.AutoField(primary_key=True, serialize=False)),
                ('contenido', models.TextField(blank=True, null=True)),
                ('fecha_creacion', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'reportes',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('session_token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Doctores',
            fields=[
                ('id_doctor', models.OneToOneField(db_column='id_doctor', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='consultas.usuarios')),
                ('especialidad', models.CharField(blank=True, max_length=100, null=True)),
                ('horario_disponible', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'db_table': 'doctores',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Pacientes',
            fields=[
                ('id_paciente', models.OneToOneField(db_column='id_paciente', on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='consultas.usuarios')),
                ('fecha_nacimiento', models.DateField(blank=True, null=True)),
                ('tel_contacto', models.CharField(blank=True, max_length=15, null=True)),
            ],
            options={
                'db_table': 'pacientes',
                'managed': False,
            },
        ),
    ]
