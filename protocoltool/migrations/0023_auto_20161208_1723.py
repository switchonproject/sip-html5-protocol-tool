# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0022_auto_20161123_1517'),
    ]

    operations = [
        migrations.AddField(
            model_name='datareq',
            name='links',
            field=models.TextField(blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='expstep',
            name='links',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='reporting',
            name='links',
            field=models.TextField(editable=False, blank=True),
            preserve_default=True,
        ),
    ]
