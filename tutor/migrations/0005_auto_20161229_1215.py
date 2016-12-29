# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-29 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0004_tutoruser_allowed_teams_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='TutorCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('courseId', models.IntegerField()),
                ('allowedTeamsNumber', models.IntegerField(default=10)),
            ],
        ),
        migrations.RemoveField(
            model_name='tutoruser',
            name='allowed_teams_number',
        ),
        migrations.AddField(
            model_name='tutorcourse',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutor.TutorUser'),
        ),
    ]
