# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-06 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20161106_1746'),
        ('student', '0002_auto_20161106_1834'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentuser',
            name='courses',
            field=models.ManyToManyField(to='main.Course'),
        ),
    ]