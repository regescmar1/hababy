# Generated by Django 5.0.6 on 2024-06-26 12:50

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CitaExtracciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('analisis_normal', models.BooleanField(blank=True, default=False, null=True)),
                ('test_o_sullivan_positivo', models.BooleanField(blank=True, default=False, null=True)),
                ('rh_negativo', models.BooleanField(blank=True, default=False, null=True)),
                ('anemia', models.BooleanField(blank=True, default=False, null=True)),
                ('observaciones', models.CharField(blank=True, max_length=255, null=True)),
                ('trimestre', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)])),
                ('usuaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CurvaLarga',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(blank=True, null=True)),
                ('analisis_normal', models.BooleanField(blank=True, default=False, null=True)),
                ('observaciones', models.CharField(blank=True, max_length=255, null=True)),
                ('trimestre', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3)])),
                ('usuaria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]