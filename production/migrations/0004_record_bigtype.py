# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-25 13:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_districtrecord_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='bigtype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='production.BigType'),
            preserve_default=False,
        ),
    ]