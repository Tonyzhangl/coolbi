# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-05-23 01:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0003_auto_20180522_2056'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bigtype',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='categoryrecord',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='district',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='districtdetail',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='districtdetailrecord',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='districtrecord',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='measurement',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='phase',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='record',
            options={'ordering': ['created_at', 'updated_at']},
        ),
    ]
