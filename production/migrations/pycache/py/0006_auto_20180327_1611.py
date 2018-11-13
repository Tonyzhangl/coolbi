# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-27 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0005_districtrecord_bigtype'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categoryrecord',
            name='district',
        ),
        migrations.RemoveField(
            model_name='categoryrecord',
            name='district_detail',
        ),
        migrations.AddField(
            model_name='categoryrecord',
            name='bigtype',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='bigtype', to='production.BigType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='districtrecord',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='records', to='production.District'),
        ),
    ]