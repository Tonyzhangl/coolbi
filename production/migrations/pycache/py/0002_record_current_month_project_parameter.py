# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-22 12:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='current_month_project_parameter',
            field=models.FloatField(blank=True, null=True),
        ),
    ]