# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 11:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_auto_20161229_0815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentuser',
            name='projectTeams',
            field=models.ManyToManyField(to='student.ProjectTeam'),
        ),
        migrations.AlterField(
            model_name='studentuser',
            name='signedProjects',
            field=models.ManyToManyField(to='main.Project'),
        ),
    ]
