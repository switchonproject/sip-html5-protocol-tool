# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0021_auto_20161122_1815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basicdataset',
            old_name='shortname',
            new_name='shortTitle',
        ),
        migrations.RenameField(
            model_name='externalprotocol',
            old_name='shortname',
            new_name='shortTitle',
        ),
    ]
