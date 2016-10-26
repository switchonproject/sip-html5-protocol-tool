# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0012_reporting_tasknr'),
    ]

    operations = [
        migrations.AddField(
            model_name='datareq',
            name='taskNr',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='expstep',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expstep',
            name='taskNr',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='reporting',
            name='done',
            field=models.BooleanField(default=False),
        ),
    ]
