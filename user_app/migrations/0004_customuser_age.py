# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 13:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_remove_customuser_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='age',
            field=models.IntegerField(blank=True, default=20, verbose_name='age'),
            preserve_default=False,
        ),
    ]
