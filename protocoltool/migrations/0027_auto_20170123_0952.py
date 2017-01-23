# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('protocoltool', '0026_auto_20170120_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicdataset',
            name='experimentIdea',
            field=models.TextField(max_length=1200, blank=True),
        ),
        migrations.AlterField(
            model_name='basicdataset',
            name='researchObjective',
            field=models.TextField(max_length=130, blank=True),
        ),
    ]
