# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 20:50
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20161107_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateTimeField(blank=True, verbose_name=datetime.datetime.now),
        ),
    ]
