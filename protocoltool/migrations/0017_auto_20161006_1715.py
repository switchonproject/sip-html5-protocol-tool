# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0016_auto_20161006_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expstep',
            name='deadline',
            field=models.DateField(default=datetime.date.today, help_text=b'Please use the following format: <em>YYYY-MM-DD</em>.', blank=True),
        ),
    ]
