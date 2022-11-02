# Generated by Django 4.1.2 on 2022-10-30 00:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asistente',
            fields=[
                ('idAsistente', models.AutoField(primary_key=True, serialize=False)),
                ('nombres', models.CharField(max_length=100, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=100, verbose_name='Apellidos')),
                ('documento', models.CharField(max_length=100, verbose_name='Documento')),
                ('telefono', models.CharField(max_length=10, verbose_name='telefono')),
                ('correo', models.CharField(max_length=50, verbose_name='correo')),
                ('tipo_aporte', models.CharField(max_length=50, verbose_name='tipo_aporte')),
                ('tipo_persona', models.CharField(max_length=50, verbose_name='tipo_persona')),
            ],
            options={
                'verbose_name': 'Asistente',
                'verbose_name_plural': 'Asistentes',
            },
        ),
        migrations.CreateModel(
            name='Preregistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=100, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=100, verbose_name='Apellidos')),
                ('documento', models.CharField(max_length=100, verbose_name='Documento')),
                ('telefono', models.CharField(max_length=10, verbose_name='telefono')),
                ('correo', models.CharField(max_length=50, verbose_name='correo')),
            ],
            options={
                'verbose_name': 'Preregistro',
                'verbose_name_plural': 'Preregistro',
            },
        ),
        migrations.CreateModel(
            name='Donacion',
            fields=[
                ('idDonacion', models.AutoField(primary_key=True, serialize=False)),
                ('tipo_donacion', models.CharField(max_length=45, verbose_name='tipo de donacion')),
                ('Asistente_idAsistente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainSistema.asistente')),
            ],
            options={
                'verbose_name': 'Donacion',
                'verbose_name_plural': 'Donaciones',
            },
        ),
    ]