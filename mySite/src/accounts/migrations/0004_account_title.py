# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-06-01 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_account_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='title',
            field=models.CharField(default='abc', max_length=120),
            preserve_default=False,
        ),
    ]
