# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0015_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datareq',
            name='deadline',
            field=models.DateField(default=datetime.date.today, help_text=b'Please use the following format: <em>YYYY-MM-DD</em>.', blank=True),
            preserve_default=True,
        ),
    ]
