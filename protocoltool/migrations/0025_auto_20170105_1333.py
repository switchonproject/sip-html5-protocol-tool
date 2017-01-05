# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0024_auto_20161212_1645'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicdataset',
            name='hidden',
            field=models.BooleanField(default=True),
        ),
    ]
