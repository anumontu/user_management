# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 14:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='id',
        ),
        migrations.AlterField(
            model_name='token',
            name='token',
            field=models.TextField(max_length=100, primary_key=True, serialize=False),
        ),
    ]
