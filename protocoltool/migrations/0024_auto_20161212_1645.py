# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0023_auto_20161208_1723'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basicdataset',
            old_name='checked',
            new_name='hidden',
        ),
    ]
