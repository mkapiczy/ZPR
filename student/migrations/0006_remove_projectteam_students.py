# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-26 11:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_projectteam_students'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectteam',
            name='students',
        ),
    ]
