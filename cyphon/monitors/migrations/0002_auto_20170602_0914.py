# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-02 13:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitors', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitor',
            options={'ordering': ['name']},
        ),
    ]
