# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-01 14:44
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0003_auto_20170301_1443'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]
