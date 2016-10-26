# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0002_basicdataset_checked'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='basicdataset',
            name='principles',
        ),
        migrations.AddField(
            model_name='datareq',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
