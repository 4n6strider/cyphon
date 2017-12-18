# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-02 20:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('jira', 'jira'), ('twitter', 'twitter'), ('virustotal', 'virustotal')], max_length=16, unique=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'supplier',
                'verbose_name_plural': 'suppliers',
            },
        ),
    ]
