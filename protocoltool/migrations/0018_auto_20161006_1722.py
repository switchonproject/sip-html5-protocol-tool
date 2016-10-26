# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0017_auto_20161006_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datareq',
            name='deadline',
            field=models.DateField(default=datetime.date.today, blank=True),
        ),
        migrations.AlterField(
            model_name='expstep',
            name='deadline',
            field=models.DateField(default=datetime.date.today, blank=True),
        ),
    ]
