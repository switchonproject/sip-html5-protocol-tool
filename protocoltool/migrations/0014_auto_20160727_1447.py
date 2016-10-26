# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0013_auto_20160726_1644'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datareq',
            old_name='description',
            new_name='properties',
        ),
    ]
