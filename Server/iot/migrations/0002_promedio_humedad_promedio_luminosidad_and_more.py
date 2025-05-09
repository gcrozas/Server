# Generated by Django 4.1.4 on 2023-02-08 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promedio_humedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hum', models.CharField(max_length=2)),
                ('dia_inicio', models.DateTimeField()),
                ('dia_fin', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Historico de la humedad',
                'verbose_name_plural': 'Historico de la humedad',
                'get_latest_by': 'dia_fin',
            },
        ),
        migrations.CreateModel(
            name='Promedio_luminosidad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lum', models.CharField(max_length=3)),
                ('dia_inicio', models.DateTimeField()),
                ('dia_fin', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Historico de la luminosidad',
                'verbose_name_plural': 'Historico de la luminosidad',
                'get_latest_by': 'dia_fin',
            },
        ),
        migrations.CreateModel(
            name='Promedio_presencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mov', models.CharField(max_length=1)),
                ('dia_inicio', models.DateTimeField()),
                ('dia_fin', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Historico de presencia',
                'verbose_name_plural': 'Historico de presencia',
                'get_latest_by': 'dia_fin',
            },
        ),
        migrations.CreateModel(
            name='Promedio_temperatura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp', models.CharField(max_length=2)),
                ('dia_inicio', models.DateTimeField()),
                ('dia_fin', models.DateTimeField()),
            ],
            options={
                'verbose_name': 'Historico de la temperatura',
                'verbose_name_plural': 'Historico de la temperatura',
                'get_latest_by': 'dia_fin',
            },
        ),
    ]
