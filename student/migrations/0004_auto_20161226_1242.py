# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-26 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_remove_project_signed_students'),
        ('student', '0003_studentuser_courses'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentuser',
            name='signed_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Project'),
        ),
        migrations.AlterField(
            model_name='projectteam',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Project'),
        ),
    ]
