# Generated by Django 5.0 on 2023-12-27 21:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='nit',
            field=models.CharField(max_length=13, unique=True),
        ),
        migrations.AlterField(
            model_name='factura',
            name='cliente',
            field=models.ForeignKey(blank=True, default='CF', null=True, on_delete=django.db.models.deletion.CASCADE, to='ventas.cliente', to_field='nit'),
        ),
        migrations.AlterField(
            model_name='factura',
            name='maestro',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='producto',
            name='nombre',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
