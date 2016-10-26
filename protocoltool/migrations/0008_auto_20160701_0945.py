# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0007_auto_20160701_0938'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datareq',
            old_name='properties',
            new_name='description',
        ),
    ]
