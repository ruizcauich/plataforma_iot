# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-19 22:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='campo',
            name='sensor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Sensor'),
        ),
        migrations.AddField(
            model_name='dispositivo',
            name='proyecto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Proyecto'),
        ),
        migrations.AddField(
            model_name='sensor',
            name='dispositivo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Dispositivo'),
        ),
        migrations.AddField(
            model_name='valor',
            name='campo',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='dashboard.Campo'),
        ),
    ]
