# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_post_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='creation_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]