# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 17:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentuser',
            name='project_team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='student.ProjectTeam'),
        ),
    ]
