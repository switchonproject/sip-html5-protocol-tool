# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0003_auto_20160622_1611'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expstep',
            old_name='output',
            new_name='properties',
        ),
        migrations.RenameField(
            model_name='resultrep',
            old_name='output',
            new_name='properties',
        ),
    ]
