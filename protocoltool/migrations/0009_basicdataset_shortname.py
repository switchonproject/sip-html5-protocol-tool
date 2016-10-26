# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0008_auto_20160701_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='basicdataset',
            name='shortname',
            field=models.CharField(default='Short experiment name', max_length=100),
            preserve_default=False,
        ),
    ]
