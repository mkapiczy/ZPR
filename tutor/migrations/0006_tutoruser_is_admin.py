# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-18 19:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutor', '0005_auto_20161229_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutoruser',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
